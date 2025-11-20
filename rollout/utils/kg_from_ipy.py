import json
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NotebookConverter:
    """Convert Jupyter notebooks to Python scripts for knowledge graph construction."""
    
    def __init__(self, notebook_dir: str, output_dir: str = None, 
                 preserve_structure: bool = True):
        """
        Initialize the converter.
        
        Parameters:
        -----------
        notebook_dir : str
            Directory containing .ipynb files (will search recursively)
        output_dir : str, optional
            Directory for output .py files (default: same as notebook_dir)
        preserve_structure : bool
            Preserve directory structure in output (default: True)
        """
        self.notebook_dir = Path(notebook_dir)
        self.output_dir = Path(output_dir) if output_dir else self.notebook_dir
        self.preserve_structure = preserve_structure
        self.conversion_log = []
        
    def find_all_notebooks(self) -> List[Path]:
        """Recursively find all .ipynb files."""
        notebooks = list(self.notebook_dir.rglob("*.ipynb"))
        # Filter out checkpoint files
        notebooks = [nb for nb in notebooks if ".ipynb_checkpoints" not in str(nb)]
        logger.info(f"Found {len(notebooks)} notebooks")
        return notebooks
    
    def convert_single_notebook(self, notebook_path: Path) -> Optional[Path]:
        """
        Convert a single notebook to Python script.
        
        Returns:
        --------
        Path to the created .py file, or None if conversion failed
        """
        try:
            # Determine output path
            if self.preserve_structure:
                rel_path = notebook_path.relative_to(self.notebook_dir)
                output_path = self.output_dir / rel_path.with_suffix('.py')
            else:
                output_path = self.output_dir / (notebook_path.stem + '.py')
            
            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert using nbconvert
            result = subprocess.run([
                "jupyter", "nbconvert",
                "--to", "script",
                "--output", str(output_path),
                str(notebook_path)
            ], check=True, capture_output=True, text=True)
            
            logger.info(f"✓ Converted: {notebook_path.name} -> {output_path}")
            self.conversion_log.append({
                'notebook': str(notebook_path),
                'python_file': str(output_path),
                'status': 'success'
            })
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Failed to convert {notebook_path.name}: {e.stderr}")
            self.conversion_log.append({
                'notebook': str(notebook_path),
                'python_file': None,
                'status': 'failed',
                'error': str(e)
            })
            return None
        except Exception as e:
            logger.error(f"✗ Error processing {notebook_path.name}: {e}")
            self.conversion_log.append({
                'notebook': str(notebook_path),
                'python_file': None,
                'status': 'error',
                'error': str(e)
            })
            return None
    
    def convert_all(self) -> List[Path]:
        """
        Convert all notebooks to Python scripts.
        
        Returns:
        --------
        List of successfully created .py files
        """
        notebooks = self.find_all_notebooks()
        converted_files = []
        
        logger.info(f"Starting conversion of {len(notebooks)} notebooks...")
        
        for i, notebook in enumerate(notebooks, 1):
            logger.info(f"[{i}/{len(notebooks)}] Processing: {notebook.name}")
            py_file = self.convert_single_notebook(notebook)
            if py_file:
                converted_files.append(py_file)
        
        # Summary
        success_count = len(converted_files)
        fail_count = len(notebooks) - success_count
        logger.info(f"\n{'='*60}")
        logger.info(f"Conversion complete: {success_count} succeeded, {fail_count} failed")
        logger.info(f"{'='*60}\n")
        
        return converted_files
    
    def extract_notebook_metadata(self, notebook_path: Path) -> Dict:
        """
        Extract metadata from notebook for knowledge graph enrichment.
        
        Returns metadata like: author, title, imports, function definitions, etc.
        """
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            metadata = {
                'path': str(notebook_path),
                'name': notebook_path.stem,
                'cell_count': len(notebook['cells']),
                'code_cells': [],
                'markdown_cells': [],
                'imports': set(),
                'functions': [],
                'classes': []
            }
            
            # Extract cell information
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    source = ''.join(cell['source'])
                    metadata['code_cells'].append(source)
                    
                    # Extract imports
                    for line in source.split('\n'):
                        line = line.strip()
                        if line.startswith('import ') or line.startswith('from '):
                            metadata['imports'].add(line)
                    
                    # Extract function definitions
                    for line in source.split('\n'):
                        line = line.strip()
                        if line.startswith('def '):
                            func_name = line.split('(')[0].replace('def ', '')
                            metadata['functions'].append(func_name)
                        elif line.startswith('class '):
                            class_name = line.split('(')[0].split(':')[0].replace('class ', '')
                            metadata['classes'].append(class_name)
                
                elif cell['cell_type'] == 'markdown':
                    source = ''.join(cell['source'])
                    metadata['markdown_cells'].append(source)
            
            metadata['imports'] = list(metadata['imports'])
            return metadata
            
        except Exception as e:
            logger.error(f"Error extracting metadata from {notebook_path}: {e}")
            return None
    
    def get_conversion_report(self) -> str:
        """Generate a detailed conversion report."""
        total = len(self.conversion_log)
        success = sum(1 for log in self.conversion_log if log['status'] == 'success')
        failed = total - success
        
        report = [
            "="*70,
            "NOTEBOOK CONVERSION REPORT",
            "="*70,
            f"Total notebooks processed: {total}",
            f"Successfully converted: {success}",
            f"Failed conversions: {failed}",
            "="*70,
        ]
        
        if failed > 0:
            report.append("\nFailed conversions:")
            for log in self.conversion_log:
                if log['status'] != 'success':
                    report.append(f"  - {Path(log['notebook']).name}: {log.get('error', 'Unknown error')}")
        
        return '\n'.join(report)
    
    def save_conversion_log(self, log_path: str = "conversion_log.json"):
        """Save conversion log to JSON file."""
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.conversion_log, f, indent=2)
        logger.info(f"Conversion log saved to: {log_path}")


def build_knowledge_graph_from_notebooks(
    notebook_dir: str,
    kg_builder_function,  # Your existing KG construction function
    output_dir: str = None,
    cleanup_py_files: bool = False,
    extract_metadata: bool = True
) -> Dict:
    """
    Complete pipeline: Convert notebooks -> Build knowledge graph.
    
    Parameters:
    -----------
    notebook_dir : str
        Directory containing .ipynb files
    kg_builder_function : callable
        Your existing function that builds KG from .py files
        Should have signature: kg_builder_function(py_files: List[Path]) -> knowledge_graph
    output_dir : str, optional
        Directory for temporary .py files
    cleanup_py_files : bool
        Whether to delete .py files after KG construction (default: False)
    extract_metadata : bool
        Whether to extract and include notebook metadata (default: True)
    
    Returns:
    --------
    Dict containing knowledge graph and metadata
    """
    # Setup
    if output_dir is None:
        output_dir = Path(notebook_dir) / "converted_py_files"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Convert notebooks
    converter = NotebookConverter(notebook_dir, output_dir)
    py_files = converter.convert_all()
    
    # Print report
    print(converter.get_conversion_report())
    converter.save_conversion_log(output_dir / "conversion_log.json")
    
    if not py_files:
        logger.error("No Python files were successfully converted!")
        return None
    
    # Extract metadata if requested
    metadata = {}
    if extract_metadata:
        logger.info("\nExtracting notebook metadata...")
        notebooks = converter.find_all_notebooks()
        for notebook in notebooks:
            meta = converter.extract_notebook_metadata(notebook)
            if meta:
                metadata[str(notebook)] = meta
        
        # Save metadata
        metadata_path = output_dir / "notebook_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Metadata saved to: {metadata_path}")
    
    # Build knowledge graph using your existing function
    logger.info(f"\nBuilding knowledge graph from {len(py_files)} Python files...")
    knowledge_graph = kg_builder_function(py_files)
    
    # Cleanup if requested
    if cleanup_py_files:
        logger.info("\nCleaning up temporary Python files...")
        for py_file in py_files:
            py_file.unlink()
        logger.info("Cleanup complete")
    
    return {
        'knowledge_graph': knowledge_graph,
        'metadata': metadata,
        'converted_files': [str(f) for f in py_files],
        'conversion_log': converter.conversion_log
    }


# Example usage with your existing KG builder
def example_usage():
    """Example of how to use the pipeline."""
    
    # Assuming you have a function like this:
    def your_existing_kg_builder(py_files: List[Path]):
        """Your existing knowledge graph construction function."""
        # Your implementation here
        # This function takes a list of .py files and builds a KG
        kg = {}  # Your KG structure
        
        for py_file in py_files:
            # Your KG construction logic
            pass
        
        return kg
    
    # Run the complete pipeline
    result = build_knowledge_graph_from_notebooks(
        notebook_dir="./data_science_notebooks",
        kg_builder_function=your_existing_kg_builder,
        output_dir="./temp_py_files",
        cleanup_py_files=False,  # Keep .py files for inspection
        extract_metadata=True     # Extract additional metadata
    )
    
    # Access results
    kg = result['knowledge_graph']
    metadata = result['metadata']
    
    print(f"\nKnowledge graph constructed with {len(metadata)} notebooks")
    
    return result



def batch_convert_notebooks_for_kg(notebook_dir: str, output_dir: str = None) -> List[Path]:
    """
    Simple batch converter for KG pipeline.
    
    Returns list of converted .py files.
    """
    from pathlib import Path
    import subprocess
    
    notebook_dir = Path(notebook_dir)
    output_dir = Path(output_dir) if output_dir else notebook_dir / "py_files"
    output_dir.mkdir(exist_ok=True)
    
    # Find all notebooks
    notebooks = [nb for nb in notebook_dir.rglob("*.ipynb") 
                 if ".ipynb_checkpoints" not in str(nb)]
    
    converted = []
    print(f"Converting {len(notebooks)} notebooks...")
    
    for i, nb in enumerate(notebooks, 1):
        py_path = output_dir / (nb.stem + ".py")
        try:
            subprocess.run([
                "jupyter", "nbconvert", "--to", "script",
                "--output", str(py_path), str(nb)
            ], check=True, capture_output=True)
            converted.append(py_path)
            print(f"[{i}/{len(notebooks)}] ✓ {nb.name}")
        except Exception as e:
            print(f"[{i}/{len(notebooks)}] ✗ {nb.name}: {e}")
    
    print(f"\nConverted: {len(converted)}/{len(notebooks)}")
    return converted

# # Usage
# py_files = batch_convert_notebooks_for_kg("./notebooks")
# kg = your_existing_kg_builder(py_files)

if __name__ == "__main__":
    # Simple conversion only
    converter = NotebookConverter(
        notebook_dir="./notebooks",
        output_dir="./python_scripts"
    )
    py_files = converter.convert_all()
    print(converter.get_conversion_report())