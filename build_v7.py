"""Generate a bounded-search V7 experiment from the verified V3 main.py.
Run on branch v7-search-candidate, then commit main.py for local Docker grading.
"""
import ast,base64,lzma
from pathlib import Path

src=Path("main.py").read_text()
calls=[n for n in ast.walk(ast.parse(src)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="b85decode"]
assert len(calls)==1,"Expected one compressed payload"
raw=ast.literal_eval(calls[0].args[0])
source=lzma.decompress(base64.b85decode(raw)).decode()
changes={"limit=22000":"limit=15000","if q>=7:return a":"if q>=5:return a","ply<12:d+=1":"ply<7:d+=1","if ply>=45:":"if ply>=40:"}
for old,new in changes.items():
    assert source.count(old)==1,("Unexpected V3 source",old)
    source=source.replace(old,new)
compile(source,"engine_src.py","exec")
compressed=base64.b85encode(lzma.compress(source.encode(),preset=9)).decode()
packed="import lzma,base64\nexec(lzma.decompress(base64.b85decode("+repr(compressed)+")))\n"
assert len(packed.encode())<=4096,"Engine exceeds 4KB"
Path("main.py").write_text(packed)
Path("engine_src.py").write_text(source)
print("V7 candidate built:",len(packed.encode()),"bytes. Grading is still required.")
