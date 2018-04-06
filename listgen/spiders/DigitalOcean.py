import json

import scrapy
from scrapy import signals
from pydispatch import dispatcher

import urllib3

import os


class DigitalOceanSpider(scrapy.Spider):
    name = 'digitalocean'

    start_urls = ['https://stat.ripe.net/data/searchcomplete/data.json?resource=DIGITALOCEAN']

    github_access_url = "https://api.github.com/gists"
    github_token = os.environ['GITHUB_TOKEN']
    github_gist_id = os.environ['GITHUB_GIST_ID']
    gist = ""

    def __init__(self, **kwargs):
        super(DigitalOceanSpider, self).__init__(**kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        print("# DigitalOcean prefixes from RIPE")
        jsonresponse = json.loads(response.body_as_unicode())
        for cats in jsonresponse["data"]["categories"]:
            if cats["category"] == "ASNs":
                for asn in cats["suggestions"]:
                    self.gist += "# {}\n".format(asn["value"])
                    as_url = 'https://stat.ripe.net/data/announced-prefixes/data.json?resource={}'.format(asn["value"])
                    yield scrapy.Request(as_url, callback=self.parse_prefixes)

    def parse_prefixes(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        for prefix in jsonresponse["data"]["prefixes"]:
            self.gist += "{}\n".format(prefix["prefix"])

    def spider_closed(self):
        data = {'files': {'digitalocean.ipset': {'content': self.gist}}}
        encoded_data = json.dumps(data).encode('utf-8')
        http = urllib3.PoolManager()
        r = http.request('PATCH', '{}/{}'.format(self.github_access_url, self.github_gist_id),
                         body=encoded_data,
                         headers={'Authorization': 'token {}'.format(self.github_token),
                                  'Content-Type': 'application/json',
                                  'User-Agent': 'urllib3'})
        if r.status == 200:
            exit(0)
        else:
            exit(1)
