def convert_notebook_to_html(notebook_path, html_path=None, execute=True):
    """
    Convert a Jupyter notebook to HTML, optionally executing it first.
    
    Parameters:
    -----------
    notebook_path : str
        Path to the .ipynb file
    html_path : str, optional
        Path to output HTML file (default: same name with .html extension)
    execute : bool
        Whether to execute the notebook before converting (default: True)
    """
    import subprocess
    from pathlib import Path
    
    if html_path is None:
        html_path = Path(notebook_path).stem + ".html"
    
    cmd = ["jupyter", "nbconvert", "--to", "html"]
    
    if execute:
        cmd.append("--execute")
    
    cmd.extend(["--output", html_path, notebook_path])
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully converted to: {html_path}")
    except FileNotFoundError:
        print("Error: Please install nbconvert: pip install nbconvert")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")

# Usage:
convert_notebook_to_html("my_images.ipynb")