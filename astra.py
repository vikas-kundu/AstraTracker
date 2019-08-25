# -*- coding: utf-8 -*-
import time
import re
import mechanize
from bs4 import BeautifulSoup

print('''                                                                                                                                                                                                                     

             _______  _______ _________ _______  _______ 
            (  ___  )(  ____ \\__   __/(  ____ )(  ___  )
            | (   ) || (    \/   ) (   | (    )|| (   ) |
            | (___) || (_____    | |   | (____)|| (___) |
            |  ___  |(_____  )   | |   |     __)|  ___  |
            | (   ) |      ) |   | |   | (\ (   | (   ) |
            | )   ( |/\____) |   | |   | ) \ \__| )   ( |
            |/     \|\_______)   )_(   |/   \__/|/     \|
_________ _______  _______  _______  _        _______  _______ 
\__   __/(  ____ )(  ___  )(  ____ \| \    /\(  ____ \(  ____ )
   ) (   | (    )|| (   ) || (    \/|  \  / /| (    \/| (    )|
   | |   | (____)|| (___) || |      |  (_/ / | (__    | (____)|
   | |   |     __)|  ___  || |      |   _ (  |  __)   |     __)
   | |   | (\ (   | (   ) || |      |  ( \ \ | (      | (\ (   
   | |   | ) \ \__| )   ( || (____/\|  /  \ \| (____/\| ) \ \__
   )_(   |/   \__/|/     \|(_______/|_/    \/(_______/|/   \__/
                                                               
''')

#various python sets and lists to store data
all_author_pages=list()
article_name=list()
final={}
count={}

#This function gets all the Author Pages
def get_all_pages(final_link):
    r=br.open(final_link)
    soup = BeautifulSoup(r, "html.parser")
    for i in soup.find_all('div', {'class': 'page-numbers clearfix'}):
        all_links= i.find_all('a', href=True)
        for i in all_links:
            all_author_pages.append(str(i['href']))
    
#This function scraps titles form all author pages one by one
def get_titles(article):
    r=br.open(article)    
    soup = BeautifulSoup(r, "html.parser")
    for i in soup.find_all('h2',{'class':'post-title'}):
        for j in i.find_all('a',title=True):
            title_convert=str(j['title'].encode("utf-8"))
            article_name.append(title_convert)

#This is a utility function to deal with UTF to ASCII conversion problems in python
def utf_filter(value):
    value=re.sub(r'[^\x00-\x7F]+','', value)
    return value

#This function scraps articles views using search queries of Astra
def title_view_scrapper(title_name):  
    str_query=utf_filter(title_name)
    search_url="https://www.getastra.com/blog/?s="+str_query.encode('utf-8')
    finalURL=search_url.replace(" ", "+")   #Astra seach parameter needs + instead of spaces
    limit_query=finalURL[:92]               #Used to limit the query to 92 characters otherwise Astra search results dont show anything for large searches
    r=br.open(limit_query)
    soup=BeautifulSoup(r,"html.parser")
    for i in soup.find_all('article'):
        for j in i.find_all('h2',{'class':'post-title'}):
            for k in j.find_all('a',title=True):
                title_post=str(k['title'].encode('utf-8'))
                str1=utf_filter(title_name)
                str2=utf_filter(title_post)
                if(str1==str2):
                    for l in i.find_all('div',{'class':'post-meta clearfix'}):
                        for m in l.find_all('span'):
                            txt=m.text
                            num=re.sub("\D", "",txt)
                            final[str_query]=num
                else:
                    continue

def filterTheDict(dictObj, callback):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if callback((key, value)):
            newDict[key] = value
    return newDict


#initialize
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders=[('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#print the remaining pages containing articles
name=str(raw_input("Enter the first word of your UserName on Astra site (i.e. UserName is vikas kundu so first word is vikas):"))
link="https://www.getastra.com/blog/author/"
final_link=link+name
all_author_pages.append(final_link)
get_all_pages(final_link)

# Get all the author pages
print("                    *****Author Pages*******\n")
for i in all_author_pages:
    print(i)
    get_titles(i)
print("\n                  *********END************ \n Please be patient Discovering Articles \n")
    

#Gets views using Title name and prints title name
for i in article_name:
        title_view_scrapper(i)
        strn= utf_filter(i)
        print("\n Title of Article Discovered: "+strn)
	
    
# Printing all the values from the final dictionary
print("\n Now Showing Article Views \n ")
time.sleep(3)
for key,val in final.items():    
	print (key+" : "+val+" Views")
	time.sleep(1)
	

# Scrapping Diagnostics	
print("\n No of titles discovered: "+str(len(article_name)))
print(" No of titles scrapped: "+str(len(final)))    

print("\n           **********ARTICLES WITH 4000+ VIEWS********* \n")
count = filterTheDict(final, lambda elem: int(elem[1])>4000)
for key,val in count.items():
    print(key+" : "+val+" Views")
    time.sleep(1)

