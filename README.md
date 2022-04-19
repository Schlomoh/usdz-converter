# glTF to USDZ converter
Python gltf to usdz converter using docker image <a href='https://hub.docker.com/r/plattar/python-xrutils'>plattar/xrutils</a>.

This can convert `.gltf` and `.glb` files into apples `.usdz` file type using googles available <a href='https://github.com/google/usd_from_gltf'>usd_from_gltf</a>. 

## Installation

A requirements.txt is included and can be used to install the necessary requirements.

```shell
 pip install -r requirements.txt 
```
 
 or (if python3 and pip3 are not the default)
 
 ```shell
 pip3 install -r requirements.txt
```

Also docker has to be installed on the host machine. If you're using this tool on a windows machine you will hav to activate the WSL option 
in docker and install the WSL extension for windows.

## Usage

Run the main.py script with the argument `-h` to see the the command info. 

for a single file conversion simply type: 

```shell
python main.py path/to/input/file.gltf
```
This will create a `_out` folder inside the projects root directory.

You can also define a custom output directory by typing: 
```shell
python main.py path/to/input/file.gltf -o /path/to/output/dir
```

When defining the input you can also set the parameter to a directory containing gltf files. By default every directory gets read out recursively 
,so including all of its subdirectories.

To disable this set the `-r` flag to `False`.

