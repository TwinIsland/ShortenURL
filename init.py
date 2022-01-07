# -*- coding:utf-8 -*-
"""
 @COPYRIGHT: TwinIsland
 @FILENAME: init.py
 @DESCRIPTION: init file for ShortURL.py
 @DATE: 6/1/2002
"""

baseURL = "https://erdao.me/"  # web base url
sqliteAddress = "./shortLink.db"  # sqlite address
shift_possibility = 0.5  # possibility limit for shifting the length of short url
support_url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'  # url pattern
