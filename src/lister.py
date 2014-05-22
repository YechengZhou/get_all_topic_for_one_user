# -*- coding: utf-8 -*-
"""
author: Yecheng Zhou
Date: 2014/5/21 Fuck, it is 520, but i'm facing to the a stupid thinkpad, WTF
Description:
This is a fucking fetcher to get the info we need.
"""

import urllib2
import sys
import difflib
from sgmllib import SGMLParser
from myStack import myStack
import urllib
import cookielib
from lxml import html as HTML


def current_frame(): # return the frame object for the caller'stack frame
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back


class group_url_lister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []
        self.in_div = False


    def start_div(self, attrs):
        for k, v in attrs:
            if k == 'class' and v == 'title':
                self.in_div = True

    def end_div(self):
        self.in_div = False

    def start_a(self, attrs):
        if self.in_div:
            href = [v for k, v in attrs if k == 'href']
            if href:
                self.urls.extend(href)
                self.in_div = False


class user_finder_discussion_page(object):
    def __init__(self, target_page):
        self.target_page = target_page
        handler_temp = urllib2.urlopen(self.target_page)
        self.content = handler_temp.read()
        handler_temp.close()

    def find(self, user_main_page_url=None, username=None):
        """
        def get_cur_func():
            try:
                raise Exception
            except:
                f = sys.exc_info()[2].tb_frame.f_back
            return (f.f_code.co_name, f.f_lineno)
        """
        assert user_main_page_url or username, "Please provide at least one para from user_main_page_url and username for %s" % "find"
        try:
            if self.content.find(user_main_page_url):
                return True, "url"
        except:
            print "find user_main_page_url failed in %s" % self.target_page

        try:
            if self.content.find(username):
                return True, "username"
        except:
            print "find username failed in %s" % self.target_page


class author_lister(SGMLParser):  # content of http://www.douban.com/group/douban911/discussion?start=50 should be feed

    def __init__(self, user_home_page_url):
        SGMLParser.reset(self)
        self.user_home_page_url = user_home_page_url
        self.author_topic_dic = {}
        self.in_tr = False
        self.in_topic_url_td = False
        self.in_nowrap_user_td = False
        self.in_user_a = False
        self.url_stack = myStack()  # default length is 50, which is the default number of topics in douban topic page
        self.user_url_stack = myStack()
        self.username_stack = myStack()

    def start_tr(self, attrs):
        for k, v in attrs:
            if k == 'class' and v == '':
                self.in_tr = True

    def end_tr(self):
        self.in_tr = False

    def start_td(self, attrs):
        if self.in_tr:
            type(attrs)
            if len(attrs) == 1:
                for k, v in attrs:
                    if k == "class" and v == "title":
                        self.in_topic_url_td = True
                    else:
                        if k == "nowrap" and v == "nowrap":
                            self.in_nowrap_user_td = True
            else:
                pass


    def end_td(self):
        self.in_topic_url_td = False
        self.in_nowrap_uer_td = False

    def start_a(self, attrs):
        if self.in_topic_url_td:  # means in below td block
            """
            <td class="title">
                    <a href="http://www.douban.com/group/topic/53090343/" title="【号外】那些明星大腕投资的网站，冠希那个太逗了" class="">【号外】那些明星大腕投资的网站，冠希那个太逗了</a>
                </td>
            """
            for k, v in attrs:
                if k == 'href':
                    self.url_stack.push(v[0] if isinstance(v,
                                                           list) else v) # push it in stack firstly, if can't find user later, pop it, may have performance issue, to be tested
        elif self.in_nowrap_user_td:
            """
            <td nowrap="nowrap"><a href="http://www.douban.com/group/people/86194017/" class="">南笙</a></td>
            """
            for k, v in attrs:
                if k == 'href':
                    self.user_url_stack.push(v[0] if isinstance(v, list) else v)
                    self.in_user_a = True


    def handle_data(self, data):
        if self.in_user_a:
            self.username_stack.push(data)



if __name__ == '__main__':
    al = author_lister('http://www.douban.com/group/people/60318558/')
    content = urllib2.urlopen('http://www.douban.com/group/douban911/discussion?start=50').read()
    al.feed(content)
    print al.username_stack