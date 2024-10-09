import streamlit as st
from news_fetcher import NewsFetcher
from user_profiles import UserProfile
from recommender import Recommender

st.markdown("""
    <style>
        .main {
            background-color: #F0F8FF; 
        }
        .sidebar .sidebar-content {
            background-color: #E0FFFF; 
        }
        .stButton>button {
            background-color:
            color: #FFFFFF;
        }
    </style>
""", unsafe_allow_html=True)

api_key = st.secrets["news_api"]["key"]
news_fetcher = NewsFetcher(api_key)
user_id = st.sidebar.text_input("Enter your user ID:", value="default_user")
user_profile = UserProfile(user_id)

st.sidebar.header("Update Preferences")
categories = st.sidebar.multiselect("Select Categories", ["Business", "Technology", "Sports", "Entertainment"])
sources = st.sidebar.multiselect("Select Sources", ["bbc-news", "cnn", "techcrunch", "the-verge"])
topics = st.sidebar.text_area("Enter Topics of Interest (comma-separated)").split(",")

if st.sidebar.button("Save Preferences"):
    user_profile.update_preferences(categories=categories, sources=sources, topics=topics)

st.markdown("<h1 style='text-align: center;'>Your World, Your News</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align: center;'>Welcome, {user_id}!</h2>", unsafe_allow_html=True)
st.write("<div style='height: 50px;'></div>", unsafe_allow_html=True)  

# Fetch and display news
if st.button("Get Your News"):
    try:
        preferences = user_profile.get_preferences()
        articles = news_fetcher.fetch_and_summarize(query=",".join(preferences['topics']), sources=preferences['sources'])
        recommender = Recommender(user_profile)
        recommended_articles = recommender.recommend(articles)

        for article in recommended_articles:
            st.header(article['title'])
            st.write(article['summary'])
    except Exception as e:
        st.error(f"An error occurred: {e}")