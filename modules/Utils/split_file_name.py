def split_file_name(file):
    found = False
    i = len(file) - 1
            
    while i >= 0:
        if file[i] == '/':
            file_name = file[i + 1: len(file)]
            file_path = file[0: i + 1]
            found = True
            break
        i -= 1

    if not found:
        file_path = './'
        file_name = file

    split = {
        'file_path' : file_path,
        'file_name' : file_name
    }
    print('The input selection was split into ' + file_path + ' and ' + file_name, chr(10))

    return split