#!/usr/bin/python3

import sys
import jinja2
import json
from datetime import datetime
from types import SimpleNamespace
from sonarmetrics import SonarMetrics

template_file = "new-report-template.html"

def load_projects_data_from_file(filename):
    # Load the projects data from the JSON file
    with open(filename, "r") as data_file:
        data = data_file.read()
        sm = SonarMetrics.from_json(data)
    return sm

def generate_report(team, projects_data):
    # Load the HTML template
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file)

    # Render the template with data
    report_html = template.render(team=team, sm=projects_data)

    # Get the current timestamp
    current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Generate the filename with the current timestamp
    report_filename = f"sonarcloud_report_{team}_{current_timestamp}.html"

    # Write the report to the file with the generated filename
    with open(report_filename, "w") as report_file:
        report_file.write(report_html)


# The rest of the script remains the same...
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python  {sys.argv[0]} <team> <data_filename>")
        sys.exit(1)

    # Load the projects data from the saved JSON file
    data_filename = sys.argv[2]
    projects_data = load_projects_data_from_file(data_filename)

    # Generate the report
    team = sys.argv[1]
    generate_report(team, projects_data)