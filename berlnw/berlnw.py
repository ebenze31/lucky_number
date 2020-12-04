# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import os
import mysql.connector
import datetime as dt

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lucky_number"
    )
print("Connect")

time = dt.datetime.now()
#print(time)

url_home = 'https://www.berlnw.com/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%9A%E0%B8%AD%E0' \
           '%B8%A3%E0%B9%8C%E0%B8%A1%E0%B8%87%E0%B8%84%E0%B8%A5/filter?page='
home = requests.get(url_home)
soup = BeautifulSoup(home.text,'html.parser')

# clear database
mycursor = mydb.cursor()
sql_delete = "DELETE FROM berlnw "
mycursor.execute(sql_delete)
mydb.commit()
print(mycursor.rowcount, "บรรทัด ที่ลบ")

#loop
active_page = 26
page = 25
c = 1
while active_page > page:

    data_arr = {
        c: {
            'network':"",
            'phone_number':"",
            'gender':"",
            'price':"",
            'active':""
        }
    }
    # print(data_arr)
    url = url_home + str(active_page) + "&sort_limit=1000&v="
    print("URL = ",url)

    home = requests.get(url)
    soup = BeautifulSoup(home.text,'html.parser')

    # ตรวจสอบว่ามีข้อมูลรึป่าว
    Property = soup.find("div",{"class":"getProperty"}).text
    Property_split = Property.split(" ")
    getProperty = Property_split[-1]
    #print("getProperty >>",getProperty)

    # เก็บข้อมูล
    if getProperty == "ไม่พบข้อมูล":
        print(">>>>>> เสร็จเรียบร้อย <<<<<<<")
        page += 1
    else:
        print("active_page = ", active_page)

        ## หาข้อมูลใน TABLE
        table = soup.find("div", {"class": "tableshow"})

        # เบอร์
        phone_all = table.find_all("form", {"action": "/ทำนายเบอร์"})
        for ph in phone_all:
            key_phone = ph.find('input')['value']
            value_phone = ph.find("a", {"class": "phone"}).text
            # print("key >>", key_phone)
            #print("phone >>", value_phone)
            data_arr[c]["phone_number"] = value_phone

        # เครือข่าย
        img_all = table.find_all('img')
        for img in img_all:
            img_old = str(img)
            img_old_split_1 = img_old.split("_")
            img_old_split_2 = img_old_split_1[-1].split(".")
            network = img_old_split_2[0]
            #print("network >>", network)
            data_arr[c]["network"] = network

        # เพศ
        gender_all = table.find_all("td", {"class": "gender"})
        for gen in gender_all:
            gg = str(gen)
            gg_split_1 = gg.split("<")
            gg_split_2 = gg_split_1[1].split(">")
            gender = gg_split_2[1]
            #print("GENDER >>", gender)
            data_arr[c]["gender"] = gender

        # ราคา
        p_all = table.find_all("td", {"class": "price"})
        for pp in p_all:
            p = str(pp)
            p_split_1 = p.split(".")
            p_split_2 = p_split_1[0].split(">")
            price = int(p_split_2[1])
            #print("PRICE >>",price)
            data_arr[c]["price"] = price

        # สถานะ
        status_all = table.find_all("td", {"class": "status"})
        for sta in status_all:
            try:
                key_status = sta.find('button')['id']
                value_status = sta.find("button", {"class": "reserves"}).text
            except:
                continue
            #print("key >>", key_status)
            #print("value",c," >>", value_status)
            data_arr[c]["active"] = value_status
            print(data_arr)


        c = c + 1
        active_page += 1
        page += 1


    # print("active_page รอบใหม่ = ", active_page)
    # print("page  = ", page)


