import bs4 as bs
import urllib.request


def good_input(b):
    if b is (None or b):
        return False
    return True


def basic_state(table_rows, year, f):
    city_state = ""
    for tr in table_rows:
        td = tr.find_all('td')
        # add information from the row/variables to a list
        row = []
        if td[0].text:
            city_state = td[0].text
        for i in td[1:]:
            if i.text:
                row.append(i.text)
        row.append(city_state)
        row.append(year)
        write = ""
        # move information from list to string:
        if row.__len__() is not 4:
            print("problem with row " + str(row))
        else:
            for i in row:
                if i:
                    write += str(i) + ","
            # write to exampleOutput.csv
            f.write(write + "\n")


def link_handler(state_link):
    # collect information from the title of each link
    return_list = []
    words = state_link.text.split(" ")
    state = ""
    year = words[-2] + " " + words[-1]
    # collect what state each link is for, or throw it away if it is not a dean's list link
    while not words[0].startswith("Dean"):
        state += " " + words[0]
        words.pop(0)
    # build a link for each state, then navigate and create a bs object for it
    text_string = "https://www.ndsu.edu/" + state_link.get('href')
    url2 = urllib.request.urlopen(text_string)
    soup = bs.BeautifulSoup(url2, 'html.parser')
    table = soup.find('table')
    table_rows = table.find_all('tr')
    return_list.append(table_rows)
    return_list.append(year)
    return_list.append(state)
    return return_list
