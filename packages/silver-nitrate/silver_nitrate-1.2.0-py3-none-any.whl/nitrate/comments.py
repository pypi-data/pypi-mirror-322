"""
Code for dealing with Flickr comments.

In particular, it has some code shared across our
"""

import re
import typing
from xml.etree import ElementTree as ET

import httpx

from .xml import find_required_elem


def fix_wikipedia_links(comment_text: str) -> str:
    """
    Fix Wikipedia links in Flickr comments.

    Flickr's comment parser will try to auto-detect links, and it assumes
    punctuation isn't part of links, but this breaks links to some
    Wikipedia pages, for example:

        https://en.wikipedia.org/wiki/William_Barnes_Jr.

    It will omit the final period from the link, which means it goes to
    the wrong page.

    This function will fix the Wikipedia links auto-detected by Flickr.
    It moves any trailing punctuation that's part of the link inside
    the <a>.  We aren't changing the text of the comment, just the
    auto-detected HTML markup.

    See https://github.com/Flickr-Foundation/commons.flickr.org/issues/297
    """
    for m in re.finditer(
        r'<a href="https://en\.wikipedia\.org/wiki/(?P<slug1>[A-Za-z_]+)"'
        r' rel="noreferrer nofollow">'
        r"en\.wikipedia\.org/wiki/(?P<slug2>[A-Za-z_]+)"
        r"</a>"
        # The suffix can be:
        #
        #   - a full stop, which stands alone
        #   - some text in parentheses, which is a disambiguation string.
        #     This must be some non-empty text in parens.
        #
        r"(?P<suffix>\.|\([^\)]+\))",
        comment_text,
    ):
        print(m)
        # This is a defensive measure, because it was easier than
        # getting lookback groups working in the regex.
        if m.group("slug1") != m.group("slug2"):  # pragma: no cover
            continue

        orig_title = m.group("slug1")

        # If there's a Wikipedia page with this exact title, then the
        # link works and we can leave it as-is.
        if _get_wikipedia_page(orig_title) == "found":
            continue

        # Otherwise, check to see if there's a page with the suffix
        # added -- and if there does, use that as the new link.
        alt_title = orig_title + m.group("suffix")

        print(orig_title)
        print(alt_title)

        if _get_wikipedia_page(alt_title) == "found":
            comment_text = comment_text.replace(
                m.group(0),
                (
                    f'<a href="https://en.wikipedia.org/wiki/{alt_title}" '
                    'rel="noreferrer nofollow">'
                    f"en.wikipedia.org/wiki/{alt_title}</a>"
                ),
            )

    return comment_text


WikipediaPageStatus = typing.Literal["found", "redirected", "not_found"]


def _get_wikipedia_page(title: str) -> WikipediaPageStatus:
    """
    Look up a page on Wikipedia and see whether it:

    1.  Exists, with the given title
    2.  Exists, but the title is normalized/redirected
    3.  Isn't found

    """
    resp = httpx.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvprop": "timestamp",
            "format": "xml",
        },
    )
    resp.raise_for_status()

    # Note: the ElementTree API is not hardened against untrusted XML,
    # but we trust the Wikipedia API enough to try this.
    xml = ET.fromstring(resp.text)

    # The API response will contain a single ``page`` element,
    # like so:
    #
    #    <?xml version="1.0"?>
    #    <api batchcomplete="">
    #      <query>
    #        <normalized>
    #          <n from="William_Barnes_Jr" to="William Barnes Jr"/>
    #        </normalized>
    #        <pages>
    #          <page _idx="-1" ns="0" title="William Barnes Jr" missing=""/>
    #        </pages>
    #      </query>
    #    </api>

    # If the <page> element has the ``missing`` attribute, then there's
    # no such page.
    page = find_required_elem(xml, path=".//page")

    if "missing" in page.attrib:
        return "not_found"

    # If the <page> element has the exact same title as the thing we
    # searched for, then it exists.
    #
    # (Note: Wikipedia replaces spaces with underscores in URLs, which
    # we undo to compare titles.)
    if page.attrib["title"] == title.replace("_", " "):
        return "found"

    # If we found a <page> element but it doesn't have the expected title,
    # we may have been redirected.
    if xml.find(".//normalized") is not None:
        return "redirected"

    # This should never happen in practice so we can't test it, but we
    # include it for the sake of easy debugging if it does.
    else:  # pragma: no cover
        raise RuntimeError(
            f"Unable to parse Wikipedia API response for {title!r}: {resp.text}"
        )
