# Google_Books
This repository contains data harvested from Google's GRIN interface with Harvard's grin-to-s3 tools, plus additional scripts and data of our own.

all_books.tsv is the entire set of books retrieved via this call:


```
$ python grin.py --directory=Harvard --resource="_all_books?format=text&mode=all" > _all_books.tsv
```

