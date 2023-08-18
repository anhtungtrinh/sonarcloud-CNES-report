#!/usr/bin/python3

import requests
import jinja2
import json
import sys
import os
from datetime import datetime
from sonarmetrics import SonarMetrics
from team_project import load_team_projects

tp_file = "team_project.json"

def get_project_metrics(project_key, token):
    base_url = f"https://sonarcloud.io/api/measures/component"
    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "component": project_key,
        "metricKeys": "bugs,vulnerabilities,security_hotspots,code_smells,coverage,duplicated_lines_density",
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data["component"]["measures"]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def save_projects_data_to_file(team, projects_data):
    # Get the current timestamp
    current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Generate the filename with the current timestamp
    data_filename = f"sonarcloud_data_{team}_{current_timestamp}.json"

    # Save the projects data to the JSON file
    with open(data_filename, "w") as data_file:
        data_file.write(projects_data.to_json())

def get_team_data(file, team, token):
    tp = load_team_projects(tp_file, team)

    if tp:
        report_data = []
        sm = SonarMetrics()

        for project in tp["projects"]:
            if project:
                project_key = project["key"]
                project_name = project["name"]

                metrics = get_project_metrics(project_key, token)
                if metrics:
                    print(f"Loading metrics for project: {project_name} ({project_key}):")
                    project_data = {
                        "project_name": project_name,
                        "bugs": next((int(m["value"]) for m in metrics if m["metric"] == "bugs"), 0),
                        "vulnerabilities": next((int(m["value"]) for m in metrics if m["metric"] == "vulnerabilities"), 0),
                        "code_smells": next((int(m["value"]) for m in metrics if m["metric"] == "code_smells"), 0),
                        "security_hotspots": next((int(m["value"]) for m in metrics if m["metric"] == "security_hotspots"), 0),
                        "coverage": next((float(m["value"]) for m in metrics if m["metric"] == "coverage"), 0),
                        "duplicated_lines_density": next((float(m["value"]) for m in metrics if m["metric"] == "duplicated_lines_density"), 0),
                    }
                    report_data.append(project_data)
                    sm.add_project_data(project_data)
                else:
                    print(f"Failed to retrieve metrics for project: {project_name} ({project_key})")
        save_projects_data_to_file(team, sm)
    else:
        print("Failed to retrieve the list of projects.")


    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <team>")
        sys.exit(1)

    if 'SONAR_TOKEN' not in os.environ:
        print(f"SONAR_TOKEN is not defined")
        sys.exit(1)
    sonarcloud_token = os.environ['SONAR_TOKEN']

    get_team_data(tp_file, sys.argv[1], sonarcloud_token)