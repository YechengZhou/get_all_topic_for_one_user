# -*- coding: utf-8 -*-
"""
author: Yecheng Zhou
Date: 2014/5/21 Fuck, it is 520, but i'm facing to the a stupid thinkpad, WTF
Description:
This is a fucking fetcher to get the info we need.
"""

import urllib2
from sgmllib import SGMLParser
from myStack import myStack



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


class discussion_page_user_finder(object):
    def __init__(self, target_page, internet_or_file):
        self.target_page = target_page
        # true means read from internet, false means read from local file
        if internet_or_file:
            handler_temp = urllib2.urlopen(self.target_page)
            self.content = handler_temp.read()
        else:
            handler_temp = open(self.target_page, 'r')
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
            print user_main_page_url, self.target_page
            loc_index = self.content.find(user_main_page_url)
            if loc_index != -1:
                return True, "url", loc_index
        except:
            print "find user_main_page_url failed in %s" % self.target_page

        try:
            print username, self.target_page
            loc_index = self.content.find(username)
            if loc_index != -1:
                return True, "username", loc_index
        except:
            print "find username failed in %s" % self.target_page


class author_lister(SGMLParser):  # content of http://www.douban.com/group/douban911/discussion?start=50 should be feed
    """
    list all authors in this page, restore in list
    """

    def __init__(self):
        SGMLParser.reset(self)
        self.author_name_list = myStack(25)
        self.author_link_list = myStack(25)
        self.in_right_td = False
        self.in_user_a = False

    def start_td(self, attrs):
        if len(attrs) != 1:
            pass
        for k, v in attrs:
            if k == 'nowrap' and v == 'nowrap':
                self.in_right_td = True

    def end_td(self):
        self.in_right_td = False

    def start_a(self, attrs):
        need_check_class = False
        """
            <td nowrap="nowrap"><a href="http://www.douban.com/group/people/78284459/" class="">随便你吧</a></td>
        """
        if not self.in_right_td:
            pass
        elif len(attrs) != 2:
            pass
        else:
            for k, v in attrs:
                if k == 'href':  # href 先出现, 压栈
                    self.author_link_list.push(v[0] if isinstance(v, list) else v)
                    need_check_class = True
                if k == 'class' and v == '':
                    if need_check_class:
                        need_check_class = False

            if need_check_class: # 说明href后没有遇到class=""
                self.author_link_list.pop()
                need_check_class = False
            else:
                # 成功得到 username
                self.in_user_a = True

    def end_a(self):
        self.in_user_a = False

    def handle_data(self, data):
        if self.in_user_a:
            self.author_name_list.push(data)


class topic_liter(SGMLParser):
    """
    <td class="title">
        <a href="http://www.douban.com/group/topic/53402791/" title="苦逼小编来晒公司发的端午粽子！求关注！" class="">苦逼小编来晒公司发的端午粽子！求关注！</a>
    </td>
    """

    def __init__(self):
        SGMLParser.reset(self)
        self.in_td = False
        self.topic_link_list = myStack(25)  ## 默认情况下 一页只有25个 topic
        self.topic_name_list = myStack(25)

    def start_td(self, attrs):
        if len(attrs) == 1 and attrs[0] == ('class', 'title'):
            self.in_td = True

    def end_td(self):
        self.in_td = False

    def start_a(self, attrs):
        href_pushed = False
        name_pushed = False
        if self.in_td and len(attrs) == 3:
            for k, v in attrs:
                if k == 'href':
                    self.topic_link_list.push(v)
                    href_pushed += True
                if href_pushed and k == 'title':
                    self.topic_name_list.push(v)
                    name_pushed = True
                if href_pushed and k == 'class' and v == '' and name_pushed:
                    href_pushed = False
                    name_pushed = False
            if href_pushed or name_pushed:
                self.topic_link_list.pop()

    def end_a(self):
        pass


class group_lister(SGMLParser):
    """
    Get all groups that the specific user
    """

    def __init__(self):
        SGMLParser.reset(self)
        self.in_div = False
        self.dic_name_href = {}
        self.temp_key = None

    def start_div(self, attrs):
        for k, v in attrs:
            if k == 'class' and v == 'title':
                self.in_div = True

    def end_div(self):
        self.in_div = True

    def start_a(self, attrs):
        if self.in_div:
            #print type(attrs)  #  it is tuple list
            #print attrs
            for k, v in attrs:
                if k == 'title':
                    self.dic_name_href[v] = ""
                    self.temp_key = v
                if k == 'href' and self.temp_key:
                    self.dic_name_href[self.temp_key] = v
                    self.temp_key = None

    def get_name_href_dic(self):
        return self.dic_name_href


def find_user_topic_in_current_page_by_user_link(content, user_link):
    index = content.find(user_link)
    if index == -1:
        print "failed to find user main page url in this page"
    else:
        return index


class douban_group_topic_finder_by_user_link():
    def __init__(self, user_link=None, user_name=None, pages = 10): # 默认抓取每个小组前10页的帖子，即25×10=250个
        self.user_link = user_link
        self.user_joins_link = (user_link + "joins/") if user_link[-1] == '/' else (user_link + "/joins/")
        print self.user_joins_link
        self.user_name = user_name
        self.joined_group_dic = None  # key is topic name and value is topic url
        self.topic_by_this_user = [] # tuple list (topic_name,topic_link)
        self.pages= pages

    def get_groups_user_join(self):

        url_handler = urllib2.urlopen(self.user_joins_link)
        content = url_handler.read()
        url_handler.close()

        gl = group_lister()
        gl.feed(content)
        self.joined_group_dic = gl.dic_name_href  # 小组名为key url为value

    def find_user_topics(self):
        self.get_groups_user_join()
        if self.joined_group_dic == None or len(self.joined_group_dic) == 0:
            raise "This User have no group joined, so he has no right to publish topics"
        for k in self.joined_group_dic:
            #logging.DEBUG("scraping group %s, link %s" % k,self.joined_group_dic[k])
            #http://www.douban.com/group/douban911/discussion?start=0
            self.joined_group_dic[k] += "discussion"
            # TODO 遍历帖子
            for i in range(self.pages): # 遍历10页帖子
                this_page_url = self.joined_group_dic[k] + "?start=" + str(i * 25)
                print "this page :", this_page_url
                # 查看网页源代码是否有这个用户的链接
                this_handler = urllib2.urlopen(this_page_url)
                this_content = this_handler.read()
                if this_content.find(self.user_link) != -1: # 说明存在此用户，在这个页中
                    al = author_lister()
                    al.feed(this_content)
                    tl = topic_liter()
                    tl.feed(this_content)
                    if al.author_name_list.size == tl.topic_link_list.size:
                        # 话题发起者和活体数目是对应的，便利发起者找到对应的用户
                        for j in range(al.author_name_list.size):
                            if al.author_link_list.index(j) == self.user_link:
                                print "found one matched: %s, %s" % (tl.topic_name_list.index(j), tl.topic_link_list.index(j))
                                self.topic_by_this_user.append(
                                    ( tl.topic_name_list.index(j), tl.topic_link_list.index(j) ))


if __name__ == '__main__':
    #al = author_lister('http://www.douban.com/group/people/88915011/') # pass user home page url to the lister

    #uf = discussion_page_user_finder('test.html',False)

    #x = uf.find('http://www.douban.com/group/people/88915011/')
    #print x
    #content = urllib2.urlopen('http://www.douban.com/group/douban911/discussion?start=0').read()
    #content = ff.read()
    #df = douban_group_topic_finder_by_user_link()
    # 得到这个用户加入的所有小组
    """
    x = urllib2.urlopen('http://www.douban.com/group/people/juliandawn/joins').read()
    gl = group_lister()
    gl.feed(x)
    print gl.dic_name_href
    """

    df = douban_group_topic_finder_by_user_link(user_link='http://www.douban.com/group/people/68363866/')
    df.find_user_topics()
    for i in df.topic_by_this_user:
        print "Topic Name: %s && Topic Link: %s" % (i[0],i[1])



