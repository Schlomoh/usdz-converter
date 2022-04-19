def directory_check(directory):

    end = len(directory) - 1 
    if directory[end] != '/':
        directory = directory  + '/'
    return directory

        