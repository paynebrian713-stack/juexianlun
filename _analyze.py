"""Inspect raw original SVG for format patterns."""
import re

svg = open('E:/界限论/docs/reality-map.svg', encoding='utf-8').read()

print("=== opacity patterns ===")
for i, line in enumerate(svg.splitlines()):
    if 'pacity' in line.lower():
        print(f'  L{i+1}: {line[:150]}')

print("\n=== font-size ===")
for i, line in enumerate(svg.splitlines()):
    if 'font-size' in line.lower():
        print(f'  L{i+1}: {line[:150]}')
