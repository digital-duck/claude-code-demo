from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class FileType(Enum):
    """Supported file types for knowledge graph construction."""
    PYTHON = ['.py']
    JUPYTER = ['.ipynb']
    SQL = ['.sql']
    JAVASCRIPT = ['.js', '.jsx']
    TYPESCRIPT = ['.ts', '.tsx']
    WORD = ['.docx']
    POWERPOINT = ['.pptx']
    EXCEL = ['.xlsx', '.xls', '.csv']
    
    @classmethod
    def from_extension(cls, extension: str):
        """Get FileType from file extension."""
        extension = extension.lower()
        for file_type in cls:
            if extension in file_type.value:
                return file_type
        return None


class FileProcessor(ABC):
    """Abstract base class for file processors."""
    
    @abstractmethod
    def can_process(self, file_path: Path) -> bool:
        """Check if this processor can handle the file."""
        pass
    
    @abstractmethod
    def extract_knowledge(self, file_path: Path) -> Dict[str, Any]:
        """Extract knowledge graph elements from the file."""
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """Return list of supported file extensions."""
        pass


class JupyterProcessor(FileProcessor):
    """Process Jupyter notebooks."""
    
    def __init__(self, temp_dir: str = "./temp_py"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
        self.converter = NotebookConverter(
            notebook_dir=".",
            output_dir=self.temp_dir
        )
    
    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix == '.ipynb'
    
    def extract_knowledge(self, file_path: Path) -> Dict[str, Any]:
        """Extract knowledge from Jupyter notebook."""
        # Convert to .py
        py_file = self.converter.convert_single_notebook(file_path)
        
        # Extract metadata from original notebook
        metadata = self.converter.extract_notebook_metadata(file_path)
        
        # Build KG from converted Python file
        kg_data = {
            'source_file': str(file_path),
            'file_type': 'jupyter_notebook',
            'converted_py': str(py_file) if py_file else None,
            'metadata': metadata,
            'entities': [],
            'relationships': []
        }
        
        if py_file and py_file.exists():
            # Use your existing Python KG builder
            py_kg = self._build_python_kg(py_file)
            kg_data['entities'].extend(py_kg.get('entities', []))
            kg_data['relationships'].extend(py_kg.get('relationships', []))
        
        return kg_data
    
    def _build_python_kg(self, py_file: Path) -> Dict:
        """Build KG from Python file (placeholder for your implementation)."""
        # Your existing Python KG logic here
        return {'entities': [], 'relationships': []}
    
    def get_supported_extensions(self) -> List[str]:
        return ['.ipynb']


class PythonProcessor(FileProcessor):
    """Process Python files."""
    
    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix == '.py'
    
    def extract_knowledge(self, file_path: Path) -> Dict[str, Any]:
        """Extract knowledge from Python file."""
        # Your existing Python KG logic
        return {
            'source_file': str(file_path),
            'file_type': 'python',
            'entities': [],
            'relationships': []
        }
    
    def get_supported_extensions(self) -> List[str]:
        return ['.py']


class SQLProcessor(FileProcessor):
    """Process SQL files."""
    
    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix == '.sql'
    
    def extract_knowledge(self, file_path: Path) -> Dict[str, Any]:
        """Extract knowledge from SQL file."""
        # Your existing SQL KG logic
        return {
            'source_file': str(file_path),
            'file_type': 'sql',
            'entities': [],
            'relationships': []
        }
    
    def get_supported_extensions(self) -> List[str]:
        return ['.sql']


class JavaScriptProcessor(FileProcessor):
    """Process JavaScript/TypeScript files."""
    
    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix in ['.js', '.jsx', '.ts', '.tsx']
    
    def extract_knowledge(self, file_path: Path) -> Dict[str, Any]:
        """Extract knowledge from JS/TS file."""
        # Your existing JS/TS KG logic
        return {
            'source_file': str(file_path),
            'file_type': 'javascript',
            'entities': [],
            'relationships': []
        }
    
    def get_supported_extensions(self) -> List[str]:
        return ['.js', '.jsx', '.ts', '.tsx']


class OfficeDocumentProcessor(FileProcessor):
    """Process Office documents (docx, pptx, xlsx)."""
    
    def __init__(self):
        self.supported = ['.docx', '.pptx', '.xlsx', '.xls']
    
    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix in self.supported
    
    def extract_knowledge(self, file_path: Path) -> Dict[str, Any]:
        """Extract knowledge from Office document."""
        # Your existing Office document KG logic
        return {
            'source_file': str(file_path),
            'file_type': f'office_{file_path.suffix[1:]}',
            'entities': [],
            'relationships': []
        }
    
    def get_supported_extensions(self) -> List[str]:
        return self.supported


class UnifiedKnowledgeGraphBuilder:
    """Unified knowledge graph builder supporting multiple file types."""
    
    def __init__(self):
        self.processors: List[FileProcessor] = []
        self.register_default_processors()
        self.kg_data = {
            'entities': [],
            'relationships': [],
            'metadata': {},
            'files_processed': []
        }
    
    def register_default_processors(self):
        """Register all default file processors."""
        self.register_processor(PythonProcessor())
        self.register_processor(JupyterProcessor())
        self.register_processor(SQLProcessor())
        self.register_processor(JavaScriptProcessor())
        self.register_processor(OfficeDocumentProcessor())
    
    def register_processor(self, processor: FileProcessor):
        """Register a custom file processor."""
        self.processors.append(processor)
        logger.info(f"Registered processor: {processor.__class__.__name__}")
    
    def get_processor(self, file_path: Path) -> Optional[FileProcessor]:
        """Get appropriate processor for a file."""
        for processor in self.processors:
            if processor.can_process(file_path):
                return processor
        return None
    
    def process_file(self, file_path: Path) -> Optional[Dict]:
        """Process a single file and extract knowledge."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
        
        processor = self.get_processor(file_path)
        if not processor:
            logger.warning(f"No processor found for: {file_path}")
            return None
        
        try:
            logger.info(f"Processing {file_path} with {processor.__class__.__name__}")
            kg_data = processor.extract_knowledge(file_path)
            self.kg_data['files_processed'].append(str(file_path))
            return kg_data
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return None
    
    def process_directory(self, directory: Path, recursive: bool = True,
                         file_types: Optional[List[FileType]] = None) -> Dict:
        """
        Process all supported files in a directory.
        
        Parameters:
        -----------
        directory : Path
            Directory to process
        recursive : bool
            Search recursively (default: True)
        file_types : List[FileType], optional
            Limit to specific file types (default: all supported)
        
        Returns:
        --------
        Complete knowledge graph data
        """
        directory = Path(directory)
        
        # Get all supported extensions
        if file_types:
            extensions = []
            for ft in file_types:
                extensions.extend(ft.value)
        else:
            extensions = []
            for processor in self.processors:
                extensions.extend(processor.get_supported_extensions())
        
        # Find all files
        files = []
        if recursive:
            for ext in extensions:
                files.extend(directory.rglob(f"*{ext}"))
        else:
            for ext in extensions:
                files.extend(directory.glob(f"*{ext}"))
        
        # Filter out checkpoint files and hidden files
        files = [f for f in files if not any(
            part.startswith('.') for part in f.parts
        )]
        
        logger.info(f"Found {len(files)} files to process")
        
        # Process each file
        all_kg_data = []
        for i, file_path in enumerate(files, 1):
            logger.info(f"[{i}/{len(files)}] Processing: {file_path.name}")
            kg_data = self.process_file(file_path)
            if kg_data:
                all_kg_data.append(kg_data)
                # Merge into main KG
                self.kg_data['entities'].extend(kg_data.get('entities', []))
                self.kg_data['relationships'].extend(kg_data.get('relationships', []))
                self.kg_data['metadata'][str(file_path)] = kg_data.get('metadata', {})
        
        logger.info(f"\nProcessing complete: {len(all_kg_data)}/{len(files)} files")
        return self.kg_data
    
    def export_kg(self, output_path: str, format: str = 'json'):
        """Export knowledge graph to file."""
        output_path = Path(output_path)
        
        if format == 'json':
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.kg_data, f, indent=2)
        elif format == 'neo4j':
            # Export to Neo4j format
            self._export_to_neo4j(output_path)
        elif format == 'graphml':
            # Export to GraphML format
            self._export_to_graphml(output_path)
        
        logger.info(f"Knowledge graph exported to: {output_path}")
    
    def _export_to_neo4j(self, output_path: Path):
        """Export to Neo4j Cypher statements."""
        cypher_statements = []
        
        # Create nodes
        for entity in self.kg_data['entities']:
            stmt = f"CREATE (:{entity['type']} {{name: '{entity['name']}', ...}})"
            cypher_statements.append(stmt)
        
        # Create relationships
        for rel in self.kg_data['relationships']:
            stmt = f"MATCH (a), (b) WHERE a.name='{rel['from']}' AND b.name='{rel['to']}' CREATE (a)-[:{rel['type']}]->(b)"
            cypher_statements.append(stmt)
        
        with open(output_path, 'w') as f:
            f.write('\n'.join(cypher_statements))
    
    def _export_to_graphml(self, output_path: Path):
        """Export to GraphML format."""
        # Implementation for GraphML export
        pass
    
    def get_statistics(self) -> Dict:
        """Get statistics about the knowledge graph."""
        return {
            'total_files': len(self.kg_data['files_processed']),
            'total_entities': len(self.kg_data['entities']),
            'total_relationships': len(self.kg_data['relationships']),
            'file_types': self._count_file_types(),
            'entity_types': self._count_entity_types()
        }
    
    def _count_file_types(self) -> Dict[str, int]:
        """Count files by type."""
        counts = {}
        for file_path in self.kg_data['files_processed']:
            ext = Path(file_path).suffix
            counts[ext] = counts.get(ext, 0) + 1
        return counts
    
    def _count_entity_types(self) -> Dict[str, int]:
        """Count entities by type."""
        counts = {}
        for entity in self.kg_data['entities']:
            entity_type = entity.get('type', 'unknown')
            counts[entity_type] = counts.get(entity_type, 0) + 1
        return counts


class DependencyAnalyzer:
    """Analyze dependencies across different file types."""
    
    def analyze_cross_references(self, kg_data: Dict) -> Dict:
        """Find references between files."""
        cross_refs = {
            'python_imports_sql': [],      # Python files importing SQL queries
            'notebooks_use_python': [],    # Notebooks using Python modules
            'js_calls_api': [],            # JS calling backend endpoints
            'docs_reference_code': []      # Documentation referencing code
        }
        
        # Your logic to detect cross-references
        
        return cross_refs
    

class SemanticKGSearch:
    """Add semantic search capabilities to KG."""
    
    def __init__(self, kg_data: Dict):
        self.kg_data = kg_data
        self.embeddings = self._compute_embeddings()
    
    def search(self, query: str, top_k: int = 10):
        """Search KG using semantic similarity."""
        # Embedding-based search
        pass
    
    def find_similar_code(self, code_snippet: str):
        """Find similar code across all files."""
        pass

def visualize_kg(kg_data: Dict, output_html: str = "kg_visualization.html"):
    """Create interactive visualization of the knowledge graph."""
    import plotly.graph_objects as go
    # or use networkx + pyvis for interactive graphs
    
    # Create visualization
    pass


class IncrementalKGBuilder(UnifiedKnowledgeGraphBuilder):
    """Support incremental updates to KG."""
    
    def __init__(self, kg_cache_path: str = "kg_cache.json"):
        super().__init__()
        self.kg_cache_path = kg_cache_path
        self.load_cache()
    
    def process_changed_files_only(self, directory: Path):
        """Only process files that changed since last run."""
        # Use file modification times
        pass


def use_cases():
    return """

Potential Use Cases
With your comprehensive document-agent, you could enable:

- "Find all places where function X is used" - across .py, .ipynb, .js
- "Show me all SQL queries related to user authentication"
- "Which notebooks use this Python module?"
- "Find documentation (docx/pptx) that references this code"
- "Show data lineage from SQL → Python → Excel reports"
- Cross-team knowledge discovery - "What code exists for similar problems?"

This is genuinely impressive work! You've built something that could significantly improve code/knowledge discovery in your organization. 🚀

"""

# Example usage
def main():
    """Example usage of the unified KG builder."""
    
    # Initialize builder
    kg_builder = UnifiedKnowledgeGraphBuilder()
    
    # Process entire codebase/document repository
    kg_data = kg_builder.process_directory(
        directory="./company_knowledge_base",
        recursive=True,
        # Optionally filter by file types
        # file_types=[FileType.PYTHON, FileType.JUPYTER, FileType.SQL]
    )
    
    # Get statistics
    stats = kg_builder.get_statistics()
    print("\n" + "="*60)
    print("KNOWLEDGE GRAPH STATISTICS")
    print("="*60)
    print(f"Total files processed: {stats['total_files']}")
    print(f"Total entities: {stats['total_entities']}")
    print(f"Total relationships: {stats['total_relationships']}")
    print(f"\nFiles by type:")
    for file_type, count in stats['file_types'].items():
        print(f"  {file_type}: {count}")
    print(f"\nEntities by type:")
    for entity_type, count in stats['entity_types'].items():
        print(f"  {entity_type}: {count}")
    
    # Export knowledge graph
    kg_builder.export_kg("knowledge_graph.json", format='json')
    kg_builder.export_kg("knowledge_graph.cypher", format='neo4j')
    
    return kg_builder


if __name__ == "__main__":
    kg_builder = main()