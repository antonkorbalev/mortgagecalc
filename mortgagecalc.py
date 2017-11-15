import datetime as d
from modules.mortgagelib import calculate_mortgage
import terminaltables

# mortgage start date
date_start = d.date(2017, 11, 3)
# total price
total_price = 8128000
# % of initial payment
initial_percent = 15
# interest rate
ir = 9.4
# total monts of mortgage
total_months = 240
# payments to decrease time
# ex: {4 : 100000 } pay on 4th month 100000 to decrease time
time_payments = {}
# payments to decrease sum
# ex: {4 : 100000 } pay on 4th month 100000 to decrease sum
sum_payments = {}

data, months_total, total_payed = calculate_mortgage(
    date_start,
    total_price,
    initial_percent,
    ir,
    total_months,
    time_payments,
    sum_payments)

data_table = terminaltables.GithubFlavoredMarkdownTable(data)
data_table.title = 'Calculation'
print(data_table.table)