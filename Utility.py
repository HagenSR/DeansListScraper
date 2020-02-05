import bs4 as bs
import urllib.request


def good_input(b):
    if b and (not b.isspace()):
        return True
    return False


def row_handler(table_rows, year, file):
    '''
    pulls information out of each row, throwing it away if it doesn't have enough entries to be valid
    (Name, Major, Year, city, location)
    :param table_rows: a collection of rows containing deans list information 
    :param year: a year and semester for a given table
    :param file: a file to write to
    :return: nothing, this method writes directly to a csv file
    '''
    city = ""
    state = ""
    for tr in table_rows:
        td = tr.find_all('td')
        # add information from the row/variables to a list
        row = []
        if good_input(td[0].text):
            city = td[0].text.split(",")[0]
            state = td[0].text.split(",")[1]
        for i in td[1:]:
            if good_input(i.text):
                row.append(i.text)
        row.append(city)
        row.append(state)
        row.append(year)
        write = ""
        # Checks to see if row is valid
        if (row.__len__() is not 5) or (row[0].startswith("Name")):
            print("problem with row " + str(row))
        else:
            # move information from list to string:
            for i in row:
                # doesn't write a comma to the last entry in row
                if i and i is row[-1]:
                    write += "\"" + str(i) + "\""
                else:
                    write += "\"" + " ".join(str(i).split()) + "\"" + ","
            # write to exampleOutput.csv
            file.write(write + "\n")


def rows_finder(link):
    """
    takes a link, then finds the table rows and table information needed for that page
    :param link: a link to a specific states deans list
    :return: a string representing year and a list of all the table row elements from the deans list table
    """
    # collect information from the title of each link
    words = link.text.split(" ")
    if "" in words:
        words.remove("")
    year = words[-2] + " " + words[-1]
    # collect what state each link is for, or throw it away if it is not a dean's list link
    while "Dean" not in words[0]:
        words.pop(0)
    # build a link for each state, then navigate and create a bs object for it
    text_string = "https://www.ndsu.edu/" + link.get('href')
    url2 = urllib.request.urlopen(text_string)
    soup = bs.BeautifulSoup(url2, 'html.parser')
    # finds all the tables in the file and returns the last one,
    # which (for the NDSU page) is the table that holds the information we want
    table = soup.find_all('table')[-1]
    # checks to see if there is a table within a table
    table_rows = table.find_all('tr')
    rows_info = [year, table_rows]
    return rows_info
