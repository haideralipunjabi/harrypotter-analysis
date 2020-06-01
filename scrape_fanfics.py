from bs4 import BeautifulSoup as soup
import requests
import json

main_url ="https://www.fanfiction.net/book/Harry-Potter/?&srt=4&r=10&len=100&p=%s"
base_url = "https://www.fanfiction.net"

freq = {}
count = 0


def story_generator():
    for i in range(1,11):
        r = requests.get(main_url%(i))
        s = soup(r.text,features="html5lib")
        stories = s.findAll('a',"stitle")
        for story in stories:
            global count
            count += 1
            print("Yield %s: %s"%(count,story.text))
            yield story.attrs['href']


def generate_frequency(words):
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    

def scrape_chapter(url):
    r = requests.get(url)
    s = soup(r.text, features="html5lib")
    return s.select_one(".storytext").text
    

for storyurl in story_generator():
    r = requests.get(base_url+storyurl)
    s = soup(r.text,features="html5lib")
    chap_select = s.select_one("#chap_select")
    chapters = int(len(list(chap_select.children)))
    file = open("fics/%s.txt"%(storyurl.split("/")[2]),"w")
    for i in range(1,chapters+1):
        url_parts = storyurl.split("/")
        url_parts[3] = str(i)
        file.write(scrape_chapter(base_url+"/".join(url_parts)))
    file.close()

