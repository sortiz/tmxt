"""Transform TMX in a tab-separated text file according to the code list
specified.

Usage:
  tmxt.py --codelist=<langcodes> [INPUT_FILE [OUTPUT_FILE]]

Options:
  --codelist=<langcodes>   Comma-separated list of langcodes (i.e. "en,es").
  
I/O Defaults:
  INPUT_FILE               Defaults to stdin.
  OUTPUT_FILE              Defaults to stdout.
"""

from docopt import docopt
import re
import sys
import xml.parsers.expat

def process_tmx(input, output, codelist):
    curlang  = ""
    curtuv   = []
    intuv    = False
    tu       = {}
    p1       = re.compile(r'\n')
    p2       = re.compile(r'  *')    
    fmt      = ("{}\t"*len(codelist)).strip()+"\n"

    def se(name, attrs):
        nonlocal intuv, curtuv, tu, curlang, codelist
        if intuv:
            curtuv.append("")
        elif name == "tu":
            tu = {i:'' for i in codelist}
        elif name == "tuv":
            if "xml:lang" in attrs:
                curlang = attrs["xml:lang"]
            elif "lang" in attrs:
                curlang = attrs["lang"]
        elif name == "seg":
            curtuv = []
            intuv = True
            
    def ee(name):
        nonlocal intuv, curtuv, p1, p2, tu, curlang, codelist, fmt, output
        if name == "tu":
            output.write(fmt.format(*[tu[lang] for lang in codelist]))

        elif name == "seg":
            intuv = False
            mystr = p2.sub(' ', p1.sub(' ', "".join(curtuv))).strip()
            tu[curlang] = mystr
            curlang = ""
    
    def cd(data):
        nonlocal intuv, curtuv
        if intuv:
            curtuv.append(data)

    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler  = se
    p.EndElementHandler    = ee
    p.CharacterDataHandler = cd
    p.ParseFile(input) 

if __name__ == '__main__':
    arguments = docopt(__doc__, version='tmxt 1.0')
    
    input = sys.stdin.buffer if not arguments["INPUT_FILE"] else open(arguments["INPUT_FILE"], "rb")
    output = sys.stdout if not arguments["OUTPUT_FILE"] else open(arguments["OUTPUT_FILE"], "w")    

    list = arguments["--codelist"].split(",")
    
    if len(list) > 1:
        process_tmx(input, output, list)
    
    input.close()
    output.close()
