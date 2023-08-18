#!/usr/bin/python3
import json
import sys

class SonarProjectEntry:
    def __init__(self, name, key):
        self.name = name
        self.key = key    


class TeamProjects:
    def __init__(self, organization, projects):
        self.organization = organization
        self.projects = projects

def load_team_projects(pm_file, team):
    with open(pm_file, "r") as file:
        loaded_json = file.read()
        mapping = json.loads(loaded_json)

    if team in mapping:
        projects = mapping[team]
    else:
        projects = None
    return projects

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <team>")
        sys.exit(1)

    tp_file = "team_project.json"
    projects = load_team_projects(tp_file, sys.argv[1])
    print(projects)
