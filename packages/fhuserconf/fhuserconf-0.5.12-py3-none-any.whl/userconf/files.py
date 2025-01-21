"""UserConf - Files."""

# from os import makedirs
# from os.path import abspath, exists, join
from pathlib import Path


class FilesManager:
    """User configuration file manager."""

    # def __init__(self, root_path: str):
    def __init__(self, root_path: Path):
        """Initialize the instance with a file directory path.

        The files or directories managed by this class are inside the root
        directory (`root_path`). If the root directory doesn't exist, it will
        be created along all its intermediate directories the first time the
        `get_path` method is called.

        :param root_path: Relative or absolute path of the root directory. If
        it's a relative path, it's converted to its absolute path.
        """
        # self._root_path = abspath(root_path)
        self._root_path = root_path.absolute()

    @property
    # def root_path(self) -> str:
    def root_path(self) -> Path:
        """Return the absolute path of the root directory.

        :return: Directory path.
        """
        return self._root_path

    # def get_path(self, name: str) -> str:
    def get_path(self, name: str) -> Path:
        """Return the absolute path of a managed file or directory.

        The path returned is the absolute path of the root directory
        (`self._root_path`) followed by the name of the given file or directory
        (`name`). If the root directory doesn't exist, it's created along all
        its intermediate directories.

        :param name: File/directory name.
        :return: File/directory path.
        """
        # if not exists(self._root_path):
        #     makedirs(self._root_path)
        if not self._root_path.exists():
            self._root_path.mkdir(parents=True)

        if not (self._root_path / name).parent.exists():
            (self._root_path / name).parent.mkdir(parents=True)

        # return join(self._root_path, name)
        return self._root_path / name
