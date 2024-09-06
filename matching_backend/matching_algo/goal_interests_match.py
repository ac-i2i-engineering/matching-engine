from matching_algo.models import UserProfile

def calculate_interests_goals_scores(interest_weight=5.0):
    user_profiles = UserProfile.objects.all()

    # Define 2D matrix for all possible pairs of user profiles
    similarity_scores = [[0 for _ in range(len(user_profiles))] for _ in range(len(user_profiles))]

    # Total number of interest and goal attributes
    total_interests = 7  # Number of interest fields
    total_goals = 5  # Number of goal fields

    # Calculate scores for each pair of user profiles
    for i in range(len(user_profiles)):
        for j in range(len(user_profiles)):
            if i != j:
                # Get user profiles
                user1 = user_profiles[i]
                user2 = user_profiles[j]

                # Calculate interest similarity
                matching_interests = (
                    (user1.interest_arts == user2.interest_arts) +
                    (user1.interest_education == user2.interest_education) +
                    (user1.interest_finance == user2.interest_finance) +
                    (user1.interest_healthcare == user2.interest_healthcare) +
                    (user1.interest_sustainability == user2.interest_sustainability) +
                    (user1.interest_social_impact == user2.interest_social_impact) +
                    (user1.interest_technology == user2.interest_technology)
                )
                interest_score = float(matching_interests / total_interests)

                # Calculate goal similarity
                matching_goals = (
                    (user1.goal_learn == user2.goal_learn) +
                    (user1.goal_relations == user2.goal_relations) +
                    (user1.goal_idea == user2.goal_idea) +
                    (user1.goal_problems == user2.goal_problems) +
                    (user1.goal_win_support == user2.goal_win_support)
                )
                goal_score = float(matching_goals / total_goals)

                # Combine scores with interest_weight applied to interest score
                similarity_score = goal_score + (interest_weight * interest_score)
                similarity_scores[i][j] = similarity_score

                # Debug information
                print(f"User {i} and User {j} - Similarity Score: {similarity_score}")

    return similarity_scores