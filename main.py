from selenium import webdriver
from selenium.webdriver.common.by import By
import time as t
import json

links = []
titles = []
bodies = [] 


homePageURL = "https://www.investing.com/news/commodities-news"

driver = webdriver.Chrome()
driver.get(homePageURL)


leftbody = driver.find_element(By.ID, "leftColumn")
articles = leftbody.find_elements(By.CLASS_NAME, "js-article-item")
for article in articles:
    element = article.find_element(By.CLASS_NAME, "textDiv")        #for opdowiedzialny za zebranie linkow do poszczegolnych artykolow i ich tytulow
    item = element.find_element(By.CLASS_NAME,"title")
    link = item.get_attribute("href")
    links.append(link)
    title = item.get_attribute("title")
    titles.append(title)


for link in links:
    driver.get(link)
    item = driver.find_element(By.CLASS_NAME, "WYSIWYG")    #z poszczegolnych artykulow lapiemy tekst i dzieli na numerowane paragrafy
    paragraphs = item.find_elements(By.TAG_NAME, "p")
    i = 0
    body = {}
    for paragraph in paragraphs:
        if len(paragraph.text)>0:   #warunek na pozbycie sie pustych paragrafow np. {p3: ''}
            index = "p" + f"{i+1}"
            body[index] = paragraph.text
            i += 1            
    bodies.append(body)

driver.quit()

jsonfile = open("result.json","w")

articles = {"article":[]}
for i in range(0,len(links)):       #zapis wynikow do jsona
    item = {
        "title" : titles[i],
        "link" : links[i],
        "text" : bodies[i]
    }
    articles["article"].append(item)

json.dump(articles,jsonfile,indent=4)
jsonfile.close()



