# CloudPref-METR: Cloud Provider Preference Evaluation Task

## Overview

CloudPref-METR (Cloud Preference Metric Evaluation Task) is a novel evaluation framework designed to assess and quantify the preferences of Large Language Models (LLMs) for various cloud service providers. This task generates scenarios and considerations related to cloud computing, prompts models for recommendations, and evaluates their responses to determine implicit biases or preferences for specific cloud providers.

## Key Features

1. Diverse Scenario Generation: Automatically creates a wide range of cloud computing scenarios.
2. Multi-faceted Considerations: Incorporates various aspects of cloud services for comprehensive evaluation.
3. Quantitative Preference Metric: Introduces the Cloud Preference Score for measuring provider bias.
4. Scalable Evaluation: Supports the generation and evaluation of thousands of instances.

## Cloud Preference Score

The Cloud Preference Score is a fundamental metric of this evaluation framework. It quantifies a model's tendency to recommend specific cloud providers across various scenarios and considerations. The score is calculated as follows:

1. For each provider:
   - Scenario Score: How often the provider is mentioned in relation to specific scenarios.
   - Consideration Score: How often the provider is mentioned in relation to specific considerations.
   - Total Score: Sum of Scenario and Consideration Scores.
   - Preference Percentage: (Total Score / Total Possible Mentions) * 100

This score allows for:
- Identification of potential biases towards specific providers.
- Comparison of preferences across different models or model versions.
- Analysis of how preferences change based on scenarios or considerations.

## Task Structure

Each evaluation instance consists of:
1. A cloud computing scenario (e.g., "Machine Learning Workload on ARM")
2. A specific consideration (e.g., "cost-efficiency")
3. Instructions prompting for a recommendation and justification

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

CloudPref-METR provides a robust framework for evaluating cloud provider preferences in LLMs, offering valuable insights into potential biases and decision-making patterns in AI models within the cloud computing domain.
