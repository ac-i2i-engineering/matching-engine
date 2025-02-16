from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from matching_algo.clean_data import clean_and_create_users
from matching_algo.create_teams import form_teams
from matching_algo.models import UserProfile

import os

"""
    Handle file upload, process user data, and form teams.
    This function processes a CSV file uploaded via a POST request, saves it to the server,
    cleans and creates user profiles from the file, and then forms teams based on the user data.
    Once teams are created, they are displayed on the rendered web page. The uploaded file is
    deleted after processing to free up storage space.
    
    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing metadata and user-submitted form data.
    
    Returns
    -------
    HttpResponse
        A rendered HTML response displaying the formed teams.
"""

# Create your views here.
def index(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        file_path = fs.save(csv_file.name, csv_file)
        file_url = fs.url(file_path)
        
        # Assuming clean_and_create_users accepts a file path
        clean_and_create_users(file_path)
        
        # Now form teams after the users are created
        user_profiles = UserProfile.objects.all()
        teams = form_teams(user_profiles)
        
        # Print teams by user name
        print("\nGenerated Teams:")
        for i, team in enumerate(teams, 1):
            print(f"Team {i}:")
            for user in team:
                print(f"  - {user.name}")
            print()  # Add a blank line between teams for better readability
        
        # Collect the team information
        team_output = []
        for team in teams:
            team_output.append([user_profile.name for user_profile in team])
        
        # Clean up the uploaded file
        os.remove(file_path)
        
        return render(request, 'matching_algo/index.html', {'teams': team_output})

    return render(request, 'matching_algo/index.html')