import bs4 as bs
import urllib.request
import Utility

if __name__ == "__main__":
    # NDSU likes to hide the deans lists, so you need to manually find the landing page for each semester
    listLandingPage = ['https://www.ndsu.edu/news/studentnews/deanslistspring2019/'
        ,'https://www.ndsu.edu/news/studentnews/deanslistfall2018/'
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
    f = open("exampleOutput.csv", "w")
    # reduced list due to large csv file
    for link in listLandingPage[:3]:
        # creates a BS object for each Semester's landing page
        url = urllib.request.urlopen(link)
        soup = bs.BeautifulSoup(url, 'html.parser')
        # Find all links on the page
        links = soup.find_all('a')
        for x in links:
            try:
                # collects table rows and other information about table
                rows_info = Utility.rows_handler(x)
                # collect information from each row in the table
                Utility.row_handler(rows_info[1], rows_info[0], f)
            except IndexError:
                print(end="")
                # do nothing, throw away bad link