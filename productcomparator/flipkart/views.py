from django.shortcuts import render
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
# Create your views here

def fetch_amazon_product(sinput):
    path="C:\Program Files\drivers\chromedriver-win64"

    """options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)"""
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.in")
    sleep(3)
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    # type the keyword in searchbox
    search_box.send_keys(sinput)
    # create WebElement for a search button
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')
    # click search_button
    search_button.click()
    productInfo = driver.find_elements(By.XPATH, '//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/span')
    price = driver.find_elements(By.XPATH, '//span[@class="a-price-whole"]')
    img = driver.find_elements(By.XPATH, '//img[@class="s-image"]')
    link = driver.find_elements(By.XPATH, '//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
    rating = driver.find_elements(By.XPATH, '//div[@class="a-row a-size-small"]/span')
    data={
        "soldby": [],
        "productInfo": [],
        "price": [],
        "link": [],
        "img":[],
        "rating":[]
    }

    for c,item in enumerate(rating):
        if c%2!=0:
            continue
        data['rating'].append(item.get_attribute("aria-label")[:3])
        if c==8:
            break

    for c,item in enumerate(productInfo):
        data['productInfo'].append(item.text)
        data['soldby'].append("amazon")
        if c==4:
            break

    for c,item in enumerate(price):
        data['price'].append(item.text)
        if c==4:
            break
    for c,item in enumerate(img):
        data['img'].append(item.get_attribute("src"))
        if c==4:
            break
    for c,item in enumerate(link):
        data['link'].append(item.get_attribute("href"))
        if c==4:
            break
            
    print(data)
    #driver.quit()
    new_data={}
    length=len(data['productInfo'])+len(data['price'])+len(data['link'])+len(data['soldby'])+len(data['img'])+len(data['img'])
    if length<30:
        return {}
    for i in range(5):
        d={}
        d['productInfo']=data['productInfo'][i]
        d['price']=data['price'][i]
        d['link']=data['link'][i]
        d['img']=data['img'][i]
        d['soldby']=data['soldby'][i]
        d['rating']=data['rating'][i]
        
        new_data[i]=d
    for key in new_data:
        print(key,new_data[key])  
    return new_data






def fetch_flipkart_product(sinput):
    def generate_url(part1,part2,search_for,ch):
        url=part1
        list1=list(search_for)
        #print(list1)
        l=len(list1)
        for i in range(0,l):
            if list1[i]==' ':
                list1[i]=ch
            url=url+list1[i]
        url=url+part2
        return url
    search_for=sinput
    #amazon_url=generate_url('https://www.amazon.in/s?k=','&ref=nb_sb_noss_1',search_for,'+')
    fl_url=generate_url('https://www.flipkart.com/search?q=','&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off',search_for,'%20')

    headers2 = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    #r1 = requests.get(amazon_url, headers=headers)
    r2=requests.get(fl_url,headers=headers2)
    content2=r2.content
    #content = r1.content
    if  r2.status_code!=200:
        print('Sorry cannot fetch data for this product right now!!')
    print("3333333333333")
    soup2=BeautifulSoup(content2,features="html.parser")#chnage features="html.parser"
    #soup1=BeautifulSoup(content)

    data={
        "Sold By": [],
        "Product Info": [],
        "Price": [],
        "Link To Site": [],
        "img":[],
        "rating":[]
    }

    #_4rR01T,s1Q9rs,_2WkVRV,IRpwTa
    #_30jeq3
    #_2r_T1I,_396cs4
    #_________________________________________________________--
    cnt=0
    for t in soup2.find_all('div',class_='_3LWZlK'):
        data["rating"].append(t.get_text())
        cnt+=1
        if cnt==5:
            break
    
    cnt=0
    for t in soup2.find_all('img',class_='_2r_T1I'):
        
        data["img"].append(t.get('src'))
        cnt+=1
        if cnt==5:
            break
    for t in soup2.find_all('img',class_='_396cs4'):
        #print(t.get('src'))
        data["img"].append(t.get('src'))
        #print(data['img'])
        cnt+=1
        if cnt==5:
            break
    #_____________________________________________--
    cnt=0
    for t in soup2.find_all('a',class_='_4rR01T'):
        data["Sold By"].append('Flipkart')
        data["Product Info"].append(t.get_text())
        cnt+=1
        if cnt==5:
            break

    if len(data["Sold By"])<=5:
        for t in soup2.find_all('a',class_='s1Q9rs'):
            data["Sold By"].append('Flipkart')
            data["Product Info"].append(str(t.get_text()))
            cnt+=1
            if cnt==5:
                break

    if len(data["Sold By"])<=5:
        for t in soup2.find_all('a',class_='_2WkVRV'):
            data["Sold By"].append('Flipkart')
            data["Product Info"].append(str(t.get_text()))
            cnt+=1
            if cnt==5:
                break
        for t in soup2.find_all('a',class_='IRpwTa'):
            data["Sold By"].append('Flipkart')
            data["Product Info"].append(str(t.get_text()))
            cnt+=1
            if cnt==5:
                break

    cnt=0
    """for t in soup2.find_all('div',attrs={'class':'_30jeq3 _1_WHN1'},text=True):
        data["Price"].append(t.get_text())
        cnt+=1
        print(cnt,data["Price"])
        if cnt==5:
            break"""
    #print(data["Price"],len(data["Price"]))
    if len(data["Price"])<=5:
        for t in soup2.find_all('div',class_='_30jeq3'):
            data["Price"].append(t.get_text())
            cnt+=1
            if cnt==5:
                break
    cnt=0
    for t in soup2.find_all('a',attrs={'class':'_1fQZEK','href':re.compile("^https://www.flipkart.com/")},href=True):
        data["Link To Site"].append(t.get('href'))
        cnt+=1
        if cnt==5:
            break
    if len(data["Link To Site"])<=5:
        for t in soup2.find_all('a',attrs={'class':'IRpwTa','href':re.compile("^https://www.flipkart.com/")},href=True):
            data["Link To Site"].append(t.get('href'))
            cnt+=1
            if cnt==5:
                break
    if len(data["Link To Site"])<=5:
        for t in soup2.find_all('a',attrs={'class':'s1Q9rs','href':re.compile("^https://www.flipkart.com/")},href=True):
            data["Link To Site"].append(t.get('href'))
            cnt+=1
            if cnt==5:
                break
    new_data={}
    length=len(data['Product Info'])+len(data['Price'])+len(data['Link To Site'])+len(data['Sold By'])+len(data['img'])
    if length<25:
        return {}
    for i in range(5):
        d={}
        d['productInfo']=data['Product Info'][i]
        d['price']=data['Price'][i]
        d['link']=data['Link To Site'][i]
        d['img']=data['img'][i]
        d['soldby']=data['Sold By'][i]
        d['rating']=data['rating'][i]
        
        new_data[i]=d
    for key in new_data:
        print(key,new_data[key])  
    return new_data


def index(request):
    context={}
    print(request.method)
    if request.method=='POST':
        a=request.POST['productname']
        #print(requests.get(a).text)
        ans=fetch_flipkart_product(a)
        ans2=fetch_amazon_product(a)
        #print(ans)
        context={"pname":ans,"pname2":ans2}
        
    return render(request,'flipkart/index.html',context=context)