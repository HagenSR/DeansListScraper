import bs4 as bs
import urllib.request
import re
import sqlite3
import time


def good_input(b):
    if b and (not b.isspace()):
        return True
    return False


def fix_input(b):
    """
    Removes unwanted Characters, Replaces Abbreviation of State with Full name
    :param b: A string to be cleaned
    :return: A cleaned string
    """
    b = re.sub("Dean's List", "", b)
    b = re.sub("Dean's", "", b)
    b = re.sub("List", "", b)
    b = re.sub("'", " ", b)
    b = re.sub("  *", " ", b)
    b = re.sub("\xa0$", "", b)
    b = re.sub("[.]", "", b)
    b = re.sub("^ Minn$", "Minnesota", b)
    b = re.sub("^ ND$", "North Dakota", b)
    b = re.sub("^ SD$", "South Dakota", b)
    b = re.sub("^ Wis$", "Wisconsin", b)
    b = re.sub("^ Mont$", "Montana", b)
    return b.strip()


def csv_row_handler(table_rows, year, file):
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
                row.append(fix_input(i.text))
        row.append(fix_input(city))
        row.append(fix_input(state))
        row.append(fix_input(year))
        write = ""
        # Checks to see if row is valid
        if (row.__len__() != 5) or (row[0].startswith("Name")):
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


def sql_handler(table_rows, year, conn):
    '''
    pulls information out of each row, throwing it away if it doesn't have enough entries to be valid
    (Name, Major, Year, city, location)
    :param table_rows: a collection of rows containing deans list information
    :param year: a year and semester for a given table
    :param file: a database to write to
    :return: nothing, this method writes directly to a csv file
    '''
    city = ""
    state = ""
    cursor = conn.cursor()
    for tr in table_rows:
        td = tr.find_all('td')
        # add information from the row/variables to a list
        studentList = []
        year_list = []
        if good_input(td[0].text):
            city = fix_input(td[0].text.split(",")[0])
            state = fix_input(td[0].text.split(",")[1])
        for i in td[1:]:
            if good_input(i.text):
                studentList.append(fix_input(str(i.text)))
        studentList.append(fix_input(str(city)))
        studentList.append(fix_input(str(state)))
        year_list.append(fix_input(str(year)))

        write = ""
        # Checks to see if row is valid
        if (studentList.__len__() != 4) or (studentList[0].startswith("Name")):
            print("problem with row " + str(studentList))
        else:
            # move information from list to string:
            try:
                st = str.format(
                    "INSERT INTO student VALUES ('{0}','{1}','{2}','{3}')", *tuple(studentList))
                cursor.execute(st)
                conn.commit()
            except Exception as e:
                cursor = conn.cursor()
                # print(e)
                # Student was already in database, get Student ID
            try:
                strn = str.format(
                    "SELECT ROWID FROM student WHERE name = '{0}'", studentList[0])
                cursor.execute(strn)
                id = cursor.fetchone()
                year_list.insert(0, id[0])
                cursor.execute(str.format(
                    "INSERT INTO semester VALUES ({0},'{1}')", *tuple(year_list)))
            except Exception as e:
                x = 1
                # print(e)
            conn.commit()


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


def createTable(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "CREATE TABLE student(name varchar(60),major varchar(60),city varchar(60),state varchar(60), UNIQUE(name, city, state));")
        cursor.execute(
            "CREATE TABLE semester(id int,semester varchar(30) ,UNIQUE(id, semester), foreign key(id) REFERENCES student(ROWID));")
    except Exception as e:
        print(e)
    cursor.close()
    conn.commit()
