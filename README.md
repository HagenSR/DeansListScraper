# DeansListScraper
Python code that scrapes deans list information from multiple semesters and states from the NDSU website. The HTML tables provided by NDSU are hard to search and impossible to sort. This CSV file creator allows you to open entire semesters or even years in excel, where you can sort by name, major, year or hometown.


select distinct semester from semester where semester like '%List%' or semester like '%dean%'

select * from student join semester on student.rowid = id AND name like 'Sean% Hagen';