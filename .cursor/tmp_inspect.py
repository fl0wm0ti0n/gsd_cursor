with open('g:/workdir/github/sonstiges/gsd_cursor/docs/engineering/state.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(1242, 1248):
    print(f"{i+1}: [{lines[i].rstrip(chr(10))}]")
