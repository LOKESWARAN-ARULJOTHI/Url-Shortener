# Url-Shortener
THis is url shortener

Link to the project https://shrtyurl.herokuapp.com/
This project is an url shortener app
It is build by using flask as backend and SQLAlchemy for db
It will shorten your link and generate a 7 character short link



1M / day
length - 7 chars

Data capacity model:

*long url - 2 kb (2048 chars)
*short url -  17 b (17 chars)
*created at - 7 b (epoc time)
*expire at - 7 bytes

total ===== 2.031 kb

30M/month -> 60.7GB/month -> 0.7TB/Year -> 3.6TB/ 5years

* MD5 hash - i/p - string = length of 25
	* prob - lot of collisions

* Base 62 -i/p - int = 62^7(7chars) = 3.5Trillion combinations
	a-z - 26
	A-Z - 26
	1-9 - 10
if we get 1000 post/sec we  can generate for 110 years

-in base 10 - only 10M combinations(10^7)

NoSQL is better for consistency, availability, scalability

Use COUNTERS
single point failure if we use only one counter
so use multiple counters

Use zoo keeper service from apache foundation to maintain the coordination of counters
