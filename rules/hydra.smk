"""
Hydra configuration management rules for Snakemake workflow.
"""

rule validate_config:
    """Validate Hydra configuration files."""
    output:
        "config/validation_report.json"
    shell:
        "python scripts/validate_config.py"

rule compose_config:
    """Compose configuration for specific algorithm and dataset."""
    input:
        "config/validation_report.json"
    output:
        "config/composed/{dataset}_{algorithm}.yaml"
    shell:
        "python scripts/compose_config.py {wildcards.dataset} {wildcards.algorithm}"
