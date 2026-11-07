"""Build and verify the supplemental Chinese PAK, without modifying the base game."""
import csv
import hashlib
import io
import json
from pathlib import Path
from asset_tool import collect
from pak_tool import Pak, PAK, write_pak
from translate_catalog import translations
from translate_help import rows, translated_rows

ROOT = Path(__file__).parent
OUT = ROOT / "release"
OUT.mkdir(exist_ok=True)
localized = translated_rows()
catalog = dict(translations)
for source, target in zip(rows, localized):
    if source["SourceString"] != target["SourceString"]:
        catalog[source["SourceString"]] = target["SourceString"]
for source, target in list(catalog.items()):
    catalog[source.replace("\r\n", "\n")] = target
    catalog[source.replace("\r\n", "\n").replace("\n", "\r\n")] = target

files, changes = {}, []
for path, asset in collect(ROOT / "original/HereSphere/Content/UI"):
    result = asset.translate(catalog)
    if result:
        header, data, count = result
        name = path.relative_to(ROOT / "original").as_posix()
        files[name] = header
        files[name.removesuffix(".uasset") + ".uexp"] = data
        changes.append(dict(asset=name, translated_properties=count))
        print(path.stem, count, flush=True)

csv_data = io.StringIO(newline="")
writer = csv.DictWriter(csv_data, fieldnames=["Key", "SourceString"], lineterminator="\r\n")
writer.writeheader()
writer.writerows(localized)
files["HereSphere/Content/Localization/MenuStringTable.csv"] = csv_data.getvalue().encode("utf-8-sig")
(OUT / "MenuStringTable.zh-CN.csv").write_bytes(files["HereSphere/Content/Localization/MenuStringTable.csv"])
patch = OUT / "HereSphere_Chinese_P.pak"
write_pak(patch, files)
reader = Pak(patch)
assert set(reader.entries) == set(files)
for name, data in files.items():
    assert reader.read(name) == data
    assert hashlib.sha1(data).digest() == reader.entries[name]["digest"]
assert [r["Key"] for r in localized] == [r["Key"] for r in rows]
report = dict(base_pak=PAK.name, base_pak_sha256=hashlib.file_digest(PAK.open("rb"), "sha256").hexdigest(),
              patch_sha256=hashlib.file_digest(patch.open("rb"), "sha256").hexdigest(),
              patch_bytes=patch.stat().st_size, files=len(files), assets=len(changes),
              translated_properties=sum(c["translated_properties"] for c in changes),
              help_entries_translated=sum(s["SourceString"] != t["SourceString"] for s,t in zip(rows,localized)),
              help_entries_total=len(rows), changes=changes)
(OUT / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
(ROOT / "translations.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k != "changes"}, indent=2))
