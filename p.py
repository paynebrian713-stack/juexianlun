import os
files = [
    ("界限论_附录W_v8_7.md", "界限论_附录W_v8_6.md"),
    ("界限论_第二章_可读重写_v0_20.md", "界限论_第二章_可读重写_v0_21.md"),
    ("界限论_尾声_可读重写_v0_13.md", "界限论_尾声_可读重写_v0_13.md"),
    ("界限论_第四章_可读重写_v0_25.md", "界限论_第四章_可读重写_v0_25.md"),
    ("界限论_第八章_可读重写_v0_24.md", "界限论_第八章_可读重写_v0_24.md"),
    ("界限论_第六章_可读重写_v0_22.md", "界限论_第六章_可读重写_v0_22.md"),
    ("界限论_第七章_可读重写_v0_27.md", "界限论_第七章_可读重写_v0_27.md"),
    ("界限论_第一章_可读重写_v0_21.md", "界限论_第一章_可读重写_v0_21.md"),
    ("界限论_第三章_可读重写_v1_5.md", "界限论_第三章_可读重写_v1_5.md"),
    ("界限论_第五章_可读重写_v0_14.md", "界限论_第五章_可读重写_v0_14.md"),
    ("界限论_第零章_可读重写_v0_35.md", "界限论_第零章_可读重写_v0_35.md"),
]
for dl, proj in files:
    dp = os.path.join(r"E:\download", dl)
    pp = os.path.join(r"E:\界限论", proj)
    ds = os.path.getsize(dp) if os.path.exists(dp) else None
    ps = os.path.getsize(pp) if os.path.exists(pp) else None
    if ds and ps:
        delta_d = ds - ps
        dll = open(dp,encoding="utf-8").readline().strip()[:80]
        pll = open(pp,encoding="utf-8").readline().strip()[:80]
        v = "→ 下载更新" if ds>ps else ("→ 项目更新" if ds<ps else "→ 相同大小")
        print(f"{dl[:25]:28s} [下载 {ds:>6}B] vs [项目 {ps:>6}B] {'+' if delta_d>0 else ''}{delta_d}B {v}")
        print(f"  DL title: {dll}")
        print(f"  PJ title: {pll}")
    elif ds:
        print(f"{dl[:30]:33s} only in download ({ds}B)")
    else:
        print(f"{dl[:30]:33s} only in project ({ps}B)")
