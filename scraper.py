# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
import sqlite3
from bs4 import BeautifulSoup
import requests

def get_html(url):
    r = requests.get(url)
    return r.text


def main():
    url = 'https://ciu.nstu.ru/student/time_table_view?idgroup=31173&fk_timetable=37954'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    div = soup.find('em').text.strip()

    d = div.split('  ')[0].split('Сегодня ')[1]
    w = div.split('Идет ')[1]
    
    conn = sqlite3.connect("data.sqlite")
    cursor = conn.cursor()
    
    cursor.execute("""DROP TABLE week""")
    cursor.execute("""CREATE TABLE weeks (week text, date text)""")
    data = [(w, d,)]
    sql = "DELETE FROM weeks WHERE week != ''"
    cursor.execute(sql)
    conn.commit()
    
    cursor.execute("INSERT INTO weeks (week, date) VALUES (?, ?)", data[0])
    conn.commit()
    
    sql = "SELECT * FROM weeks"
    cursor.execute(sql)
    print(cursor.fetchall())

if __name__ == '__main__':
    main()
