# DeansListScraper
Python code that scrapes deans list information from multiple semesters and states from the NDSU website. The HTML tables provided by NDSU are hard to search and impossible to sort. This PostgreSQL database creator enters the information into two tables, Student and Semester, allowing you to search using SQL querries

TO USE
1. Update landing page links if applicable in the main.py class
2. download PostgreSQL, set up a user and enter the Command "CREATE TABLE deanslist;"
3. update the connString in main.py to match your username and password (if applicable, update port information which is set to default)
4. Run the program
5. Enter Queries!

A common query might be "SELECT * FROM student NATURAL JOIN semester WHERE name LIKE 'Sean%Hagen';" which would return all the semesters that Sean Hagen made the dean's list


