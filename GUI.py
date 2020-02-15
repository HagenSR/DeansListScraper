from builtins import list

import PySimpleGUI as gui

listLandingPage = ['https://www.ndsu.edu/news/studentnews/deanslistfall2019/',
                   'https://www.ndsu.edu/news/studentnews/deanslistspring2019/',
                   'https://www.ndsu.edu/news/studentnews/deanslistfall2018/',
                   'https://www.ndsu.edu/news/studentnews/deanslistspring2018/',
                   'https://www.ndsu.edu/news/studentnews/deanslistfall2017/',
                   'https://www.ndsu.edu/news/studentnews/deanslistspring2017/',
                   'https://www.ndsu.edu/news/studentnews/deanslistfall2016/',
                   'https://www.ndsu.edu/news/studentnews/deanslistspring2016/',
                   'https://www.ndsu.edu/news/studentnews/deanslistfall2015/',
                   'https://www.ndsu.edu/news/studentnews/deanslistspring2015/',
                   'https://www.ndsu.edu/news/studentnews/deanslistfall2014/',
                   'https://www.ndsu.edu/news/studentnews/deanslistspring2014/',
                   'https://www.ndsu.edu/news/studentnews/deanslistfall2013/',
                   'https://www.ndsu.edu/news/studentnews/deanslistspring2013/',
                   'https://www.ndsu.edu/news/studentnews/deanslistfall2012/',
                   'https://www.ndsu.edu/news/studentnews/deanslistspring2012/']


def get_window():
    """
    Creates a window that prompts the user to enter a Connection string, Update Link List
    :return: a tuple where index [1][0] contains the connection string and [1][1] contains the
    list of links to be traversed
    """
    layout = [
        [gui.Text('Please enter a database connection string, and modify the landing pages if valid')],
        [gui.Text('Database Connection String', size=(20, 1)),
         gui.InputText('dbname=deanslist user=postgres password=yourPassword', size=(55, 1))],
        [gui.Text('URL landing Pages', size=(20, 1)), gui.Multiline(listLandingPage, size=(55, 20))],
        [gui.Text("(Please wait until window disappears)")],
        [gui.Submit(), gui.Cancel()]
    ]

    window = gui.Window('Dean\'s List Scraper').Layout(layout)
    values = window.Read()
    return values
