# Changed Filter

Quick panel filter for git changed files with staging status. Navigate quickly to files you're working on based on their git status.

## Features

- Filter changed files by status: All Changes, Staged Only, Unstaged Only
- Hierarchical drill-down interface
- Shows file counts for each filter
- Full paths relative to git repository root
- Works with any git repository

## Installation

### Via Package Control

1. Open Command Palette (Cmd+Shift+P / Ctrl+Shift+P)
2. Select "Package Control: Add Repository"
3. Enter: `https://brady-zip.github.io/sublime-text-packages/repositories.json`
4. Open Command Palette again
5. Select "Package Control: Install Package"
6. Select "Changed Filter"

### Manual Installation

Clone this repository into your Sublime Text Packages directory:

```bash
cd ~/Library/Application\ Support/Sublime\ Text/Packages/
git clone https://github.com/brady-zip/sublime-changed-filter.git "Changed Filter"
```

## Usage

1. Open Command Palette (Cmd+Shift+P / Ctrl+Shift+P)
2. Type "Changed Filter" and select it
3. Choose a filter:
   - **All Changes** - Shows all staged and unstaged files
   - **Staged Only** - Shows only files in the staging area
   - **Unstaged Only** - Shows only files with unstaged changes or untracked files
4. Select a file to open it

### Keyboard Shortcut (Optional)

Add to your user key bindings (Preferences → Key Bindings):

```json
{
    "keys": ["super+shift+g"],
    "command": "changed_filter"
}
```

## Requirements

- Git must be installed and available in PATH
- Current file/project must be in a git repository

## License

MIT License - see LICENSE file for details
