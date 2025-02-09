# team_matching.py
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import logging
from datetime import datetime

@dataclass
class UserProfile:
    """Data class representing a user's profile with all relevant matching attributes."""
    user_id: str
    role: str  # 'engineer', 'finance', etc.
    interests: List[str]
    goals: List[str]
    skills: List[str]
    experience_level: int
    availability: Dict[str, List[str]]
    timezone: str
    preferred_team_size: Optional[int] = None

@dataclass
class Team:
    """Data class representing a formed team."""
    team_id: str
    members: List[UserProfile]
    compatibility_score: float
    skills_coverage: Dict[str, int]
    timezone_span: List[str]

class TeamMatchingEngine:
    """Main class for handling the team matching process."""
    
    def __init__(self, logging_level=logging.INFO):
        """Initialize the matching engine with logging configuration."""
        self.logger = self._setup_logging(logging_level)
        self.user_profiles = []
        self.teams = []

    def clean_and_create_users(self, csv_path: Path) -> pd.DataFrame:
        """
        Clean input CSV data and create standardized user data.
        
        Parameters
        ----------
        csv_path : Path
            Path to the input CSV file
            
        Returns
        -------
        pd.DataFrame
            Cleaned and standardized user data
        """
        self.logger.info(f"Processing CSV file: {csv_path}")
        
        df = pd.read_csv(csv_path)
        
        # Standardize column names
        df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]
        
        # Basic data cleaning
        df = df.dropna(subset=['user_id', 'role'])
        df = df.drop_duplicates(subset=['user_id'])
        
        # Standardize roles
        role_mapping = {
            'swe': 'engineer',
            'software engineer': 'engineer',
            'dev': 'engineer',
            'financial analyst': 'finance',
            'fin': 'finance'
        }
        df['role'] = df['role'].map(lambda x: role_mapping.get(x.lower(), x.lower()))
        
        self.logger.info(f"Processed {len(df)} valid user records")
        return df

    def create_user_profiles(self, df: pd.DataFrame) -> List[UserProfile]:
        """
        Create UserProfile instances from cleaned DataFrame.
        
        Parameters
        ----------
        df : pd.DataFrame
            Cleaned user data
            
        Returns
        -------
        List[UserProfile]
            List of created UserProfile instances
        """
        self.user_profiles = []
        
        for _, row in df.iterrows():
            profile = UserProfile(
                user_id=row['user_id'],
                role=row['role'],
                interests=self._parse_list_field(row.get('interests', '')),
                goals=self._parse_list_field(row.get('goals', '')),
                skills=self._parse_list_field(row.get('skills', '')),
                experience_level=int(row.get('experience_level', 0)),
                availability=self._parse_availability(row.get('availability', '')),
                timezone=row.get('timezone', 'UTC'),
                preferred_team_size=row.get('preferred_team_size')
            )
            self.user_profiles.append(profile)
        
        self.logger.info(f"Created {len(self.user_profiles)} user profiles")
        return self.user_profiles

    def calculate_final_scores(self, user1: UserProfile, user2: UserProfile) -> float:
        """
        Calculate the overall compatibility score between two users.
        
        Parameters
        ----------
        user1, user2 : UserProfile
            User profiles to compare
            
        Returns
        -------
        float
            Final compatibility score between 0 and 1
        """
        weights = {
            'cosine_similarity': 0.3,
            'interests_goals': 0.3,
            'timezone_compatibility': 0.2,
            'experience_balance': 0.2
        }
        
        scores = {
            'cosine_similarity': self.calculate_cosine_similarity(user1, user2),
            'interests_goals': self.calculate_interests_goals_scores(user1, user2),
            'timezone_compatibility': self._calculate_timezone_compatibility(user1, user2),
            'experience_balance': self._calculate_experience_balance(user1, user2)
        }
        
        final_score = sum(score * weights[key] for key, score in scores.items())
        return round(final_score, 2)

    def calculate_cosine_similarity(self, user1: UserProfile, user2: UserProfile) -> float:
        """Calculate skill-based cosine similarity between two users."""
        all_skills = list(set(user1.skills + user2.skills))
        
        # Create skill vectors
        vector1 = [1 if skill in user1.skills else 0 for skill in all_skills]
        vector2 = [1 if skill in user2.skills else 0 for skill in all_skills]
        
        # Calculate cosine similarity
        similarity = cosine_similarity([vector1], [vector2])[0][0]
        return round(float(similarity), 2)

    def calculate_interests_goals_scores(self, user1: UserProfile, user2: UserProfile) -> float:
        """Calculate compatibility based on shared interests and goals."""
        shared_interests = len(set(user1.interests) & set(user2.interests))
        shared_goals = len(set(user1.goals) & set(user2.goals))
        
        max_interests = max(len(user1.interests), len(user2.interests))
        max_goals = max(len(user1.goals), len(user2.goals))
        
        if max_interests == 0 and max_goals == 0:
            return 0.0
        
        interests_score = shared_interests / max_interests if max_interests > 0 else 0
        goals_score = shared_goals / max_goals if max_goals > 0 else 0
        
        return round((interests_score + goals_score) / 2, 2)

    def form_teams(self, team_size: int = 4) -> List[Team]:
        """
        Form optimal teams based on roles and compatibility scores.
        
        Parameters
        ----------
        team_size : int
            Desired size of each team
            
        Returns
        -------
        List[Team]
            List of formed teams
        """
        self.teams = []
        available_users = self.user_profiles.copy()
        
        while len(available_users) >= team_size:
            # Form initial team based on roles
            team_members = self._form_initial_team(available_users, team_size)
            
            if not team_members:
                break
                
            # Calculate team compatibility
            team = Team(
                team_id=f"team_{len(self.teams) + 1}",
                members=team_members,
                compatibility_score=self._calculate_team_compatibility(team_members),
                skills_coverage=self._calculate_skills_coverage(team_members),
                timezone_span=self._calculate_timezone_span(team_members)
            )
            
            self.teams.append(team)
            available_users = [u for u in available_users if u not in team_members]
        
        # Handle leftover users
        if available_users:
            self._handle_leftover_users(available_users)
        
        self.logger.info(f"Formed {len(self.teams)} teams")
        return self.teams

    def _form_initial_team(self, available_users: List[UserProfile], team_size: int) -> List[UserProfile]:
        """Form initial team ensuring role distribution."""
        engineers = [u for u in available_users if u.role == 'engineer']
        finance = [u for u in available_users if u.role == 'finance']
        
        if not engineers or not finance:
            return []
            
        # Start with best engineer-finance pair
        eng_fin_pairs = [
            (eng, fin, self.calculate_final_scores(eng, fin))
            for eng in engineers
            for fin in finance
        ]
        
        if not eng_fin_pairs:
            return []
            
        best_pair = max(eng_fin_pairs, key=lambda x: x[2])
        team = [best_pair[0], best_pair[1]]
        
        # Add remaining members based on compatibility
        remaining_users = [u for u in available_users if u not in team]
        while len(team) < team_size and remaining_users:
            best_next_member = max(
                remaining_users,
                key=lambda u: sum(self.calculate_final_scores(u, member) for member in team)
            )
            team.append(best_next_member)
            remaining_users.remove(best_next_member)
        
        return team

    def _handle_leftover_users(self, leftover_users: List[UserProfile]) -> None:
        """Handle users that couldn't be placed in complete teams."""
        if not leftover_users:
            return
            
        # Try to add to existing teams if they improve team compatibility
        for user in leftover_users[:]:
            best_team = max(
                self.teams,
                key=lambda t: self._calculate_team_compatibility(t.members + [user])
            )
            
            current_score = best_team.compatibility_score
            new_score = self._calculate_team_compatibility(best_team.members + [user])
            
            if new_score >= current_score:
                best_team.members.append(user)
                best_team.compatibility_score = new_score
                best_team.skills_coverage = self._calculate_skills_coverage(best_team.members)
                best_team.timezone_span = self._calculate_timezone_span(best_team.members)
                leftover_users.remove(user)
        
        # Create a new team with any remaining users
        if leftover_users:
            self.teams.append(Team(
                team_id=f"team_{len(self.teams) + 1}_partial",
                members=leftover_users,
                compatibility_score=self._calculate_team_compatibility(leftover_users),
                skills_coverage=self._calculate_skills_coverage(leftover_users),
                timezone_span=self._calculate_timezone_span(leftover_users)
            ))

    @staticmethod
    def _parse_list_field(field: str) -> List[str]:
        """Parse comma-separated string fields into lists."""
        if pd.isna(field) or not field:
            return []
        return [item.strip().lower() for item in str(field).split(',')]

    @staticmethod
    def _parse_availability(availability: str) -> Dict[str, List[str]]:
        """Parse availability string into structured format."""
        if pd.isna(availability) or not availability:
            return {}
        # Expected format: "Monday:9-17,Tuesday:10-18"
        availability_dict = {}
        pairs = availability.split(',')
        for pair in pairs:
            if ':' in pair:
                day, hours = pair.split(':')
                availability_dict[day.strip()] = hours.strip().split('-')
        return availability_dict

    @staticmethod
    def _setup_logging(level):
        """Setup logging configuration."""
        logger = logging.getLogger('TeamMatchingEngine')
        logger.setLevel(level)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def _calculate_team_compatibility(self, members: List[UserProfile]) -> float:
        """Calculate overall team compatibility score."""
        if len(members) < 2:
            return 0.0
            
        scores = []
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                scores.append(self.calculate_final_scores(members[i], members[j]))
        
        return round(sum(scores) / len(scores), 2)

    def _calculate_skills_coverage(self, members: List[UserProfile]) -> Dict[str, int]:
        """Calculate team's skill coverage."""
        skills_count = {}
        for member in members:
            for skill in member.skills:
                skills_count[skill] = skills_count.get(skill, 0) + 1
        return skills_count

    def _calculate_timezone_span(self, members: List[UserProfile]) -> List[str]:
        """Calculate team's timezone coverage."""
        return sorted(list(set(member.timezone for member in members)))

    def _calculate_timezone_compatibility(self, user1: UserProfile, user2: UserProfile) -> float:
        """Calculate timezone compatibility between two users."""
        if user1.timezone == user2.timezone:
            return 1.0
        # Simple timezone difference calculation
        try:
            tz1 = int(user1.timezone.replace('UTC', '').replace('+', ''))
            tz2 = int(user2.timezone.replace('UTC', '').replace('+', ''))
            diff = abs(tz1 - tz2)
            return max(0, 1 - (diff / 12))  # 12 hours max difference
        except ValueError:
            return 0.5  # Default score if timezone parsing fails

    def _calculate_experience_balance(self, user1: UserProfile, user2: UserProfile) -> float:
        """Calculate experience level compatibility."""
        diff = abs(user1.experience_level - user2.experience_level)
        max_diff = 5  # Assuming experience levels from 0-5
        return max(0, 1 - (diff / max_diff))