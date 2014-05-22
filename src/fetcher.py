# -*- coding: utf-8 -*-
"""
author: Yecheng Zhou
Date: 2014/5/20 Fuck, it is 520, but i'm facing to the a stupid thinkpad, WTF
Description:
This is a fucking fetcher to get the info we need.
"""
import urllib2
import difflib
from lister import group_url_lister , author_lister
from sgmllib import SGMLParser
import urllib
import cookielib
from lxml import html as HTML


class Fetcher(object): # is quite easy, we don't even need to login to get topic page info
    def __init__(self, user_id  = '34852019', group_name = "all"): # default get all , user_id default is mine
        self.user_id = user_id  # this is the wanted people
        self.group_name = group_name

    def fetch(self, url = "http://www.douban.com/group/topic/"):
        print 'fetch url: ', url
        req = urllib2.Request(url)
        url_handler = urllib2.urlopen(req)
        content = url_handler.read()
        url_handler.close()
        return content

    def get_user_group(self): # get which group the user join
        user_group_homepage_url = "http://www.douban.com/group/people/" + str(self.user_id) + "/joins"
        content = self.fetch(url = user_group_homepage_url)
        parser = group_url_lister()
        parser.feed(content)
        parser.close()
        return parser.urls

if __name__ == "__main__":
    fe = Fetcher()
    urls = fe.get_user_group()
    content = fe.fetch(urls[0])
    #al = author_lister(urls)
    #print
    for i in urls: print i
