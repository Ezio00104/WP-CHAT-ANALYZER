import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall", )
    selected_user = st.sidebar.selectbox("Show analysis with respect to ", user_list)
    if st.sidebar.button("Show analysis"):

        #stats area
        num_messages,words,num_media_messages,num_links= helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total messages: ")
            st.title(num_messages)
        with col2:
            st.header("Total Words: ")
            st.title(words)
        with col3:
            st.header("Media Shared: ")
            st.title(num_media_messages)
        with col4:
            st.header("links shared:")
            st.title(num_links)

        #finding the busisest user in group
        if selected_user == 'Overall':
            st.title('Most busy users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 =st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #WordCloud
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1],color='grey')
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        #emojis

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

