Here's how to set up npm to install global packages without sudo by using a local npm directory:

## 1. Create the global directory
```bash
mkdir ~/.npm-global
```

## 2. Configure npm to use this directory
```bash
npm config set prefix '~/.npm-global'
```

## 3. Add to your PATH
Add this line to your shell profile file (`~/.bashrc`, `~/.zshrc`, or `~/.profile`):

```bash
export PATH=~/.npm-global/bin:$PATH
```

## 4. Reload your shell configuration
```bash
# For bash
source ~/.bashrc

# For zsh  
source ~/.zshrc

# Or just restart your terminal
```

## 5. Now you can install global packages without sudo
```bash
npm install -g package-name
```

## Verify it's working
```bash
# Check npm config
npm config get prefix
# Should show: /home/yourusername/.npm-global

# Test with a package
npm install -g cowsay
cowsay "It works!"
```

The packages will now be installed in `~/.npm-global/lib/node_modules/` and executables in `~/.npm-global/bin/`, all owned by your user account. No more `sudo` needed!