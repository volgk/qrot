# This file is a part of qrot program.
#
# (c) volgk,        <dear.volgk@gmail.com>
# (c) chinarulezzz, <alexandr.savca89@gmail.com>
#
# See LICENSE file for copyright and license details.

import json
import sys
from   subprocess import Popen

with open ('engines.json') as f:
    engines = json.load(f)


def search_engines(search, exception):

	search_available = []

	for engine in engines:
		for target in search:
			if target == engine:
				search_available.append(engine)
			elif target in engines[engine]['tags']:
				search_available.append(engine)

	for engine in search_available:
		for except_target in exception:
			if engine == except_target:
				search_available.remove(engine)
			elif except_target in engines[engine]['tags']:
				search_available.remove(engine)

	return search_available


def print_engines():

    print ("ENGINES")
    print ("=======\n")
    for engine in sorted(engines):
        print(engine)


def print_tags():

    print ("TAGS            NR OF ENGINES")
    print ("=============================\n")

    tags = []

    for engine in sorted(engines):
        for tag in engines[engine]['tags']:
            tags.append(tag)

    for tag in sorted(list(set(tags))):
        print('{:<18} {:>5g}'.format(tag, tags.count(tag)))


def open_browser(browser, profile, search, exception, queries, via):

	urls = []

	for engine in search_engines(search, exception):
		for query in queries:
			urls.append(engines[engine]['url'].format(query))
			for via_engine in search_engines(via, exception):
				if '@web-search-engine' in engines[via_engine]['tags']:
					urls.append(engines[via_engine]['url'].format(f"site:{engine} {query}"))
				else:
					urls.append(engines[via_engine]['url'].format(query))

	for url in urls:
		Popen([browser, '-P', profile, '--new-tab', url])

# End of File
