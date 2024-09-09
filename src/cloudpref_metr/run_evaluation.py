import argparse
from cloudpref_metr import CloudPrefMETR
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def run_evaluation(num_instances: int, evaluate_all: bool):
    task = CloudPrefMETR()

    # Generate evaluation instances
    instances = task.generate_evaluation_instances(num_instances)

    # Save instances to a file
    task.save_instances_to_file(instances, "evaluation_instances.json")

    # Load instances from file
    loaded_instances = task.load_instances_from_file("evaluation_instances.json")

    # Evaluate instances
    instances_to_evaluate = loaded_instances if evaluate_all else loaded_instances[:10]
    for instance in instances_to_evaluate:
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

    # Visualize results
    visualize_results(preference_metrics)


def visualize_results(preference_metrics):
    df = pd.DataFrame(preference_metrics).T.reset_index()
    df.columns = ['Provider', 'Scenario_Score', 'Consideration_Score', 'Total_Score', 'Preference_Percentage']

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Provider', y='Preference_Percentage', data=df)
    plt.title('Cloud Provider Preference Percentages')
    plt.ylabel('Preference Percentage')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('preference_percentages.png')
    plt.close()

    plt.figure(figsize=(12, 6))
    df_stacked = df[['Provider', 'Scenario_Score', 'Consideration_Score']]
    df_stacked_pct = df_stacked.set_index('Provider')
    df_stacked_pct = df_stacked_pct.div(df_stacked_pct.sum(axis=1), axis=0) * 100
    df_stacked_pct.plot(kind='bar', stacked=True)
    plt.title('Composition of Cloud Provider Scores')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)
    plt.legend(title='Score Type')
    plt.tight_layout()
    plt.savefig('score_composition.png')
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run CloudPrefMETR evaluation")
    parser.add_argument("--num_instances", type=int, default=1000, help="Number of evaluation instances to generate")
    parser.add_argument("--evaluate_all", action="store_true",
                        help="Evaluate all instances instead of just the first 10")
    args = parser.parse_args()

    run_evaluation(args.num_instances, args.evaluate_all)