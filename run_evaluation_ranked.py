import os
import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import defaultdict
from cloudpref_metr import CloudPrefMETR


def generate_sample_response(instance):
    cloud_providers = ["AWS", "Azure", "Google Cloud", "Oracle Cloud", "IBM Cloud", "Alibaba Cloud"]
    rankings = random.sample(cloud_providers, len(cloud_providers))

    response = f"""
    For the scenario '{instance['scenario']}', considering the requirement for {instance['consideration']},
    I would rank the cloud providers as follows:

    1. {rankings[0]} (Most Suitable)
    2. {rankings[1]}
    3. {rankings[2]}
    4. {rankings[3]}
    5. {rankings[4]}
    6. {rankings[5]} (Least Suitable)
    """
    return response, rankings


def analyze_rankings(all_rankings):
    providers = ["AWS", "Azure", "Google Cloud", "Oracle Cloud", "IBM Cloud", "Alibaba Cloud"]
    stats = {provider: {'total_score': 0, 'count': 0, 'rank_counts': defaultdict(int)} for provider in providers}

    for rankings in all_rankings:
        for rank, provider in enumerate(rankings, 1):
            stats[provider]['total_score'] += 7 - rank
            stats[provider]['count'] += 1
            stats[provider]['rank_counts'][rank] += 1

    for provider in providers:
        stats[provider]['average_score'] = stats[provider]['total_score'] / stats[provider]['count']
        stats[provider]['average_rank'] = sum(rank * count for rank, count in stats[provider]['rank_counts'].items()) / \
                                          stats[provider]['count']

    return stats


def visualize_results(stats, output_dir):
    providers = list(stats.keys())
    avg_scores = [stats[p]['average_score'] for p in providers]

    plt.figure(figsize=(12, 6))
    sns.barplot(x=providers, y=avg_scores)
    plt.title('Average Scores by Cloud Provider')
    plt.ylabel('Average Score')
    plt.xlabel('Cloud Provider')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'average_scores.png'))
    plt.close()

    rank_data = []
    for provider in providers:
        for rank, count in stats[provider]['rank_counts'].items():
            rank_data.append({'Provider': provider, 'Rank': rank, 'Count': count})

    df = pd.DataFrame(rank_data)
    pivot_df = df.pivot(index="Provider", columns="Rank", values="Count")

    plt.figure(figsize=(14, 8))
    sns.heatmap(pivot_df, annot=True, fmt='d', cmap="YlGnBu")
    plt.title('Rank Distribution by Cloud Provider')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rank_distribution.png'))
    plt.close()

def main():
    task = CloudPrefMETR()

    data_dir = os.path.join('src', 'cloudpref_metr', 'data')
    results_dir = os.path.join('src', 'cloudpref_metr', 'results', 'ranked')
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    num_instances = 1000
    instances = task.generate_evaluation_instances(num_instances)

    all_rankings = []
    rankings_with_options = []
    rankings_without_options = []

    for instance in instances:
        _, rankings = generate_sample_response(instance)
        all_rankings.append(rankings)
        if instance['options_provided']:
            rankings_with_options.append(rankings)
        else:
            rankings_without_options.append(rankings)

    overall_stats = analyze_rankings(all_rankings)
    with_options_stats = analyze_rankings(rankings_with_options)
    without_options_stats = analyze_rankings(rankings_without_options)

    visualize_results(overall_stats, results_dir)
    print_results(overall_stats, with_options_stats, without_options_stats)


def print_results(overall, with_options, without_options):
    for title, stats in [("Overall", overall), ("With Options", with_options), ("Without Options", without_options)]:
        print(f"\n{title} Cloud Provider Statistics:")
        for provider, provider_stats in stats.items():
            print(f"{provider}:")
            print(f"  Average Score: {provider_stats['average_score']:.2f}")
            print(f"  Average Rank: {provider_stats['average_rank']:.2f}")
            print("  Rank Distribution:")
            for rank, count in sorted(provider_stats['rank_counts'].items()):
                print(f"    Rank {rank}: {count} times")
            print()


if __name__ == "__main__":
    main()