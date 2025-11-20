import json
import subprocess
from pathlib import Path

def render_images(img_path_list, output_notebook="display_images.ipynb", 
                  title="Image Gallery", images_per_row=2,
                  execute_and_export=False, output_html=None):
    """
    Generate a Jupyter notebook to display images from a list of file paths.
    
    Parameters:
    -----------
    img_path_list : list
        List of image file paths (strings or Path objects)
    output_notebook : str
        Name of the output .ipynb file (default: "display_images.ipynb")
    title : str
        Title for the notebook (default: "Image Gallery")
    images_per_row : int
        Number of images to display per row (default: 2)
    execute_and_export : bool
        If True, execute the notebook and export to HTML (default: False)
    output_html : str
        Name of output HTML file (default: same name as notebook with .html extension)
    
    Returns:
    --------
    str : Path to the created notebook file (and HTML if execute_and_export=True)
    """
    
    # [Previous notebook creation code remains the same...]
    # Create notebook structure
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Add title cell
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [f"# {title}\n\nTotal images: {len(img_path_list)}"]
    })
    
    # Add imports cell
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from IPython.display import Image, display\n",
            "from pathlib import Path\n",
            "import matplotlib.pyplot as plt\n",
            "from PIL import Image as PILImage"
        ]
    })
    
    # Add matplotlib display cell
    code_lines = [
        f"# Display {len(img_path_list)} images",
        f"fig, axes = plt.subplots({(len(img_path_list) + images_per_row - 1) // images_per_row}, {images_per_row}, figsize=(15, {5 * ((len(img_path_list) + images_per_row - 1) // images_per_row)}))",
        "if len(axes.shape) == 1:",
        "    axes = axes.reshape(-1, 1)",
        "",
        "images = ["
    ]
    
    for path in img_path_list:
        code_lines.append(f'    r"{path}",')
    
    code_lines.extend([
        "]",
        "",
        "for idx, img_path in enumerate(images):",
        f"    row = idx // {images_per_row}",
        f"    col = idx % {images_per_row}",
        "    if Path(img_path).exists():",
        "        img = PILImage.open(img_path)",
        "        axes[row, col].imshow(img)",
        "        axes[row, col].set_title(Path(img_path).name, fontsize=10)",
        "        axes[row, col].axis('off')",
        "    else:",
        "        axes[row, col].text(0.5, 0.5, 'Image not found', ha='center', va='center')",
        "        axes[row, col].set_title(Path(img_path).name, fontsize=10)",
        "        axes[row, col].axis('off')",
        "",
        "# Hide empty subplots",
        f"for idx in range(len(images), {((len(img_path_list) + images_per_row - 1) // images_per_row) * images_per_row}):",
        f"    row = idx // {images_per_row}",
        f"    col = idx % {images_per_row}",
        "    axes[row, col].axis('off')",
        "",
        "plt.tight_layout()",
        "plt.show()"
    ])
    
    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code_lines
    })
    
    # Write notebook to file
    with open(output_notebook, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)
    
    print(f"Notebook created: {output_notebook}")
    
    # Execute and export to HTML if requested
    if execute_and_export:
        if output_html is None:
            output_html = Path(output_notebook).stem + ".html"
        
        execute_and_convert_to_html(output_notebook, output_html)
        return output_notebook, output_html
    
    return output_notebook


def execute_and_convert_to_html(notebook_path, html_path):
    """
    Execute a Jupyter notebook and convert it to HTML.
    
    Parameters:
    -----------
    notebook_path : str
        Path to the input .ipynb file
    html_path : str
        Path to the output .html file
    """
    try:
        print(f"Executing notebook: {notebook_path}")
        
        # Execute and convert in one command
        subprocess.run([
            "jupyter", "nbconvert",
            "--to", "html",
            "--execute",
            "--output", html_path,
            notebook_path
        ], check=True)
        
        print(f"HTML exported: {html_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during execution/conversion: {e}")
    except FileNotFoundError:
        print("Error: jupyter nbconvert not found. Install with: pip install nbconvert")


# Example usage:
if __name__ == "__main__":
    image_paths = [
        "image1.jpg",
        "image2.png",
        "image3.jpg",
    ]
    
    # Create notebook and export to HTML
    render_images(
        image_paths, 
        output_notebook="my_images.ipynb",
        title="My Image Gallery",
        images_per_row=2,
        execute_and_export=True,  # Enable execution and HTML export
        output_html="my_images.html"  # Optional: specify HTML filename
    )