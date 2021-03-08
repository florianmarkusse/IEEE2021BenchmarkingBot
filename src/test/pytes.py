import datetime



string = "2020-10-22T20:03:04"
date_time_obj  = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')

print('Date:', date_time_obj.date())

new_start_date = "created>={date}".format(date=date_time_obj.date())

print(new_start_date)

print("found {current_date}".format(current_date=datetime.datetime.now().strftime("%Y-%m-%d")))