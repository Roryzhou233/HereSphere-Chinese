"""Edit tagged UI text properties in this UE4.25 cooked asset layout."""
import io
import struct
from pathlib import Path
from pak_tool import string


def text_string(value):
    data = value.encode("utf-16-le") + b"\0\0"
    return struct.pack("<i", -len(data) // 2) + data


class Asset:
    def __init__(self, header, data):
        self.header = header
        self.data = data
        f = io.BytesIO(header)
        assert f.read(4) == bytes.fromhex("c1832a9e")
        assert struct.unpack("<i", f.read(4))[0] == -7
        f.seek(20)
        versions, = struct.unpack("<i", f.read(4))
        f.seek(versions * 20, 1)
        self.header_size, = struct.unpack("<i", f.read(4))
        string(f)
        self.fields = f.tell()
        flags, count, offset, _, _, self.export_count, self.export_offset = struct.unpack("<Iiiiiii", f.read(28))
        f.seek(offset)
        self.names = []
        for _ in range(count):
            self.names.append(string(f))
            f.read(4)
        self.exports = []
        for i in range(self.export_count):
            at = self.export_offset + 104 * i
            size, offset = struct.unpack_from("<qq", header, at + 28)
            assert offset >= self.header_size and offset + size <= self.header_size + len(data)
            self.exports.append((at, offset - self.header_size, size))
        self.properties = []
        types = {i: n for i, n in enumerate(self.names) if n.endswith("Property")}
        for tid, kind in types.items():
            needle = struct.pack("<ii", tid, 0)
            start = 0
            while True:
                at = data.find(needle, start)
                if at < 0:
                    break
                start = at + 1
                if at < 8 or at + 17 >= len(data):
                    continue
                name, number = struct.unpack_from("<ii", data, at - 8)
                size, index = struct.unpack_from("<ii", data, at + 8)
                if not 0 <= name < len(self.names) or number != 0 or not 0 < size < len(data) or not 0 <= index < 1024:
                    continue
                extra = 24 if kind == "StructProperty" else 8 if kind in ("ArrayProperty", "SetProperty", "ByteProperty") else 16 if kind in ("MapProperty", "EnumProperty") else 1 if kind == "BoolProperty" else 0
                guid = at + 16 + extra
                if guid >= len(data) or data[guid] not in (0, 1):
                    continue
                content = guid + 1 + (16 if data[guid] else 0)
                if content + size > len(data):
                    continue
                if not any(e <= at - 8 < content + size <= e + n for _, e, n in self.exports):
                    continue
                self.properties.append(dict(at=at - 8, size_at=at + 8, content=content,
                                            size=size, kind=kind, name=self.names[name]))

    def texts(self):
        for prop in self.properties:
            if prop["kind"] not in ("StrProperty", "TextProperty"):
                continue
            f = io.BytesIO(self.data)
            f.seek(prop["content"])
            try:
                if prop["kind"] == "TextProperty":
                    flags, history = struct.unpack("<Ib", f.read(5))
                    if history != 0:
                        continue
                    namespace, key = string(f), string(f)
                elif prop["name"] not in ("Text", "HintText", "Label"):
                    continue
                start = f.tell()
                value = string(f)
                if f.tell() != prop["content"] + prop["size"]:
                    continue
                yield dict(source=value, start=start, end=f.tell(), property=prop["name"], kind=prop["kind"])
            except (UnicodeError, struct.error, ValueError):
                continue

    def translate(self, translations):
        edits = []
        for item in self.texts():
            source = item["source"]
            if source in translations and source != translations[source]:
                edits.append((item["start"], item["end"], text_string(translations[source])))
        if not edits:
            return None
        edits.sort()
        assert all(a[1] <= b[0] for a, b in zip(edits, edits[1:]))
        data, header = bytearray(self.data), bytearray(self.header)
        # Nested tagged properties include their children's payload in their size.
        for prop in self.properties:
            delta = sum(len(new) - (end - start) for start, end, new in edits
                        if prop["content"] <= start < end <= prop["content"] + prop["size"])
            if delta:
                struct.pack_into("<i", data, prop["size_at"], prop["size"] + delta)
        for at, offset, size in self.exports:
            before = sum(len(new) - (end - start) for start, end, new in edits if end <= offset)
            inside = sum(len(new) - (end - start) for start, end, new in edits if offset <= start < end <= offset + size)
            struct.pack_into("<qq", header, at + 28, size + inside, self.header_size + offset + before)
        # BulkDataStartOffset is a package-relative int64 at the end of the summary.
        old_bulk = self.header_size + len(self.data) - 4
        needle = struct.pack("<q", old_bulk)
        positions = [i for i in range(0, self.names_offset()) if header[i:i+8] == needle]
        for at in positions:
            struct.pack_into("<q", header, at, old_bulk + sum(len(new) - (end-start) for start,end,new in edits))
        for start, end, new in reversed(edits):
            data[start:end] = new
        result = Asset(bytes(header), bytes(data))
        expected = [translations.get(t["source"], t["source"]) for t in self.texts()]
        assert [t["source"] for t in result.texts()] == expected
        return bytes(header), bytes(data), len(edits)

    def names_offset(self):
        return struct.unpack_from("<i", self.header, self.fields + 8)[0]


def collect(root):
    for path in sorted(Path(root).rglob("*.uasset")):
        if path.with_suffix(".uexp").is_file():
            yield path, Asset(path.read_bytes(), path.with_suffix(".uexp").read_bytes())


if __name__ == "__main__":
    import json
    rows = []
    for path, asset in collect("original/HereSphere/Content/UI"):
        for item in asset.texts():
            rows.append(dict(file=str(path), **item))
    Path("ui-text-properties.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    unique = sorted(set(r["source"] for r in rows))
    Path("ui-sources.json").write_text(json.dumps(unique, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"UI text properties: {len(rows)}; unique strings: {len(unique)}")
