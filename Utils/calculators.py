import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

def convert_date_pt(date):
    treated_date = '01-' + '-'.join(date.lower().split(' '))
    return datetime.strptime(treated_date, '%d-%B-%Y')