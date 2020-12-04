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
while active_page >  page:

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
            # print("value >>", value_phone)

            mycursor = mydb.cursor()

            sql = "INSERT INTO berlnw (created_at, phone_number) VALUES (%s, %s)"
            val = (time, value_phone)
            mycursor.execute(sql, val)

            mydb.commit()

        # เครือข่าย
        img_all = table.find_all('img')
        for img in img_all:
            img_old = str(img)
            img_old_split_1 = img_old.split("_")
            img_old_split_2 = img_old_split_1[-1].split(".")
            network = img_old_split_2[0]
            print("IMG >>", network)

        # # เพศ
        # gender = table.find("td", {"class": "gender"}).text
        # print("GENDER >>", gender)
        #
        # # ราคา
        # p = table.find("td", {"class": "price"}).text
        # p_split = p.split(".")
        # price = int(p_split[0])
        # print("PRICE >>",price)
        #
        # # สถานะ
        # status_all = table.find_all("td", {"class": "status"})
        # for sta in status_all:
        #     status = sta
        #     key_status = sta.find('button')['id']
        #     value_status = sta.find("button", {"class": "reserves"}).text
        #
        #     print("key >>", key_status)
        #     print("value >>", value_status)
        #
        #
        active_page += 1
        page += 1


    # print("active_page รอบใหม่ = ", active_page)
    # print("page  = ", page)


