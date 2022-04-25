from ipaddress import summarize_address_range
import feedparser
import json
import csv

#Known
dataset1 = open('valid.csv',"w", newline='',)
writer1 = csv.writer(dataset1, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
dataset2 = open('invalid.csv',"w", newline='')
writer2 = csv.writer(dataset1, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#unknown
dataset3 = open('mix.csv',"w", newline='')
writer3 = csv.writer(dataset1, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)


def get_posts_details(url):
    news_feed = feedparser.parse(url)
    posts = news_feed.entries
    news_dump = []

    print(posts[0])
    for post in posts:
        item = {}
        item['title'] = post.title
        item['link'] = post.link
        item['summary'] = post.summary
        news_dump.append(item)
    return news_dump  # returning the details which is dictionary


url = "http://feeds.bbci.co.uk/news/video_and_audio/world/rss.xml"
url2 = "https://www.globalissues.org/news/feed"

data = get_posts_details(url)  # return blogs data as a dictionary

if data:
# printing as a json string with indentation level = 2
    for item in data:
        writer1.writerow([item['title'] , item['summary'] , item['link']])
else:
    print("None")
