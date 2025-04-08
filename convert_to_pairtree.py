from pathlib import Path
from shutil import copyfile

# quick implementation of PairTree

dirtyChars = (0x22, 0x2a, 0x2b, 0x2c ,0x3c ,0x3d, 0x3e, 0x3f ,0x5c, 0x5e, 0x7c)
cleanChars = [i for i in range(0x21, 0x7e) if i not in dirtyChars]

trantab = str.maketrans("/:.", "=+,")

def cleanChar(char):
    if ord(char) in cleanChars:
        return char
    else:
        return "^{0:x}".format(ord(char))

def id2ppath(id:str) -> Path:
    cleaned:str = "".join([cleanChar(i) for i in id]).translate(trantab)
    return Path(*[cleaned[i:i+2] for i in range(0, len(cleaned), 2)])

src_path = Path("/Users/wulfmanc/gh/pulibrary/Google_Books/grin_processed/pod_xml")
ptree_top = Path("/tmp/ptree")

def copy_to_tree(src_path:Path, ptree_top:Path) -> None:
    for f in src_path.rglob("*.xml"):
        destination:Path = ptree_top / id2ppath(f.stem)
        destination.mkdir(parents=True, exist_ok=True)
        copyfile(f, destination / f.name)
