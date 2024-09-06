import pandas as pd
import re
from sklearn.preprocessing import MultiLabelBinarizer
from matching_algo.models import UserProfile

# Define the expected columns
expected_columns = [
    'Timestamp', 'Email Address', 'Full Name', 'Class Year', 'Major', 'Additional Major 1', 
    'Additional Major 2', 'Domains of Interest', 'Do you have an idea big or small?', 
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
    """Load CSV file."""
    pd.set_option('display.max_columns', None)
    df = pd.read_csv(file_path)
    print(df)
    return df

def check_columns(df, expected_columns):
    """Check if all expected columns are present in the CSV."""
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in the CSV: {missing_columns}")

def clean_text(text):
    """Clean text fields."""
    if pd.isna(text):
        return ''
    text = text.strip().lower()  # Remove whitespace and convert to lowercase
    text = re.sub(r'\s*,\s*', ', ', text)  # Ensure consistent spacing
    return text

def apply_cleaning(df):
    """Apply cleaning to the relevant columns."""
    df['Domains of Interest'] = df['Domains of Interest'].apply(clean_text)
    df['What are your goals for the Lab?'] = df['What are your goals for the Lab?'].apply(clean_text)
    df['What role are you interested in taking on a team?'] = df['What role are you interested in taking on a team?'].apply(clean_text)

def split_and_match(df):
    """Split and match against standard categories."""
    df['Domains of Interest'] = df['Domains of Interest'].apply(lambda x: [domain for domain in domains_of_interest if domain in x])
    df['What are your goals for the Lab?'] = df['What are your goals for the Lab?'].apply(lambda x: [goal for goal in goals_for_lab if goal in x])
    df['What role are you interested in taking on a team?'] = df['What role are you interested in taking on a team?'].apply(lambda x: [role for role in roles_interested if role in x])

def create_binary_features(df):
    """Convert lists into binary encoded columns using MultiLabelBinarizer."""
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
    """Concatenate the original dataframe with the binary encoded features and drop original text columns."""
    df_profiles = pd.concat([df, df_domains, df_goals, df_roles], axis=1)
    df_profiles.drop(['Domains of Interest', 'What are your goals for the Lab?', 'What role are you interested in taking on a team?'], axis=1, inplace=True)
    return df_profiles

def filter_responses(df_profiles):
    """Filter to only include responses where 'Do you already have a team?' is 'No – match me with a team'."""
    return df_profiles[df_profiles['Do you already have a team?'] == 'No – match me with a team']

def create_user_profiles(df_filtered):
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
    print(df_filtered.head())