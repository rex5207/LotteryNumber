from selenium import webdriver
from lunisolar import ChineseDate
from bs4 import BeautifulSoup
import time
import re
import urllib2

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def strip_int(input):
    return re.sub("\D", "", input)


if __name__ == "__main__":
    # driver = webdriver.Chrome("./chromedriver")

    years = range(2004, 2018)
    # moon_landing = ChineseDate.from_gregorian(2017, 6, 19)
    # print moon_landing.month, moon_landing.day
    lottery_years = []
    lottery_month = []
    lottery_day = []
    lottery_number = []

    for year in years:
        url = 'http://www.nfd.com.tw/lottery/49-year/49-f' + str(year) + '.htm'
        # driver.get(url)
        # time.sleep(3)
        # soup = BeautifulSoup(driver.page_source, "html.parser")
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        lty_year = soup.find_all('tr')
        for day in lty_year[1:]:
            content = day.find_all('td')
            lottery_years.append(strip_int(content[0].text))
            date = strip_int(strip_int(content[1].text))
            lottery_month.append(date[:2])
            lottery_day.append(date[2:])
            winner = []
            winner.append(strip_int(content[3].text))
            winner.append(strip_int(content[4].text))
            winner.append(strip_int(content[5].text))
            winner.append(strip_int(content[6].text))
            winner.append(strip_int(content[7].text))
            winner.append(strip_int(content[8].text))
            winner.append(strip_int(content[9].text))
            lottery_number.append(winner)

    f = open("lottery_numbers", 'w')
    for i in range(len(lottery_years)):
        f.write(lottery_years[i] + ' ')
        f.write(lottery_month[i] + ' ')
        f.write(lottery_day[i] + ' ')
        f.writelines(' '.join(lottery_number[i]))
        f.write('\n')
    f.close
