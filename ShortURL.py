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
        self._sqliteAddress = f["sqliteAddress"]
        self._baseURL = f["baseURL"]
        self._shift_possibility = f["shift_possibility"]
        self._blacklist = f["blacklist"]
        self._support_url_pattern = f["support_url_pattern"]
        self._pattern = re.compile(self._support_url_pattern)
        self._min_length = f["min_length"]
        self._max_length = f["max_length"]
        self._max_length = 8 if self._max_length == -1 else self._max_length
        if self._min_length > self._max_length or self._min_length <= 0 \
                or self._shift_possibility <= 0 \
                or self._shift_possibility >= 1:
            raise ValueError("value invalid, check your config")
        self._shift_total = [36 ** i for i in range(self._min_length, self._max_length + 1)]
        if not os.path.exists(self._sqliteAddress):
            con = sq.connect(self._sqliteAddress)
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

        self._con = sq.connect(self._sqliteAddress)
        self._db = self._con.cursor()
        self._tLength = [i[0] for i in self._db.execute("SELECT Count(*) FROM LINKS")][0]
        self._connect_status = True

    def __generate_rand_phase(self):
        db_full = True
        length = self._min_length
        for i in range(len(self._shift_total)):
            if (self._shift_total[i] - self._tLength) / self._shift_total[i] > self._shift_possibility:
                db_full = False
                break
            length += 1
        result = ""
        if db_full:
            return False
        for i in range(length):
            result += chr(random.randint(ord('a'), ord('z'))) if random.randint(0, 1) else str(random.randint(0, 9))
        return result

    def check_legal_url(self, link):
        url = re.findall(self._pattern, link)
        bk = False
        for i in self._blacklist:
            if i in link:
                bk = True
                break
        if len(link) > 100 or len(url) == 0 or bk:
            return False
        return True

    def len(self):
        return self._tLength

    def add(self, link):
        if not self._connect_status:
            return "ERROR"
        if not self.check_legal_url(link):
            return "ILLEGAL"
        r = [i[0] for i in self._db.execute("SELECT RED from LINKS WHERE LINK = '{}'".format(link))]
        if len(r) != 0:
            return r[0]
        red = self.__generate_rand_phase()
        if not red:
            return "FULL"
        while len([i[0] for i in self._db.execute("SELECT * from LINKS WHERE RED = '{}'".format(red))]) != 0:
            red = self.__generate_rand_phase()
        self._db.execute("INSERT INTO LINKS (LINK, RED, TIME) \
                   VALUES ('{link}','{red}', '{time}')".format(link=link, red=red, time=int(time.time())))
        self._con.commit()
        self._tLength += 1
        return red

    def get(self, url):
        if not self._connect_status:
            return "ERROR"
        if not self.check_legal_url(url):
            return "ILLEGAL"
        mode = ["RED", "LINK"]
        if self._baseURL in url:  # red -> link
            mode = ["LINK", "RED"]
            url = url.split("/")[-1]
        r = [i[0] for i in self._db.execute("SELECT {mode1} from LINKS WHERE {mode2} = '{url}'"
                                            .format(url=url, mode1=mode[0], mode2=mode[1]))]
        if len(r) != 0:
            return r[0]
        return "NONE"

    def status(self):
        return {"total": self._tLength,
                "db": self._sqliteAddress,
                "connection": "on" if self._connect_status else "off",
                "blacklist": self._blacklist,
                "slot": [
                    round((self._shift_total[i] - self._tLength) / self._shift_total[i] - self._shift_possibility, 3)
                    for i in range(len(self._shift_total))]
                }

    def get_base_url(self):
        return self._baseURL

    def connect(self):
        if self._connect_status:
            print("already connect")
        else:
            self._con = sq.connect(self._sqliteAddress)
            self._db = self._con.cursor()
            self._tLength = [i[0] for i in self._db.execute("SELECT Count(*) FROM LINKS")][0]
            self._connect_status = True
            print("reconnect success")

    def close(self):
        self._con.close()
        self._connect_status = False
        print("close successful")


if __name__ == "__main__":
    print("module loaded")
