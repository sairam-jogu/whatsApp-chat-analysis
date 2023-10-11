
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import re

extract = URLExtract()
def fetch_details(selected_user, df):
    if selected_user != "Overall Analysis":
        df = df[df['users'] == selected_user]
    media_count = df[df['messages'] == '<Media omitted>\n'].shape[0]
    messages = []
    for message in df['messages']:
        messages.extend(message.split())
    wordCount = len(messages)
    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))
    return df.shape[0], media_count, wordCount, len(links)

def fetch_busy_users(df):
    names = df['users'].value_counts().head()
    df2 = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'users': 'percent'})
    return names,df2

def fetch_word_cloud(selected_user,df):
    if selected_user != "Overall Analysis":
        df = df[df['users'] == selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc

def fetch_most_common_words(selected_user,df):
    f = open("stopWords.txt",'r')
    stop_words = f.read()

    if selected_user != "Overall Analysis":
        df = df[df['users'] == selected_user]
    temp = df[df['users'] != "Message"]
    temp = temp[temp['messages'] != "<Media Omitted>\n"]
    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    data = pd.DataFrame(Counter(words).most_common(20))
    return data

def fetch_most_frequent_emojis(selected_user,df):
    if selected_user != 'Overall Analysis':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis_in_message = re.findall(r':(?:[^:\s]+):', emoji.demojize(message))
        emojis.extend(emojis_in_message)
    actual_emojis = [emoji.emojize(emoji_text) for emoji_text in emojis]
    emoji_df = pd.DataFrame(Counter(actual_emojis).most_common(len(Counter(actual_emojis))))
    return emoji_df

def fetch_monthly_data(selected_user,df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def fetch_dates_data(selected_user,df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def fetch_week_data(selected_user,df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def fetch_month_data(selected_user,df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def fetch_activity(selected_user,df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    weekely_activity = df.pivot_table(index='day_name', columns="timing", values='messages',
                                      aggfunc='count').fillna(0)
    return weekely_activity