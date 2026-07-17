import re, os

BASE = "E:/界限论"
chapters = [
    ("第三章", f"{BASE}/界限论_第三章_可读重写_v1_9.md", "E:/download/界限论_第三章_可读重写_v1_10.md", "v1_10"),
    ("第四章", f"{BASE}/界限论_第四章_可读重写_v0_35.md", "E:/download/界限论_第四章_可读重写_v0_36.md", "v0_36"),
    ("第零章", None, "E:/download/界限论_第零章_可读重写_v0_43.md", "v0_43"),
]

# 第零章 uses a different path pattern
chapters[2] = ("第零章", f"{BASE}/界限论_第零章_可读重写_v0_42.md", "E:/download/界限论_第零章_可读重写_v0_43.md", "v0_43")

print("=== File sizes ===")
for name, prj_path, dl_path, ver in chapters:
    prj_size = os.path.getsize(prj_path) if os.path.exists(prj_path) else 0
    dl_size = os.path.getsize(dl_path)
    delta = dl_size - prj_size
    sign = "+" if delta >= 0 else ""
    print(f"  {name}: project={prj_size}, download={dl_size} ({sign}{delta} bytes)")

print("\n=== DL first line ===")
for name, prj_path, dl_path, ver in chapters:
    with open(dl_path, encoding="utf-8") as f:
        first = f.readline().strip()
    print(f"  {name}: {first[:120]}")

print("\n=== DL history tail ===")
for name, prj_path, dl_path, ver in chapters:
    with open(dl_path, encoding="utf-8") as f:
        txt = f.read()
    hist = txt.rsplit("\n---\n", 1)[1] if len(txt.rsplit("\n---\n", 1)) >= 2 else ""
    vv = re.findall(r"v([\d.]+)→v([\d.]+)", hist)
    if vv:
        print(f"  {name} ({len(vv)} entries): {', '.join(f'{a}->{b}' for a,b in vv[:5])}{'...' if len(vv) > 5 else ''}")
    else:
        print(f"  {name}: no *-style history entries, checking > → format...")
        gt = re.findall(r"\*\*v([\d.]+)", hist)
        if gt:
            print(f"    > → format: {gt[:5]}{'...' if len(gt)>5 else ''}")
