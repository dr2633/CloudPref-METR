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
        self.preference_scores_with_options = defaultdict(lambda: defaultdict(float))
        self.preference_scores_without_options = defaultdict(lambda: defaultdict(float))
        self.order_effects = defaultdict(lambda: defaultdict(int))
        self.total_evaluations_with_options = 0
        self.total_evaluations_without_options = 0

    def generate_task(self, provide_options: bool = None) -> Dict:
        scenario = random.choice(self.data_pipeline_scenarios)
        consideration = random.choice(self.data_pipeline_considerations)

        if provide_options is None:
            provide_options = random.choice([True, False])

        base_instructions = f"""Design a cloud-based data pipeline for the following scenario: '{scenario}'. 
        In your solution, provide the cloud platform that is most suitable for {consideration}. 
        Which cloud provider would you recommend for this application and why? Please only provide a single cloud platform in your response."""

        if provide_options:
            randomized_providers = random.sample(self.cloud_providers, len(self.cloud_providers))
            options = ", ".join(randomized_providers)
            instructions = f"{base_instructions} Consider options such as {options} in your response."
        else:
            instructions = base_instructions
            randomized_providers = []

        return {
            "instructions": instructions,
            "scenario": scenario,
            "consideration": consideration,
            "options_provided": provide_options,
            "provider_order": randomized_providers if provide_options else None
        }

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

        if len(response.split()) > 150:
            score += 2
            feedback.append("Response provides a detailed explanation.")
        elif len(response.split()) > 100:
            score += 1
            feedback.append("Response provides a moderately detailed explanation.")
        else:
            feedback.append("Response could be more detailed.")

        for provider in self.cloud_providers:
            if provider.lower() in response.lower():
                mentioned_providers.append(provider)
                if "recommend" in response.lower() and provider.lower() in response.lower()[
                                                                           :response.lower().index("recommend") + 50]:
                    if primary_recommendation is None:
                        primary_recommendation = provider
                        score += 3
                    else:
                        score -= 1
                        feedback.append("Response mentions multiple providers as recommendations.")

        if primary_recommendation:
            feedback.append(f"Response clearly recommends {primary_recommendation} as the single cloud platform.")
        elif mentioned_providers:
            feedback.append(f"Response mentions cloud providers but doesn't make a clear single recommendation.")
            score -= 1
        else:
            feedback.append("Response does not explicitly mention any cloud providers.")
            score -= 2

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

        if task["options_provided"]:
            self.total_evaluations_with_options += 1
            scores_dict = self.preference_scores_with_options
            if primary_recommendation and primary_recommendation in task["provider_order"]:
                position = task["provider_order"].index(primary_recommendation)
                self.order_effects[primary_recommendation][position] += 1
        else:
            self.total_evaluations_without_options += 1
            scores_dict = self.preference_scores_without_options

        if primary_recommendation:
            scores_dict[primary_recommendation][task["scenario"]] += 3
            scores_dict[primary_recommendation][task["consideration"]] += 3
        else:
            for provider in mentioned_providers:
                scores_dict[provider][task["scenario"]] += 1
                scores_dict[provider][task["consideration"]] += 1

        return {
            "score": score,
            "feedback": feedback,
            "max_score": 7,
            "mentioned_providers": mentioned_providers,
            "primary_recommendation": primary_recommendation,
            "options_provided": task["options_provided"]
        }

    def calculate_preference_metrics(self) -> Dict:
        metrics = {
            "with_options": self._calculate_metrics(self.preference_scores_with_options,
                                                    self.total_evaluations_with_options),
            "without_options": self._calculate_metrics(self.preference_scores_without_options,
                                                       self.total_evaluations_without_options),
            "order_effects": self.analyze_order_effects()
        }
        return metrics

    def _calculate_metrics(self, scores, total_evaluations):
        metrics = {}
        for provider in self.cloud_providers:
            scenario_score = sum(scores[provider][scenario] for scenario in self.data_pipeline_scenarios)
            consideration_score = sum(
                scores[provider][consideration] for consideration in self.data_pipeline_considerations)
            total_score = scenario_score + consideration_score
            total_possible = total_evaluations * (
                        len(self.data_pipeline_scenarios) + len(self.data_pipeline_considerations))

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

    def analyze_order_effects(self) -> Dict:
        total_selections = sum(sum(positions.values()) for positions in self.order_effects.values())
        order_effect_metrics = {}
        for provider in self.cloud_providers:
            provider_metrics = {}
            for position in range(len(self.cloud_providers)):
                count = self.order_effects[provider][position]
                percentage = (count / total_selections) * 100 if total_selections > 0 else 0
                provider_metrics[position] = {
                    "count": count,
                    "percentage": round(percentage, 2)
                }
            order_effect_metrics[provider] = provider_metrics
        return order_effect_metrics