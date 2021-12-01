from datetime import datetime

from aviasales_holidays.aviasales_prise import Prise


def main(year: int = datetime.now().year,
         month: int = datetime.now().month,
         day: int = datetime.now().day,
         delta: int = 7):

    for days in range(7):
        new_day = day - days
        if new_day >= 1:
            response = Prise(year, month, new_day, delta)
            response.get_prise()
    for days in range(7):
        new_day = day + days
        if new_day <= 31:
            response = Prise(year, month, new_day, delta)
            response.get_prise()

if __name__ == '__main__':
    main(2022, 2, 10)
