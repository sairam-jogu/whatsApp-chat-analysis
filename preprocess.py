import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [date.strip(' -') for date in dates]
    date_format = '%d/%m/%y, %I:%M %p'
    df = pd.DataFrame({'messages': messages, "dates": dates})
    df['dates'] = pd.to_datetime(df['dates'], format=date_format)
    users = []
    msgs = []

    for message in df['messages']:
        splitting = re.split(':\s', message, maxsplit=1)

        if len(splitting) == 2:
            username, message_text = splitting
            users.append(username)
            msgs.append(message_text)
        else:
            users.append('Message')
            msgs.append(message)

    df['users'] = users
    df['messages'] = msgs
    df['year'] = df['dates'].dt.year
    df['month_num'] = df['dates'].dt.month
    df['only_date'] = df['dates'].dt.date
    df['month'] = df['dates'].dt.month_name()
    # df.drop(['year'], axis=1)
    df['day'] = df['dates'].dt.day
    df['day_name'] = df['dates'].dt.day_name()
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute

    timings = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            timings.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            timings.append(str('00') + "-" + str(hour + 1))
        else:
            timings.append(str(hour) + "-" + str(hour + 1))
    df['timing'] = timings
    return df

