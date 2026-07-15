lines=open(r'E:\界限论\assemble_full.py',encoding='utf-8').readlines()
for i in range(848,892):
    if i<len(lines):
        print(f'{i+1}: {lines[i].rstrip()[:200]}')
