from pathlib import Path
from lxml import etree
import argparse
from lxml import etree
from pathlib import Path

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


def split_large_xml(input_file, output_top_dir):
    """
    Splits a large XML file containing <marc:record> elements inside a 
    <marc:collection> root element in the namespace 
    'http://www.loc.gov/MARC21/slim' into separate smaller XML files.
    
    - Names each file based on the value of <controlfield tag="001">.
    - Creates an output directory named after the input filename.


    :param input_file: Path to the large XML file.
    :param output_top_dir: Directory where individual record files will be stored.
    """
    ns = {'marc': 'http://www.loc.gov/MARC21/slim'}  # Define namespace
    input_path = Path(input_file)
    top_dir = Path(output_top_dir)
    
    top_dir.mkdir(parents=True, exist_ok=True)

    # Parse the file and find records inside /marc:collection/marc:record
    # context = etree.iterparse(input_file, events=('end',), tag=f'{{{ns["marc"]}}}record')
    context = etree.iterparse(input_file, tag=f'{{{ns["marc"]}}}record')
    
    for event, elem in context:
        # Find the controlfield with tag="001"
        controlfield = elem.find(f'{{{ns["marc"]}}}controlfield[@tag="001"]', namespaces=ns)
        if controlfield is not None and controlfield.text:
            record_id = controlfield.text.strip()
        else:
            record_id = f"unknown_{hash(elem)}"  # Fallback if no ID found

        output_dir = top_dir / id2ppath(record_id)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{record_id}.xml"

        # Write record to file with XML declaration
        record_tree = etree.ElementTree(elem)
        with open(output_file, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            record_tree.write(f, encoding="UTF-8", xml_declaration=False)

        # Clear element from memory
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

# Example usage:
# split_large_xml("princeton-2023-02-12-delta-marcxml.xml")


def main():
    pod_dir = Path("/Users/wulfmanc/gh/pulibrary/Google_Books/pod")
    test_file = pod_dir / Path('princeton-2023-02-12-delta-marcxml.xml')

    # collection = etree.parse(test_file)

    split_large_xml(test_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a large MARCXML file into individual records.")
    parser.add_argument("input_file", help="Path to the input MARCXML file")
    parser.add_argument("output_dir", help="Path to the output directory")

    args = parser.parse_args()
    split_large_xml(args.input_file, args.output_dir)
