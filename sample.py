# -*- coding:utf-8 -*-
"""
 @COPYRIGHT: TwinIsland
 @FILENAME: sample.py
 @DESCRIPTION: Test ShortURL class
 @DATE: 6/1/2002
"""
import ShortURL

func = ShortURL.ShortURL()

# For first time use, init the database
# func.init()

# add link
result1 = func.add("https://baidu.com")
result2 = func.add("https://erdao.com")
print(result1)
print(result2)

# check total length
print(func.len())

# add duplicate
result1 = func.add("https://baidu.com")
print(result1)
print(func.len())

# check from original link / short link
result1 = func.get("https://baidu.com")
result2 = func.get("https://notexist.com")
print(result1)
print(result2)

# do not forget to close the session
func.close_session()
