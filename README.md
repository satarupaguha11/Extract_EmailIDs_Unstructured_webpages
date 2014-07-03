Extract_EmailIDs_Unstructured_webpages
======================================

Requirements
------------
This has been tested on Python 2.7.
The libaries used are BeautifulSoup 4, re, urllib and urllib2.

How to compile and run code
---------------------------
One needs to open the file in a Python Editor and then run the file code.py.
The location where the results.txt file has to be stored in the machine, must be changed in the code.py file


Results.txt file
----------------
The results.txt file has 2000 lines, 1 line per business. Every line contains the following values separated by tabs: business id, business name, business phone number, business home page URL, contact-us URL for the business, email id for the business.

Heuristics
-----------
The Python library Beautiful Soup has been used to find tags in each of the given yelp pages and the business home pages. Using the regular expressions, we match the different variations of the word 'Contact' in the home page tags. The Python Regular Expressions library re has been used for this purpose. When they match, we take the corresponding href value as the contact-us page url. If it is a relative link, we append the home page url with this link. Now from the contact-us page, we use the regular expression '\w+@\w+\.\w+' to find the email id from the tags on the page. This regular expression finds those instances which contain a '@' and a '.' following and following by any alphanumeric character.



