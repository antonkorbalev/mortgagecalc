import dateutil.relativedelta as du
import math
import datetime as d


def get_percents_payment_per_period(debt_sum, rate, days_count, days_in_year):
    return (debt_sum * rate * days_count / (100 * days_in_year))


def get_total_payment(debt, num_months, rate):
    rate = rate / 100 / 12
    pow = math.pow(1 + rate, num_months)
    return debt * rate * pow / (pow - 1)


def get_days_in_year(year):
    d1 = d.datetime(year, 1, 1)
    d2 = d.datetime(year + 1, 1, 1)
    return (d2 - d1).days


def calculate_percents(date, new_date, credit_value, rate):
    if new_date.month == 1:
        dy1 = get_days_in_year(new_date.year)
        p1 = get_percents_payment_per_period(credit_value,
                                             rate,
                                             (new_date - d.date(new_date.year, 1, 1)).days,
                                             dy1)
        dy2 = get_days_in_year(new_date.year - 1)
        p2 = get_percents_payment_per_period(credit_value,
                                             rate,
                                             (d.date(new_date.year, 1, 1) - date).days,
                                             dy2)
        percents = p1 + p2
    else:
        percents = get_percents_payment_per_period(credit_value,
                                                   rate,
                                                   (new_date - date).days,
                                                   get_days_in_year(new_date.year))
    if percents <= 0:
        percents = 0

    return percents


def calculate_mortgage(date_start,
                       cost,
                       percent_payment,
                       rate,
                       num_months,
                       decrease_time_payments,
                       decrease_sum_payments):
    initial_payment = cost * percent_payment / 100
    credit_value = cost - initial_payment
    date = date_start - du.relativedelta(months=1)
    data = list()
    data.append(['№', 'Date', ' Total payed', 'Total payment', 'Percents', 'Debt', 'Add payment', 'Rest'])
    total_payment = get_total_payment(credit_value, num_months, rate)
    num = 0
    total_payed = 0

    while credit_value > 0:
        new_date = date + du.relativedelta(months=1)
        percents = calculate_percents(date, new_date, credit_value, rate)
        add = 0
        if num in decrease_time_payments:
            add = add + decrease_time_payments[num]
        if num in decrease_sum_payments:
            add = add + decrease_sum_payments[num]
        if credit_value < total_payment:
            total_payment = credit_value
            credit_value = 0
        else:
            credit_value = credit_value - (total_payment - percents) - add
        total_payed += total_payment + add
        data.append([num, new_date, round(total_payed, 2), round(total_payment, 2), round(percents, 2), round(total_payment - percents, 2), add, round(credit_value, 2)]);
        if num in decrease_sum_payments:
            total_payment = get_total_payment(credit_value, num_months - num - 1, rate)
        num = num + 1
        date = new_date

    return data, num, total_payed
