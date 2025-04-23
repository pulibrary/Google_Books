# Designing a Pipeline for Copying Books from GRIN

# General Considerations

## Scale

GRIN says PUL has 277,970 books Google Books. Harvard says the default
conversion rate (how many books GRIN can process into downloadable
tarballs) is about 5,000 per day. Assuming we can download tarballs as
fast as GRIN can put them up, that means a minimum of 56 days to process
everything.

The size of the <sub>converted</sub> pool at Google Books is also 5,000:
once the pool size reaches 5000, older packages are replaced with new
ones in the pool.

# Harvard's Pipeline

Harvard implements a pipeline in a script called `liberate.py`.

It assumes you have already:

- Downloaded a list of GB barcodes (using instadin's `grin.py` script)
  (<sub>allfiles</sub>.tsv)
- Downloaded the latest MARCXML dump from Stanford's POD aggregator
  (latest was princeton-2023-02-10-full-marcxml.xml)
- Used process<sub>podxml</sub>.py to match all the Google barcodes
  against POD records and augment them (records in
  grin<sub>processed</sub>/pod<sub>xml</sub>)

`Liberate.py` does much more than we want to do at the moment:

> Processing does a few things:
>
> 1.  Decrypt and unpack each \`.tar.gz.gpg\` archive
> 2.  Extract and upload \`LIBRARY<sub>BARCODE</sub>.xml\` (as
>     \`BARCODE.xml\`)
> 3.  Compile the page-by-page text OCR files into one .txt file,
>     \`BARCODE.txt\` and as a tarball of each page as a single file,
>     \`BARCODE.txt.tar.gz\`. Both of these are uploaded to s3.
> 4.  If POD XML file(s) exists within \`–output<sub>dir</sub>\`'s
>     \`pod<sub>xml</sub>\` subdirectory, upload any matching files as
>     \`BARCODE.pod.xml\`.
> 5.  If a MODS XML file can be found in Harvards Library Cloud, upload
>     that.
> 6.  As data is collected and put into S3, a \`.retrieval\` sister file
>     containing a timestamp is uploaded.

# Another Approach

Rather than have a single, long-running process to do all the work, a
more asynchronous approach would almost certainly be superior. One
process manages the <sub>allbooks</sub> list: what books have been
copied over to our bucket, what books should be queued up next, based on
the state of the <sub>converted</sub> pool.

Another process monitors the queue of books to be processed

## Tell Google to make a barcode ready for download

Use Harvard's grin.py script to do this:

``` bash
$ python grin.py --directory=PRNC --method=POST --resource="_process?barcodes=123&barcodes=456&barcodes=789"
```
