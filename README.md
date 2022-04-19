# Import/Export Converter

### Conversion module for the augmentable platform
#### Using Docker Containers for the usdz, fbx and obj conversion
#### Using PyGltfLib for gltf and glb handling
#### Using Python Image Library (PILlow) for texture customization (resizing, format conversion, channel splitting)

## Basic Usage of the legacy version (modularized version is not yet functional)

#### For now only the export is working properly with mandatory texture resizing

The input argument `-i` takes folders with a seperate folder inside containing the gltf files. 
You can also select the individual `.gltf` file to be converted. At the moment you **cannot** select a folder directly containig files.

To not resize Textures set the `-d` and `-q` parameter to `100`.  

When the `-q` argument is set to a percentage it gets multiplied by 95% meaning the MAX compression quality when setting `-q 100` is 95%. 

Even when not resizing gltf textures, they have to be present as seperate files in the same directory as the .gltf and .bin files.
So embedded gltf files can currently not be handled.

At the moment all parameters have to be set

1. `-i` *the input location*
2. `-o` *the output location*
3. `-c` *the conversion either* `gltf-usdz` *or* `gltf-glb` *for now*
4. `-m` *the method so either* `i` *for import (not working) or* `e` *for export*  
(can currently only be `e`)
5. `-d` *the percentage of the texture downsizing*
6. `-q` *the percentage of the texture compression quality*

### Exporting USDZ

##### Docker has to be installed and running to use the USDZ converter.

#### One may use the 'start_usdz.py' for a single script execution with preset arguments and in/out folders.

#### Single file conversion:

To convert gltf files to the USDZ format use the command line to execute following command:

```
python3 controller.py -i location/to/file.gltf -o location/to/output -c gltf-usdz -m e -d 50 -q 50 
```

- sets the input to a single gltf file
- sets the output to a certain directory
- sets the conversion method to convert from gltf to usdz
- sets the method to use the *exporter*
- sets the resizing percentage to 50% so half the original resolution
- sets the comopression quality to 50%


### Exporting GLB 
...