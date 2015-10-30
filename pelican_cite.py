# -*- coding: utf-8 -*-
"""
pelican-cite
==============

A Pelican plugin that provices a BibTeX-style reference system within
pelican sites. 

Based on teh Pelican BibTeX plugin written by Vlad Niculae <vlad@vene.ro>
"""

import logging
import re
import sys

try:
    from pybtex.database.input.bibtex import Parser
    from pybtex.database.output.bibtex import Writer
    from pybtex.database import BibliographyData, PybtexError
    from pybtex.backends import html
    from pybtex.style.formatting.unsrt import Style as UnsrtStyle
    from pybtex.plugin import find_plugin
    pyb_imported = True
except ImportError:
    pyb_imported = False

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator
from .author_year import LabelStyle

if sys.version_info[0] < 3:
    reload(sys)  
    sys.setdefaultencoding('utf8')

__version__ = '0.2.0'

JUMP_BACK = '<a class="cite-backref" href="#ref-{0}-{1}" title="Jump back to reference {1}">{2}</a>'
CITE_RE = re.compile("\[&#64;(&#64;)?\s*(\w.*?)\s*\]")

class Style(UnsrtStyle):
    name = 'inline'
    default_sorting_style = 'author_year_title'
    default_label_style = 'author_year'
    
    def __init__(self, label_style=None, name_style=None, sorting_style=None, abbreviate_names=False, **kwargs):
        self.name_style = find_plugin('pybtex.style.names', name_style or self.default_name_style)()
        self.label_style = LabelStyle()
        self.sorting_style = find_plugin('pybtex.style.sorting', sorting_style or self.default_sorting_style)()
        self.format_name = self.name_style.format
        self.format_labels = self.label_style.format_labels
        self.sort = self.sorting_style.sort
        self.abbreviate_names = abbreviate_names


logger = logging.getLogger(__name__)
global_bib = None
if pyb_imported:
    style = Style()
    backend = html.Backend()
else:
    style = None
    backend = None

def get_bib_file(article):
    """
    If a bibliography file is specified for this article/page, parse
    it and return the parsed object.
    """
    if 'publications_src' in article.metadata:
        refs_file = article.metadata['publications_src']
        try:
            local_bib = Parser().parse_file(refs_file)
            return local_bib
        except PybtexError as e:
            logger.warn('`pelican_bibtex` failed to parse file %s: %s' % (
                refs_file,
                str(e)))
            return global_bib
    else:
        return global_bib


def process_content(article):
    """
    Substitute the citations and add a bibliography for an article or
    page, using the local bib file if specified or the global one otherwise.
    """
    data = get_bib_file(article)
    if not data:
        return
    content = article._content
    content = content.replace("@","&#64;")

    # Scan post to figure out what citations are needed
    cite_count = {}
    replace_count = {}
    for citation in CITE_RE.findall(content):
        if citation[1] not in cite_count:
            cite_count[citation[1]] = 1
            replace_count[citation[1]] = 1
        else:
            cite_count[citation[1]] += 1

    # Get formatted entries for the appropriate bibliographic entries
    cited = []
    for key in data.entries.keys():
        if key in cite_count: cited.append(data.entries[key])
    if len(cited) == 0: return
    formatted_entries = style.format_entries(cited)

    # Get the data for the required citations and append to content
    labels = {}
    content += '<hr>\n<h2>Bibliography</h2>\n'
    for formatted_entry in formatted_entries:
        key = formatted_entry.key
        ref_id = key.replace(' ','')
        label = ("<a href='#" + ref_id + "' id='ref-" + ref_id + "-{0}'>"
                + formatted_entry.label + "</a>")
        t = formatted_entry.text.render(backend)
        t = t.replace('\\{', '&#123;')
        t = t.replace('\\}', '&#125;')
        t = t.replace('{', '')
        t = t.replace('}', '')
        text = ("<p id='" + ref_id + "'>" + t)
        for i in range(cite_count[key]):
            if i == 0:
                text += ' ' + JUMP_BACK.format(ref_id,1,'↩')
                if cite_count[key] > 1:
                    text += JUMP_BACK.format(ref_id,1,' <sup>1</sup> ')
            else:
                text += JUMP_BACK.format(ref_id,i+1,'<sup>'+str(i+1)+'</sup> ')
        text += '</p>'
        content += text + '\n'
        labels[key] = label

    # Replace citations in article/page
    cite_count = {}
    def replace_cites(match):
        label = match.group(2)
        if label in labels:
            if label not in cite_count:
                cite_count[label] = 1
                replace_count[label] = 1
            else:
                cite_count[label] += 1
            lab = labels[label].format(cite_count[label])
            if '&#64;&#64;' in match.group():
                return lab
            else:
                m = re.search(">\s*\(\s*(.*?),\s*(.*?)\s*\)\s*<",lab)
                lab = lab[0:m.start()] + '>' + m.group(1) + ' (' + m.group(2) + ')<' + lab[m.end():]
                return lab
        else:
            logger.warn('No BibTeX entry found for key "{}"'.format(label))
            return match.group(0)
    
    content = CITE_RE.sub(replace_cites,content)
    article._content = content
    

def add_citations(generators):
    global global_bib
    if not pyb_imported:
        logger.warn('`pelican-cite` failed to load dependency `pybtex`')
        return

    if 'PUBLICATIONS_SRC' in generators[0].settings:
        refs_file = generators[0].settings['PUBLICATIONS_SRC']
        try:
            global_bib = Parser().parse_file(refs_file)
        except PybtexError as e:
            logger.warn('`pelican_bibtex` failed to parse file %s: %s' % (
                refs_file,
                str(e)))

    # Process the articles and pages
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                process_content(article)
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                process_content(page)


def register():
    signals.all_generators_finalized.connect(add_citations)
