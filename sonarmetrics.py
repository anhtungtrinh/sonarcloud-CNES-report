#!/usr/bin/python3

import json

class SonarMetrics:
    def __init__(self):
        # Global metrics that aggregate project metrics
        self.global_metrics = {
            "bugs": 0,
            "vulnerabilities": 0,
            "security_hotspots": 0,
            "code_smells": 0,
        }
        # List to hold project metrics
        self.project_metrics = []

    def add_project_data(self, project_data) -> None:
        self.project_metrics.append(project_data)
        self.global_metrics["bugs"] += project_data["bugs"]
        self.global_metrics["vulnerabilities"] += project_data["vulnerabilities"]
        self.global_metrics["security_hotspots"] += project_data["security_hotspots"]
        self.global_metrics["code_smells"] += project_data["code_smells"]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_data):
        # Deserialize the JSON string and reconstruct the object
        data = json.loads(json_data)
        sonar_metrics_object = cls()
        sonar_metrics_object.global_metrics = data["global_metrics"]
        sonar_metrics_object.project_metrics = data["project_metrics"]

        return sonar_metrics_object


if __name__ == "__main__":
    # Replace these values with your actual SonarCloud organization and token

    p1 = {
        "bugs": 2,
        "vulnerabilities": 3,
        "security_hotspots": 5,
        "code_smells": 7
    }

    p2 = {
        "bugs": 11,
        "vulnerabilities": 13,
        "security_hotspots": 17,
        "code_smells": 19
    }


    sm = SonarMetrics()
    sm.add_project_data(p1)
    sm.add_project_data(p2)

    with open("test.json", "w") as file:
        file.write(sm.to_json())

    with open("test.json", "r") as file:
        json_data = file.read()
        inst = SonarMetrics.from_json(json_data=json_data)

        print(sm.to_json())
