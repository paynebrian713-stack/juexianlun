import difflib
a = open(r"E:\download\界限论_第四章_可读重写_v0_27.md", encoding="utf-8").read().splitlines(True)
b = open(r"E:\界限论\界限论_第四章_可读重写_v0_29.md", encoding="utf-8").read().splitlines(True)
diff = list(difflib.unified_diff(a, b, fromfile="v27", tofile="v29", n=0))
# Show only lines that were REMOVED (starting with -)
removed = []
for l in diff:
    if l.startswith("-") and not l.startswith("---"):
        removed.append(l[1:].rstrip())
    elif l.startswith("+") and not l.startswith("+++"):
        # show added too
        pass
print(f"Removed lines: {len(removed)}")
for line in removed[:50]:
    print(line[:200])
# Also count added lines
added = [l[1:].rstrip() for l in diff if l.startswith("+") and not l.startswith("+++")]
print(f"\nAdded lines: {len(added)}")
for line in added[:20]:
    print(line[:200])
