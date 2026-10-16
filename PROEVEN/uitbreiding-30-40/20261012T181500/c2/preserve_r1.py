from pathlib import Path
OUT=Path(__file__).resolve().parent
target=OUT/'NativeU40.r1.cs'
assert not target.exists()
target.write_bytes((OUT/'NativeU40.cs').read_bytes())
print('Preserved actual r1 fixture C# source before new loader/chain assertions')
