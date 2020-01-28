import bs4 as bs
import urllib.request


if __name__ == "__main__":
    listLandingPage = ['https://www.ndsu.edu/news/studentnews/deanslistfall2018/']
    for  link in listLandingPage:
        url = urllib.request.urlopen('https://www.ndsu.edu/news/studentnews/deanslistfall2018/')
        soup = bs.BeautifulSoup(url, 'html.parser')
        descen = soup.find(id='c564014')
        links = descen.find_all('a');
        print(links)
        # print(listLinks)
        # for states in listLinks:
        #     url2 = urllib.request.urlopen('https://www.ndsu.edu/news/studentnews/deanslistfall2018/')
        #     soup2 = bs.BeautifulSoup(url2, 'html.parser')
        #     table = soup.find('table')
        #     tableRows = table.find_all('tr')
        #     location = "Woops"
        #     for tr in tableRows[1:]:
        #         td = tr.find_all('td')
        #         if tr.find('td').text != "":
        #             location = tr.find('td').text
        #         row = [i.text for i in td[1:]]
        #         row.append(location)
        #         print(row)