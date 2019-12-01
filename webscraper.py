from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import mysql.connector
import itertools

namesList = []
kitchensList = []
reviewCount = []
averageDeliveryTime = []
deliveryCost = []
minimumOrder = []
hrefLinks = []
ratingNumbers = []
lastWrittenReviews = []


def ProcessExtract():
    postcode = str(input("Proszę podać kod pocztowy: "))
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


def processTransform():
    for eachDeliveryCost in deliveryCost :
        if (eachDeliveryCost == 'GRATIS') :
            deliveryCost[deliveryCost.index(eachDeliveryCost)] = 0
        else :
            deliveryCost[deliveryCost.index(eachDeliveryCost)] = eachDeliveryCost[:-3] 

    for eachMiniumOrder in minimumOrder :
        minimumOrder[minimumOrder.index(eachMiniumOrder)] = eachMiniumOrder[4:-3]



def processLoad():
    mydb = mysql.connector.connect(host='serwer1911877.home.pl', database='31775790_etl', user='31775790_etl', password='fOXMs2si', auth_plugin='mysql_native_password')
    ratingNumbers_list = list(itertools.chain(*ratingNumbers))  

    mycursor = mydb.cursor()

    for a, b, c, d, e, f, g, h in zip(namesList, kitchensList, reviewCount, averageDeliveryTime, deliveryCost, minimumOrder, ratingNumbers, lastWrittenReviews):
            query = 'INSERT INTO info(title, kitchen, review_count, average_delivery_time, delivery_cost, minimum_order, rating_number, last_written_review) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            values = (a, b, c, d, e, f, g, h)
            mycursor.execute(query,values)
            mydb.commit()



def main():
    ProcessExtract()
    processTransform()
    processLoad()


  
if __name__== "__main__":
  main()