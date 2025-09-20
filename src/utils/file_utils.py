
# small helper utilities
import os

def save_bytesio_to_file(bytes_io, path):
    with open(path, 'wb') as f:
        f.write(bytes_io.read())
    return path
