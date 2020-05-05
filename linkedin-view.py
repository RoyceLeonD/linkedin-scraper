'''
    Updated File.
    Author: Royce Leon DSouza
    Last Edit: 5/5/2020
    Comments: Started Working on the file Summer of 2019. And Bringing it back to life.
'''
import argparse, os, time
import urlparse, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
#Following Imports allow csv exports/
import csv
import requests
import random

def getPeopleLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url: 
            if '/in/' in url:
                links.append('https://www.linkedin.com'+url)
    return links

def getJobLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:       
            if '/jobs' in url:
                links.append(url)
    return links

def getPeopleInfo(page,browser):
    print "Scrapping Info"
    Name = str(page.find('h1', class_='pv-top-card-section__name inline t-24 t-black t-normal').get_text())
    Title = str(page.find('h2', class_='pv-top-card-section__headline mt1 t-18 t-black t-normal').get_text())
    #location = str(page.find('h3', class_='pv-top-card-section__location t-16 t-black--light t-normal mt1 inline-block').get_text())
    URL = browser.current_url

    URL_post = "https://hooks.zapier.com/hooks/catch/4928909/jg9yr8/silent/"
    PARAMS = {
        'Name':str(Name),
        'Title':str(Title),
        'URL':str(URL)
    }
    r = requests.post(URL_post, data = PARAMS) 
    print "Added"

def getID(url):
    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query)['id'][0]

def toScrollorNottoScroll(browser):
    number = random.randint(1,100)
    print "random number genorated"
    try:
        if number <50:
            time.sleep(random.uniform(0.5,4.9))
            number_to = str(random.randint(600,2400))
            print "number <50, and number_to genorated"
            browser.execute_script("window.scrollTo(0, "+number_to+")") 
            print "scrolled"
            toScrollorNottoScroll(browser)
        else:
            time.sleep(random.uniform(0.5,2.9))
            number_to = str(random.randint(600,2400))
            browser.execute_script("window.scrollTo(0, "+number_to+")")
    except:
        print "Scrapper Broke"

def ViewBot(browser,args,plist_in):
    visited = []
    pList = plist_in
    count = 0
    retry = 0
    people_page = 'https://www.linkedin.com/search/results/all/?keywords=ceo%20centre%20county&origin=SPCK&spellCorrectionEnabled=false'
    #people_page = 'https://www.linkedin.com/groups/1976445/members/'
    browser.get(people_page)
    try:
        if retry > 2:
            pList = 0
            if retry > 5:
                browser.close()
        if count >99:
            browser.close()
        while True:
            #sleep to make sure everything loads, add random to make us look human.
            time.sleep(random.uniform(1.5,5.9))
            page = BeautifulSoup(browser.page_source)
            people = getPeopleLinks(page)
            if people:
                for person in people:
                    if person not in visited:
                        pList.append(person)
                        visited.append(person)
            if pList:
                for persons in pList: #if there is people to look at look at them   
                    person = pList.pop(0)
                    browser.get(person)

                    toScrollorNottoScroll(browser)


                    current_page = BeautifulSoup(browser.page_source)
                    people = getPeopleLinks(current_page)
                    #getPeopleInfo(current_page,browser)
                    if people:
                        for person in people:
                            if person not in visited:
                                pList.append(person)
                                visited.append(person)

                    count += 1
                    print "Got: " + person + " Count: "+str(count)
            else: #otherwise find people via the job pages
                jobs = getJobLinks(page)
                if jobs:
                    job = random.choice(jobs)
                    root = 'http://www.linkedin.com'
                    roots = 'https://www.linkedin.com'
                    if root not in job or roots not in job:
                        job = 'https://www.linkedin.com'+job
                    browser.get(job)
                else:
                    print "I'm Lost Exiting"
                    break

        #Output (Make option for this)           
        print "[+] "+browser.title+" Visited! \n("\
            +str(count)+"/"+str(len(pList))+") Visited/Queue)"

    except:
        browser.close()
        browser = webdriver.Firefox()

        browser.get("https://linkedin.com/uas/login")

        time.sleep(random.uniform(1.5,5.9))

        emailElement = browser.find_element_by_id("username")
        emailElement.send_keys(args.email)
        passElement = browser.find_element_by_id("password")
        passElement.send_keys(args.password)
        passElement.submit()

        print "[+] Success! Logged In, Bot Starting0!, Again"
        time.sleep(random.uniform(1.5,5.9))


        ViewBot(browser,args,pList)

def logon(args):
    browser = webdriver.Firefox()
    browser.get("https://linkedin.com/uas/login")

    time.sleep(random.uniform(1.5,5.9))

    emailElement = browser.find_element_by_id("username")
    emailElement.send_keys(args.email)
    passElement = browser.find_element_by_id("password")
    passElement.send_keys(args.password)
    passElement.submit()

    return browser
                            

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("email", help="linkedin email")
    parser.add_argument("password", help="linkedin password")
    args = parser.parse_args()

    browser = logon(args)
    #browser2 = logon(args)

    
    print "[+] Success! Logged In, Bot Starting!"
    time.sleep(random.uniform(1.5,5.9))


    ViewBot(browser,args,[])
    browser.close()

if __name__ == '__main__':
    Main()