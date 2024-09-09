import os
from cloudpref_metr import CloudPrefMETR

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

        # In a real scenario, you'd get this response from an AI model
        sample_response = f"""
        For the scenario '{instance['scenario']}', a cloud-based data pipeline can be designed using various services.
        To address the consideration of {instance['consideration']}, we can utilize managed services that offer scalability and robustness.
        The architecture would involve data ingestion, storage, processing, and analytics components, all designed to meet the specific requirements of the scenario.
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

    # Here you would add code to generate and save the PNG files to the results directory

if __name__ == "__main__":
    main()