import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import fetchData
import preprocess

st.sidebar.title("Whatsapp -analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)
    st.header("Analyze your Chat !!",divider='rainbow')
    # st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)
    code1 ='''
        #to convert into python Date Format 
        date_format = '%d/%m/%y, %I:%M %p 
        # 04/11/21, 10:26pm ------> 2021-11-04 22:24:00
        df['dates'] = pd.to_datetime(df['dates'], format=date_format)'''
    st.code(code1,language='python')

    st.dataframe(df)

    user_list = df['users'].unique().tolist()
    user_list.remove('Message')
    user_list.sort()
    user_list.insert(0, "Overall Analysis")
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show analysis"):
        count, media_count, wordCount, links_count= fetchData.fetch_details(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(count)
        with col2:
            st.header("Media Shared")
            st.title(media_count)
        with col3:
            st.header("Words Count")
            st.title(wordCount)
        with col4:
            st.header("Links Shared")
            st.title(links_count)

        if selected_user == 'Overall Analysis':
            st.header("Most Busiest Users",divider='rainbow')
            code2 = '''
                    #Fetching Busy Users 
                    def fetch_busy_users(df):
                        names = df['users'].value_counts().head()
                        return names
                    '''
            st.code(code2,language='python')
            x,pie_df = fetchData.fetch_busy_users(df)
            names = x.index
            count = x.values
            col1,col2 = st.columns(2)

            with col1:
                busy = sns.barplot(data=df, x=names, y=count)
                plt.xticks(rotation="vertical")
                # plt.figure(figsize=(7,10))
                busy.set_title("Top 5 Busiest Persons in the group")
                busy.set_xlabel("User Names")
                busy.set_ylabel("Messages Count")
                st.pyplot(busy.get_figure())
            with col2:
                # palette_color = sns.color_palette('bright')
                # pie_chart = plt.pie(pie_df.head()['count'], labels=pie_df.head()['percent'], colors=palette_color, autopct='%0f%%', )
                # st.pyplot(pie_chart.get_figure())
                st.dataframe(pie_df)
            # prompt = st.chat_input("Ask about the plots you required")
            # if prompt:
            #     with st.chat_message("user"):
            #         st.write("Hello")
            #         st.bar_chart(data=df,x=names,y=count)




        st.header("Most Frequent Words", divider='rainbow')
        st.code('''
                    from wordcloud import WordCloud
                    def fetch_word_cloud(selected_user,df):
                        if selected_user != "Overall Analysis":
                            df = df[df['users'] == selected_user]

                        wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
                        df_wc = wc.generate(df['messages'].str.cat(sep=" "))
                        return df_wc
                ''')
        df_wc = fetchData.fetch_word_cloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)

        st.pyplot(fig)

        st.header("Most Frequent Words",divider="rainbow")
        df_fw = fetchData.fetch_most_common_words(selected_user,df)
        # st.dataframe(df_fw)
        fig,ax = plt.subplots()
        sns.barplot(data=df_fw,x=df_fw[1],y=df_fw[0],orient='h')
        plt.xlabel("Count")
        plt.ylabel("Words")
        st.pyplot(fig)


        st.header("Most Frequent Emojis",divider="rainbow")
        df_emoji = fetchData.fetch_most_frequent_emojis(selected_user,df)
        # st.dataframe(df_emoji)
        st.code('''
                import re
                import emoji
                from collections import Counter
                def fetch_most_frequent_emojis():
                    emojis = []
                    for message in df['messages']:
                        emojis_in_message = re.findall(r':(?:[^:\s]+):', emoji.demojize(message))
                        emojis.extend(emojis_in_message)
                    actual_emojis = [emoji.emojize(emoji_text) for emoji_text in emojis]
                    emoji_df = pd.DataFrame(Counter(actual_emojis).most_common(len(Counter(actual_emojis))))
                    return emoji_df
                ''')
        col1,col2 = st.columns(2)
        with col1:
            fig,ax2 = plt.subplots()
            # sns.set_palette("Set3")
            ax2.pie(df_emoji.head()[1],labels=df_emoji.head()[0],autopct='%1.1f%%',startangle=90)
            ax2.axis('equal')
            st.pyplot(fig)
        with col2:
            fig,ax3 = plt.subplots()
            sns.barplot(data=df_emoji,x=df_emoji.head()[0],y=df_emoji.head()[1])
            st.pyplot(fig)


