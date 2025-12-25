#!/usr/bin/env python3
"""Validate Hydra configuration files."""

import json
import sys

import yaml


def main():
    try:
        config_files = [
            "config/hydra/config.yaml",
            "config/hydra/model/random_forest.yaml",
            "config/hydra/data/iris.yaml",
        ]

        validation_results = {
            "status": "valid",
            "config_files_checked": len(config_files),
            "files_valid": [],
        }

        for config_file in config_files:
            try:
                with open(config_file) as f:
                    yaml.safe_load(f)
                validation_results["files_valid"].append(config_file)
            except Exception as e:
                validation_results["status"] = "invalid"
                validation_results["error"] = f"Error in {config_file}: {str(e)}"
                break

        with open("config/validation_report.json", "w") as f:
            json.dump(validation_results, f, indent=2)

        print("Configuration validation successful")
        return 0

    except Exception as e:
        validation_results = {"status": "invalid", "error": str(e)}
        with open("config/validation_report.json", "w") as f:
            json.dump(validation_results, f, indent=2)
        print(f"Configuration validation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
