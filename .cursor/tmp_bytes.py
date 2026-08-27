path = 'g:/workdir/github/sonstiges/gsd_cursor/docs/engineering/state.md'
with open(path, 'rb') as f:
    data = f.read()
needle = b'ext_scheduled_phase=/execute (role=dev per US-0069'
idx = data.find(needle)
print("FOUND at:", idx)
if idx >= 0:
    chunk = data[idx:idx+400]
    print("BYTES:", chunk)
