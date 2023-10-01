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
                pie_fig = pie_df.plot(kind='pie')


            # prompt = st.chat_input("Ask about the plots you required")
            # if prompt:
            #     with st.chat_message("user"):
            #         st.write("Hello")
            #         st.bar_chart(data=df,x=names,y=count)

