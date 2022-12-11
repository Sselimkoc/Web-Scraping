from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def process(data):
    clean_data = []
    soup = BeautifulSoup(data, "html.parser")
    people = soup.find_all(
        "div", {"class": "search-result-mobile-section md-lg-hidden"})

    for person in people:
        dict = {}
        dict["name"] = person.find(
            "a", {"class": "gray-block cursor"}).text.strip()
        dict["location"] = person.find_all("p")[1].text         #take all data from website as dict
        dict["number"] = person.find_all("p")[2].text
        clean_data.append(dict)
    return clean_data

gold_list = []
path = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()                 #this hide the display of chrome
options.add_argument("headless")
chrome_options=options
browser = webdriver.Chrome(executable_path=path) #, chrome_options=options

for i in range(1, 22):
    browser.get(f"https://www.gibsondunn.com/?paged1={i}&search=lawyer&type=lawyer&s&office%5B0%5D=1717&school")
    data = browser.page_source
    clean_person_data = process(data)
    gold_list.extend(clean_person_data)

df = pd.DataFrame(gold_list)
df = df.drop_duplicates(subset=None, keep="first", inplace=False)
df.to_csv("sample.csv", sep=',', encoding='utf-8', index=(False))
