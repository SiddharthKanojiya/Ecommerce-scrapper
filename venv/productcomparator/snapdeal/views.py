from django.shortcuts import render

from bs4 import BeautifulSoup
import requests
import re



#from selenium.webdriver.chrome.options import Options


#from .models import Product
from .serializers import ProductSerializers
from rest_framework.response import Response
from .serializers import productclass
from rest_framework.decorators import api_view
from re import sub
from decimal import Decimal

# Create your views here.


def fetch_snapdeal_product(sinput):
    
    def generate_url(part1,search_for,ch):
        url=part1
        list1=list(search_for)
        #print(list1)
        l=len(list1)
        for i in range(0,l):
            if list1[i]==' ':
                list1[i]=ch
            url=url+list1[i]
        return url
    search_for=sinput
    snapdealurl=generate_url('https://www.snapdeal.com/search?keyword=',search_for,'%20')+"&sort=rlvncy"
    print(snapdealurl)

    headers2 = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    #r1 = requests.get(amazon_url, headers=headers)
    r2=requests.get(snapdealurl,headers=headers2)
    content2=r2.content
    #content = r1.content
    print("3333333333333")
    soup2=BeautifulSoup(content2,features="html.parser")
    

    #print(soup2.find_all('img',class_='product-image wooble'))
    product_limit=5
    c=0
    new_data=[]
    pid=set()
    for t in soup2.find_all('div',class_='col-xs-6 favDp product-tuple-listing js-tuple',limit=product_limit):
        #print(t.get('src'),data['img'])
        ele=t.get('id')
        print(ele)
        data={}
        if ele not in pid:
            ratinghtml=t.find('div',class_='filled-stars')
            if ratinghtml:
                #print(,end=" ")
                rate=float(ratinghtml.get("style")[6:8])/20
                if rate<1:
                    rate*=10
                data["rating"]=rate            
            imagehtml=t.find('img',class_='product-image')
            if not imagehtml.get('src'):
                imagehtml=t.find('img',class_='product-image lazy-load')
                data["img"]=imagehtml.get('data-src')
                imagehtml=None
            if imagehtml:
                #print(,end=" ")
                data["img"]=imagehtml.get('src')
            
            titlehtml=t.find('p',class_='product-title')
            if titlehtml:
                #print(,end=" ")
                data["productInfo"]=titlehtml.get('title')
            linkhtml=t.find('a',class_='dp-widget-link noUdLine')
            if linkhtml:
                #print(,end=" ")
                data["link"]=linkhtml.get('href')
            pricehtml=t.find('span',class_='lfloat product-price')
            if pricehtml:
                #print(,end=" ")
                data["price"]=pricehtml.get('data-price')
            data["soldby"]="Snapdeal"
        pid.add(ele)
        new_data.append(data)
        print()
    return new_data
    #print(len(data["price"]),len(data["link"]),len(data["productInfo"]),len(data["img"]),len(data["rating"]))
    
    
    
    
@api_view(['GET','POST'])
def snapdealapi(request):
    #ans=Product.objects.filter(sinput="puma shoes")
    
    query=request.query_params.get("sinput")
    sortby=request.query_params.get("sortby")
    #print(sortby=="\"price\"",sortby)
    fp=fetch_snapdeal_product(query)
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