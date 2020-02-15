import bs4 as bs
import urllib.request
import Utility
import GUI

if __name__ == "__main__":
    # Create window, prompt user for links, ConnString
    values = GUI.get_window()
    # sets up database
    print(values[1])
    Utility.setup(values[1][0])
    # reduced list due to large csv file
    try:
        for link in values[1][1].split(" "):
            # creates a BS object for each Semester's landing page
            url = urllib.request.urlopen(link)
            soup = bs.BeautifulSoup(url, 'html.parser')
            # Find all links on the page
            links = soup.find_all('a')
            for x in links:
                try:
                    # collects table rows and other information about table
                    rows_info = Utility.rows_finder(x)
                    # collect information from each row in the table
                    # then writes it to a database
                    Utility.row_handler(rows_info[1], rows_info[0], values[1][0])
                except IndexError:
                    # do nothing, throw away bad link
                    print(end="")
    except IndexError and ValueError:
        # do nothing, throw away bad link
        print(end="")
