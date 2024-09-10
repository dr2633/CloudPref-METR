import os
import random
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from cloudpref_metr import CloudPrefMETR


def generate_sample_response(instance):
    cloud_providers = ["AWS", "Azure", "Google Cloud", "Oracle Cloud", "IBM Cloud", "Alibaba Cloud"]
    primary_provider = random.choice(cloud_providers)

    return f"""
    For the scenario '{instance['scenario']}', I would recommend {primary_provider} as the primary cloud platform, 
    particularly considering the requirement for {instance['consideration']}.
    """


def main():
    task = CloudPrefMETR()

    data_dir = os.path.join('src', 'cloudpref_metr', 'data')
    results_dir = os.path.join('src', 'cloudpref_metr', 'results', 'simple')
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    num_instances = 1000
    instances = task.generate_evaluation_instances(num_instances)

    recommendations = defaultdict(int)
    recommendations_with_options = defaultdict(int)
    recommendations_without_options = defaultdict(int)

    for instance in instances:
        sample_response = generate_sample_response(instance)
        evaluation = task.evaluate_response(sample_response, instance)
        provider = evaluation['primary_recommendation']

        recommendations[provider] += 1
        if instance['options_provided']:
            recommendations_with_options[provider] += 1
        else:
            recommendations_without_options[provider] += 1

    visualize_results(recommendations, recommendations_with_options, recommendations_without_options, results_dir)
    print_results(recommendations, recommendations_with_options, recommendations_without_options)


def visualize_results(overall, with_options, without_options, output_dir):
    data = [
        ('Overall', overall),
        ('With Options', with_options),
        ('Without Options', without_options)
    ]

    for name, counts in data:
        plt.figure(figsize=(10, 6))
        providers = list(counts.keys())
        values = list(counts.values())
        sns.barplot(x=providers, y=values)
        plt.title(f'Cloud Provider Recommendations - {name}')
        plt.ylabel('Number of Recommendations')
        plt.xlabel('Cloud Provider')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'recommendations_{name.lower().replace(" ", "_")}.png'))
        plt.close()


def print_results(overall, with_options, without_options):
    total = sum(overall.values())
    print("Overall Recommendations:")
    for provider, count in overall.items():
        print(f"{provider}: {count} ({count / total * 100:.2f}%)")

    print("\nRecommendations with Options Provided:")
    total = sum(with_options.values())
    for provider, count in with_options.items():
        print(f"{provider}: {count} ({count / total * 100:.2f}%)")

    print("\nRecommendations without Options Provided:")
    total = sum(without_options.values())
    for provider, count in without_options.items():
        print(f"{provider}: {count} ({count / total * 100:.2f}%)")


if __name__ == "__main__":
    main()