# -*- coding:utf-8 -*-
"""
 @COPYRIGHT: TwinIsland
 @FILENAME: sample.py
 @DESCRIPTION: Test ShortURL class
 @DATE: 6/1/2021
"""
import ShortURL

func = ShortURL.ShortURL()

# add link
result = func.add("https://sougo.com")
print(result)

# check total length
print(str(func.len()) + "\n")

# add duplicate
result = func.add("https://sougo.com")
print(result + "\n")

# check from original link / short link
result = func.get("https://sougo.com")
result2 = func.get("https://NOTEXIST.com")
print(result)
print(result2 + "\n")

# check illegal url
print(func.add("baidu.com"))
print(func.get("notURL"))

# don't forget to close the session
func.close()
