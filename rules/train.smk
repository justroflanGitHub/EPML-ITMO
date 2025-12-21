"""
Model training rules for the ML pipeline.
"""

rule train_model:
    """Train a model with specified algorithm."""
    input:
        train="data/processed/{dataset}/train.csv",
        config="config/composed/{dataset}_{algorithm}.yaml"
    output:
        model="models/{dataset}/{algorithm}/model.pkl",
        params="models/{dataset}/{algorithm}/params.json",
        training_log="models/{dataset}/{algorithm}/training.log"
    params:
        dataset="{dataset}",
        algorithm="{algorithm}"
    threads: 4
    shell:
        "python scripts/train_model.py {params.dataset} {params.algorithm} {input.config}"
