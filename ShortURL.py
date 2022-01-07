# -*- coding:utf-8 -*-
"""
 @COPYRIGHT: TwinIsland
 @FILENAME: ShortURL.py
 @DESCRIPTION: Model layer for shorten link service
 @DATE: 6/1/2002
"""

import random
import sqlite3 as sq
import re
import init

baseURL = init.baseURL
sqliteAddress = init.sqliteAddress
shift_possibility = init.shift_possibility
support_url_pattern = init.support_url_pattern


class ShortURL:
    __con = sq.connect(sqliteAddress)
    __db = __con.cursor()
    __pattern = re.compile(support_url_pattern)

    def init(self):
        try:
            self.__db.execute('''
            CREATE TABLE links
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   LINK CHAR(50)  UNIQUE NOT NULL,
                   RED CHAR(5) UNIQUE NOT NULL );''')
        except Exception as e:
            raise Exception("Fail to initialize database: " + str(e))

    def __generate_rand_phase(self):
        pos = [1190,
               39270,
               1256640,
               38955840]
        total = [i[0] for i in self.__db.execute("SELECT Count(*) FROM LINKS")][0]
        length = 0
        for i in range(len(pos)):
            if (pos[i] - total) / pos[i] > shift_possibility:
                length = i + 2
                break
        if 5 < length <= 0:
            raise IndexError("Length must be larger than 0")
        result = ""
        for i in range(length):
            result += chr(random.randint(ord('a'), ord('z'))) if random.randint(0, 1) else str(random.randint(0, 9))
        return result

    def __check_url(self, link):
        url = re.findall(self.__pattern, link)
        if len(link) > 50 or len(url) == 0:
            raise IndexError("illegal url")

    def len(self):
        total = [i[0] for i in self.__db.execute("SELECT Count(*) FROM LINKS")][0]
        return total

    def add(self, link):
        self.__check_url(link)
        r = [i[0] for i in self.__db.execute("SELECT RED from LINKS WHERE LINK = '{}'".format(link))]
        if len(r) != 0:
            return r[0]
        red = baseURL + self.__generate_rand_phase()
        while len([i[0] for i in self.__db.execute("SELECT * from LINKS WHERE RED = '{}'".format(red))]) != 0:
            red = baseURL + self.__generate_rand_phase()
        self.__db.execute("INSERT INTO LINKS (LINK, RED) \
                   VALUES ('{link}','{red}')".format(link=link, red=red))
        self.__con.commit()
        return red

    def get(self, url):
        self.__check_url(url)
        mode = ["RED", "LINK"]
        if baseURL in url:  # red -> link
            mode = ["LINK", "RED"]
        r = [i[0] for i in self.__db.execute("SELECT {mode1} from LINKS WHERE {mode2} = '{url}'"
                                             .format(url=url, mode1=mode[0], mode2=mode[1]))]
        if len(r) != 0:
            return r[0]
        return None

    def close_session(self):
        self.__con.close()
