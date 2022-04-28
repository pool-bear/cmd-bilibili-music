import requests
import json
import sys
import re

def search(keyword, page = 1, tids = 3, **kwargs):
    head = "http://api.bilibili.com/x/web-interface/search/type"
    page_parsed = "?page=" + str(page)
    search_type = "&search_type=video"
    keyword_parsed = "&keyword=" + keyword
    tids = "&tids=" + str(tids)
    kwargs = ""
    try:
        for k, v in kwargs.items():
            kwargs += "&" + str(k) + "=" + str(v)
    except:
        pass
    url = head + page_parsed + search_type + keyword_parsed + tids + kwargs
    response = requests.get(url)
    raw = json.loads(response.text)
    numPages = raw["data"]["numPages"]
    video_matrix = raw["data"]["result"]    
    for video in video_matrix:
        video["title"] = re.sub(r"<em class=\"keyword\">(.*?)</em>", r"\1", video["title"])
    display(video_matrix, page, numPages)
    return video_matrix, page, numPages

def display(video_matrix, page, numPages):
    count = 0
    for video in video_matrix:
        count += 1
        print("{:<2}|".format(count), end = " ")
        print(video["title"])
    print(str(page) + "/" + str(numPages))

def turnPage(direction, page, numPages):
    if direction == "-":
        if page == 1:
            return page
        else:
            return page - 1
    elif direction == "=":
        if page == numPages:
            return page
        else:
            return page + 1