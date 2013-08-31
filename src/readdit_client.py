__author__ = 'kent'

from time import sleep
import urllib.request
from json import loads
import os

import praw


def get_links(subscribe):
    r = praw.Reddit(user_agent='User-Agent: rbot/1.0 by draculacwg')
    submissions = r.get_subreddit(subscribe).get_hot(limit=20)
    results = list()
    for submission in submissions:
        results.append(submission.url)
    return results


def download_images(subscribe, link, album=None):
    assert isinstance(link, str)
    if link.endswith('.jpg') or link.endswith('.gif'):
        if album is None:
            folder = "../images/" + subscribe
        else:
            folder = "../images/" + subscribe + '/' + album

        filename = link[link.rindex('/') + 1:]
        try:
            os.makedirs(folder)
        except FileExistsError:
            pass

        path = folder + '/' + filename

        try:
            with open(path):
                print('PASS: file exist =>' + path)
        except IOError:
            print("downloading : " + path)
            urllib.request.urlretrieve(link, filename=path)


def album_json(album_id):
    url = 'https://api.imgur.com/3/gallery/album/%s/json' % (album_id)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'Authorization': 'Client-ID 69a8c05a5598b21'}  # it's my client id, use yours instead, pls
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    json_obj = loads(the_page.decode('utf-8'))
    return json_obj


def is_image(link: str) -> bool:
    jpg = link.find('jpg') != -1
    gif = link.find('gif') != -1
    return jpg or gif


def is_thumbnails(link: str) -> bool:
    return link.endswith('m')


def get_original_link_from_thumb(link):
    return link[:-1] + '.jpg'


def is_album(link: str) -> bool:
    return link.find('/a/') != -1


subscribes = ['nsfw', 'gonewild', 'RealGirls', 'NSFW_GIF', 'nsfw_gifs', 'LegalTeens', 'AsianGirls']


for subscribe in subscribes:
    print('====' + subscribe + '====')
    links = get_links(subscribe)
    for link in links:
        if is_image(link):
            download_images(subscribe, link)
        elif is_thumbnails(link):
            new_link = get_original_link_from_thumb(link)
            download_images(subscribe, new_link)
        elif is_album(link):
            print("album url: %s" % link)
            album_id = link[len('http://imgur.com/a/'):]
            json = album_json(album_id)
            images = json['data']['images']
            for img in images:
                download_images(subscribe, img['link'], album_id)
        else:
            download_images(subscribe, link + '.jpg')
    sleep(5)

# TODO fetch this album : http://imgur.com/r/nsfw/top/all
