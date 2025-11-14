"""
Changed Filter - Quick panel filter for git changed files with staging status

Author: brady-zip
License: MIT
"""
import sublime
import sublime_plugin
import subprocess
import os


class ChangedFilterCommand(sublime_plugin.WindowCommand):
    """Command to show changed files filtered by staging status"""

    def run(self):
        """Entry point for the command"""
        # Initialize state
        self.git_root = None
        self.all_files = []
        self.staged_files = []
        self.unstaged_files = []
        self.current_level = 'filter'
        self.selected_filter = None

        # Check if in git repository and get changed files
        if not self._check_git_repo():
            self._show_error("Not in a git repository")
            return

        if not self._get_changed_files():
            self._show_error("No changed files")
            return

        # Show filter selection
        self._show_filter_selection()

    def _check_git_repo(self):
        """Check if current directory is in a git repository"""
        try:
            # Get the git root directory
            result = subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                cwd=self._get_working_directory(),
                capture_output=True,
                text=True,
                check=True
            )
            self.git_root = result.stdout.strip()
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False

    def _get_working_directory(self):
        """Get the current working directory from the window"""
        # Try to get directory from active view
        view = self.window.active_view()
        if view and view.file_name():
            return os.path.dirname(view.file_name())

        # Try to get from window folders
        folders = self.window.folders()
        if folders:
            return folders[0]

        # Fallback to home directory
        return os.path.expanduser('~')

    def _get_changed_files(self):
        """Get changed files from git status"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.git_root,
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout.strip()
            if not output:
                return False

            # Parse git status output
            for line in output.split('\n'):
                if len(line) < 3:
                    continue

                status = line[:2]
                file_path = line[3:].strip()

                # Remove quotes if present (git adds them for paths with spaces)
                if file_path.startswith('"') and file_path.endswith('"'):
                    file_path = file_path[1:-1]

                self.all_files.append((file_path, status))

                # Categorize files
                first_char = status[0]
                second_char = status[1]

                # Staged: first character is not space or ?
                if first_char not in (' ', '?'):
                    self.staged_files.append(file_path)

                # Unstaged: second character is not space OR untracked
                if second_char != ' ' or status == '??':
                    self.unstaged_files.append(file_path)

            # Sort files alphabetically
            self.all_files.sort(key=lambda x: x[0])
            self.staged_files.sort()
            self.unstaged_files.sort()

            return len(self.all_files) > 0

        except subprocess.CalledProcessError as e:
            self._show_error(f"Error running git: {e}")
            return False
        except FileNotFoundError:
            self._show_error("Git not found in PATH")
            return False

    def _show_filter_selection(self):
        """Show the filter selection quick panel"""
        # Get unique file counts (a file can be in both staged and unstaged)
        all_count = len(set([f[0] for f in self.all_files]))
        staged_count = len(self.staged_files)
        unstaged_count = len(self.unstaged_files)

        items = [
            [f"All Changes ({all_count} files)", "Show all staged and unstaged files"],
            [f"Staged Only ({staged_count} files)", "Show only files in the staging area"],
            [f"Unstaged Only ({unstaged_count} files)", "Show only unstaged changes and untracked files"]
        ]

        self.window.show_quick_panel(
            items,
            self._on_filter_selected,
            placeholder="Changed Filter |"
        )

    def _on_filter_selected(self, index):
        """Handle filter selection"""
        if index == -1:
            return

        # Map index to filter type
        filter_types = ['all', 'staged', 'unstaged']
        self.selected_filter = filter_types[index]

        # Show files for selected filter
        self._show_file_list()

    def _show_file_list(self):
        """Show the file list for the selected filter"""
        # Get files based on selected filter
        if self.selected_filter == 'all':
            files = [f[0] for f in self.all_files]
            # Remove duplicates while preserving order
            seen = set()
            files = [f for f in files if not (f in seen or seen.add(f))]
            filter_name = "All Changes"
        elif self.selected_filter == 'staged':
            files = self.staged_files
            filter_name = "Staged Only"
        else:  # unstaged
            files = self.unstaged_files
            filter_name = "Unstaged Only"

        if not files:
            self._show_error(f"No {filter_name.lower()}")
            return

        self.window.show_quick_panel(
            files,
            self._on_file_selected,
            placeholder=f"Changed Filter | {filter_name} |",
            on_highlight=None
        )

    def _on_file_selected(self, index):
        """Handle file selection"""
        if index == -1:
            # User pressed ESC, go back to filter selection
            self._show_filter_selection()
            return

        # Get the selected file
        if self.selected_filter == 'all':
            files = [f[0] for f in self.all_files]
            # Remove duplicates while preserving order
            seen = set()
            files = [f for f in files if not (f in seen or seen.add(f))]
        elif self.selected_filter == 'staged':
            files = self.staged_files
        else:
            files = self.unstaged_files

        file_path = files[index]
        full_path = os.path.join(self.git_root, file_path)

        # Open the file
        self.window.open_file(full_path)

    def _show_error(self, message):
        """Show error message in quick panel"""
        self.window.show_quick_panel(
            [[message]],
            None,
            flags=sublime.MONOSPACE_FONT,
            placeholder="Changed Filter |"
        )

    def is_enabled(self):
        """Command is always enabled (shows error if not in git repo)"""
        return True
