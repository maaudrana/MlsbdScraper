
import csv
import time
from selenium import webdriver
driver = webdriver.Firefox()
tag = input("What you want to search: ")
post_want = int(input("Input the number of post you want scrape: "))
source = f"https://www.instagram.com/explore/tags/{tag}/"
name = source.split("/")[-2]
driver.get(source)
#maximizing the window
driver.maximize_window()

from bs4 import BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
li = soup.find_all("li", class_="Y8-fY ")


links = []

post_row = soup.find_all("div", class_="Nnq7C weEfm")
for posts in post_row:
    for post in posts:
        #getting relational link and appending to the list
        links.append("https://www.instagram.com" + post.find("a")['href'])

SCROLL_PAUSE_TIME = 10
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while(1):    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(len(links))

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    post_row = soup.find_all("div", class_="Nnq7C weEfm")

    for posts in post_row:
        for post in posts:
            links.append("https://www.instagram.com" + post.find("a")['href'])

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if len(set(links))>=post_want:
        break
    if new_height == last_height:
        break
    last_height = new_height
    if len(links) >= post_want:
        print(links)
        with open('seacrh_post_result.csv','w') as file:
            writer = csv.writer(file)
            for i in range(post_want):
                writer.writerow([links[i]])
        break
print(links)
