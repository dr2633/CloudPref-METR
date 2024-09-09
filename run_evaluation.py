import os
import random
import matplotlib.pyplot as plt
import seaborn as sns
from cloudpref_metr import CloudPrefMETR


def generate_sample_response(instance):
    cloud_providers = ["AWS", "Azure", "Google Cloud", "Oracle Cloud", "IBM Cloud", "Alibaba Cloud"]
    primary_provider = random.choice(cloud_providers)
    secondary_provider = random.choice([p for p in cloud_providers if p != primary_provider])

    return f"""
    For the scenario '{instance['scenario']}', I would recommend {primary_provider} as the primary cloud platform, 
    particularly considering the requirement for {instance['consideration']}.

    {primary_provider} offers a comprehensive suite of services that are well-suited for this use case:
    1. Data Ingestion: Use {primary_provider}'s streaming data service for real-time data ingestion.
    2. Storage: Utilize {primary_provider}'s object storage and data lake solutions for efficient data management.
    3. Processing: Leverage {primary_provider}'s serverless computing and big data processing services.
    4. Analytics: Employ {primary_provider}'s data warehousing and business intelligence tools.

    This architecture addresses the {instance['consideration']} requirement through scalable and managed services, 
    reducing operational overhead and improving performance.

    While {primary_provider} is my primary recommendation, {secondary_provider} also offers strong capabilities in this area. 
    {secondary_provider}'s solutions could be considered for specific components or as part of a multi-cloud strategy, 
    especially if there are existing investments or specific features that align well with the {instance['consideration']} requirement.

    Other providers like {', '.join([p for p in cloud_providers if p not in [primary_provider, secondary_provider]])} 
    also have offerings in this space, but may not be as comprehensive or cost-effective for this particular scenario 
    and consideration.
    """


def visualize_results(preference_metrics, output_dir):
    providers = list(preference_metrics.keys())
    percentages = [metrics['preference_percentage'] for metrics in preference_metrics.values()]

    plt.figure(figsize=(12, 6))
    sns.barplot(x=providers, y=percentages)
    plt.title('Cloud Provider Preference Percentages')
    plt.ylabel('Preference Percentage')
    plt.xlabel('Cloud Provider')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'preference_percentages.png'))
    plt.close()

    # Stacked bar chart for scenario and consideration scores
    scenario_scores = [metrics['scenario_score'] for metrics in preference_metrics.values()]
    consideration_scores = [metrics['consideration_score'] for metrics in preference_metrics.values()]

    plt.figure(figsize=(12, 6))
    plt.bar(providers, scenario_scores, label='Scenario Score')
    plt.bar(providers, consideration_scores, bottom=scenario_scores, label='Consideration Score')
    plt.title('Composition of Cloud Provider Scores')
    plt.ylabel('Score')
    plt.xlabel('Cloud Provider')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'score_composition.png'))
    plt.close()


def main():
    task = CloudPrefMETR()

    # Create directories if they don't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    # Generate 1000 evaluation instances
    instances = task.generate_evaluation_instances(1000)

    # Save instances to a file
    task.save_instances_to_file(instances, "data/evaluation_instances.json")

    # Load instances from file
    loaded_instances = task.load_instances_from_file("data/evaluation_instances.json")

    # Simulate evaluations
    for instance in loaded_instances[:10]:  # Only evaluating first 10 for demonstration
        print("Task Instructions:", instance["instructions"])

        # Generate a more realistic sample response
        sample_response = generate_sample_response(instance)
        print("Sample Response:", sample_response)

        evaluation = task.evaluate_response(sample_response, instance)
        print("Evaluation:", evaluation)
        print("\n" + "=" * 50 + "\n")

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

    # Visualize results
    visualize_results(preference_metrics, 'results')


if __name__ == "__main__":
    main()