class Recommender:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def recommend(self, articles):
        preferences = self.user_profile.get_preferences()
        recommended_articles = []

        for article in articles:
            if any(topic in article['title'] for topic in preferences['topics']):
                recommended_articles.append(article)

        return recommended_articles
