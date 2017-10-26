#!/usr/bin/env python3

import psycopg2

db = psycopg2.connect(database="news")
c = db.cursor()

c.execute('''SELECT title, count(log.*) AS views
             FROM articles, log
             WHERE path = '/article/' || slug
             GROUP BY title
             ORDER BY views DESC
             LIMIT 3;''')
results1 = (c.fetchall())
print('{:-^50}'.format('3 most popular articles of all time'))
for title, views in results1:
    print('{:35}{:>9} views'.format(title, str(views)))
print('\n')


c.execute('''SELECT name, count(log.*) AS views
             FROM log, articles, authors
             WHERE authors.id = author
                 AND path = '/article/' || slug
                 AND status = '200 OK'
             GROUP BY name
             ORDER BY views DESC;''')
results2 = c.fetchall()
print('{:-^50}'.format('Most popular authors'))
for name, views in results2:
    print('{:35}{:>9} views'.format(name, str(views)))
print('\n')


c.execute('''SELECT DISTINCT breq.time::DATE, (cast(nofind AS FLOAT) / allreq)
             FROM breq, daytotalrequests
             WHERE breq.time::DATE = daytotalrequests.time::DATE
                 AND (cast(nofind AS FLOAT) / allreq) > 0.01;''')
results3 = c.fetchall()
print('{:-^50}'.format('Days with more than 1% errors'))
for date, failpercent in results3:
    print('{:%Y-%m-%d} {:>33.3%} error'.format(date, failpercent))

db.close()
