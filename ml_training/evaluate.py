import os
import json
import joblib
import pandas as pd

def generate_report():
    # Load metadata generated during training
    metadata_path = os.path.join('data', 'trained_model', 'model_metadata.json')
    if not os.path.exists(metadata_path):
        print(f"Metadata file not found at {metadata_path}")
        return
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    test_metrics = metadata.get('test_metrics', {})
    classification_report = metadata.get('classification_report', {})

    # Build markdown report
    lines = []
    lines.append('# Model Evaluation Report')
    lines.append('')
    lines.append('## Test Set Metrics')
    lines.append('| Metric | Value |')
    lines.append('|---|---|')
    for metric, value in test_metrics.items():
        if isinstance(value, list):
            # Skip complex structures like confusion matrix
            continue
        lines.append(f'| {metric} | {value:.4f} |')
    lines.append('')
    lines.append('## Classification Report')
    lines.append('```')
    lines.append(json.dumps(classification_report, indent=2))
    lines.append('```')

    report_path = os.path.join('ml_training', 'evaluation_report.md')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Evaluation report written to {report_path}")

if __name__ == '__main__':
    generate_report()
