#!/usr/bin/env python3
import sys
import requests
import os
from pathlib import Path
from urllib.request import urlretrieve
from urllib.parse import urlparse, urljoin
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

def get_all_images(url):
    """
    Returns all images as part of an dict.
    """
    print('Extracting assets from html')
    soup = bs(requests.get(url).content, "html.parser")
    imgs = {}
    for a in soup.find_all("a", class_='originalNameLink'):
        temp = {}
        temp['name'] = a['download'] #the filename
        temp['url'] =  urljoin(url, a['href']) #The lonk
        imgs[a['download']] = temp
    return imgs

def download(img, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    print('Downloading:', img['name'])
    Path(pathname).mkdir(parents=True, exist_ok=True)
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # get the file name
    filename = img['name']
    urlretrieve(img['url'], pathname + '/' + img['name'])

def main(url):
    print('Hello World')
    imgs = get_all_images(url)
    for img in imgs:
        # for each image, download it
        download(imgs[img], 'downloads')

if len(sys.argv) < 2:
    print('Requires target URL.')
    exit(0)
main(sys.argv[1])
