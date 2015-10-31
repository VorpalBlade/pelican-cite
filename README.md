pelican-cite
==============

Allows the use of BibTeX citations within a Pelican site. 

Requirements
============

`pelican-cite` requires `pybtex`.

```bash
pip install pybtex
```

How to Use
==========

This plugin reads a user-specified BibTeX file and generates bibliographic
information within your articles and pages.

Configuration is simply:

```python
PUBLICATIONS_SRC = 'content/pubs.bib'
```

If the file is present and readable, then content will be scanned for references
to citation keys. These take the format `[@Bai2011]` or `[@@Bai2011]`. These
will be replaced by incline citations which provide links to the full
bibliographic information at the end of the article. The former reference would
be replaced by a citation of the form "Bai & Stone (2011)", while the latter
would be replaced by "(Bai & Stone, 2011)". 

If a citation key is used which does not exist within the BibTeX file then
a warning will be displayed.

The BibTeX file may, optionally, be provided or overridden on a per-article
basis by supplying the meta-data `publications_src`.

Attribution
===========
`pelican-cite` is based on the
[pelican-bibtex](https://github.com/vene/pelican-bibtex) plugin written by
[Vlad Niculae](https://github.com/vene).
