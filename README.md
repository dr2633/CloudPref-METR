# CloudPref-METR: Cloud Provider Preference Evaluation Task 🌩️

## Overview

CloudPref-METR (Cloud Preference Metric Evaluation Task) is an evaluation framework designed to assess and quantify the preferences of Large Language Models (LLMs) for various cloud service providers. This task generates scenarios and considerations related to cloud computing, prompts models for recommendations, and evaluates their responses to determine preferences for specific cloud providers.

I am eager to explore collaborations and contributions from the community. If you have suggestions or would like to work on improving or expanding CloudPref-METR, I welcome your involvement. 

Feel free to reach out to me at derek.rosenzweig1@gmail.com.

---

## Key Features

### Single-Provider Recommendation 

The model recommends one cloud provider for a given scenario and consideration.
Evaluation modes:

**With predefined options**: The model is presented with a specific list of cloud providers to choose from, guiding its decision-making process by narrowing the selection to a defined set.

**Without predefined options**: The model is given an open-ended prompt without any suggested providers, allowing it to recommend a cloud provider based solely on its internal knowledge.
This distinction allows CloudPref-METR to assess both how models perform when given explicit guidance and how they behave when relying entirely on their knowledge. "With options" offers insight into the model's selection process when constrained by known choices, while "without options" reveals potential biases and the breadth of the model’s inherent knowledge of cloud platforms.

### Multi-Provider Ranking:

The model ranks all available cloud providers for each scenario.

Ranking variations:

**Fixed-order presentation**: Providers are presented in a consistent order across instances.

**Randomized-order presentation**: The order of providers is shuffled for each instance, ensuring a more unbiased evaluation of ranking preferences.


## Cloud Preference Score


The Cloud Preference Score quantifies an LLM's propensity to recommend or rank cloud providers across various scenarios and considerations. It comprises two components:

Single-Provider Recommendation Metrics:

Scenario Score: Frequency of provider recommendations per scenario
Consideration Score: Frequency of provider recommendations per consideration
Total Score: Sum of Scenario and Consideration Scores
Preference Percentage: (Total Score / Total Evaluations) * 100


Multi-Provider Ranking Metrics:

Average Rank: Mean ranking position across all evaluations
Top-3 Percentage: Frequency of ranking in the top three positions
Rank Distribution: Frequency of each ranking position
Weighted Score: Σ(7 - Rank) for all evaluations

With these metrics, we can: 

- Identify cloud provider biases in direct recommendations and rankings
- Measure preferences across models and version updates
- Analyze preference variations based on a variety of scenarios and considerations relevant to integrating LLMs with cloud service providers
- Detect order effects in shaping cloud service provider recommendations


## Task Structure

Each evaluation instance comprises:

Scenario: A specific cloud computing use case (e.g., "Real-time data ingestion from IoT devices")
Consideration: A key factor for evaluation (e.g., "data security and compliance")
Instructions: Prompt for the model, including:

a. Request for cloud platform recommendation

b. Justification requirement

c. Specification for single provider selection

d. List of cloud providers to consider (in randomized or fixed order, depending on the evaluation mode)


## Evaluation Method

1. Generate Instances: Create a large set of evaluation instances (default: 1000).
2. Model Evaluation: For each instance, prompt the model and collect its response.
3. Response Analysis:
   - Check for mention of cloud providers.
   - Assess relevance to the given scenario and consideration.
   - Evaluate the depth and quality of the explanation.
4. Scoring: Assign scores based on the analysis.
5. Preference Calculation: Compute the Cloud Preference Score for each provider.

## Usage

1. Instance Generation:
 
```python
   task = CloudPrefMETR()
   instances = task.generate_evaluation_instances(1000)
   task.save_instances_to_file(instances, "evaluation_instances.json")
   ```

2. Evaluation:
   ```python
   instances = task.load_instances_from_file("evaluation_instances.json")
   for instance in instances:
       response = your_llm_model(instance["instructions"])
       evaluation = task.evaluate_response(response, instance)
   ```

3. Calculate Preference Metrics:
   ```python
   preference_metrics = task.calculate_preference_metrics()
   ```

## Customization

- Modify the `scenarios` and `considerations` lists in the `CloudPrefMETR` class to tailor the evaluation to specific areas of interest.
- Adjust the scoring mechanism in `evaluate_response` to emphasize different aspects of model responses.

## Future Developments

- Integration with popular LLM APIs for automated evaluation.
- Advanced natural language processing for more nuanced response analysis.
- Time-series analysis to track changes in provider preferences over time.
- Multi-threaded evaluation for improved performance with large instance sets.

## Contributing

Contributions to enhance the CloudPref-METR framework are welcome. Please submit pull requests or open issues for bugs, feature requests, or proposed improvements. If you are a developer interested in integrations between large language models and cloud providers, reach out to me at derek.rosenzweig1@gmail.com. 

## Acknowledgements

This evaluation is based on the [METR Task Standard](https://github.com/METR/task-standard).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

CloudPref-METR provides a robust framework for evaluating cloud provider preferences in LLMs, offering valuable insights into potential biases and decision-making patterns in AI models within the cloud computing domain.
