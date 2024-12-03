import json
from jinja2 import Environment, FileSystemLoader
import argparse

def load_data(json_file):
    """Load the JSON data from the specified file."""
    with open(json_file, 'r') as file:
        return json.load(file)

def generate_html_report(data, template_path, output_file):
    """Generate an HTML report from the data using the specified template."""
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template('report_template.html')

    metrics = {metric['metric']: metric['value'] for metric in data['measures']['component']['measures']}
    issues = data['issues']

    html_content = template.render(
        project_name=data['project_name'],
        project_key=data['project_key'],
        metrics=metrics,
        issues=issues,
        float=float,  # Pass float function to the template
        int=int       # Pass int function to the template
    )

    with open(output_file, 'w') as output:
        output.write(html_content)
    print(f"Report successfully generated: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate an HTML report from JSON data.')
    parser.add_argument('json_file', help='Path to the JSON file')
    args = parser.parse_args()

    json_file = args.json_file
    template_path = "./templates"
    output_file = "CNES_Report.html"

    # Load data and generate report
    data = load_data(json_file)
    generate_html_report(data, template_path, output_file)

if __name__ == "__main__":
    main()