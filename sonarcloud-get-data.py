#!/usr/bin/python3

import requests
import json
import sys
import os
from datetime import datetime

SONARCLOUD_URL = 'https://sonarcloud.io'

def get_project_measures(project_key, token):
    """
    Fetches a comprehensive set of measures for the specified project from SonarCloud.
    """
    url = f"{SONARCLOUD_URL}/api/measures/component"
    headers = {"Authorization": f"Bearer {token}"}
    metric_keys = [
        'ncloc', 'complexity', 'violations', 'bugs', 'vulnerabilities',
        'code_smells', 'coverage', 'duplicated_lines_density', 'sqale_index',
        'reliability_rating', 'security_rating', 'sqale_rating', 'security_hotspots'
    ]
    params = {
        'component': project_key,
        'metricKeys': ','.join(metric_keys)
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching measures for {project_key}: {e}")
        return None

def get_project_issues(project_key, token):
    """
    Retrieves all issues for the specified project from SonarCloud, handling pagination.
    """
    base_url = f"{SONARCLOUD_URL}/api/issues/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        'componentKeys': project_key,
        'types': 'BUG,VULNERABILITY,CODE_SMELL',
        'ps': 500  # Page size
    }

    issues = []
    page = 1
    total = 1

    while (page - 1) * params['ps'] < total:
        params['p'] = page
        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            issues.extend(data.get('issues', []))
            total = data.get('total', 0)
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issues for {project_key}: {e}")
            break

    return issues

def save_project_data(project_key, project_name, measures, issues):
    """
    Saves the project's measures and issues to a JSON file.
    """
    current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data_filename = f"{project_key}_data_{current_timestamp}.json"
    project_data = {
        'project_key': project_key,
        'project_name': project_name,
        'measures': measures,
        'issues': issues
    }
    with open(data_filename, 'w') as data_file:
        json.dump(project_data, data_file, indent=2)
    print(f"Data saved to {data_filename}")

def load_team_projects(file_path, team):
    """
    Loads the list of projects for the specified team from a JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(team, [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading team projects from {file_path}: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <team>")
        sys.exit(1)

    if 'SONAR_TOKEN' not in os.environ:
        print("SONAR_TOKEN is not defined")
        sys.exit(1)
    sonarcloud_token = os.environ['SONAR_TOKEN']

    team = sys.argv[1]
    tp_file = "team_project.json"

    # Load the team data
    with open(tp_file, 'r') as file:
        team_data = json.load(file)

    if team in team_data:
        projects = team_data[team].get('projects', [])
        for project in projects:
            project_key = project['key']
            project_name = project['name']
            measures = get_project_measures(project_key, sonarcloud_token)
            issues = get_project_issues(project_key, sonarcloud_token)
            if measures and issues:
                save_project_data(project_key, project_name, measures, issues)
            else:
                print(f"Failed to retrieve data for project: {project_name} ({project_key})")
    else:
        print(f"No projects found for team: {team}")