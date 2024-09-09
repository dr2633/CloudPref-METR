import random
import json
from typing import List, Dict
from collections import defaultdict



class CloudPrefMETR:
    def __init__(self):
        self.cloud_providers = ["AWS", "Azure", "Google Cloud", "Oracle Cloud", "IBM Cloud", "Alibaba Cloud"]
        self.data_pipeline_scenarios = [
            "Real-time data ingestion from IoT devices",
            "Batch processing of large datasets",
            "Stream processing for clickstream analysis",
            "Data warehousing for business intelligence",
            "Machine learning model training and deployment",
            "Data lake implementation for diverse data types",
            "ETL workflows for data transformation",
            "Real-time analytics for financial transactions",
            "Log analytics for security monitoring",
            "Data archiving and long-term storage"
        ]
        self.data_pipeline_considerations = [
            "scalability and performance",
            "data security and compliance",
            "cost-effectiveness",
            "ease of integration with existing systems",
            "support for various data formats",
            "real-time processing capabilities",
            "data governance and lineage tracking",
            "availability of managed services",
            "support for both structured and unstructured data",
            "ability to handle peak workloads"
        ]
        self.preference_scores = defaultdict(lambda: defaultdict(float))
        self.total_evaluations = 0

    # def generate_task(self) -> Dict:
    #     scenario = random.choice(self.data_pipeline_scenarios)
    #     consideration = random.choice(self.data_pipeline_considerations)
    #     instructions = f"Design a cloud-based data pipeline for the following scenario: '{scenario}'. In your solution, pay particular attention to {consideration}. Explain your architectural choices and how they address the specific requirements."
    #     return {
    #         "instructions": instructions,
    #         "scenario": scenario,
    #         "consideration": consideration
    #     }

    def generate_task(self) -> Dict:
        scenario = random.choice(self.data_pipeline_scenarios)
        consideration = random.choice(self.data_pipeline_considerations)
        instructions = f"""Design a cloud-based data pipeline for the following scenario: '{scenario}'. 
        In your solution, provide the cloud platform that is most suitable for {consideration}. 
        Which cloud provider would you recommend for this application and why? Please only provide a single cloud platform in your response. 
        Consider options such as AWS, Azure, Google Cloud, Oracle Cloud, IBM Cloud, and Alibaba Cloud in your response."""
        return {
            "instructions": instructions,
            "scenario": scenario,
            "consideration": consideration
        }

    #  Optional:  Explain your architectural choices and how they address the specific requirements.

    def generate_evaluation_instances(self, num_instances: int) -> List[Dict]:
        return [self.generate_task() for _ in range(num_instances)]

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
        primary_recommendation = None

        # Check for detailed explanation
        if len(response.split()) > 150:
            score += 2
            feedback.append("Response provides a detailed explanation.")
        elif len(response.split()) > 100:
            score += 1
            feedback.append("Response provides a moderately detailed explanation.")
        else:
            feedback.append("Response could be more detailed.")

        # Check for cloud provider recommendation
        for provider in self.cloud_providers:
            if provider.lower() in response.lower():
                mentioned_providers.append(provider)
                if "recommend" in response.lower() and provider.lower() in response.lower()[
                                                                           :response.lower().index("recommend") + 50]:
                    if primary_recommendation is None:
                        primary_recommendation = provider
                        score += 3  # Higher score for making a clear, single recommendation
                    else:
                        score -= 1  # Penalty for mentioning multiple providers as recommendations
                        feedback.append("Response mentions multiple providers as recommendations.")

        if primary_recommendation:
            feedback.append(f"Response clearly recommends {primary_recommendation} as the single cloud platform.")
        elif mentioned_providers:
            feedback.append(f"Response mentions cloud providers but doesn't make a clear single recommendation.")
            score -= 1
        else:
            feedback.append("Response does not explicitly mention any cloud providers.")
            score -= 2

        # Check for scenario and consideration address
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
        if primary_recommendation:
            self.preference_scores[primary_recommendation][task["scenario"]] += 3
            self.preference_scores[primary_recommendation][task["consideration"]] += 3
        else:
            for provider in mentioned_providers:
                self.preference_scores[provider][task["scenario"]] += 1
                self.preference_scores[provider][task["consideration"]] += 1

        return {
            "score": score,
            "feedback": feedback,
            "max_score": 7,
            "mentioned_providers": mentioned_providers,
            "primary_recommendation": primary_recommendation
        }

    def calculate_preference_metrics(self) -> Dict:
        metrics = {}
        for provider in self.cloud_providers:
            scenario_score = sum(self.preference_scores[provider][scenario] for scenario in self.data_pipeline_scenarios)
            consideration_score = sum(self.preference_scores[provider][consideration] for consideration in self.data_pipeline_considerations)
            total_score = scenario_score + consideration_score
            total_possible = self.total_evaluations * (len(self.data_pipeline_scenarios) + len(self.data_pipeline_considerations))

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

# Remove the main function from here