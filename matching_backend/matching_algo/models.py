from django.db import models



class UserProfile(models.Model):

    """
    Represents a user profile with personal details, interests, goals, and roles.
    This model stores user-related information, including name, academic interests,
    professional goals, and preferred roles in projects. It also provides fields
    for additional user input.
    
    Attributes
    ----------
    name : CharField
        The full name of the user. Defaults to 'Dhyey Mavani'.
    majors : CharField
        A string containing all the user's academic majors.
    
    Interest Fields
    ---------------
    interest_arts : BooleanField
        Indicates if the user is interested in arts-related fields.
    interest_education : BooleanField
        Indicates if the user is interested in education-related fields.
    interest_finance : BooleanField
        Indicates if the user is interested in finance-related fields.
    interest_healthcare : BooleanField
        Indicates if the user is interested in healthcare-related fields.
    interest_sustainability : BooleanField
        Indicates if the user is interested in sustainability-related fields.
    interest_social_impact : BooleanField
        Indicates if the user is interested in social impact-related fields.
    interest_technology : BooleanField
        Indicates if the user is interested in technology-related fields.
    
    Goal Fields
    -----------
    goal_learn : BooleanField
        Specifies if the user aims to learn new skills.
    goal_relations : BooleanField
        Specifies if the user aims to build professional relationships.
    goal_idea : BooleanField
        Specifies if the user aims to develop new ideas.
    goal_problems : BooleanField
        Specifies if the user aims to tackle complex problems.
    goal_win_support : BooleanField
        Specifies if the user aims to gain support for a project or initiative.
    
    Role Fields
    -----------
    role_business : BooleanField
        Indicates if the user is interested in business-related roles.
    role_engineer : BooleanField
        Indicates if the user is interested in engineering-related roles.
    role_finance : BooleanField
        Indicates if the user is interested in finance-related roles.
    
    Additional Information
    ----------------------
    add_info : TextField
        Optional field for users to provide extra details about themselves.
    idea : TextField
        Optional field for users to share innovative ideas or concepts.
    
    Methods
    -------
    __str__()
        Returns the user's name as the string representation of the object.
"""
    # Add name field
    name = models.CharField(max_length=255, default='Dhyey Mavani')
    
    # Combine all majors into one string
    majors = models.CharField(max_length=255)
    
    # Domains of Interest
    interest_arts = models.BooleanField(default=False)
    interest_education = models.BooleanField(default=False)
    interest_finance = models.BooleanField(default=False)
    interest_healthcare = models.BooleanField(default=False)
    interest_sustainability = models.BooleanField(default=False)
    interest_social_impact = models.BooleanField(default=False)
    interest_technology = models.BooleanField(default=False)
    
    # Goals for the Lab
    goal_learn = models.BooleanField(default=False)
    goal_relations = models.BooleanField(default=False)
    goal_idea = models.BooleanField(default=False)
    goal_problems = models.BooleanField(default=False)
    goal_win_support = models.BooleanField(default=False)
    
    # Roles interested in
    role_business = models.BooleanField(default=False)
    role_engineer = models.BooleanField(default=False)
    role_finance = models.BooleanField(default=False)
    
    # Additional information
    add_info = models.TextField(blank=True, null=True)
    idea = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name