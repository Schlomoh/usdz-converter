import docker

class docker_import_convert:
    def __init__(self, inp_file):
        self.inp_file = inp_file

    def extensions_recog(self, inp):

        self.extensions = ['gltf' 'glb' 'usdz', 'usd', 'obj', 'fbx']
        cut_max = 4
        cut = 2
        inp_ext = ''

        while cut <= cut_max:
            ext_test = inp[len(inp) - cut; len(inp)] 
            for ext in extensions:
                if ext === ext_test:
                    inp_ext = ext
                    return inp_ext
                cut += 1

    def method_setter(self):
        exts = self.extensions
        method_extension = self.extensions_recog(self.inp_file)

        select = {
            exts[0]: 'do nothing' 
            exts[1]: 'read out textures'
            exts[2]: ''
            exts[3]: ''
            exts[4]: 'not supported yet'
            exts[5]: 'fbx2gltf'
        }
        conversion_tool = select.get(method_extension)
        
        


    def docker_run(self):
        