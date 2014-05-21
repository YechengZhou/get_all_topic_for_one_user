"""
author: Yecheng Zhou
Date: 2014/5/21 Fuck, it is 520, but i'm facing to the a stupid thinkpad, WTF
Description:
This is a fucking fetcher to get the info we need.
"""

import urllib2
import difflib
from sgmllib import SGMLParser
import urllib
import cookielib
from lxml import html as HTML

class group_url_lister(SGMLParser):

    def reset(self):
        SGMLParser.reset(self)
        self.urls = []
        self.in_div = False


    def start_div(self, attrs):
        for k,v in attrs:
            if k== 'class' and v == 'title':
                print k,v
                self.in_div = True

    def end_div(self):
        self.in_div = False

    def start_a(self, attrs):
        if self.in_div:
            href = [v for k, v in attrs if k == 'href']
            if href:
                self.urls.extend(href)
                self.in_div = False