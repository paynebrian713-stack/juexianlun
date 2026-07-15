c8 = open(r"E:\界限论\界限论_附录W_v8_8.md", encoding="utf-8").read()
# find backtick block with 公理 Σ
import re
blocks = re.findall(r'```\n(.*?)```', c8, re.DOTALL)
for b in blocks:
    if '公理 Σ' in b:
        lines = b.splitlines()
        for i, line in enumerate(lines):
            print(f"L{i}: {repr(line)}")
