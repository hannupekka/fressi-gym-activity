# Simple parser for Fressi gym activities

Fetches, parses and formats gym activity for [Fressi](http://www.fressi.fi/) gyms.

Requirements
------------
 * Fressi web reservation credentials for http://fressi.bypolar.fi/
 * python (created & tested with 2.6.6)
  * [BeautifulSoup 4](http://www.crummy.com/software/BeautifulSoup/)
  * [mechanize](http://wwwsearch.sourceforge.net/mechanize/)


Basic usage
-----------
Running ```python fressi.py -h``` gives you information about parameters:
```bash
Usage: fressi.py [options]

Options:
  -h, --help            show this help message and exit
  -u USERNAME, --username=USERNAME
                        username to log in with
  -p PASSWORD, --password=PASSWORD
                        password to go with username
  --csv                 format output to CSV
  --html                format output to HTML

  Duplicate entry fix:
    Polars system sometimes marks duplicates when checking in to gym

    -d, --duplicates    show multiple entries for same day
```

Examples
--------
1. Generating HTML page from all activities

  ```python fressi.py -u username -p password --html > index.html```
  
2. Getting the total count for all activities

  ```python fressi.py -u username -p password | wc -l```
    
3. Getting list of activies for autumn 2012 sorted ascending

  ```python fressi.py -u username -p password | grep -E '2012-(08|09|10)' | sort```
  
Troubleshooting
----------------
1. Can't login

  If your credentials contains for example scandinavic characters, login may fail if your terminal/connection character set is not UTF-8.

