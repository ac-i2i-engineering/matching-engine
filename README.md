# Matching Engine
This is the matching engine we are building to match students with each other &amp; ideas!

To clone the app, run in terminal:

```bash
git clone https://github.com/ac-i2i-engineering/matching-engine.git
cd matching-engine
```

Set-up a virtual environment and activate it to "containerize" the dependencies:

```bash
python3 -m venv env
source env/bin/activate
```

To run the app locally, run:

```bash
pip install -r requirements.txt
cd matching_backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
# System Architecture

```mermaid
graph TD
    A[Upload CSV File] -->|CSV File| B[clean_and_create_users]
    B --> J[standardize and create_user_profiles]
    
    J --> |CSV FileUserProfile Instances Created| L[form_teams]
    
    L --> M[calculate_final_scores from user_profiles]
    M --> N[calculate_cosine_similarity from user_profiles]
    M --> O[calculate_interests_goals_scores from user_profiles]
    
    L --> P[Form Initial Teams based on roles]
    P --> Q[Match Best Engineer and Finance based on scores]
    Q --> R[Handle Leftover Users & Create Final Teams]
    R --> |Team Data| U[Render Teams in HTML]
```

# CI/CD Testing & Deployment Pipeline

We use modularized `pytest-django`-based unit-tests and `GitHub Actions` to test our backend ("business") logic in an end-to-end CI/CD environment. We also run custom regression-tests and deployment/integration-tests through a combination of technologies like [Railway](https://railway.app/), [Vercel](https://vercel.com/) & `npm`. This is to have health-checks on the system & give our developers extensive experience in technologies that they most-likely will encounter in industry settings.

![image](https://github.com/user-attachments/assets/d51e5950-e859-4f95-bec9-98fb41eb450e)
![image](https://github.com/user-attachments/assets/abe2b142-8e5a-4bde-80d3-e5f5c4c7bfae)


# Demo & screenshots: (Last updated 10th Sept, 2024)

- **Youtube Demo link:** https://youtu.be/oAPVXGaYS8Q

![image](https://github.com/user-attachments/assets/5c34a4ef-7936-437b-8c41-4898a0dfefbb)
![image](https://github.com/user-attachments/assets/50fcefee-292e-432b-85e0-248cb8e123d4)
