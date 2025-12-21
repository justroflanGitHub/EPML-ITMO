"""
Model evaluation rules for the ML pipeline.
"""

rule evaluate_model:
    """Evaluate trained model on test data."""
    input:
        model="models/{dataset}/{algorithm}/model.pkl",
        test="data/processed/{dataset}/test.csv",
        config="config/composed/{dataset}_{algorithm}.yaml"
    output:
        metrics="reports/{dataset}/{algorithm}/metrics.json",
        predictions="reports/{dataset}/{algorithm}/predictions.csv",
        confusion_matrix="reports/{dataset}/{algorithm}/confusion_matrix.csv",
        classification_report="reports/{dataset}/{algorithm}/classification_report.csv"
    params:
        dataset="{dataset}",
        algorithm="{algorithm}"
    shell:
        "python scripts/evaluate_model.py {params.dataset} {params.algorithm} {input.model} {input.test} {input.config}"

rule cross_validation:
    """Perform cross-validation evaluation."""
    input:
        train="data/processed/{dataset}/train.csv",
        config="config/composed/{dataset}_{algorithm}.yaml"
    output:
        cv_results="reports/{dataset}/{algorithm}/cv_results.json",
        cv_summary="reports/{dataset}/{algorithm}/cv_summary.json"
    params:
        dataset="{dataset}",
        algorithm="{algorithm}"
    shell:
        "python scripts/cross_validation.py {params.dataset} {params.algorithm} {input.train} {input.config}"
