from hashlib import md5


class D3D9Generator:
    _renderer_offset = 65780
    _renderer_len = 16
    _gpu_offset = _renderer_offset + _renderer_len
    _gpu_len = 24

    _full_hash = "F72386EFF8B866EB881FE8E87261A2B3"
    _partial_hash = "1E5F7C4EBE25B462A8F61B40907B1BD3"

    def __init__(self, source: bytes):
        self._dll_array = bytearray(source)

    def set_renderer(self, name: str):
        self.set_bytes(self._renderer_offset, self._renderer_len, name)

    def set_gpu(self, name: str):
        self.set_bytes(self._gpu_offset, self._gpu_len, name)

    def set_bytes(self, start: int, length: int, value: str):
        for i in range(length):
            if len(value) > i:
                self._dll_array[start + i] = ord(value[i])
            else:
                self._dll_array[start + i] = 0x00

    def has_full_hash(self):
        return self._full_hash.lower() in md5(self._dll_array).hexdigest().lower()

    def has_partial_hash(self):
        start = self._gpu_offset + self._gpu_len
        end = start + len(self._dll_array) - (self._gpu_offset + self._gpu_len)

        md = md5()
        md.update(self._dll_array[: self._renderer_offset - 1])
        md.update(self._dll_array[start:end])

        return self._partial_hash.lower() in md.hexdigest().lower()

    def write_dll(self, filename: str):
        with open(filename, "wb") as file:
            file.write(self._dll_array)


def main():
    with open("d3d9_source.dll", "rb") as file:
        source_dll = file.read()

    generator = D3D9Generator(source_dll)
    if not generator.has_full_hash():
        raise Exception("Internal DLL is corrupted")

    gpu = ""

    while len(gpu) == 0:
        gpu = input("Enter your GPU name: ")

    print(f"Generating d3d9.dll for {gpu}")

    generator.set_gpu(gpu)

    if not generator.has_partial_hash():
        raise Exception("Internal DLL is corrupted after setting")

    generator.write_dll("d3d9.dll")


if __name__ == "__main__":
    main()
