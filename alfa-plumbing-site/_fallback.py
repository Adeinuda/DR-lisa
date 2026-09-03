import pathlib, ast

# ---------------- 1. one default artifact again: one-page.html, self-contained -------------
b = pathlib.Path('/home/user/DR-lisa/alfa-plumbing-site/build.py')
t = b.read_text(encoding='utf-8')
old = """    rc = one_page.main()                  # one-page.html: nothing outside the file
    rc |= one_page.main(assets=True)      # one-page.assets.html: for renderers that block data: URIs
    if rc:
        raise SystemExit(rc)"""
new = """    rc = one_page.main()                  # one-page.html: nothing outside the file
    if rc:
        raise SystemExit(rc)
    # the sibling variant is opt-in tooling, not a second deliverable:
    #   python3 one_page.py --assets"""
assert old in t, "collate"
t = t.replace(old, new, 1)
b.write_text(t, encoding='utf-8')
ast.parse(t)

# ---------------- 2. every frame gets a fallback that can only help ----------------------
p = pathlib.Path('/home/user/DR-lisa/alfa-plumbing-site/one_page.py')
o = p.read_text(encoding='utf-8')

old_swap = """    if embed:
        text = re.sub(r"<img\\b[^>]*>", swap, text)"""
new_swap = """    if embed:
        text = re.sub(r"<img\\b[^>]*>", swap, text)
        # if the host renders this file in a context that refuses data: URLs, the same bytes are
        # sitting in assets/img/ beside it, so ask for those instead of leaving a blank frame
        text = re.sub(r'<img src="(data:image/jpeg;base64,[^"]+)"( alt="[^"]*")',
                      _fallback, text)"""
assert old_swap in o, "swap hook"
o = o.replace(old_swap, new_swap, 1)

helper = '''def _fallback(m):
    uri, alt = m.group(1), m.group(2)
    name = "assets/img/%s.jpg" % _ALT_TO_FILE.get(alt.strip('alt="').strip('"'), "")
    if not name.startswith("assets/img/%") :
        pass
    return '<img src="%s"%s onerror="this.onerror=null;this.src=&quot;%s&quot;"' % (
        uri, alt, _file_for(uri))


def _file_for(uri):
    """The source path a frame fell back from, looked up through the payload cache."""
    for rel, cached in _URI_CACHE.items():
        if cached == uri:
            return rel
    return "assets/img/water-heaters.jpg"


_ALT_TO_FILE = {}

'''
o = o.replace("def inline_assets(text, embed=True):", helper + "def inline_assets(text, embed=True):", 1)
p.write_text(o, encoding='utf-8')
ast.parse(o)
print("wired")
