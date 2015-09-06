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

Template Example
================

You probably want to define a 'publications.html' direct template.  Don't forget
to add it to the `DIRECT\_TEMPLATES` configuration key.  Note that we are escaping
the BibTeX string twice in order to properly display it.  This can be achieved
using `forceescape`.

```python
{% extends "base.html" %}
{% block title %}Publications{% endblock %}
{% block content %}

<script type="text/javascript">
    function disp(s) {
        var win;
        var doc;
        win = window.open("", "WINDOWID");
        doc = win.document;
        doc.open("text/plain");
        doc.write("<pre>" + s + "</pre>");
        doc.close();
    }
</script>
<section id="content" class="body">
    <h1 class="entry-title">Publications</h1>
    <ul>
    {% for key, year, text, bibtex, pdf, slides, poster in publications %}
    <li id="{{ key }}">{{ text }}
    [&nbsp;<a href="javascript:disp('{{ bibtex|replace('\n', '\\n')|escape|forceescape }}');">Bibtex</a>&nbsp;]
    {% for label, target in [('PDF', pdf), ('Slides', slides), ('Poster', poster)] %}
    {{ "[&nbsp;<a href=\"%s\">%s</a>&nbsp;]" % (target, label) if target }}
    {% endfor %}
    </li>
    {% endfor %}
    </ul>
</section>
{% endblock %}
```

Attribution
===========
`pelican-cite` is based on the
[pelican-bibtex](https://github.com/vene/pelican-bibtex) plugin written by
[Vlad Niculae](https://github.com/vene).
