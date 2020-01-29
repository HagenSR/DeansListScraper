import bs4 as bs
import urllib.request


def goodInput(b):
    for i in b:
        if i is None or i.isspace():
            return False
    return True


def basicState(tableRows, year, f):
    state = ""
    for tr in tableRows[1:]:
        td = tr.find_all('td')
        # update city location if applicable
        if tr.find('td').text != "":
            city = tr.find('td').text.split(",")[0]
        # add information from the row/variables to a list
        row = [i.text for i in td[1:]]
        row.append(city)
        row.append(state)
        row.append(year)
        write = ""
        # move information from list to string
        if goodInput(row):
            for i in row:
                write += str(i) + ","
            # write to exampleOutput.csv
            f.write(write + "\n")


def linkHandler(stateLink):
    # collect information from the title of each link
    returnList = []
    words = stateLink.text.split(" ")
    state = ""
    year = words[-2] + " " + words[-1]
    # collect what state each link is for, or throw it away if it is not a dean's list link
    while not words[0].startswith("Dean"):
        state += " " + words[0]
        words.pop(0)
    # build a link for each state, then navigate and create a bs object for it
    textString = "https://www.ndsu.edu/" + stateLink.get('href')
    url2 = urllib.request.urlopen(textString)
    soup = bs.BeautifulSoup(url2, 'html.parser')
    table = soup.find('table')
    tableRows = table.find_all('tr')
    returnList.append(tableRows)
    returnList.append(year)
    returnList.append(state)
    return returnList
