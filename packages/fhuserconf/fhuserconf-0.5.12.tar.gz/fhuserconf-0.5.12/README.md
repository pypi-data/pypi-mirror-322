# UserConf

本项目在`UserConf`基础上，做了一些调整，具体如下：

- 配置文件存储位置, 由用户目录调整到当前目录;
- 中文支持: json文件统一使用`utf-8`编码; `Key`支持中文;
- 增加对Python 3.8 的支持;
- 去除对 os.path 的依赖;
- FilesManager 支持创建多层级目录
- 最后重新打包(fhuserconf);

Install from PyPI (Python Package Index)

```bash
pip install fhuserconf
```

UserConf is a user configuration management Python library. It stores key-value
settings in a JSON file and manages data files and directories. The JSON file
and the data files and directories are inside a directory that is inside the
user home directory.

- Version: 0.5.0
- Author: Jose A. Jimenez (jajimenezcarm@gmail.com)
- License: MIT License
- Repository: https://github.com/jajimenez/userconf

## Usage example

```python
from userconf import UserConf

# Create an instance of the UserConf class providing an application ID. The
# settings JSON file is "settings.json" and the directory for data files and
# directories is "files". The "settings.json" file and the "files" directory
# will be created inside a directory which name is a period (".") followed by
# the application ID, which will be created inside the user's home directory
# (e.g. "/home/user/.app/settings.json" and "/home/user/.app/files" in Linux).
uc = UserConf("example-app")

# Set a setting value given the setting key and the value. The value can be any
# object serializable to JSON (a string, an integer, a list, a dictionary...).
uc.settings.set("example-key", "Example value")

# Get a setting value given the setting key. If the key doesn't exist, None is
# returned.
value = uc.settings.get("example-key")
print(value)

# Set a default value to return if the setting doesn't exist
value = uc.settings.get("example-key-2", "Default value")
print(value)

# Delete a setting given its key
uc.settings.delete("example-key")

# Delete all the settings
uc.settings.delete_all()

# Get an absolute path for a data file. This doesn't create the file but it
# creates its directory and all the intermediate directories if they don't
# exist, so that the application using this library can save data in this path
# without having to create its directory.
path = uc.files.get_path("example-file.txt")
print(path)
```

## How to install

We can install UserConf in the following ways:

### Install from PyPI (Python Package Index)

```bash
pip install userconf
```

### Install from the source code

```bash
python setup.py install
```

### Generate a package and install it

We can generate and install the **built package** or the **source archive**
from the source code. The *wheel* package is needed for generating the built
package.

To generate and install the **built package** (preferred), run the following
commands from the project directory:

```bash
pip install wheel
python setup.py bdist_wheel
pip install ./dist/userconf*.whl
```

To generate and install the **source archive**, run the following commands from
the project directory:

```bash
python setup.py sdist
pip install ./dist/userconf*.tar.gz
```

## How to run the unit tests

To run all the unit tests, run the following command from the project
directory:

```bash
python -m unittest discover test
```