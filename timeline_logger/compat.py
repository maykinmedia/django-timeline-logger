import sys


# Safely importing the HTML parser utility, highly dependent on Python versions
if sys.version_info >= (3, 4):
    # From v3.4.0 in advance
    import html
else:
    # Python 2.x versions
    from HTMLParser import HTMLParser
    html = HTMLParser()
