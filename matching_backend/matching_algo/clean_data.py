import pandas as pd
import re
from sklearn.preprocessing import MultiLabelBinarizer
from matching_algo.models import UserProfile

# Define the expected columns
expected_columns = [
    'Timestamp', 'Email Address', 'Full Name', 'Class Year', 'Major', 'Additional Major 1', 
    'Additional Major 2', 'Domains of Interest', 'Do you have an idea (big or small)?',
    'What is your idea?', 'What stage are you at?', 'What role are you interested in taking on a team?',
    'What are your goals for the Lab?', 'Provide any additional information about yourself.',
    'Do you already have a team?', 'Has your team been registered?',
    'If your team has not registered enter your email below and we will send you the form.'
]

# Define the standard categories
domains_of_interest = ['arts', 'education', 'finance', 'healthcare', 'sustainability', 'social impact', 'technology']
goals_for_lab = ['learn about entrepreneurship and startups', 'build relationships', 'test my current idea', 'solve world problems', 'win i2i\'s support']
roles_interested = ['business strategy', 'engineering', 'financial']

def load_csv(file_path):
    """
    Load and configure display settings for a CSV file.
    
    This function reads a CSV file using pandas and configures the display 
    settings to show all columns in the dataframe.
    
    Parameters
    ----------
    file_path : str
        The path to the CSV file to be loaded.
        
    Returns
    -------
    pandas.DataFrame
        A pandas DataFrame containing the contents of the CSV file.
    """
    """Load CSV file."""
    pd.set_option('display.max_columns', None)
    df = pd.read_csv(file_path)
    return df

def check_columns(df, expected_columns):
    """
    Verify that all required columns are present in the DataFrame.
    
    This function checks whether all expected columns exist in the provided 
    DataFrame and raises an error if any are missing.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to check for expected columns.
    expected_columns : list of str
        A list of column names that should be present in the DataFrame.
        
    Raises
    ------
    ValueError
        If any expected columns are missing from the DataFrame, with a message 
        listing the missing columns.
    """
    """Check if all expected columns are present in the CSV."""
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in the CSV: {missing_columns}")

def clean_text(text):
    """Clean and standardize text input by removing whitespace, converting to lowercase,
    and ensuring consistent spacing around commas.
    
    Parameters
    ----------
    text : str or pd.NA
        The input text to be cleaned. Can be either a string or pandas NA value.
    
    Returns
    -------
    str
        The cleaned and standardized text string. Returns an empty string if input
        is pd.NA.
    """
    """Clean text fields."""
    if pd.isna(text):
        return ''
    text = text.strip().lower()  # Remove whitespace and convert to lowercase
    text = re.sub(r'\s*,\s*', ', ', text)  # Ensure consistent spacing
    return text

def apply_cleaning(df):
    """Apply text cleaning operations to specific columns in the dataframe.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe containing the columns to be cleaned:
        'Domains of Interest', 'What are your goals for the Lab?',
        and 'What role are you interested in taking on a team?'
    
    Returns
    -------
    None
        The function modifies the dataframe in place.
    """
    """Apply cleaning to the relevant columns."""
    df['Domains of Interest'] = df['Domains of Interest'].apply(clean_text)
    df['What are your goals for the Lab?'] = df['What are your goals for the Lab?'].apply(clean_text)
    df['What role are you interested in taking on a team?'] = df['What role are you interested in taking on a team?'].apply(clean_text)

def split_and_match(df):
    """Match text in specified columns against standard categories and convert
    to lists of matching categories.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe containing the columns to be processed:
        'Domains of Interest', 'What are your goals for the Lab?',
        and 'What role are you interested in taking on a team?'
    
    Returns
    -------
    None
        The function modifies the dataframe in place, converting text in specified
        columns to lists of matching standard categories from predefined lists
        (domains_of_interest, goals_for_lab, roles_interested).
    """
    """Split and match against standard categories."""
    df['Domains of Interest'] = df['Domains of Interest'].apply(lambda x: [domain for domain in domains_of_interest if domain in x])
    df['What are your goals for the Lab?'] = df['What are your goals for the Lab?'].apply(lambda x: [goal for goal in goals_for_lab if goal in x])
    df['What role are you interested in taking on a team?'] = df['What role are you interested in taking on a team?'].apply(lambda x: [role for role in roles_interested if role in x])

def create_binary_features(df):
    """Convert lists into binary encoded columns using MultiLabelBinarizer."""
    """
    Convert categorical list columns into binary encoded features using MultiLabelBinarizer.
    
    This function takes a DataFrame containing list-based categorical columns and 
    converts them into binary encoded features using scikit-learn's MultiLabelBinarizer.
    It processes three specific columns: 'Domains of Interest', goals, and roles.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing the categorical list columns to be encoded
        
    Returns
    -------
    tuple of pandas.DataFrame
        A tuple containing three DataFrames:
        - Binary encoded features for Domains of Interest
        - Binary encoded features for Goals
        - Binary encoded features for Roles
    """
    # Create binary features for Domains of Interest
    mlb_domains = MultiLabelBinarizer(classes=domains_of_interest)
    df_domains = pd.DataFrame(mlb_domains.fit_transform(df['Domains of Interest']), columns=mlb_domains.classes_, index=df.index)
    
    # Create binary features for Goals
    mlb_goals = MultiLabelBinarizer(classes=goals_for_lab)
    df_goals = pd.DataFrame(mlb_goals.fit_transform(df['What are your goals for the Lab?']), columns=mlb_goals.classes_, index=df.index)
    
    # Create binary features for Roles
    mlb_roles = MultiLabelBinarizer(classes=roles_interested)
    df_roles = pd.DataFrame(mlb_roles.fit_transform(df['What role are you interested in taking on a team?']), columns=mlb_roles.classes_, index=df.index)
    
    return df_domains, df_goals, df_roles

def concatenate_and_drop(df, df_domains, df_goals, df_roles):
    """
    Combine original DataFrame with binary encoded features and remove original text columns.
    
    This function concatenates the original DataFrame with the binary encoded feature 
    DataFrames and removes the original text columns that were used to create the 
    binary features.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Original DataFrame containing the text columns
    df_domains : pandas.DataFrame
        Binary encoded features for Domains of Interest
    df_goals : pandas.DataFrame
        Binary encoded features for Goals
    df_roles : pandas.DataFrame
        Binary encoded features for Roles
        
    Returns
    -------
    pandas.DataFrame
        A combined DataFrame with binary encoded features and original text columns removed
    """

    """Concatenate the original dataframe with the binary encoded features and drop original text columns."""
    df_profiles = pd.concat([df, df_domains, df_goals, df_roles], axis=1)
    df_profiles.drop(['Domains of Interest', 'What are your goals for the Lab?', 'What role are you interested in taking on a team?'], axis=1, inplace=True)
    return df_profiles

def filter_responses(df_profiles):
    """
    Filter DataFrame to include only unmatched team responses.
    
    This function filters the DataFrame to only include rows where the 
    'Do you already have a team?' column has the value 'No – match me with a team',
    effectively selecting only those participants who need team matching.
    
    Parameters
    ----------
    df_profiles : pandas.DataFrame
        Input DataFrame containing participant profiles and team status
        
    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame containing only unmatched participants
    """
    """Filter to only include responses where 'Do you already have a team?' is 'No – match me with a team'."""
    return df_profiles[df_profiles['Do you already have a team?'] == 'No – match me with a team']

def create_user_profiles(df_filtered):
    """
    Create UserProfile instances from a filtered DataFrame containing user information.
    
    This function iterates through each row of the filtered DataFrame and creates
    UserProfile instances with various attributes including personal information,
    interests, goals, and roles. Each profile is saved to the database.
    
    Parameters
    ----------
    df_filtered : pandas.DataFrame
        A filtered DataFrame containing user information with columns for personal
        details, interests, goals, and roles. Expected columns include 'Full Name',
        'Major', 'Additional Major 1', 'Additional Major 2', and various binary
        interest/goal/role indicators.
        
    Returns
    -------
    None
        The function saves UserProfile instances to the database but doesn't
        return any values.
    """
    """Create UserProfile instances from the filtered dataframe."""
    for index, row in df_filtered.iterrows():
        user_profile = UserProfile(
            name=row['Full Name'],
            majors=f"{row['Major']}, {row['Additional Major 1']}, {row['Additional Major 2']}".strip(', '),
            interest_arts=row['arts'],
            interest_education=row['education'],
            interest_finance=row['finance'],
            interest_healthcare=row['healthcare'],
            interest_sustainability=row['sustainability'],
            interest_social_impact=row['social impact'],
            interest_technology=row['technology'],
            goal_learn=row['learn about entrepreneurship and startups'],
            goal_relations=row['build relationships'],
            goal_idea=row['test my current idea'],
            goal_problems=row['solve world problems'],
            goal_win_support=row['win i2i\'s support'],
            role_business=row['business strategy'],
            role_engineer=row['engineering'],
            role_finance=row['financial'],
            add_info=row['Provide any additional information about yourself.'],
            idea=row['What is your idea?']
        )
        user_profile.save()

def clean_and_create_users(file_path):
    """
    Process a CSV file containing user data and create UserProfile instances.
    
    This function serves as the main pipeline for processing user data. It loads
    the CSV file, performs various cleaning and transformation operations, and
    ultimately creates UserProfile instances. The processing steps include column
    validation, data cleaning, feature creation, and filtering.
    
    Parameters
    ----------
    file_path : str
        The path to the CSV file containing the user data. The file should
        contain all required columns as specified in the expected_columns
        variable.
    
    Returns
    -------
    None
        The function processes the data and creates UserProfile instances but
        doesn't return any values. It also sets pandas display option to show
        all columns.
    
    Notes
    -----
    The function performs the following steps:
    1. Loads the CSV file
    2. Validates the presence of required columns
    3. Cleans the data
    4. Splits and matches relevant fields
    5. Creates binary features for domains, goals, and roles
    6. Concatenates and processes the final DataFrame
    7. Filters responses
    8. Creates UserProfile instances
    """
    """Main function to process the CSV file and create UserProfile instances."""
    df = load_csv(file_path)
    check_columns(df, expected_columns)
    apply_cleaning(df)
    split_and_match(df)
    df_domains, df_goals, df_roles = create_binary_features(df)
    df_profiles = concatenate_and_drop(df, df_domains, df_goals, df_roles)
    df_filtered = filter_responses(df_profiles)
    
    # Create UserProfile instances
    create_user_profiles(df_filtered)
    
    # Print the filtered and processed dataframe
    pd.set_option('display.max_columns', None)