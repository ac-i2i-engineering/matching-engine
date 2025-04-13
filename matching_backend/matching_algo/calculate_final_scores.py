from matching_algo.cosine_similarity import calculate_cosine_similarity
from matching_algo.goal_interests_match import calculate_interests_goals_scores
from matching_algo.models import UserProfile


def calculate_final_scores(user_profiles):

    """
    Calculate combined similarity scores between user profiles based on multiple metrics.
    This function computes similarity scores between all pairs of user profiles by combining
    matching similarities (based on interests and goals) with cosine similarities. The final
    score for each pair is the sum of their matching and cosine similarity scores.

    Parameters
    ----------
    user_profiles : list
        A list of user profile objects containing information about users'
        interests, goals, and other relevant attributes for matching.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - final_scores : list of list of float
            A 2D matrix where element [i][j] represents the combined similarity
            score between user_profiles[i] and user_profiles[j].
        - user_profiles : list
            The original list of user profile objects, unchanged.
"""
    
    final_scores = [[0 for _ in range(len(user_profiles))] for _ in range(len(user_profiles))]
    
    # Calculate matching similarity scores
    print("calculating matching similarities")
    matching_similarities = calculate_interests_goals_scores(user_profiles)
    
    # calculatie cosine similarity scores
    print("calculating cosine similarities")
    cosine_similarities = calculate_cosine_similarity(user_profiles)
    
    # combine matching similarities with cosine similarities
    for i in range(len(cosine_similarities)):
        for j in range(len(cosine_similarities[i])):
            final_scores[i][j] = cosine_similarities[i][j] + matching_similarities[i][j]
    
    return final_scores, user_profiles

