# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import os
import mysql.connector
import datetime as dt
import connect

# user = "root"
# password=""
# database="number"

#connection เป็น {}
connection = connect.confunc()
mydb = mysql.connector.connect(
        host="localhost",
        user=connection['user'],
        password=connection['password'],
        database=connection['database']
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
sql_delete = "DELETE FROM numbers"
mycursor.execute(sql_delete)
mydb.commit()
print(mycursor.rowcount, "บรรทัด ที่ลบ")

#loop
active_page = 1 # 1
# page = 0 # 0

# while active_page > page:
while True:

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
        # page += 1
        break;

    #ประกาศ Array
    network_arr = []
    phone_arr = []
    gender_arr = []
    price_arr = []
    status_arr = []
    print("active_page = ", active_page)
    print("--------------------------")

    ## หาข้อมูลใน TABLE
    table = soup.find("div", {"class": "tableshow"})


    # เครือข่าย
    # data_network = "" # ประกาศตัวแปรเพื่อรับค่า
    img_all = table.find_all('img')
    for img in img_all:
        img_old = str(img)
        img_old_split_1 = img_old.split("_")
        img_old_split_2 = img_old_split_1[-1].split(".")
        #network คือ string
        network = img_old_split_2[0]
        #print("network >>", network)
        # network_arr = [network]
        network_arr.append(network)
        # data_network = network_arr
        # print(network_arr)

        # for i in range(len(network_arr)):
        #     network = network_arr[i]
        # for network in network_arr:
        #     data_network = network
    print(network_arr)


    # เบอร์
    phone_all = table.find_all("form", {"action": "/ทำนายเบอร์"})
    for ph in phone_all:
        key_phone = ph.find('input')['value']
        value_phone = ph.find("a", {"class": "phone"}).text
        # print("key >>", key_phone)
        # print("phone >>", value_phone)
        # phone_arr = [value_phone]
        phone_arr.append(value_phone)
        # print(phone_arr)
        # for i in range(len(phone_arr)):
        #     phone = phone_arr[i]
        # for phone in phone_arr:
        #     data_phone = phone
            # print(data_phone)
    print(phone_arr)

    # # เพศ
    # gender_all = table.find_all("td", {"class": "gender"})
    # for gen in gender_all:
    #     gg = str(gen)
    #     gg_split_1 = gg.split("<")
    #     gg_split_2 = gg_split_1[1].split(">")
    #     gender = gg_split_2[1]
    #     #print("GENDER >>", gender)
    #     gender_arr = [gender]
    #     # print(gender_arr)


    # ราคา
    p_all = table.find_all("td", {"class": "price"})
    for pp in p_all:
        p = str(pp)
        p_split_1 = p.split(".")
        p_split_2 = p_split_1[0].split(">")
        price = p_split_2[1]
        #print("PRICE >>",price)
        # price_arr = [price]
        price_arr.append(price)
        # print(price_arr)
        # for price in price_arr:
        #     data_price = price
            # print(data_price)
    print(price_arr)


    # สถานะ
    # status_all = table.find_all("td", {"class": "status"})
    # for sta in status_all:
    #     try:
    #         key_status = sta.find('button')['id']
    #         value_status = sta.find("button", {"class": "reserves"}).text
    #     except:
    #         value_status = "จองแล้ว"
    #     #print("key >>", key_status)
    #     #print("value",c," >>", value_status)
    #     # status_arr = [value_status]
    #     status_arr.append(value_status)
    #     # for status in status_arr:
    #     #     data_status = status
    #         # print(data_status)
    # print(status_arr)


    mycursor = mydb.cursor()
    for i in range(len(phone_arr)):
        sql1 = "INSERT INTO numbers (number, price, operator)" \
               " VALUES (%s, %s, %s)"
        val1 = [
            (
                phone_arr[i],
                price_arr[i],
                network_arr[i]
            )
        ]
        mycursor.executemany(sql1, val1)
        mydb.commit()

    active_page += 1
    # page += 1



    # print("active_page รอบใหม่ = ", active_page)
    # print("page  = ", page)

