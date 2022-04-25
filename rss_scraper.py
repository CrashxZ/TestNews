from ipaddress import summarize_address_range
import feedparser
import json
import csv

#Known
dataset1 = open('valid.csv',"a", newline='')
writer1 = csv.writer(dataset1, delimiter=',')
dataset2 = open('invalid.csv',"a", newline='')
writer2 = csv.writer(dataset2, delimiter=',')
#unknown
dataset3 = open('mix.csv',"a", newline='')
writer3 = csv.writer(dataset3, delimiter=',')


def get_posts_details(url):
    news_feed = feedparser.parse(url)
    posts = news_feed.entries
    news_dump = []

    # print(posts[0])
    for post in posts:
        item = {}
        item['title'] = post.title
        item['link'] = post.link
        try:
            item['summary'] = post.summary
        except:
            item['summary'] = post.description
        news_dump.append(item)
    return news_dump  # returning the details which is dictionary


url = "http://feeds.bbci.co.uk/news/video_and_audio/world/rss.xml"
url2 = "https://www.globalissues.org/news/feed"
url3 = "https://www.theguardian.com/world/rss"
url4 = "https://defence-blog.com/feed/"
url5 = "https://news.google.com/rss/search?q=world%20%news"

fake1 = "https://www.thepoke.co.uk/category/news/feed/"
fake2 = "https://www.theonion.com/rss"

test1 = "http://rss.cnn.com/rss/cnn_topstories.rss"

data = []
data2 = []
data3 = []

data = data + get_posts_details(url)
data = data + get_posts_details(url2)
data = data + get_posts_details(url3)
data = data + get_posts_details(url4)
data = data + get_posts_details(url4)

data2 = data2 + get_posts_details(fake1)
data2 = data2 + get_posts_details(fake2)

data3 = data3 + get_posts_details(test1)


# writer1.writerow(['title' , 'summary' , 'link'])
# writer2.writerow(['title' , 'summary' , 'link'])
writer3.writerow(['title' , 'summary' , 'link'])

if data:
# printing as a json string with indentation level = 2
    for item in data:
        #print(type(item))
        writer1.writerow([item['title'] , item['summary'] , item['link']])
    print("Collected  Verified Data")
else:
    print("Problem with Verified Data")

if data2:
    for item in data2:
        #print(type(item))
        writer2.writerow([item['title'] , item['summary'] , item['link']])
    print("Collected Fake Data")
else:
    print("Problem with Fake Data")


if data3:
    for item in data3:
        #print(type(item))
        writer3.writerow([item['title'] , item['summary'] , item['link']])
    print("Collected Test Data")
else:
    print("Problem with test Data")


