from django.shortcuts import render

# Create your views here.

from bs4 import BeautifulSoup
import requests




#from selenium.webdriver.chrome.options import Options


#from .models import Product
from .serializers import ProductSerializers
from rest_framework.response import Response
from .serializers import productclass
from rest_framework.decorators import api_view


# Create your views here.


def fetch_reliance_digital_product(sinput):
    
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
    relianceurl=generate_url('https://www.reliancedigital.in/search?q=',search_for,'%20')+":relevance"
    print(relianceurl)

    headers2 = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    #r1 = requests.get(amazon_url, headers=headers)
    r2=requests.get(relianceurl,headers=headers2)
    content2=r2.content
    #content = r1.content
    print("3333333333333")
    soup2=BeautifulSoup(content2)
    
    new_data=[]
    
    for t in soup2.find_all('div',class_='sp grid',limit=5):
        data={}
        titlehtml=t.find('img',class_='img-responsive imgCenter')
        if titlehtml:
            data['productInfo']=titlehtml.get('title')
        imghtml=t.find('img',class_='img-responsive imgCenter')
        if imghtml:
            data['img']="https://www.reliancedigital.in"+imghtml.get('data-srcset')
        pricehtml=t.find('span',class_='TextWeb__Text-sc-1cyx778-0 llZwTv')
        if pricehtml:
            data['price']=pricehtml.text[1:]
        linkhtml=t.find('a')
        if linkhtml:
            data['link']="https://www.reliancedigital.in"+linkhtml.get('href')
        data['soldby']="Reliance Digital"
        data['rating']=None
        new_data.append(data)
    return new_data
        #print(len(data["price"]),len(data["link"]),len(data["productInfo"]),len(data["img"]),len(data["rating"]))
        
        
    
    
@api_view(['GET','POST'])
def reliance_digitalapi(request):
    #ans=Product.objects.filter(sinput="puma shoes")
    
    query=request.query_params.get("sinput")
    sortby=request.query_params.get("sortby")
    #print(sortby=="\"price\"",sortby)
    fp=fetch_reliance_digital_product(query)
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