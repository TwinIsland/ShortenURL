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
import time


class ShortURL:
    def __init__(self):
        f = json.load(open("config.json", "r"))
        self.__sqliteAddress = f["sqliteAddress"]
        self.__baseURL = f["baseURL"]
        self.__shift_possibility = f["shift_possibility"]
        self.__blacklist = f["blacklist"]
        self.__support_url_pattern = f["support_url_pattern"]
        self.__pattern = re.compile(self.__support_url_pattern)
        self.__min_length = f["min_length"]
        self.__max_length = f["max_length"]
        self.__max_length = 5 if self.__max_length == -1 else self.__max_length
        if self.__min_length > self.__max_length or self.__min_length <= 0 \
                or self.__shift_possibility <= 0\
                or self.__shift_possibility >= 1:
            raise ValueError("value invalid, check your config")
        self.__shift_total = [36 ** i for i in range(self.__min_length, self.__max_length + 1)]
        if not os.path.exists(self.__sqliteAddress):
            con = sq.connect(self.__sqliteAddress)
            db = con.cursor()
            try:
                db.execute('''
                CREATE TABLE LINKS
                       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                       LINK CHAR(50)  UNIQUE NOT NULL,
                       RED CHAR(5) UNIQUE NOT NULL ,
                       TIME CHAR(10) NOT NULL)''')
                con.commit()
                con.close()
            except Exception as e:
                raise Exception("Fail to initialize database: " + str(e))

        self.__con = sq.connect(self.__sqliteAddress)
        self.__db = self.__con.cursor()
        self.__tLength = [i[0] for i in self.__db.execute("SELECT Count(*) FROM LINKS")][0]
        self.__connect_status = True

    def __generate_rand_phase(self):
        db_full = True
        length = self.__min_length
        for i in range(len(self.__shift_total)):
            if (self.__shift_total[i] - self.__tLength) / self.__shift_total[i] > self.__shift_possibility:
                db_full = False
                break
            length += 1
        result = ""
        if db_full:
            return False
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
        if not self.__connect_status:
            return "ERROR"
        if not self.__check_legal_url(link):
            return "ILLEGAL"
        r = [i[0] for i in self.__db.execute("SELECT RED from LINKS WHERE LINK = '{}'".format(link))]
        if len(r) != 0:
            return r[0]
        red = self.__generate_rand_phase()
        if not red:
            return "FULL"
        while len([i[0] for i in self.__db.execute("SELECT * from LINKS WHERE RED = '{}'".format(red))]) != 0:
            red = self.__generate_rand_phase()
        self.__db.execute("INSERT INTO LINKS (LINK, RED, TIME) \
                   VALUES ('{link}','{red}', '{time}')".format(link=link, red=red, time=int(time.time())))
        self.__con.commit()
        self.__tLength += 1
        return red

    def get(self, url):
        if not self.__connect_status:
            return "ERROR"
        if not self.__check_legal_url(url):
            return "ILLEGAL"
        mode = ["RED", "LINK"]
        if self.__baseURL in url:  # red -> link
            mode = ["LINK", "RED"]
            url = url.split("/")[-1]
        r = [i[0] for i in self.__db.execute("SELECT {mode1} from LINKS WHERE {mode2} = '{url}'"
                                             .format(url=url, mode1=mode[0], mode2=mode[1]))]
        if len(r) != 0:
            return r[0]
        return "NONE"

    def status(self):
        return {"total": self.__tLength,
                "db": self.__sqliteAddress,
                "connection": "on" if self.__connect_status else "off",
                "blacklist": self.__blacklist,
                "slot": [int((1 - self.__shift_possibility) * i) for i in self.__shift_total]
                }

    def connect(self):
        if self.__connect_status:
            print("already connect")
        else:
            self.__con = sq.connect(self.__sqliteAddress)
            self.__db = self.__con.cursor()
            self.__tLength = [i[0] for i in self.__db.execute("SELECT Count(*) FROM LINKS")][0]
            self.__connect_status = True
            print("reconnect success")

    def close(self):
        self.__con.close()
        self.__connect_status = False
        print("close successful")


if __name__ == "__main__":
    print("module loaded")
