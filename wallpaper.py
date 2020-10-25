# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 09:56:07 2020

Script to download all (maximun 20) the highest quality wallpapers of your choice

@author: AAYUSH MISHRA
"""

import os
import bs4
import requests

search = input('What are you looking for: ')
url = 'https://www.hdwallpapers.in/search.html?q=' + search

res = requests.get(url)
res.raise_for_status

soup = bs4.BeautifulSoup(res.text, 'html.parser')
errors = soup.select('.errors')

if len(errors) != 0:
    print('\nSorry, no wallpapers found with your search term. Please try other searches.\n')
else:
    os.makedirs(search, exist_ok = True)
    thumbs = soup.select('.thumb a')
    for i in range(len(thumbs)):
        nextUrl = 'https://www.hdwallpapers.in' + thumbs[i].get('href')
        newres = requests.get(nextUrl)
        newres.raise_for_status
        
        newSoup = bs4.BeautifulSoup(newres.text, 'html.parser')
        newLink = newSoup.select('.wallpaper-resolutions a')
        
        if len(newLink) == 0:
            continue
        
        imageUrl = 'https://www.hdwallpapers.in' + newLink[-1].get('href')
        print('\nDownloading wallpaper %s...' % (imageUrl))
        imageres = requests.get(imageUrl)
        imageres.raise_for_status
        
        imagePath = os.path.join(search, os.path.basename(imageUrl))
        imageFile = open(imagePath, 'wb')
        
        for chunk in imageres.iter_content(10000000):
            imageFile.write(chunk)
        imageFile.close()
        
    print('\nDownloaded\n')
    print('Check ' + search + ' folder')
