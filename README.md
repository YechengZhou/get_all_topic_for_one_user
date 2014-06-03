Get Douban Topics Initiated by Specified User
==========================

获得指定豆瓣id的用户所发表的所有帖子
需要提供豆瓣用户的主页url， 比如http://www.douban.com/people/73688708/

Usage:
-----------------------------------  
```python
>>>df = douban_group_topic_finder_by_user_link(user_link='http://www.douban.com/people/73688708/',pages = 100) # TODO page默认的时候搜索小组的所有帖子
>>>df.find_user_topics() # 执行查找动作
>>>df.print_result() # 输出结果
>>>result = df.get_result() # 将结果存下来 (话题标题，话题url)
```
