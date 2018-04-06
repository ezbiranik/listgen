# listgen

There are a lot of hack attempts/port-scans originating from DigitalOcean IPs.

It is pointless writing abuse emails, so we will just ban all of DigitalOcean IP space all together on the firewall.

* Download all DigitalOcean prefixes from RIPE.
* Upload prefix list to github.
* Use pfBlockerNG to download this list and block IPs.

## Install

```
pip install -r requirements.txt
scrapy crawl digitalocean
```

## Environment variables
```GITHUB_TOKEN``` - token for gist upload

```GITHUB_GIST_ID``` - gist id to update