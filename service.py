from abc import ABC

from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import ShortURL
import configparser
import tornado.ioloop
import tornado.web
from pywebio.platform.tornado import webio_handler

config = configparser.ConfigParser()
config.read("service.ini", encoding='utf-8')
config = config['SERVICE']


def index_page():
    set_env(title=config['title'])

    def validate_url(callback):
        if not shortUrl.check_legal_url(callback):
            return "link illegal!"

    shortUrl = ShortURL.ShortURL()
    put_markdown("# [{}]({})".format(config['title'], config['link'] + ':' + config['proxy']))
    server_status = shortUrl.status()
    put_table([
        ["Total", "DB", "Connection", "Slot"],
        [server_status['total'], put_markdown('`' + server_status['db'] + '`'), server_status['connection'],
         server_status['slot']]
    ])
    link = input("Add Link:", validate=validate_url)

    status = shortUrl.add(link)
    put_markdown("## STATUS:")
    if status == "ERROR":
        out_msg = "link in blacklist, cannot be added"
    elif status == "ILLEGAL":
        out_msg = "link illegal, please check your input"
    elif status == "FULL":
        out_msg = "service run out of space"
    else:
        out_msg = put_link(shortUrl.get_base_url() + '/' + status, url=shortUrl.get_base_url() + '/' + status)
    put_table([
        ["In", "Out"],
        [link, out_msg]
    ])


class JumpHandler(tornado.web.RequestHandler, ABC):
    shortUrl = ShortURL.ShortURL()

    def get(self, path):
        origin = self.shortUrl.get(self.shortUrl.get_base_url() + '/' + path)
        if origin == 'ERROR' or origin == "ILLEGAL" or origin == "NONE":
            print("redirect fail, try {}".format(self.shortUrl.get_base_url() + '/' + path))
            self.redirect(config['link'] + ':' + config['proxy'])
        else:
            print("redirect ok, try {}".format(path))
            self.redirect(origin)


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", webio_handler(index_page)),
        (r"/([^/]+)", JumpHandler)
    ])
    application.listen(port=int(config['proxy']), address='localhost')
    print("short link application start at: ", config['link'] + ':' + config['proxy'])
    tornado.ioloop.IOLoop.current().start()
