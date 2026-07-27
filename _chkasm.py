with open('E:/界限论/assemble_full.py', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(1622, 1756):
    print(f'{i+1}: {lines[i].rstrip()[:160]}')
