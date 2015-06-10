#!/usr/bin/env python3

from collections import defaultdict, OrderedDict
import glob

import lib
import pywikibot

COMPOSER = OrderedDict([
    ('phplint', 'jakub-onderka/php-parallel-lint'),
    ('MW-CS', 'mediawiki/mediawiki-codesniffer'),
])
NPM = OrderedDict([
    ('banana', 'grunt-banana-checker'),
    ('csslint', 'grunt-contrib-csslint'),
    ('jshint', 'grunt-contrib-jshint'),
    ('jsonlint', 'grunt-jsonlint'),
    ('jscs', 'grunt-jscs'),
])

if lib.EXTENSIONS_DIR.startswith('/data/project/ci'):
    lib.update_submodules_and_stuff(lib.EXTENSIONS_DIR)

class Reader:
    def __init__(self):
        self.data = defaultdict(dict)

    def read_composer(self, repo_name, path):
        info = lib.json_load(path)
        if 'require-dev' in info:
            for job in COMPOSER.values():
                version = info['require-dev'].get(job)
                if version:
                    self.data[repo_name][job] = version

    def read_npm(self, repo_name, path):
        info = lib.json_load(path)
        if 'devDependencies' in info:
            for job in NPM.values():
                version = info['devDependencies'].get(job)
                if version:
                    self.data[repo_name][job] = version

reader = Reader()
composers = glob.glob(lib.EXTENSIONS_DIR + '/*/composer.json')
for composer in composers:
    ext_name = composer.split('/')[-2]
    reader.read_composer(ext_name, composer)

packages = glob.glob(lib.EXTENSIONS_DIR + '/*/package.json')
for package in packages:
    ext_name = package.split('/')[-2]
    reader.read_npm(ext_name, package)

data = reader.data
# print(data)

header = """
{|class="wikitable"
! Extension
"""
for abbr in list(COMPOSER) + list(NPM):
    header += '! %s\n' % abbr
text = header
for ext_name in sorted(list(data)):
    info = data[ext_name]
    text += '|-\n|%s\n' % ext_name
    for job in COMPOSER.values():
        if job in info:
            add = info[job]
            if add == lib.get_packagist_version(job):
                add += '&#x2713;'
        else:
            add = 'n/a'
        text += '|%s\n' % add
    for job in NPM.values():
        if job in info:
            add = info[job]
            if add == lib.get_npm_version(job):
                add += '&#x2713;'
        else:
            add = 'n/a'
        text += '|%s\n' % add
text += '|}'

#print(text)
site = pywikibot.Site('mediawiki', 'mediawiki')
page = pywikibot.Page(site, 'User:Legoktm/ci')
pywikibot.showDiff(page.text, text)
#page.put(text, 'Updating table')
