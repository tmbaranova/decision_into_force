import requests
from bs4 import BeautifulSoup
import datetime

dict_month = {
    'Январь': 0,
    'Февраль': 31,
    'Март': 59,
    'Апрель': 90,
    'Май': 120,
    'Июнь': 151,
    'Июль': 181,
    'Август': 212,
    'Сентябрь': 243,
    'Октябрь': 273,
    'Ноябрь': 304,
    'Декабрь': 334,
}


def get_year(data):
    date_string = datetime.datetime.strptime(data, '%Y-%m-%d')
    year = date_string.year
    return year


def get_url(year):
    url = (f'http://www.consultant.ru/law/ref/calendar/proizvodstvennye/'
           f'{year}/#shortday')
    return url


def get_html(url):
    """Функция, получающая html со страницы с календарем"""

    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    }
    request = requests.get(url, headers=HEADERS)
    return request.text


def get_content(html):
    """Парсер календаря"""
    soup = BeautifulSoup(html, 'html.parser')
    all_months = soup.find_all('div', class_="col-md-3")
    weekends_dict = {}

    for month in all_months:
        try:
            weekends_in_month = list()
            month_name = month.find('th', colspan='7', class_='month').get_text()
            weekends = month.find('tbody')
            hol = weekends.find_all('td', class_='weekend')
            for weekend in hol:
                weekend = weekend.get_text()
                weekends_in_month.append(weekend)
            weekends_dict.update({month_name: weekends_in_month})
        except Exception:
            continue
    return weekends_dict


def dict_update(weekends_dict):
    """Функция перевода словаря с выходными в список
    с номерами выходных дней, считая от начала года"""
    lst_weekends = []
    for i in weekends_dict:
        for j in weekends_dict[i]:
            a = int(dict_month[i])+int(j)
            lst_weekends.append(a)
    return lst_weekends


def data_vstupl(data, lst_weeks):
    """Функиця расчета даты вступления решения в силу
    по дате решения и списку выходных и праздничных дней"""
    dat = datetime.datetime.strptime(data, '%Y-%m-%d')
    d = int(dat.strftime("%j"))
    year = int(dat.year)
    days_in_year = 365
    if year in [2012, 2016, 2020, 2024, 2028, 2032]:
        days_in_year = 366
    counter = 0
    while counter <= 15:
        d += 1
        if d > days_in_year:
            """СЮДА ПАРСИНГ СЛЕДУЮЩЕГО ГОДА"""
            d = d % 365
            year += 1
            url = get_url(year)
            html = get_html(url)
            content = get_content(html)
            lst_weeks = dict_update(content)

        if d not in lst_weeks:
            counter += 1
    d = str(d)
    d = f'{datetime.datetime.strptime(d,"%j").strftime("%d.%m")}.{year}'
    return d


def convert_value(decision_date):
    year = get_year(decision_date)
    url = get_url(year)
    html = get_html(url)
    content = get_content(html)
    dict = dict_update(content)
    a = (data_vstupl(decision_date, dict))
    return a




