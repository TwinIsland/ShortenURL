# -*- coding:utf-8 -*-
"""
 @COPYRIGHT: TwinIsland
 @FILENAME: ShortURL.py
 @DESCRIPTION: Model layer for shorten link service
 @DATE: 6/1/2021
"""

import random
import sqlite3 as sq
import re
import json
import os


class ShortURL:
    def __init__(self):
        f = json.load(open("config.json", "r"))
        sqliteAddress = f["config"]["sqliteAddress"]
        self.__config = f
        self.__baseURL = f["config"]["baseURL"]
        self.__shift_possibility = f["config"]["shift_possibility"]
        self.__blacklist = f["config"]["blacklist"]
        self.__support_url_pattern = f["config"]["support_url_pattern"]
        self.__pattern = re.compile(self.__support_url_pattern)

        if not os.path.exists(sqliteAddress):
            con = sq.connect(sqliteAddress)
            db = con.cursor()
            try:
                db.execute('''
                CREATE TABLE LINKS
                       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       LINK CHAR(50)  UNIQUE NOT NULL,
                       RED CHAR(5) UNIQUE NOT NULL );''')
                con.commit()
                con.close()
            except Exception as e:
                raise Exception("Fail to initialize database: " + str(e))

        self.__con = sq.connect(sqliteAddress)
        self.__db = self.__con.cursor()
        self.__tLength = [i[0] for i in self.__db.execute("SELECT Count(*) FROM LINKS")][0]

    def __generate_rand_phase(self):
        pos = [1190,
               39270,
               1256640,
               38955840]
        length = 0
        for i in range(len(pos)):
            if (pos[i] - self.__tLength) / pos[i] > self.__shift_possibility:
                length = i + 2
                break
        result = ""
        for i in range(length):
            result += chr(random.randint(ord('a'), ord('z'))) if random.randint(0, 1) else str(random.randint(0, 9))
        return result

    def __check_legal_url(self, link):
        url = re.findall(self.__pattern, link)
        bk = False
        for i in self.__blacklist:
            if i in link:
                bk = True
                break
        if len(link) > 50 or len(url) == 0 or bk:
            return False
        return True

    def len(self):
        return self.__tLength

    def add(self, link):
        if not self.__check_legal_url(link):
            return "ILLEGAL"
        r = [i[0] for i in self.__db.execute("SELECT RED from LINKS WHERE LINK = '{}'".format(link))]
        if len(r) != 0:
            return r[0]
        red = self.__baseURL + self.__generate_rand_phase()
        while len([i[0] for i in self.__db.execute("SELECT * from LINKS WHERE RED = '{}'".format(red))]) != 0:
            red = self.__baseURL + self.__generate_rand_phase()
        self.__db.execute("INSERT INTO LINKS (LINK, RED) \
                   VALUES ('{link}','{red}')".format(link=link, red=red))
        self.__con.commit()
        self.__tLength += 1
        return red

    def get(self, url):
        if not self.__check_legal_url(url):
            return "ILLEGAL"
        mode = ["RED", "LINK"]
        if self.__baseURL in url:  # red -> link
            mode = ["LINK", "RED"]
        r = [i[0] for i in self.__db.execute("SELECT {mode1} from LINKS WHERE {mode2} = '{url}'"
                                             .format(url=url, mode1=mode[0], mode2=mode[1]))]
        if len(r) != 0:
            return r[0]
        return "None"

    def close(self):
        with open("config.json", "w") as f:
            self.__config["count"] = self.__tLength
            json.dump(self.__config, f)
        f.close()
        self.__con.close()
