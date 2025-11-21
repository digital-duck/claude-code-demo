
## Create .ipynb

see claude-code-demo/rollout/utils/create_jpy.py

## Convert .ipynb to .html/.py

- API

see `claude-code-demo/rollout/utils/nb2html.py`



- CLI

```bash

pip install nbconvert
pip install nbformat nbconvert


# Execute and convert to HTML
jupyter nbconvert --to html --execute my_images.ipynb

# Convert without executing (if already executed)
jupyter nbconvert --to html my_images.ipynb

# Specify output filename
jupyter nbconvert --to html --execute --output my_gallery.html my_images.ipynb




# Basic conversion
jupyter nbconvert --to script my_notebook.ipynb

# Specify output name
jupyter nbconvert --to script --output my_script.py my_notebook.ipynb

# Convert all notebooks in directory
jupyter nbconvert --to script *.ipynb

# Without cell execution markers
jupyter nbconvert --to python --no-prompt my_notebook.ipynb

```