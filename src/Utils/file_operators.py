def get_file_size(file):
    from os import SEEK_END
    file.seek(0, SEEK_END)
    return file.tell()

GigaByte = 1073741824
#GigaByte = 40 # Test value (40B)