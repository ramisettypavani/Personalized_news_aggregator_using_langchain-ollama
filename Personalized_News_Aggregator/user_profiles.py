import json
import os

class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.profile_path = f'profiles/{self.user_id}.json'
        self.ensure_directory()
        self.load_profile()

    def ensure_directory(self):
        directory = os.path.dirname(self.profile_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def load_profile(self):
        if (os.path.exists(self.profile_path)):
            with open(self.profile_path, 'r') as file:
                self.profile = json.load(file)
        else:
            self.profile = {
                'preferences': {
                    'categories': [],
                    'sources': [],
                    'topics': []
                },
                
            }

    def save_profile(self):
        try:
            with open(self.profile_path, 'w') as file:
                json.dump(self.profile, file, indent=4)
        except IOError as e:
            print(f"An error occurred while saving the profile: {e}")

    def update_preferences(self, categories=None, sources=None, topics=None):
        if categories:
            self.profile['preferences']['categories'] = categories
        if sources:
            self.profile['preferences']['sources'] = sources
        if topics:
            self.profile['preferences']['topics'] = topics
        self.save_profile()

    def get_preferences(self):
        return self.profile['preferences']