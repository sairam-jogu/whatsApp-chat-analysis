
from urlextract import URLExtract
from wordcloud import WordCloud

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



