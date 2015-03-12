#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import requests
from boilerpipe.extract import Extractor
import codecs
import yaml
import utils_yaml
import email.utils
import datetime 

polish_dir = "input/polish/"

rss_fakt = "http://fakt.pl.feedsportal.com/c/33674/f/621991/index.rss"
# has a paywall
#rss_wyborcza = "http://gazeta.pl.feedsportal.com/c/32739/f/532601/index.rss"

# Helper method to convert from
# http://fakt.pl.feedsportal.com/c/33674/f/621991/s/44318fab/l/0L0Sfakt0Bpl0Ckatowice0Cnie0Ekupuj0Edopalaczy0E0Hartykuly0H5298860Bhtml/story01.htm
# to this
# http://www.fakt.pl/katowice/nie-kupuj-dopalaczy-,artykuly,529886.html
# to cirumvent advertisment
def convert_url(url):

	temp1 = url.split("/")[-2]
	temp2 = (temp1
		.replace("0A","0")
		.replace("0B",".")
		.replace("0C","/")
		.replace("0E","-")
		.replace("0H",",")
		.replace("0I","_")
		.replace("0L","")
		.replace("0S",""))
	return "http://" + temp2

def run():
    feed = feedparser.parse(rss_fakt)
    for item in feed["items"]:
        url = convert_url(item["link"])
        print item["published"]
        print url
        extractor = Extractor(extractor="ArticleExtractor", url=url)

        filename = url.split(",")[-1].split(".")[0]

        date = email.utils.parsedate_tz(item["published"])
        timestamp = email.utils.mktime_tz(date)
        iso = datetime.datetime.utcfromtimestamp(timestamp).isoformat()

        data = {"text": extractor.getText(), "date": iso, "url":url }

        with open(polish_dir + filename + ".yml", "w") as f:
            # see http://stackoverflow.com/questions/20352794/pyyaml-is-producing-undesired-python-unicode-output
            utils_yaml.ordered_dump(data, f, Dumper=yaml.SafeDumper, default_flow_style=False, width=100, encoding="utf-8", allow_unicode=True)


if __name__ == '__main__':
    run()