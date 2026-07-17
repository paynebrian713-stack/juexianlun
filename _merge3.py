import re, os

BASE = "E:/界限论"
chapters = [
    ("E:/界限论/界限论_第三章_可读重写_v1_9.md", "E:/download/界限论_第三章_可读重写_v1_10.md", "E:/界限论/界限论_第三章_可读重写_v1_10.md"),
    ("E:/界限论/界限论_第四章_可读重写_v0_35.md", "E:/download/界限论_第四章_可读重写_v0_36.md", "E:/界限论/界限论_第四章_可读重写_v0_36.md"),
    ("E:/界限论/界限论_第零章_可读重写_v0_42.md", "E:/download/界限论_第零章_可读重写_v0_43.md", "E:/界限论/界限论_第零章_可读重写_v0_43.md"),
]

for old_path, dl_path, new_path in chapters:
    name = os.path.basename(old_path).replace("界限论_", "").replace("_可读重写", "")
    print(f"\n--- {name} ---")
    
    with open(old_path, encoding="utf-8") as f:
        old = f.read()
    with open(dl_path, encoding="utf-8") as f:
        dl = f.read()
    
    # Extract old history
    old_parts = old.rsplit("\n---\n", 1)
    old_hist = old_parts[1] if len(old_parts) >= 2 else ""
    
    # Extract DL history
    dl_parts = dl.rsplit("\n---\n", 1)
    dl_body = dl_parts[0]
    dl_hist = dl_parts[1] if len(dl_parts) >= 2 else ""
    
    # Extract old entries (lines starting with *, contain vX->vY)
    old_entries = []
    for ln in old_hist.split("\n"):
        if ln.strip().startswith("*") and "→v" in ln[:150]:
            old_entries.append(ln.strip())
    
    # Extract DL entries
    dl_entries = []
    for ln in dl_hist.split("\n"):
        if ln.strip().startswith("*") and "→v" in ln[:150]:
            dl_entries.append(ln.strip())
    
    # Merge: put old entries first (they have the deep history), then DL's new entry
    # But avoid duplicating the last DL entry if it already exists in old
    merged_entries = []
    seen = set()
    for e in old_entries:
        # Extract vX->vY
        m = re.search(r"v([\d.]+)→v([\d.]+)", e[:150])
        key = f"{m.group(1)}→{m.group(2)}" if m else e
        if key not in seen:
            merged_entries.append(e)
            seen.add(key)
    for e in dl_entries:
        m = re.search(r"v([\d.]+)→v([\d.]+)", e[:150])
        key = f"{m.group(1)}→{m.group(2)}" if m else e
        if key not in seen:
            merged_entries.append(e)
            seen.add(key)
    
    print(f"  Old entries: {len(old_entries)}, DL entries: {len(dl_entries)}, Merged: {len(merged_entries)}")
    
    # Rebuild history: keep any non-entry preamble + merged entries + any trailer
    # Simple approach: put all merged entries, sorted by first version in key
    # But for chapters, order matters (chronological). Just use old_hist preamble + merged.
    # Find preamble (everything before first *-entry line)
    first_star = None
    for ln_num, ln in enumerate(old_hist.split("\n")):
        if ln.strip().startswith("*") and "→v" in ln[:150]:
            first_star = ln_num
            break
    
    preamble_lines = old_hist.split("\n")[:first_star] if first_star is not None else []
    preamble = "\n".join(preamble_lines) if preamble_lines else ""
    
    new_hist = preamble
    if new_hist and not new_hist.endswith("\n"):
        new_hist += "\n"
    new_hist += "\n".join(merged_entries)
    
    # Write new file
    output = dl_body + "\n---\n" + new_hist
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"  Output: {len(output)} bytes")
    
    # Verify chain
    vv = re.findall(r"v([\d.]+)→v([\d.]+)", "\n".join(merged_entries))
    for i in range(len(vv)-1):
        if vv[i][1] != vv[i+1][0]:
            print(f"  ⚠️ Chain break: v{vv[i][1]} → v{vv[i+1][0]}")
    if len(vv) >= 2:
        chain = " → ".join(f"v{a}→v{b}" for a,b in vv)
        print(f"  Chain: {chain}")
    
    # Delete old file
    os.remove(old_path)
    print(f"  Deleted {os.path.basename(old_path)}")

print("\n=== Done ===")
