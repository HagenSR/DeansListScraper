import bs4 as bs
import urllib.request
import psycopg2
import re


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
    b = b.strip()
    b = re.sub("Dean", "", b)
    b = re.sub("List", "", b)
    b = re.sub("[']", " ", b)
    b = re.sub("^[a-zA-Z ]", "", b)
    b = re.sub("  *", " ", b)
    b = re.sub("^Minn$", "Minnesota", b)
    b = re.sub("^ND$", "North Dakota", b)
    b = re.sub("^SD$", "South Dakota", b)
    b = re.sub("^Wis$", "Wisconsin", b)
    b = re.sub("^Mont$", "Montana", b)
    return b


def setup(connectionString):
    conn = psycopg2.connect(connectionString)
    cursor = conn.cursor()
    try:
        # Try to drop tables if they exist
        cursor.execute("DROP TABLE semester")
        cursor.execute("DROP TABLE student")
    except psycopg2.errors.UndefinedTable:
        # if tables didn't exist, refresh connection
        cursor.close()
        conn.close()
        conn = psycopg2.connect(connectionString)
        cursor = conn.cursor()
    cursor.execute("CREATE TABLE student(name varchar(60),major varchar(60),city varchar(60),state varchar(60),"
                   "id int GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),UNIQUE(name, major, city),"
                   "PRIMARY KEY(id));")
    cursor.execute("CREATE TABLE semester(id int,semester varchar(30) ,foreign key(id) REFERENCES student(id));")
    cursor.close()
    conn.commit()
    print("Clean")


def row_handler(table_rows, year, file):
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
    conn = psycopg2.connect(file)
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
        if (studentList.__len__() is not 4) or (studentList[0].startswith("Name")):
            print("problem with row " + str(studentList))
        else:
            # move information from list to string:
            try:
                cursor.execute("INSERT INTO student VALUES (%s,%s,%s,%s)", tuple(studentList))
            except psycopg2.errors.InFailedSqlTransaction and psycopg2.errors.UniqueViolation:
                conn = psycopg2.connect(file)
                cursor = conn.cursor()
                # Student was already in database, get Student ID
            cursor.execute('SELECT id FROM student WHERE name = \'' + studentList[0] + "\'")
            id = cursor.fetchone()
            year_list.insert(0, id)
            cursor.execute("INSERT INTO semester VALUES (%s,%s)", tuple(year_list))
            conn.commit()


def rows_finder(link):
    """
    takes a link, then finds the table rows and table information needed for that page
    :param link: a link to a specific states deans list
    :return: a string representing year and a list of all the table row elements from the deans list table
    """
    # collect information from the title of each link
    words = link.text.split(" ")
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
    soup.prettify()
    # checks to see if there is a table within a table
    table_rows = table.find_all('tr')
    rows_info = [year, table_rows]
    return rows_info
