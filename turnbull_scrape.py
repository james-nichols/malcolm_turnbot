# Author: Angus Gratton

#!/usr/bin/env python3
import requests
import itertools
import datetime
import re
import html2text
from bs4 import BeautifulSoup

CATEGORY_URLS = [ "http://www.malcolmturnbull.com.au/media/category/speeches",
                  "http://www.malcolmturnbull.com.au/media/category/speeches/P10",
                  "http://www.malcolmturnbull.com.au/media/category/speeches/P20",
                  "http://www.malcolmturnbull.com.au/media/category/speeches/P30",
                  "http://www.malcolmturnbull.com.au/media/category/speeches/P40",
                  "http://www.malcolmturnbull.com.au/media/category/speeches/P50",
                  "http://www.malcolmturnbull.com.au/media/category/speeches/P60",
                  "http://www.malcolmturnbull.com.au/media/category/speeches/P70",
                  "http://www.malcolmturnbull.com.au/media/category/speeches/P80",
                  "http://www.malcolmturnbull.com.au/media/category/speeches/P90",
]

def get_all_speech_urls():
    return list(itertools.chain(*(get_speech_urls(c) for c in CATEGORY_URLS)))

# download a category page and grab the speech URLs
def get_speech_urls(category_url):
    r = requests.get(category_url)
    s = BeautifulSoup(r.text, "html.parser")
    urls = [a["href"] for a in s.find_all("a") if "read more" in a.text.lower()]
    if len(urls) != 10:
        print("WARNING: Expected 10 speech URLs at %s, found %d." % (category_url, len(urls)))
    return urls

# scrape a speech from its URL
def scrape_speech(url):
    r = requests.get(url)
    return plaintextify_speech(r.text)

# given speech HTML page content, strip out on the speech as plaintext
def plaintextify_speech(html):
    s = BeautifulSoup(html, "html.parser")
    main = s.select("div.col-main")[0]
    # valid paragraphs of the speech itself have no class attribute
    paras = [ p.text for p in main if p.name == "p" and not "class" in p.attrs ]
    # some of the speeches already use <br/> tags instead of <p> tags for paragraph breaks
    text = html2text.html2text(" <br/><br/> ".join(paras)).strip()
    if text.endswith("Ends"):
        text = text[:-4] # strip annoying <strong>Ends</strong> on recent speeches
    return text

def get_speech_date(html):
    s = BeautifulSoup(html, "html.parser")
    dateline = s.select(".detail-meta")[0].text
    groups = re.match("(\d+)[a-zA-Z]* ([a-zA-Z]+) (20..)", dateline).groups()
    return datetime.datetime.strptime(" ".join(groups), "%d %B %Y").date()

def main():
    print("Fetching speech URLs...")
    urls = get_all_speech_urls()
    print("Got %d speeches." % len(urls))
    for url in urls:
        print("Scraping %s..." % url)
        r = requests.get(url)
        content = plaintextify_speech(r.text)
        date = get_speech_date(r.text)
        filename = "speech-%s-%s.txt" % (date.isoformat(), url.split("/")[-1])
        with open(filename, "w") as f:
            f.write(content)
        print("Saved plaintext to %s" % filename)

if __name__ == "__main__":
    main()

