from django.shortcuts import render
from django.http import HttpResponse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pyszne.models import Info
import requests
import itertools
# import mysql.connector

# Create your views here.

def index(request):
    # x = 1212;
    # return HttpResponse(x)

    return render(request, 'pyszne/index.html')

def scraper(request):
    postcode = request.POST.get("postCode", "")

    r = requests.get('https://www.pyszne.pl/' + postcode)

    html = urlopen(r.url)
    bs = BeautifulSoup(html, 'html.parser')
    # return HttpResponse(bs)

    namesList = []
    kitchensList = []
    reviewCount = []
    averageDeliveryTime = []
    deliveryCost = []
    minimumOrder = []
    hrefLinks = []
    ratingNumbers = []

    try:
        for link in bs.find('div', {'class': 'restaurants restaurantlist js-restaurantlist'}).find_all(
                'div', {'class': 'restaurant'}):
            names = link.find_all('a', {'class': 'restaurantname'})
            for a in names:
                namesList.append(a.text.strip())
            kitchens = link.find_all('div', {'class': 'kitchens'})
            for kitchen in kitchens:
                kitchensList.append(kitchen.text.strip())
            review = link.find_all('meta', itemprop='reviewCount')
            for count in review:
                reviewCount.append(count.get('content'))
            time = link.find_all('div', {'class': 'avgdeliverytime open'})
            for delivery in time:
                averageDeliveryTime.append(delivery.text.strip().lower())
            cost = link.find_all('div', {'class': 'delivery-cost js-delivery-cost'})
            for delivery in cost:
                deliveryCost.append(delivery.text.strip())
            order = link.find_all('div', {'class': 'min-order'})
            for minimum in order:
                minimumOrder.append(minimum.text.strip())
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

        # print(namesList)
        # print(kitchensList)
        # print(reviewCount)
        # print(averageDeliveryTime)
        # print(deliveryCost)
        # print(minimumOrder)
        # print(hrefLinks)

    except AttributeError:
        print('Wprowadzony kod pocztowy nie istnieje. Prosimy o sprawdzenie danych i spróbowanie ponownie.')

    for x in hrefLinks:
        r2 = requests.get('https://www.pyszne.pl/' + x + '#opinie')
        html2 = urlopen(r2.url)
        bs2 = BeautifulSoup(html2, 'html.parser')
        if (bs2.find('div', {'class': 'rating-number-container'}) != None):
            ratingNumber = bs2.find('div', {'class': 'rating-number-container'}).find('span').text.split()
            ratingNumbers.append(ratingNumber)
        else:
            ratingNumbers.append("0")

    ratingNumbers_list = list(itertools.chain(*ratingNumbers))

    for a, b, c, d, e, f, g in zip(namesList, kitchensList, reviewCount, averageDeliveryTime, deliveryCost,minimumOrder, ratingNumbers_list):
        i = Info(title=a, kitchen=b, review_count=c, average_delivery_time=d, delivery_cost=e, minimum_order=f, rating_number=g)
        i.save()

        # Tutaj bedzie jakiś return response na templatke z tymi przyciskami