#!/usr/bin/python3
# This file is a part of qrot program.
#
# (c) volgk,        <dear.volgk@gmail.com>
# (c) chinarulezzz, <alexandr.savca89@gmail.com>
#
# See LICENSE file for copyright and license details.

import argparse
import sys
from   subprocess import Popen
import os.path

sys.path.append ("/usr/share/qrot")
import search

program =  'qrot'
version =  '0.2.1'
logo    = f'''
                              ZZZZZ$=..,$ZZZZ7:                             
                             7$ZZZZZ$I:,ZZZ7$ZZ                             
                            ,$ZZZZZZZZZ$:..:$ZZ7                            
                           I$ZZZZZZZZZZ$ZZZZZZZ7                            
                          +ZZZZZZZZZZZZZZZZZZZZZ..            ~$            
                          $ZZZZZZZZZZZZZZZZZZZZ$?.........:7$Z$$            
            ZZZZZZZ7?+~:,...........,,,,,,.......,~+I7ZZZZ$ZZZI:            
           ,ZZZZZZZZZZZZZZZZZZ$$$77777777$$$$ZZZZZZZZZ$7I==,                
             ~7ZZZZZZZZZZZZZZZZZ$$77I?+=~:,.........                        
                         ...:7ZZZ7... .....:+++=~~..                        
                         ....~.:~,I77..=$$+=Z,.,:...                        
                          ....~+=:...++...=+++=,...                         
                          ~Z$777$ZZZIZZ?$Z$$III7$I                          
                           ZZZZZZZZZ:??.ZZZZZZZ$Z                           
                            I=$Z?+$Z=..=$7=IZZZ+                            
                             Z$ZZZ7=:..,?7ZZZI?                             
                              $ZZZZI....$$ZZ$?                              
                               .Z$?~...,~+$ZI                               
                                I7ZZ$?+ZZZ=                                 
                                  ~ZZZZZ7:                                  
                                    ,$?                                     
                    qrot -- OSINT helper tool. v{version}                   
                (c) volgk,        <dear.volgk@gmail.com>                    
                (c) chinarulezzz, <alexandr.savca89@gmail.com>
'''

def createParser():
    parser = argparse.ArgumentParser(
                prog='qrot',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description=logo)

    optional = parser
    optional.add_argument ('-v', '--version', action='version', version=version)

    optional.add_argument ('--list', nargs='?', choices=['tags', 'engines'],
                          default='not specified',
                          help='see the list of engines or tags. \
                                The list is long so feel free to use less and/or grep. \
                                Default: print all.')

    optional.add_argument ('-b', '--browser', nargs='?', default='firefox',
                          help='select browser for search. Default=firefox.')

    optional.add_argument ('-p', '--profile', nargs='?', default='default',
                          help='select browser\'s profile. Default=default.')

    optional.add_argument ('-e', '--exclude', nargs='*', default='not specified',
                          help='exclude selected engine(s) or tag(s)')

    optional.add_argument ('-via', '--via',   nargs='*', default='not specified',
                          help='search via others search-engines.')

    required = parser.add_argument_group('required arguments')
    required.add_argument ('-q', '--query',   nargs='*', default='not specified',
                          required='--list' not in sys.argv,
                          help='keyword or \"keywords ...\"')

    required.add_argument ('-s', '--search',  nargs='*', default='not specified',
                          required='--list' not in sys.argv,
                          help='search engine(s) or tag(s)')
    return parser


if __name__ == '__main__':
    parser = createParser ()
    args = parser.parse_args ()


    if not args.list:
        search.print_engines()
        search.print_tags()
        sys.exit(1)

    elif args.list == "tags":
        search.print_tags()
        sys.exit(2)

    elif args.list == "engines":
        search.print_engines()
        sys.exit(3)


    if not args.browser:
        print ("""
ERROR:

    -b/--browser: need to set the browser for searching.

EXAMPLE:

    Search in firefox via default profile:
    -b firefox -p default
    Note: by default, qrot already opens firefox via default profile.

    Search in chromium via google-bot profile:
    -b chromium -p google-bot

    Search in firefox via TOR profile:
    -b firefox -p tor_profile
""", file=sys.stderr)
        sys.exit(4)


    if not args.query:
        print("""
ERROR:

    -q/--query: need to choose the keyword(s) for searching.

EXAMPLE:

    Search one keyword as query:
    -q Keyword2Search

    Search multiple keywords as one query:
    -q 'Multiple Keywords To Search'

    Search multiple queries:
    -q Keyword2Search -q 'Multiple Keywords To Search'
""")
        sys.exit (5)


    if not args.search:
        print ("Error:\t-s/--search: need to choose the search engine")
        print ("\t-h/--help: to list engines and/or tags")
        sys.exit(6)


    if not args.exclude:
        print ("Error:\t-e/--exclude: need to choose the search engine(s) or tag(s) \
                                \n\t\twhich will be excluded from searching.")
        print ("\t-h/--help: to list engines and/or tags") 
        sys.exit(7)

    search.open_browser (args.browser, args.profile, args.search, args.exclude, args.query, args.via)

# End of File
