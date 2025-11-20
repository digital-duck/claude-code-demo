"""
Batch Repository Documentation Generator
Process thousands of repositories at scale with parallel processing
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging

from context_doc_generator import ContextualDocumentationGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BatchRepoDocumentationGenerator:
    """Process thousands of repositories at scale."""
    
    def __init__(self, doc_agent_kg_builder):
        self.doc_generator = ContextualDocumentationGenerator(doc_agent_kg_builder)
        self.results = []
    
    def process_organization_repos(self, repos_root: Path, 
                                   parallel: bool = True,
                                   max_workers: int = 4,
                                   filter_pattern: Optional[str] = None) -> List[Dict]:
        """
        Process all repositories in an organization.
        
        Parameters:
        -----------
        repos_root : Path
            Root directory containing all git repos
        parallel : bool
            Process repos in parallel (default: True)
        max_workers : int
            Number of parallel workers (default: 4)
        filter_pattern : str, optional
            Only process repos matching this pattern (e.g., "data-*")
        
        Returns:
        --------
        List of processing results
        """
        repos_root = Path(repos_root)
        
        # Find all git repositories
        repos = self._find_git_repos(repos_root, filter_pattern)
        
        print(f"\n{'='*70}")
        print(f"Batch Repository Documentation Generation")
        print(f"{'='*70}")
        print(f"Root directory: {repos_root}")
        print(f"Repositories found: {len(repos)}")
        print(f"Parallel processing: {parallel}")
        print(f"Max workers: {max_workers if parallel else 1}")
        print(f"{'='*70}\n")
        
        if parallel:
            return self._process_parallel(repos, max_workers)
        else:
            return self._process_sequential(repos)
    
    def _find_git_repos(self, root: Path, filter_pattern: Optional[str] = None) -> List[Path]:
        """Find all directories containing .git folder."""
        repos = []
        
        for item in root.rglob('.git'):
            if item.is_dir():
                repo_path = item.parent
                
                # Apply filter if specified
                if filter_pattern:
                    if filter_pattern in repo_path.name:
                        repos.append(repo_path)
                else:
                    repos.append(repo_path)
        
        return sorted(repos)
    
    def _process_sequential(self, repos: List[Path]) -> List[Dict]:
        """Process repositories sequentially."""
        results = []
        start_time = datetime.now()
        
        for i, repo in enumerate(repos, 1):
            print(f"\n[{i}/{len(repos)}] Processing: {repo.name}")
            print(f"Path: {repo}")
            
            try:
                repo_start = datetime.now()
                docs = self.doc_generator.generate_repo_documentation(repo)
                repo_duration = (datetime.now() - repo_start).total_seconds()
                
                result = {
                    'repo': str(repo),
                    'repo_name': repo.name,
                    'status': 'success',
                    'duration_seconds': repo_duration,
                    'docs': {k: str(v) for k, v in docs.items()},
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result)
                print(f"✓ Success (took {repo_duration:.1f}s)")
                
            except Exception as e:
                logger.error(f"✗ Error processing {repo.name}: {e}")
                result = {
                    'repo': str(repo),
                    'repo_name': repo.name,
                    'status': 'failed',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result)
        
        total_duration = (datetime.now() - start_time).total_seconds()
        self._print_summary(results, total_duration)
        
        return results
    
    def _process_parallel(self, repos: List[Path], max_workers: int) -> List[Dict]:
        """Process repositories in parallel."""
        results = []
        start_time = datetime.now()
        completed = 0
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all jobs
            future_to_repo = {
                executor.submit(self._process_single_repo, repo): repo
                for repo in repos
            }
            
            # Process results as they complete
            for future in as_completed(future_to_repo):
                repo = future_to_repo[future]
                completed += 1
                
                print(f"\n[{completed}/{len(repos)}] Completed: {repo.name}")
                
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result['status'] == 'success':
                        print(f"✓ Success (took {result['duration_seconds']:.1f}s)")
                    else:
                        print(f"✗ Failed: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    logger.error(f"✗ Error processing {repo.name}: {e}")
                    results.append({
                        'repo': str(repo),
                        'repo_name': repo.name,
                        'status': 'failed',
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
        
        total_duration = (datetime.now() - start_time).total_seconds()
        self._print_summary(results, total_duration)
        
        return results
    
    def _process_single_repo(self, repo: Path) -> Dict:
        """Process a single repository (for parallel execution)."""
        try:
            repo_start = datetime.now()
            docs = self.doc_generator.generate_repo_documentation(repo)
            repo_duration = (datetime.now() - repo_start).total_seconds()
            
            return {
                'repo': str(repo),
                'repo_name': repo.name,
                'status': 'success',
                'duration_seconds': repo_duration,
                'docs': {k: str(v) for k, v in docs.items()},
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'repo': str(repo),
                'repo_name': repo.name,
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _print_summary(self, results: List[Dict], total_duration: float):
        """Print summary statistics."""
        success_count = sum(1 for r in results if r['status'] == 'success')
        failed_count = len(results) - success_count
        
        avg_duration = sum(r.get('duration_seconds', 0) for r in results if r['status'] == 'success')
        avg_duration = avg_duration / success_count if success_count > 0 else 0
        
        print(f"\n{'='*70}")
        print(f"BATCH PROCESSING SUMMARY")
        print(f"{'='*70}")
        print(f"Total repositories: {len(results)}")
        print(f"Successfully processed: {success_count}")
        print(f"Failed: {failed_count}")
        print(f"Total time: {total_duration:.1f}s ({total_duration/60:.1f} minutes)")
        print(f"Average time per repo: {avg_duration:.1f}s")
        print(f"{'='*70}\n")
    
    def generate_summary_report(self, output_path: str = "documentation_report.json"):
        """Generate comprehensive summary report."""
        summary = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_repos': len(self.results),
                'successful': sum(1 for r in self.results if r['status'] == 'success'),
                'failed': sum(1 for r in self.results if r['status'] == 'failed')
            },
            'results': self.results,
            'statistics': self._calculate_statistics()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n{'='*70}")
        print(f"DETAILED REPORT")
        print(f"{'='*70}")
        print(f"Total repositories: {summary['metadata']['total_repos']}")
        print(f"Successfully processed: {summary['metadata']['successful']}")
        print(f"Failed: {summary['metadata']['failed']}")
        print(f"\nReport saved to: {output_path}")
        
        if summary['metadata']['failed'] > 0:
            print(f"\nFailed repositories:")
            for result in self.results:
                if result['status'] == 'failed':
                    print(f"  - {result['repo_name']}: {result.get('error', 'Unknown error')}")
        
        print(f"{'='*70}\n")
        
        return summary
    
    def _calculate_statistics(self) -> Dict:
        """Calculate processing statistics."""
        successful_results = [r for r in self.results if r['status'] == 'success']
        
        if not successful_results:
            return {
                'avg_duration': 0,
                'min_duration': 0,
                'max_duration': 0,
                'total_docs_generated': 0
            }
        
        durations = [r.get('duration_seconds', 0) for r in successful_results]
        
        return {
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'total_docs_generated': sum(len(r.get('docs', {})) for r in successful_results)
        }
    
    def export_repo_index(self, output_path: str = "repo_index.md"):
        """
        Export a markdown index of all processed repositories.
        Useful for navigation and overview.
        """
        successful_repos = [r for r in self.results if r['status'] == 'success']
        
        content = [
            "# Repository Documentation Index",
            f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Repositories**: {len(self.results)}",
            f"**Successfully Documented**: {len(successful_repos)}",
            "\n## Repository List\n"
        ]
        
        for result in sorted(successful_repos, key=lambda x: x['repo_name']):
            repo_name = result['repo_name']
            repo_path = Path(result['repo'])
            claude_md = repo_path / "CLAUDE.md"
            
            content.append(f"### {repo_name}")
            content.append(f"- **Path**: `{result['repo']}`")
            content.append(f"- **Documentation**: [CLAUDE.md]({claude_md.relative_to(Path.cwd())})")
            content.append(f"- **Files Generated**: {len(result.get('docs', {}))}")
            content.append("")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"Repository index exported to: {output_path}")
        
        return output_path


# Example usage and CLI interface
def main():
    """
    Main entry point for batch processing.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Batch generate contextual documentation for AI agents'
    )
    parser.add_argument(
        'repos_root',
        type=str,
        help='Root directory containing git repositories'
    )
    parser.add_argument(
        '--parallel',
        action='store_true',
        default=True,
        help='Process repositories in parallel (default: True)'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    parser.add_argument(
        '--filter',
        type=str,
        default=None,
        help='Only process repos matching this pattern (e.g., "data-*")'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='documentation_report.json',
        help='Output report filename (default: documentation_report.json)'
    )
    
    args = parser.parse_args()
    
    # Initialize (you'll need to provide your KG builder)
    print("Initializing batch processor...")
    print("Note: This requires your UnifiedKnowledgeGraphBuilder instance")
    
    # Uncomment and modify when you have your KG builder:
    # from unified_kg_builder import UnifiedKnowledgeGraphBuilder
    # kg_builder = UnifiedKnowledgeGraphBuilder()
    # batch_processor = BatchRepoDocumentationGenerator(kg_builder)
    # 
    # results = batch_processor.process_organization_repos(
    #     repos_root=args.repos_root,
    #     parallel=args.parallel,
    #     max_workers=args.workers,
    #     filter_pattern=args.filter
    # )
    # 
    # batch_processor.results = results
    # batch_processor.generate_summary_report(args.output)
    # batch_processor.export_repo_index("repo_index.md")
    
    print("""
Example usage:

    # Process all repos in parallel with 8 workers
    python batch_repo_processor.py /path/to/repos --workers 8
    
    # Process only data-* repos
    python batch_repo_processor.py /path/to/repos --filter "data-"
    
    # Sequential processing
    python batch_repo_processor.py /path/to/repos --parallel False
    """)


if __name__ == "__main__":
    main()
