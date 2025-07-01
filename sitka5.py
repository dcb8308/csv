import csv  
import datetime as dt

infile = open('sitka_weather_07-2018_simple.csv', 'r')

csv_file = csv.reader(infile)

header_row = next(csv_file)

print(header_row)

for index, col_header in enumerate(header_row):
    if col_header == 'TMIN':
        TMIN_index = index
    elif col_header == 'TMAX':
        TMAX_index = index
    elif col_header == 'NAME':
        NAME_index = index
    elif col_header == 'DATE':
        DATE_index = index



highs  = []
dates = []
lows = []

some_date = dt.datetime.strptime('2018-07-01', '%Y-%m-%d')
print(type(some_date))


for row in csv_file:
    try:
        if row[TMAX_index] == '' or row[TMIN_index] == '':
            raise ValueError("Missing TMAX or TMIN")
        some_date = dt.datetime.strptime(row[DATE_index], '%Y-%m-%d')
        high = int(row[TMAX_index])
        low = int(row[TMIN_index])
    except ValueError:
        print(f"Missing data for {row}")
    else:
        highs.append(high)
        lows.append(low)
        dates.append(some_date)

    


print(highs[:5])
print(dates[:5])

import matplotlib.pyplot as plt

fig = plt.figure()



plt.plot(dates, highs, c='red', alpha=0.5)
plt.plot(dates, lows, c='blue', alpha=0.5)

plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)


plt.title("Daily low and high temperatures - 2018", fontsize=16)
plt.xlabel('Dates', fontsize=16)
plt.ylabel('Temperature (F)', fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)

fig.autofmt_xdate()

plt.show()

plt.subplot(2,1,1)
plt.plot(dates, highs, c='red')
plt.title("highs")

plt.subplot(2,1,2)
plt.plot(dates, lows, c='blue')
plt.title("lows")

plt.suptitle('daily highs and lows for Sitka, Alaska')

plt.show()






