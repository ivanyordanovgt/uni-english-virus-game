def create_full_1gb_file(filename):
    size = 1 * 1024 * 1024 * 1024  # 1GB in bytes
    with open(filename, 'wb') as f:
        f.write(b'\x00' * size)


