#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import mysql.connector
import itertools
import sys
import json
import os
import csv

namesList = []
kitchensList = []
reviewCount = []
averageDeliveryTime = []
deliveryCost = []
minimumOrder = []
hrefLinks = []
ratingNumbers = []
lastWrittenReviews = []

def saveFile(name, content):
  with open("data" + name + ".json", "w+") as f:
    f.write(content)

def saveFiles():
    saveFile('namesList', json.dumps(namesList))
    saveFile('kitchensList', json.dumps(kitchensList))
    saveFile('reviewCount', json.dumps(reviewCount))
    saveFile('averageDeliveryTime', json.dumps(averageDeliveryTime))
    saveFile('deliveryCost', json.dumps(deliveryCost))
    saveFile('minimumOrder', json.dumps(minimumOrder))
    saveFile('hrefLinks', json.dumps(hrefLinks))
    saveFile('ratingNumbers', json.dumps(ratingNumbers))
    saveFile('lastWrittenReviews', json.dumps(lastWrittenReviews))

def deleteFile(name):
  os.remove("data" + name + ".json")

def loadFiles():
    global namesList
    global kitchensList
    global reviewCount
    global averageDeliveryTime
    global deliveryCost
    global minimumOrder
    global hrefLinks
    global ratingNumbers
    global lastWrittenReviews

    with open("datanamesList.json") as f:
      namesList = json.loads(f.read())
    with open("datakitchensList.json") as f:
      kitchensList = json.loads(f.read())
    with open("datareviewCount.json") as f:
      reviewCount = json.loads(f.read())
    with open("dataaverageDeliveryTime.json") as f:
      averageDeliveryTime = json.loads(f.read())
    with open("datadeliveryCost.json") as f:
      deliveryCost = json.loads(f.read())
    with open("dataminimumOrder.json") as f:
      minimumOrder = json.loads(f.read())
    with open("datahrefLinks.json") as f:
      hrefLinks = json.loads(f.read())
    with open("dataratingNumbers.json") as f:
      ratingNumbers = json.loads(f.read())
    with open("datalastWrittenReviews.json") as f:
      lastWrittenReviews = json.loads(f.read())

def deleteFiles():
  deleteFile('namesList')
  deleteFile('kitchensList')
  deleteFile('reviewCount')
  deleteFile('averageDeliveryTime')
  deleteFile('deliveryCost')
  deleteFile('minimumOrder')
  deleteFile('hrefLinks')
  deleteFile('ratingNumbers')
  deleteFile('lastWrittenReviews')

def processExtract(postcode):
    global namesList
    global kitchensList
    global reviewCount
    global averageDeliveryTime
    global deliveryCost
    global minimumOrder
    global hrefLinks
    global ratingNumbers
    global lastWrittenReviews

    r = requests.get('https://www.pyszne.pl/' + postcode)

    html = urlopen(r.url)
    bs = BeautifulSoup(html, 'html.parser')

    try:
        for link in bs.find('div', {'class':'restaurants restaurantlist js-restaurantlist'}).find_all(
            'div', {'class':'restaurant'}):
                names = link.find_all('a', {'class':'restaurantname'})
                for a in names:
                    namesList.append(a.text.strip())
                kitchens = link.find_all('div', {'class':'kitchens'})
                for kitchen in kitchens:
                    kitchensList.append(kitchen.text.strip())
                review = link.find_all('meta', itemprop='reviewCount')
                for count in review:
                    reviewCount.append(count.get('content'))
                time = link.find_all('div', {'class':'avgdeliverytime avgdeliverytimefull open'})
                for delivery in time:
                    averageDeliveryTime.append(delivery.text.strip().lower())
                cost = link.find_all('div', {'class':'delivery-cost js-delivery-cost'})
                for delivery in cost:
                    deliveryCost.append(delivery.text.strip())
                order = link.find_all('div', {'class': 'min-order'})
                for minimum in order:
                    minimumOrder.append(minimum.text.strip().lower())
                hrefs = link.find_all('a', itemprop='name')
                for href in hrefs:
                    hrefLinks.append(href.get('href'))

        while True:
            try:
                namesList.remove('{{RestaurantName}}')
                kitchensList.remove('{{RestaurantCategories}}')
                hrefLinks.remove('{{RestaurantUrl}}')
            except ValueError:
                break

        print(namesList)
        print(kitchensList)
        print(reviewCount)
        print(averageDeliveryTime)
        print(deliveryCost)
        print(minimumOrder)
        print(hrefLinks)

    except AttributeError:
        print('Wprowadzony kod pocztowy nie istnieje. Prosimy o sprawdzenie danych i spróbowanie ponownie.')

    for x in hrefLinks:
        r2 = requests.get('https://www.pyszne.pl/'+ x +'#opinie')
        html2 = urlopen(r2.url)
        bs2 = BeautifulSoup(html2, 'html.parser')
        if (bs2.find('div', {'class': 'rating-number-container'}) != None):
            ratingNumber = bs2.find('div', {'class': 'rating-number-container'}).find('span').text
            ratingNumbers.append(ratingNumber)
        else:
            ratingNumbers.append("0")
        if (bs2.find('section', {'class': 'reviewbody'}) != None):
            lastWrittenReview = bs2.find('section', {'class': 'reviewbody'}).text
            lastWrittenReviews.append(lastWrittenReview)
        else:
            lastWrittenReviews.append("Brak recenzji")

    print(ratingNumbers)
    print(lastWrittenReviews)

    saveFiles()

def processTransform():
  global deliveryCost
  global minimumOrder

  loadFiles()

  for eachDeliveryCost in deliveryCost :
    if (eachDeliveryCost == 'GRATIS') :
      deliveryCost[deliveryCost.index(eachDeliveryCost)] = 0
    else :
      deliveryCost[deliveryCost.index(eachDeliveryCost)] = eachDeliveryCost[:-3] 

  for eachMiniumOrder in minimumOrder :
    minimumOrder[minimumOrder.index(eachMiniumOrder)] = eachMiniumOrder[4:-3]

  for eachlastWrittenReview in lastWrittenReviews:
    lastWrittenReviews[lastWrittenReviews.index(eachlastWrittenReview)] = eachlastWrittenReview.replace("\n", " ")

  saveFiles()


def processLoad():
    loadFiles()

    mydb = mysql.connector.connect(host='serwer1911877.home.pl', database='31775790_etl', user='31775790_etl', password='fOXMs2si', auth_plugin='mysql_native_password')
    ratingNumbers_list = list(itertools.chain(*ratingNumbers))  

    mycursor = mydb.cursor()

    for a, b, c, d, e, f, g, h in itertools.zip_longest(namesList, kitchensList, reviewCount, averageDeliveryTime, deliveryCost, minimumOrder, ratingNumbers, lastWrittenReviews):
            query = 'INSERT INTO info(title, kitchen, review_count, average_delivery_time, delivery_cost, minimum_order, rating_number, last_written_review) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            values = (a, b, c, d, e, f, g, h)
            mycursor.execute(query,values)
            mydb.commit()

    deleteFiles()

def saveAsCsv():
  with open("import.csv", "w+", encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=' ')
    ratingNumbers_list = list(itertools.chain(*ratingNumbers))
    for a, b, c, d, e, f, g, h in itertools.zip_longest(namesList, kitchensList, reviewCount, averageDeliveryTime, deliveryCost, minimumOrder, ratingNumbers, lastWrittenReviews):
      writer.writerow([a, b, c, d, e, f, g, str(h)])



def main():
    postcode = str(input("Proszę podać kod pocztowy: "))

    processExtract(postcode)
    processTransform()
    processLoad()



  
if __name__== "__main__":
  if("processExtract" in sys.argv):
    processExtract(sys.argv[2])
  elif("processTransform" in sys.argv):
    processTransform()
  elif("processLoad" in sys.argv):
    processLoad()
  else:
    main(sys.argv[1])
