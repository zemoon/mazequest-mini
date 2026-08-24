#!/usr/bin/env python3
import pathlib

here = pathlib.Path('/tmp/mazequest_app')
b64 = (here / 'bertie.b64').read_text().strip()
data_uri = 'data:image/png;base64,' + b64

parts = [(here / f).read_text() for f in
         ('part1_style.html', 'part2_markup.html', 'part3_script.html')]
body = "\n".join(parts).replace('__BERTIE__', data_uri)

# 1) Artifact build: no doctype/html/head/body — the tool wraps it.
(here / 'mazequest-mini.html').write_text(body)

# 2) Standalone build: a complete document for opening off disk.
standalone = (
    '<!doctype html>\n<html lang="en">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    + body.split('</style>', 1)[0] + '</style>\n</head>\n<body>\n'
    + body.split('</style>', 1)[1] + '\n</body>\n</html>\n'
)
(here / 'MazeQuest-Mini.html').write_text(standalone)

for f in ('mazequest-mini.html', 'MazeQuest-Mini.html'):
    p = here / f
    print(f'{f}: {p.stat().st_size/1024:.0f} KB')
