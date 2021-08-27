import requests
import xml.etree.ElementTree as ET

RSS_FEEDS = [
  {
    "source": "https://news.yale.edu/topics/social-sciences/rss",
    "schedule": "* */3 * * *"
  },
  {
    "source": "https://rss.nytimes.com/services/xml/rss/nyt/MostViewed.xml",
    "schedule": "* */3 * * *"
  },
  {
    "source": "https://xkcd.com/rss.xml",
    "schedule": "* * */3 * *"
  }
]


def get(url, cookies=False):
  res = requests.get(url=url)
  xml = ET.fromstring(res.text)
  return xml

def main():
  feeds = []
  for item in RSS_FEEDS:
    feed = get(item['source'])[0]
    feeds.append(feed)

  entries = []
  for feed in feeds:
    for item in feed.iter('item'):
      entry = dict()

      entry['title'] = item.find('title').text
      entry['link'] = item.find('link').text
      entry['info'] = item.find('description').text
      
      date_item = item.find('pubDate')
      if date_item:
        date = date_item.text
        # TODO: Normalize date/time to current timezone
        # see https://discuss.python.org/t/get-local-time-zone/4169/3 to get local timezone
        entry['date'] = date
      else:
        entry['date'] = None
      
      author_item = item.find('author')
      entry['author'] = author_item.text if author_item else None

      entries.append(entry)

  # TODO: sort rss entries and export to file
        

if __name__ == '__main__':
  main()