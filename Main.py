import bs4 as bs
import urllib.request

if __name__ == "__main__":
    # NDSU likes to hide the deans lists, so you need to manually find the landing page for each semester
    listLandingPage = ['https://www.ndsu.edu/news/studentnews/deanslistfall2018/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistspring2018/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistfall2017/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistspring2017/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistfall2016/'
        , 'https://www.ndsu.edu/news/studentnews/deanslistspring2016/']
    # opens the file to write to
    f = open("exampleOutput.csv", "w")
    for link in listLandingPage:
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
                    year = words[-1]
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
                    city = ""
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
                        for tr in tableRows[1:]:
                            td = tr.find_all('td')
                            # update city location if applicaple
                            if tr.find('td').text != "":
                                city = tr.find('td').text.split(",")[0]
                            # add information from the row/variables to a list
                            row = [i.text for i in td[1:]]
                            row.append(city)
                            row.append(state)
                            row.append(year)
                            write = ""
                            # move information from list to string
                            for i in row:
                                write += str(i) + ","
                            # write to exampleOutput.csv
                            f.write(write + "\n")
                except IndexError:
                    print(end="")
                    # do nothing, throw away bad link
        except Exception:
            print("problem with url " + link)
