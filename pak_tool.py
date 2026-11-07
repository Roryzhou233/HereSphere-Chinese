"""Small reader/writer for the unencrypted UE4 v9 PAK used by this install."""
from pathlib import Path
import hashlib
import io
import struct
import zlib

GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\HereSphere")
PAK = GAME / "HereSphere/Content/Paks/HereSphere-WindowsNoEditor.pak"


def unpack(f, fmt):
    return struct.unpack(fmt, f.read(struct.calcsize(fmt)))


def string(f):
    n, = unpack(f, "<i")
    return f.read(n).rstrip(b"\0").decode("utf-8") if n >= 0 else f.read(-n * 2).decode("utf-16-le").rstrip("\0")


def fstring(s):
    b = s.encode("utf-8") + b"\0"
    return struct.pack("<i", len(b)) + b


class Pak:
    def __init__(self, path=PAK):
        self.path = Path(path)
        with self.path.open("rb") as f:
            f.seek(-222, 2)
            self.footer = f.read()
            magic, self.version, offset, size = struct.unpack_from("<I i q q", self.footer, 17)
            assert magic == 0x5A6F12E1 and self.version == 9
            assert self.footer[16] == 0, "Encrypted index"
            f.seek(offset)
            data = f.read(size)
            assert hashlib.sha1(data).digest() == self.footer[41:61]
        f = io.BytesIO(data)
        self.mount = string(f)
        count, = unpack(f, "<i")
        self.entries = {}
        for _ in range(count):
            name = string(f)
            start = f.tell()
            offset, size, raw_size, method = unpack(f, "<q q q I")
            digest = f.read(20)
            blocks = []
            if method:
                n, = unpack(f, "<i")
                blocks = [unpack(f, "<q q") for _ in range(n)]
            flags, block_size = unpack(f, "<B I")
            self.entries[name] = dict(offset=offset, size=size, raw_size=raw_size, method=method,
                                      digest=digest, blocks=blocks, flags=flags, header_size=f.tell()-start)
        assert f.tell() == len(data)

    def read(self, name):
        e = self.entries[name]
        assert not e["flags"] & 1
        with self.path.open("rb") as f:
            if e["method"]:
                assert self.footer[62:94].rstrip(b"\0") == b"Zlib"
                parts = []
                for start, end in e["blocks"]:
                    f.seek(e["offset"] + start)
                    parts.append(zlib.decompress(f.read(end-start)))
                data = b"".join(parts)
            else:
                f.seek(e["offset"] + e["header_size"])
                data = f.read(e["size"])
        assert len(data) == e["raw_size"]
        return data


def write_pak(path, files):
    entries = []
    with Path(path).open("wb") as f:
        for name, data in sorted(files.items()):
            offset = f.tell()
            digest = hashlib.sha1(data).digest()
            def entry(at):
                return struct.pack("<q q q I", at, len(data), len(data), 0) + digest + struct.pack("<B I", 0, 0)
            f.write(entry(0))
            f.write(data)
            entries.append(fstring(name) + entry(offset))
        index = fstring("../../../") + struct.pack("<i", len(entries)) + b"".join(entries)
        offset = f.tell()
        f.write(index)
        f.write(bytes(17) + struct.pack("<I i q q", 0x5A6F12E1, 9, offset, len(index)) + hashlib.sha1(index).digest() + bytes(161))


if __name__ == "__main__":
    pak = Pak()
    root = Path(__file__).parent / "original"
    root.mkdir(exist_ok=True)
    (Path(__file__).parent / "pak-index.txt").write_text("\n".join(pak.entries), encoding="utf-8")
    for name in pak.entries:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(pak.read(name))
    print(f"Extracted {len(pak.entries)} files; mount={pak.mount}")
