import requests
from bs4 import BeautifulSoup
from time import sleep
import sys

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


def check(url, query, start=0):
    has_found = False

    try:
        position = 0
        google_url = "http://www.google.com/search?q=" + query.replace(' ', '+') + "&start=" + str(start * 10) \
                     + '&num=10&pws=0'
        print("Checking on page# " + str(start + 1))

        r = requests.get(google_url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, 'lxml')
        results = soup.select('h3 > a')
        for idx, entry in enumerate(results):
            if url in entry['href'].strip():
                has_found = True
                position = idx + 1

        if not has_found:
            return [None, start + 1]
        else:
            return [position, start + 1]

    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error. Technical Details given below.\n")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error. Technical Details given below.\n")
        print(str(e))


args = sys.argv
if len(args) != 3:
    print("Invalid syntax. The correct syntax is: python " + args[
        0] + ' <keyword> <url>. If keyword is a multi word then enclose in double quotes')
else:
    last_page = 20
    for i in range(last_page):
        position, page_number = check(args[2], args[1], i)
        if position is not None:
            print("Found at position " + str(position) + ' on page# ' + str(page_number))
            break
        sleep(5)
        print(position, page_number)
