#!/usr/bin/env python

from __future__ import print_function
import requests, argparse
import logging

from sys import version_info
if version_info[0] > 2:
    import http.client as http_client  # Py3+ renames httplib
else:
    import httplib as http_client

def debug_api():
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

WEBSITES = [
    "https://www.instagram.com/{}/media/",
    "https://twitter.com/{}",
    "http://pastebin.com/u/{}",
    "https://www.reddit.com/user/{}.json", # use .json for reddit to avoid rate limiting and stuff
    "https://github.com/{}",
    "https://www.facebook.com/{}" # only works if the user has set a vanity url
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--userid", required=True, help="Social Media Handle")
    parser.add_argument("-d", "--debug", action="store_true", help="Prints Debug from API Call")

    args = parser.parse_args()

    username = args.userid

    if args.debug:
        debug_api()

    session = requests.session()
    session.headers['User-agent'] = 'uiuc-tsprivsec.usercheck:0.9'

    for website in WEBSITES:
        url = website.format(username)

        # use custom user agent because reddit wants bots to use them
        response = session.get(url, allow_redirects=False)
        if response.status_code == 200:
                print("[*] User exists here: " + url)
        else:
                print("[!] User NOT FOUND here: " + url)

if __name__ == '__main__':
    main()
