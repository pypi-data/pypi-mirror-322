import argparse
import hashlib
import json
import os
import random
import shutil
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tqdm import tqdm

from .ai import AI, collate
from .exceptions import AIException
from .parse import chunk

# we're using an old tree-sitter API
import warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='tree_sitter')

def main():
    parser = argparse.ArgumentParser(description='Analyze source files for relevance to a question')
    parser.add_argument('question', help='Question to check relevance against')
    parser.add_argument('--sample', type=int, help='Number of random files to sample from the input set')
    parser.add_argument('--save-cache', action='store_true', help='Keep cache directory after completion')
    parser.add_argument('--llm-concurrency', type=int, default=200, help='Maximum number of concurrent LLM requests')
    parser.add_argument('--no-refine', action='store_false', dest='refine', help='Skip refinement and combination of analyses')
    args = parser.parse_args()

    # Read Java files from stdin
    source_files = []
    for line in sys.stdin:
        file_path = line.strip()
        if not os.path.isfile(file_path):
            print(f"Warning: File does not exist: {file_path}", file=sys.stderr)
            continue
        source_files.append(file_path)

    if not source_files:
        print("Error: No valid source files provided", file=sys.stderr)
        return 1

    # Sample files if requested
    if args.sample and args.sample < len(source_files):
        source_files = random.sample(source_files, args.sample)

    # Setup cache directory
    cache_key = f"{args.question}_{len(source_files)}_{args.sample or 'all'}"
    # Hash it to get a safe directory name
    cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
    cache_dir = Path(".llmap_cache") / cache_hash
    if cache_dir.exists():
        print(f"Using cache directory: {cache_dir}", file=sys.stderr)
    else:
        print(f"Creating cache directory: {cache_dir}")

    # Initialize client
    client = AI(cache_dir)

    def load_cached_results(cache_path, phase):
        """Load cached results and errors for a phase"""
        results_file = cache_path / f"{phase}_results.jsonl"
        errors_file = cache_path / f"{phase}_errors.jsonl"
    
        results = []
        errors = []
    
        if results_file.exists():
            with open(results_file) as f:
                for line in f:
                    results.append(tuple(json.loads(line)))
                
        if errors_file.exists():
            with open(errors_file) as f:
                for line in f:
                    error_data = json.loads(line)
                    errors.append(AIException(
                        message=error_data['message'],
                        filename=error_data['filename'],
                        original_exception=None
                    ))
                
        return results, errors

    def save_results(cache_path, phase, results, errors):
        """Save results and errors for a phase"""
        results_file = cache_path / f"{phase}_results.jsonl"
        errors_file = cache_path / f"{phase}_errors.jsonl"
    
        with open(results_file, 'w') as f:
            for result in results:
                json.dump(list(result), f)
                f.write('\n')
            
        with open(errors_file, 'w') as f:
            for error in errors:
                error_dict = {
                    'message': str(error),
                    'filename': error.filename
                }
                json.dump(error_dict, f)
                f.write('\n')

    def process_batch(executor, files, process_fn, desc):
        """Process a batch of files and return results, tracking errors"""
        futures = [executor.submit(process_fn, f) for f in files]
        results = []
        errors = []
        
        for future in tqdm(futures, desc=desc):
            try:
                results.append(future.result())
            except AIException as e:
                errors.append(e)
                
        return results, errors

    # Create thread pool and process files
    errors = []
    relevant_files = []
    with ThreadPoolExecutor(max_workers=args.llm_concurrency) as executor:
        # Split files by whether we can parse a skeleton
        parseable_files = {f for f in source_files if f.endswith('.java') or f.endswith('.py')}
        other_files = [f for f in source_files if not f in parseable_files]

        # Phase 1: Generate initial relevance against skeletons for Java files
        if parseable_files:
            gen_fn = lambda f: client.skeleton_relevance(f, args.question)
            skeleton_results, phase1_errors = process_batch(
                executor, parseable_files, gen_fn, "Skeleton analysis")
            errors.extend(phase1_errors)
            # parse out the conclusion
            for file_path, analysis in skeleton_results:
                if 'LLMAP_RELEVANT' in analysis or 'LLMAP_SOURCE' in analysis:
                    relevant_files.append(file_path)

        # Add non-Java files directly to relevant_files for full source analysis
        relevant_files.extend(other_files)

        # Phase 2: extract and analyze source code chunks from relevant files
        # First get all chunks
        chunk_fn = lambda f: (f, chunk(f))
        file_chunks, phase2a_errors = process_batch(
            executor, relevant_files, chunk_fn, "Parsing full source")
        errors.extend(phase2a_errors)

        # Flatten chunks into (file_path, chunk_text) pairs for analysis
        chunk_pairs = []
        for file_path, chunks in file_chunks:
            if chunks:
                for chunk_text in chunks:
                    chunk_pairs.append((file_path, chunk_text))

        # Analyze all chunks
        analyze_fn = lambda pair: client.full_source_relevance(pair[1], args.question, pair[0])
        chunk_analyses, phase2b_errors = process_batch(
            executor, chunk_pairs, analyze_fn, "Analyzing full source")
        errors.extend(phase2b_errors)

        # Group analyses by file and combine
        analyses_by_file = defaultdict(list)
        for (file_path, analysis) in chunk_analyses:
            analyses_by_file[file_path].append(analysis)

        chunk_results = [
            (file_path, "\n\n".join(analyses))
            for file_path, analyses in analyses_by_file.items()
        ]

        # Collate and process results
        groups, large_files = collate(chunk_results)

        # Refine groups in parallel
        if args.refine:
            sift_fn = lambda g: client.sift_context(g, args.question)
            processed_contexts, phase4_errors = process_batch(
                executor, groups, sift_fn, "Refining analysis")
            errors.extend(phase4_errors)
        else:
            # If no refinement, just flatten the groups into individual results
            processed_contexts = [f'File{file_path}\n{analysis}\n\n'
                                  for group in groups for file_path, analysis in group]

    # Print any errors to stderr
    if errors:
        print("\nErrors encountered:", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        print("", file=sys.stderr)

    # Print results
    for context in processed_contexts:
        if context:
            print(context, '\n')
    for file_path, analysis in large_files:
        print(f"{file_path}:\n{analysis}\n\n")
        
    # Clean up cache unless --save-cache was specified
    if not args.save_cache:
        shutil.rmtree(cache_dir)

if __name__ == "__main__":
    main()
