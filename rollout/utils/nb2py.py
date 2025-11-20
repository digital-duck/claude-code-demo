import json
from pathlib import Path
import nbformat
from nbconvert import PythonExporter
import subprocess

def batch_convert_notebooks_to_py(directory, output_dir=None, pattern="*.ipynb"):
    """
    Convert all notebooks in a directory to Python scripts.
    
    Parameters:
    -----------
    directory : str
        Directory containing notebooks
    output_dir : str, optional
        Output directory (default: same as input)
    pattern : str
        File pattern to match (default: "*.ipynb")
    
    Returns:
    --------
    list : List of created Python files
    """
    directory = Path(directory)
    if output_dir is None:
        output_dir = directory
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
    
    notebooks = list(directory.glob(pattern))
    converted = []
    
    for nb in notebooks:
        py_path = output_dir / (nb.stem + ".py")
        try:
            subprocess.run([
                "jupyter", "nbconvert",
                "--to", "script",
                "--output", str(py_path),
                str(nb)
            ], check=True, capture_output=True)
            print(f"Converted: {nb.name} -> {py_path.name}")
            converted.append(str(py_path))
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {nb.name}: {e}")
    
    print(f"\nTotal converted: {len(converted)}/{len(notebooks)}")
    return converted



def convert_nb_to_py_with_nbformat(notebook_path, py_path=None):
    """
    Convert notebook to Python using nbformat and nbconvert.
    
    Parameters:
    -----------
    notebook_path : str
        Path to the .ipynb file
    py_path : str, optional
        Path to output .py file
    
    Returns:
    --------
    str : Path to the created Python file
    """
    if py_path is None:
        py_path = Path(notebook_path).stem + ".py"
    
    try:
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Convert to Python
        exporter = PythonExporter()
        python_code, _ = exporter.from_notebook_node(notebook)
        
        # Write to file
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(python_code)
        
        print(f"Python script created: {py_path}")
        return py_path
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None


def notebook_to_python(notebook_path, py_path=None, 
                       include_markdown=True, 
                       include_outputs=False):
    """
    Convert Jupyter notebook to Python script with custom options.
    
    Parameters:
    -----------
    notebook_path : str
        Path to the .ipynb file
    py_path : str, optional
        Path to output .py file
    include_markdown : bool
        Include markdown cells as comments (default: True)
    include_outputs : bool
        Include cell outputs as comments (default: False)
    
    Returns:
    --------
    str : Path to the created Python file
    """
    if py_path is None:
        py_path = Path(notebook_path).stem + ".py"
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    python_lines = []
    
    # Add header
    python_lines.append(f'# Converted from {Path(notebook_path).name}')
    python_lines.append('')
    
    # Process each cell
    for cell in notebook['cells']:
        cell_type = cell['cell_type']
        
        if cell_type == 'markdown' and include_markdown:
            # Add markdown as comments
            python_lines.append('# ' + '='*70)
            for line in cell['source']:
                python_lines.append(f'# {line.rstrip()}')
            python_lines.append('# ' + '='*70)
            python_lines.append('')
            
        elif cell_type == 'code':
            # Add code cells
            source = cell['source']
            if isinstance(source, list):
                python_lines.extend([line.rstrip() for line in source])
            else:
                python_lines.append(source.rstrip())
            
            # Optionally add outputs as comments
            if include_outputs and 'outputs' in cell:
                for output in cell['outputs']:
                    if 'text' in output:
                        python_lines.append('')
                        python_lines.append('# Output:')
                        text = output['text']
                        if isinstance(text, list):
                            for line in text:
                                python_lines.append(f'# {line.rstrip()}')
                        else:
                            python_lines.append(f'# {text.rstrip()}')
            
            python_lines.append('')
            python_lines.append('')
    
    # Write to file
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(python_lines))
    
    print(f"Python script created: {py_path}")
    return py_path

# Usage:
notebook_to_python("my_notebook.ipynb")
notebook_to_python("my_notebook.ipynb", include_markdown=False)
notebook_to_python("my_notebook.ipynb", include_outputs=True)

# Usage:
convert_nb_to_py_with_nbformat("my_notebook.ipynb")


# Usage:
batch_convert_notebooks_to_py("./notebooks")
batch_convert_notebooks_to_py("./notebooks", output_dir="./scripts")
