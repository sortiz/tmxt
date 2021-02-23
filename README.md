# tmxt

This tool consists on two scripts:
* `tmxplore.py`, a script to determine the language codes available inside a particular TMX file by looking to an excerpt or even the whole file.
* `tmxt.py`, to effectively transform a TMX to a tab-separated text file using the language code list provided in the command. TU propierties can also be printed if requested.

# Requirements

Requires python3 and the libraries included in requirements.txt

## Examples of usage

### `tmxplore.py`

```bash
$ python3 tmxplore.py file.tmx
en es
```

or

```bash
$ cat file.tmx | python3 tmxplore.py
en es
```

### `tmxt.py` 

```bash
$ python3 tmxt.py --codelist en,fr tm.fr-en.tmx en-fr.txt
```

Other

```bash
$ zcat largefile.tmx.gz | python3 tmxt.py --codelist en,es |gzip > bitext.en-es.gz
```

Printing TU propierties
```bash
$ python3 tmxt.py --codelist en,fr,prop1,prop2 tm.fr-en.tmx en-fr.txt
```

