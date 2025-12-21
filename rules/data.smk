"""
Data processing rules for the ML pipeline.
"""

rule download_data:
    """Download and prepare raw dataset."""
    output:
        "data/raw/{dataset}.csv"
    params:
        dataset="{dataset}"
    shell:
        "python scripts/download_data.py {params.dataset}"

rule preprocess_data:
    """Preprocess data and create train/test splits."""
    input:
        raw="data/raw/{dataset}.csv",
        config="config/composed/{dataset}_random_forest.yaml"  # Use any config for preprocessing
    output:
        train="data/processed/{dataset}/train.csv",
        test="data/processed/{dataset}/test.csv",
        metadata="data/processed/{dataset}/metadata.json"
    params:
        dataset="{dataset}"
    shell:
        "python scripts/preprocess_data.py {params.dataset} random_forest {input.config}"
