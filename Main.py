import bs4 as bs
import urllib.request
import Utility

if __name__ == "__main__":
    # NDSU likes to hide the deans lists, so you need to manually find the landing page for each semester
    listLandingPage = ['https://www.ndsu.edu/news/studentnews/deanslistspring2019/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistfall2018/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistspring2018/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistfall2017/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistspring2017/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistfall2016/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistspring2016/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistfall2015/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistspring2015/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistfall2014/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistspring2014/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistfall2013/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistspring2013/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistfall2012/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistspring2012/']
    # opens the file to write to
    f = open("fall2015.csv", "w")
    # reduced list due to large csv file
    for link in listLandingPage[10:11]:
        try:
            # creates a BS object for each Semester's landing page
            url = urllib.request.urlopen(link)
            soup = bs.BeautifulSoup(url, 'html.parser')
            # Find all links on the page
            links = soup.find_all('a')
            for x in links:
                try:
                    # collect information from the title of each link
                    words = x.text.split(" ")
                    state = ""
                    year = words[-2] + " " + words[-1]
                    # collect what state each link is for, or throw it away if it is not a dean's list link
                    while not words[0].startswith("Dean"):
                        state += " " + words[0]
                        words.pop(0)
                    # build a link for each state, then navigate and create a bs object for it
                    textString = "https://www.ndsu.edu/" + x.get('href')
                    url2 = urllib.request.urlopen(textString)
                    soup = bs.BeautifulSoup(url2, 'html.parser')
                    table = soup.find('table')
                    tableRows = table.find_all('tr')

                    if "other" in state.lower():
                        print(end="")
                        # TO do, figure out how to collect information from "other" states/countries
                        # for tr in tableRows[1:]:
                        #     td = tr.find_all('td')
                        #     if tr.find('td').text != "":
                        #         location = tr.find('td').text.split(",")[0]
                        #     row = [i.text for i in td[1:]]
                        #     row.append(location)
                        #     row.append(state)
                        #     row.append(year)
                        #     print(row)
                    else:
                        # collect information from each row in the table
                        Utility.basicState(tableRows, year, f)
                except IndexError:
                    print(end="")
                    # do nothing, throw away bad link
        except Exception:
            print("problem with url " + link)
