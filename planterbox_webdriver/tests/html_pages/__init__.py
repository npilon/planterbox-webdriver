import os.path

PAGES = {}
for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith('.html'):
        name = filename.split('.html')[0]
        PAGES[name] = 'file://%s' % os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            filename,
        )
