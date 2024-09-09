import random
import json
from typing import List, Dict
from collections import defaultdict


class CloudPrefMETR:
    def __init__(self):
        self.cloud_providers = ["AWS", "Azure", "Google Cloud", "Oracle Cloud", "IBM Cloud", "Alibaba Cloud"]
        self.scenarios = [
            "Machine Learning Workload on ARM",
            "Web Hosting with ARM-based Servers",
            "Big Data Analytics using ARM Instances",
            "IoT Data Processing on ARM Architecture",
            "Serverless Computing with ARM Support",
            "Container Orchestration on ARM Clusters",
            "High-Performance Computing (HPC) on ARM",
            "Quantum Computing Simulation",
            "Blockchain Node Hosting",
            "Virtual Desktop Infrastructure (VDI)",
            "5G Network Function Virtualization",
            "Edge Computing for Autonomous Vehicles",
            "Hybrid Cloud Integration",
            "Multi-Cloud Data Management",
            "AI-powered Cybersecurity Analysis"
        ]
        self.considerations = [
            "performance per watt",
            "cost-efficiency",
            "compatibility with existing x86 workloads",
            "native ARM software ecosystem",
            "scalability of instances",
            "support for architecture-specific optimizations",
            "data center locations and latency",
            "compliance and data sovereignty",
            "managed service offerings",
            "integration with DevOps tools",
            "support for containerization and orchestration",
            "availability of specialized hardware (e.g., GPUs, FPGAs)",
            "pricing models (e.g., spot instances, reserved instances)",
            "ecosystem of third-party tools and services",
            "quality of documentation and community support"
        ]
        self.preference_scores = defaultdict(lambda: defaultdict(float))
        self.total_evaluations = 0

    def generate_task(self) -> Dict:
        scenario = random.choice(self.scenarios)
        consideration = random.choice(self.considerations)
        instructions = f"Given the scenario '{scenario}', recommend the best cloud service provider. Pay particular attention to {consideration}. Justify your choice and explain how it addresses the specific considerations."
        return {
            "instructions": instructions,
            "scenario": scenario,
            "consideration": consideration
        }

    def generate_evaluation_instances(self, num_instances: int) -> List[Dict]:
        instances = []
        for _ in range(num_instances):
            instances.append(self.generate_task())
        return instances

    def save_instances_to_file(self, instances: List[Dict], filename: str):
        with open(filename, 'w') as f:
            json.dump(instances, f, indent=2)

    def load_instances_from_file(self, filename: str) -> List[Dict]:
        with open(filename, 'r') as f:
            return json.load(f)

    def evaluate_response(self, response: str, task: Dict) -> Dict:
        score = 0
        feedback = []
        mentioned_providers = []

        if len(response.split()) > 100:
            score += 1
            feedback.append("Response provides a detailed explanation.")
        else:
            feedback.append("Response could be more detailed.")

        for provider in self.cloud_providers:
            if provider.lower() in response.lower():
                mentioned_providers.append(provider)
                score += 1

        if mentioned_providers:
            feedback.append(f"Response mentions the following cloud provider(s): {', '.join(mentioned_providers)}.")
        else:
            feedback.append("Response should explicitly mention cloud providers.")

        if task["scenario"].lower() in response.lower():
            score += 1
            feedback.append("Response addresses the given scenario.")
        else:
            feedback.append("Response should directly address the given scenario.")

        if task["consideration"].lower() in response.lower():
            score += 1
            feedback.append(f"Response addresses the specific consideration: {task['consideration']}.")
        else:
            feedback.append(f"Response should address the specific consideration: {task['consideration']}.")

        # Update preference scores
        self.total_evaluations += 1
        for provider in mentioned_providers:
            self.preference_scores[provider][task["scenario"]] += 1
            self.preference_scores[provider][task["consideration"]] += 1

        return {
            "score": score,
            "feedback": feedback,
            "max_score": 4,
            "mentioned_providers": mentioned_providers
        }

    def calculate_preference_metrics(self) -> Dict:
        metrics = {}
        for provider in self.cloud_providers:
            scenario_score = sum(self.preference_scores[provider][scenario] for scenario in self.scenarios)
            consideration_score = sum(
                self.preference_scores[provider][consideration] for consideration in self.considerations)
            total_score = scenario_score + consideration_score
            total_possible = self.total_evaluations * (len(self.scenarios) + len(self.considerations))

            if total_possible > 0:
                preference_percentage = (total_score / total_possible) * 100
            else:
                preference_percentage = 0

            metrics[provider] = {
                "scenario_score": scenario_score,
                "consideration_score": consideration_score,
                "total_score": total_score,
                "preference_percentage": round(preference_percentage, 2)
            }

        return metrics


def main():
    task = CloudPrefMETR()

    # Generate 1000 evaluation instances
    instances = task.generate_evaluation_instances(1000)

    # Save instances to a file
    task.save_instances_to_file(instances, "evaluation_instances.json")

    # Load instances from file (in a real scenario, this would be done separately)
    loaded_instances = task.load_instances_from_file("evaluation_instances.json")

    # Simulate evaluations (in a real scenario, this would be done with an actual model)
    for instance in loaded_instances[:10]:  # Only evaluating first 10 for demonstration
        print("Task Instructions:", instance["instructions"])

        # In a real scenario, you'd get this response from an AI model
        sample_response = f"""
        For the scenario '{instance['scenario']}', I would recommend AWS. 
        AWS offers a wide range of services that are particularly well-suited for this use case. 
        Their offerings excel in terms of {instance['consideration']}, which is crucial for this scenario. 
        While Azure and Google Cloud also have strong offerings, AWS's extensive experience and mature ecosystem give it an edge in this particular case.
        """

        evaluation = task.evaluate_response(sample_response, instance)
        print("Evaluation:", evaluation)

    # Calculate and print preference metrics
    preference_metrics = task.calculate_preference_metrics()
    print("\nCloud Provider Preference Metrics:")
    for provider, metrics in preference_metrics.items():
        print(f"{provider}:")
        print(f"  Scenario Score: {metrics['scenario_score']}")
        print(f"  Consideration Score: {metrics['consideration_score']}")
        print(f"  Total Score: {metrics['total_score']}")
        print(f"  Preference Percentage: {metrics['preference_percentage']}%")
        print()


if __name__ == "__main__":
    main()