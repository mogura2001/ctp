from pathlib import Path
OUT=Path(__file__).resolve().parent
target=OUT/'NativeU40.r2.cs'
assert not target.exists()
target.write_bytes((OUT/'NativeU40.cs').read_bytes())
print('Preserved actual r2 C# fixture; next run only new chain/loader subset')
