from django.shortcuts import render

# Create your views here.
"""from bs4 import BeautifulSoup
import requests
import re"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

#from .models import Product
from .serializers import ProductSerializers
from rest_framework.response import Response
from .serializers import productclass
from rest_framework.decorators import api_view
from re import sub
from decimal import Decimal

def fetch_amazon_product(sinput,driver,search_box):
    
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
        data['price'].append(Decimal(sub(r'[^\d.]', '', item.text)))
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
    new_data=[]
    length=len(data['productInfo'])+len(data['price'])+len(data['link'])+len(data['soldby'])+len(data['img'])+len(data['img'])
    if length<30:
        return {}
    for i in range(5):
        d={}
        #Product.objects.create(sinput=sinput,productInfo=data['productInfo'][i],price=data['price'][i],link=data['link'][i],img=data['img'][i],rating=data['rating'][i])
        d['productInfo']=data['productInfo'][i]
        d['price']=data['price'][i]
        d['link']=data['link'][i]
        d['img']=data['img'][i]
        d['soldby']=data['soldby'][i]
        d['rating']=data['rating'][i]
        
        new_data.append(d) 
    return new_data



@api_view(['GET','POST'])
def amazonapi(request):
    path="C:\Program Files\drivers\chromedriver-win64"
    """options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)"""
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.in")
    sleep(3)
    dont=False
    try:
        search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    except:
        dont=True
    if dont:
        Response({"Unable to get product":"becuz of shitty amazon capcha"})
    query=request.query_params.get("sinput")
    sortby=request.query_params.get("sortby")
    #print(sortby=="\"price\"",sortby)
    fp=fetch_amazon_product(query,driver,search_box)
    #fp=sorted(fp, key=lambda i: i['price'])
    if sortby==None or sortby=="\"price\"":
        fp=sorted(fp, key=lambda i: i['price'])
        print(fp)
    else:
        fp=sorted(fp, key=lambda i: float(i['rating']))
    print("\n")
    p=[]
    for item in fp:
        p.append(productclass(sinput=query,productInfo=item['productInfo'],price=item['price'],rating=item['rating'],link=item['link'],img=item['img']))
    serializer=ProductSerializers(p,many=True)
    context={"result":serializer.data}
    return Response(context)
    