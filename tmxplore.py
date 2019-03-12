"""Explore TMX files to get all different language codes.

Usage:
  tmxplore.py [options] [INPUT_FILE]

Options:
  --no_tus=<n>  Explore the first n translation units at much [default: 10].
  --all         Explore all the file.
  
I/O Defaults:
  INPUT_FILE        Defaults to stdin.
"""

from docopt import docopt
import xml.parsers.expat
import sys

def print_result(langlist):
    print(" ".join(langlist))
    sys.exit(0)

def explore(fd, ntus=10):
    langset  = set()
    langlist = []
    ntu = 0
    
    def se(name, attrs):
        nonlocal ntu
        if name == "tuv":
            if "xml:lang" in attrs:
                if attrs["xml:lang"] not in langset:
                    langlist.append(attrs["xml:lang"])
                    langset.add(attrs["xml:lang"])
            elif "lang" in attrs:
                if attrs["lang"] not in langset:
                    langlist.append(attrs["lang"])
                    langset.add(attrs["lang"])
        elif name == "tu":
            ntu += 1
            if ntu >= ntus + 1:
                print_result(langlist)
    
    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = se
    p.ParseFile(fd)

    print_result(langlist)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='tmxplore 1.0')

    fd = sys.stdin.buffer if not arguments["INPUT_FILE"] else open(arguments["INPUT_FILE"], "rb")
    if arguments["--all"]:
        explore(fd, sys.maxsize)
    else:
        explore(fd, int(arguments["--no_tus"]))        

    fd.close()
    