import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def AajTak(moviename):
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    moviename = moviename.split(" ")
    print(moviename)

    query = "https://www.google.com/search?q="
    for word in moviename:
        query += word
        query += "+"
    query += "AajTak+movie+review+hindi"
    print(query)

    headers = {"user-agent": USER_AGENT}
    gpage = requests.get(query, headers=headers)
    gsoup = BeautifulSoup(gpage.content, 'lxml')
    print(gpage)
    if gsoup.status_code == 200:
        gsoup = BeautifulSoup(gsoup.content, "html.parser")
    # print(gpage)
    link = gsoup.find('div', class_ = 'rc')
    # print(link)
    link = link.div.a['href']
    print(link)

    page = requests.get(link)
    movie = BeautifulSoup(page.content, 'lxml')

    notreqchar = ('-','(',')','.','/','[',']', '"', ':')
    numbers = ('.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

    moviereview = ""
    try:
        moviereview = movie.find('h1', class_ = 'secArticleTitle').text
    except Exception as e:
        pass;
    moviereview = moviereview.split(':')
    try:
        moviereview = moviereview[1]
    except Exception as e:
        moviereview = moviereview[0]
    print(moviereview)
        
    movierating = ""
    try:
        movierating = movie.find('div', class_ = 'movie-rating')
        writer = movie.find('div', itemprop = 'author').span.text
        print(writer)
        writeri = writer.split(' ')[0]
        if(movierating is not None):
            movierating = movierating['data-star-value']
            movierating = movierating.split('%')[0]
            movierating = int(movierating)/20
        elif(writeri == 'सौरभ'):
            raw_movierating = movie.find('div', itemprop = 'articleBody').text
            try:
                raw_movierating = movie.find('div', itemprop = 'articleBody').text
                movierating = raw_movierating.split('स्टारः ')[1]
                movierating = movierating.split(' ')[2]
                movierating = movierating.split('\n')[0]
                temp = ""
                for i in movierating:
                    if(i in numbers):
                        temp += i
                    else:
                        break
                movierating = temp
                if(movierating == ""):
                    try:
                        movierating = raw_movierating.split('स्टारः ')[1]
                        movierating = movierating.split(' ')[0]
                        movierating = movierating.split('\n')[0]
                        temp = ""
                        for i in movierating:
                            if(i in numbers):
                                temp += i
                            else:
                                break
                        movierating = temp
                    except Exception as e:
                        movierating = -1
                        not_correct += 1
            except Exception as e:
                try:
                    movierating = raw_movierating.split('रेटिंगः ')[1]
                    movierating = movierating.split(' ')[2]
                    movierating = movierating.split('\n')[0]
                    temp = ""
                    for i in movierating:
                        if(i in numbers):
                            temp += i
                        else:
                            break
                    movierating = temp
                    if(movierating == ""):
                        try:
                            movierating = raw_movierating.split('रेटिंगः ')[1]
                            movierating = movierating.split(' ')[0]
                            movierating = movierating.split('\n')[0]
                            temp = ""
                            for i in movierating:
                                if(i in numbers):
                                    temp += i
                                else:
                                    break
                            movierating = temp
                        except Exception as e:
                            movierating = -1
                            not_correct += 1
                except Exception as e:
                    try:
                        movierating = raw_movierating.split('रेटिंगः ')
                        if(movierating[0] == raw_movierating):
                            movierating = raw_movierating.split('स्टारः ')
                            if(len(movierating) == 1):
                                movierating = -1
                                not_correct += 1
                            else:
                                movierating = movierating[1]
                                temp = ""
                                for i in movierating:
                                    if(i in numbers):
                                        temp += i
                                    else:
                                        break
                                movierating = temp
                        else:
                            movierating = movierating[1]
                            temp = ""
                            for i in movierating:
                                if(i in numbers):
                                    temp += i
                                else:
                                    break
                            movierating = temp
                    except Exception as e:
                        movierating = -1
                        not_correct += 1
        else:
            raw_movierating = movie.find('div', itemprop = 'articleBody').text
            lines = raw_movierating.split('\n')
            movierating = ""
            for i in lines:
                if(i.split(' ')[0] == 'रेटिंगः' or i.split(' ')[0] == 'स्टारः'):
                    temp = i.split(' ')[1]
                    for j in temp:
                        if(j in numbers):
                            movierating += j
                        else:
                            break
                    break
            if(movierating == ""):
                movierating = raw_movierating.split('रेटिंगः ')
                if(movierating[0] == raw_movierating):
                    movierating = raw_movierating.split('स्टारः ')
                    if(len(movierating) == 1):
                        movierating = -1
                        not_correct += 1
                    else:
                        movierating = movierating[1]
                        temp = ""
                        for i in movierating:
                            if(i in numbers):
                                temp += i
                            else:
                                break
                        movierating = temp
                else:
                    movierating = movierating[1]
                    temp = ""
                    for i in movierating:
                        if(i in numbers):
                            temp += i
                        else:
                            break
                    movierating = temp
        print(movierating)
    except Exception as e:
        pass
    data=[]
    link = link
    data.insert(0, link)
    data.insert(1, moviereview)
    data.insert(2, writer)
    data.insert(3, movierating)
    return data