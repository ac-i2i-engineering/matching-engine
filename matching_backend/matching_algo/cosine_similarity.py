# Importing necessary libraries
import pandas as pd
from matching_algo.models import UserProfile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

"""
Calculate cosine similarities between pairs of user profiles.

This function computes pairwise cosine similarity scores between all user profiles
in the provided list. It uses TF-IDF vectorization to convert text-based profile
data into numerical vectors before calculating similarities.

Parameters
----------
user_profiles : list
    A list of user profile objects, where each object contains attributes for
    majors, additional information, and project ideas.

Returns
-------
list of list of float
    A 2D matrix where element [i][j] contains the cosine similarity score
    between user_profiles[i] and user_profiles[j]. Diagonal elements are 0
    since self-comparisons are skipped.

Notes
-----
The function processes three main components of each user profile:
    - majors: Academic majors or fields of study
    - add_info: Additional information about the user
    - idea: Project or collaboration ideas

The similarity calculation uses TF-IDF vectorization to account for the
importance of terms within the context of all profiles being compared.
"""
def calculate_cosine_similarity(user_profiles):  
    # load users from db
    
    cosine_similarities = [[0 for _ in range(len(user_profiles))] for _ in range(len(user_profiles))]

    # iterate over ever user pair
    for i, user1 in enumerate(user_profiles):
        for j, user2 in enumerate(user_profiles):
            if i != j:
                # extract user data
                user1_majors = user1.majors
                user2_majors = user2.majors
                
                user1_addInfo = user1.add_info
                user2_addInfo = user2.add_info
                
                user1_idea = user1.idea
                user2_idea = user2.idea
                
                # format profiles for users
                user1_profile = {
                    'majors': user1_majors,
                    'addInfo': user1_addInfo,
                    'idea': user1_idea,
                }
                
                user2_profile = {
                    'majors': user2_majors,
                    'addInfo': user2_addInfo,
                    'idea': user2_idea,
                }
                
                # initialize vectorizer
                vectorizer = TfidfVectorizer()
                
                # fit and transform the user data
                tfidf_matrix = vectorizer.fit_transform([str(user1_profile), str(user2_profile)])  # Transform the texts into TF-IDF matrix
                cosine_similarities[i][j] = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] # Return the cosine similarity score
    
    return cosine_similarities