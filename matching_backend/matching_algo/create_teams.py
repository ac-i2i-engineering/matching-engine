from matching_algo.calculate_final_scores import calculate_final_scores
from matching_algo.models import UserProfile
from django.core.management import call_command

user_profiles = UserProfile.objects.all()

def form_teams(user_profiles):
    """
    Form teams based on user profiles and their roles.
    
    This function takes a list of user profiles and groups them into teams based
    on their roles (business, engineering, finance) while ensuring balanced team
    composition. It first calculates final scores for each user and then
    organizes them into appropriate teams.

    Parameters
    ----------
    user_profiles : list of UserProfile
        A list of user profile objects containing information about each user,
        including their roles (role_business, role_engineer, role_finance) and
        other relevant attributes needed for team formation.

    Returns
    -------
    list of list
        A list of teams, where each team is a list of user indices representing
        the members of that team.

    Notes
    -----
    The function uses the following process:
    1. Calculates final scores for all users
    2. Separates users by their roles (business, engineering, finance)
    3. Tracks used users to prevent duplicate assignments
    
    Examples
    --------
    >>> profiles = [UserProfile(role_business=True), UserProfile(role_engineer=True)]
    >>> teams = form_teams(profiles)
    >>> print(teams)
    [[0, 1]]  # Example output showing indices of team members
    """
    print("calculating final scores")
    final_scores, user_profiles = calculate_final_scores(user_profiles)
    teams = []
    used_users = set()

    print("generating teams")

    # Create role-specific user lists
    # Parameters
    # ----------
    # user_profiles : list of UserProfile
    #     The complete list of user profiles to be filtered
    # used_users : set of int
    #     Set of indices of already assigned users
    # Returns
    # -------
    # list of int
    # List of indices of users matching each role criteria


    """
    Forms balanced teams by matching business users with compatible engineers and finance professionals.
    
    This function creates teams by first selecting a business user, then finding the most
    compatible engineer and finance professional based on compatibility scores. Each user
    can only be assigned to one team.

    Parameters
    ----------
    user_profiles : list of UserProfile
        List of user profile objects containing role information and other relevant
        attributes for each user. Each profile must have boolean flags:
        role_business, role_engineer, and role_finance.
    final_scores : list of list of float
        A 2D matrix of compatibility scores between users. Higher scores indicate
        better compatibility. Shape should be (n_users, n_users).

    Returns
    -------
    list of list
        A list where each inner list represents a team containing indices of team
        members. Each team typically has 3 members: business, engineer, and finance.

    Examples
    --------
    >>> profiles = [
    ...     UserProfile(role_business=True),
    ...     UserProfile(role_engineer=True),
    ...     UserProfile(role_finance=True)
    ... ]
    >>> scores = [[0, 0.8, 0.6],
    ...          [0.8, 0, 0.7],
    ...          [0.6, 0.7, 0]]
    >>> teams = form_teams(profiles, scores)
    >>> print(teams)
    [[0, 1, 2]]  # Team with business(0), engineer(1), and finance(2) members

    """

    # Get lists of users by role
    business_users = [i for i, user in enumerate(user_profiles) if user.role_business and i not in used_users]
    engineer_users = [i for i, user in enumerate(user_profiles) if user.role_engineer and i not in used_users]
    finance_users = [i for i, user in enumerate(user_profiles) if user.role_finance and i not in used_users]

    # Form initial teams
    for business_user in business_users:
        if business_user in used_users:
            continue

        team = [business_user]
        used_users.add(business_user)

        # Find best matching engineer
        if engineer_users:
            best_engineer = max(engineer_users, key=lambda x: final_scores[business_user][x])
            team.append(best_engineer)
            used_users.add(best_engineer)
            engineer_users.remove(best_engineer)

        # Find best matching finance person
        if finance_users:
            best_finance = max(finance_users, key=lambda x: final_scores[business_user][x])
            team.append(best_finance)
            used_users.add(best_finance)
            finance_users.remove(best_finance)

        teams.append(team)

    """
    Process remaining users who haven't been assigned to teams and organize them
    into balanced teams.

    Parameters
    ----------
    user_profiles : list of UserProfile
        The complete list of user profiles available for team formation.
        Each profile contains user information and role assignments.
    used_users : set of int
        A set containing indices of users who have already been assigned to teams.
        Used to track which users still need team assignment.
    teams : list of list
        The existing teams, where each inner list contains indices of team members.
        Will be modified to include new teams formed from leftover users.

    Returns
    -------
    list of list
        Updated list of teams including both original teams and new teams formed
        from leftover users. Each inner list contains user indices representing
        team members.

    Examples
    --------
    >>> user_profiles = [UserProfile() for _ in range(5)]
    >>> used_users = {0, 1}
    >>> teams = [[0, 1]]
    >>> teams = handle_leftover_users(user_profiles, used_users, teams)
    >>> print(teams)
    [[0, 1], [2, 3, 4]]  # Original team plus new team from leftover users
    """

    # Handle leftover users
    leftover_users = [i for i in range(len(user_profiles)) if i not in used_users]

    # Create teams of 3 from leftover users
    while len(leftover_users) >= 3:
        new_team = leftover_users[:3]
        teams.append(new_team)
        leftover_users = leftover_users[3:]

    # Handle remaining users
    if leftover_users:
        if len(leftover_users) == 1:
            # If only one user is left, add them to the last team
            teams[-1].append(leftover_users[0])
        else:  # len(leftover_users) == 2
            # If two users are left, create a new team
            teams.append(leftover_users)

    # Ensure all teams have at least 2 members
    single_member_teams = [team for team in teams if len(team) == 1]
    multi_member_teams = [team for team in teams if len(team) > 1]

    """
    Balances team sizes and finalizes team formation by combining single-member teams
    and converting user indices to UserProfile objects.

    Parameters
    ----------
    single_member_teams : list of list
        A list of teams containing only one member each. Each inner list contains
        a single integer representing the user index.
    multi_member_teams : list of list
        A list of teams with multiple members. Each inner list contains integers
        representing user indices.
    user_profiles : list of UserProfile
        A list of UserProfile objects corresponding to the indices used in the teams.

    Returns
    -------
    list of list
        A list of balanced teams, where each inner list contains UserProfile objects
        instead of indices. Teams are typically of size 2-3 members.

    Examples
    --------
    >>> single_teams = [[1], [4]]
    >>> multi_teams = [[2, 3]]
    >>> profiles = [UserProfile() for _ in range(5)]
    >>> final_teams = balance_and_finalize_teams(single_teams, multi_teams, profiles)
    >>> print(len(final_teams[0]))  # Shows team size
    3
    """



    while single_member_teams:
        if len(single_member_teams) >= 2:
            # Combine two single-member teams
            new_team = single_member_teams.pop(0) + single_member_teams.pop(0)
            multi_member_teams.append(new_team)
        else:
            # Add the last single member to a team of 2 if possible, otherwise to a team of 3
            single_member = single_member_teams.pop(0)[0]
            two_member_teams = [team for team in multi_member_teams if len(team) == 2]
            if two_member_teams:
                two_member_teams[0].append(single_member)
            else:
                multi_member_teams[0].append(single_member)

    teams = multi_member_teams

    print("teams generated")

    # Flush database
    try:
        call_command('flush', interactive=False)
        print('Database flushed')
    except Exception as e:
        print('Error flushing database')
        print(e)

    # Convert user indices to UserProfile objects
    final_teams = [[user_profiles[i] for i in team] for team in teams]

    return final_teams