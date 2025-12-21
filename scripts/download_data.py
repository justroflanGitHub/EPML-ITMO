#!/usr/bin/env python3
"""Download and prepare raw dataset."""

import os
import sys

import pandas as pd
from sklearn.datasets import load_iris


def main():
    if len(sys.argv) != 2:
        print("Usage: python download_data.py <dataset>")
        return 1

    dataset = sys.argv[1]

    try:
        if dataset == "iris":
            # Load iris dataset
            iris = load_iris()
            df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
            df["target"] = iris.target
            df["target_name"] = df["target"].apply(lambda x: iris.target_names[x])

            # Ensure output directory exists
            output_file = f"data/raw/{dataset}.csv"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            df.to_csv(output_file, index=False)
            print(f"Dataset {dataset} saved to {output_file}")
            return 0
        else:
            print(f"Unsupported dataset: {dataset}")
            return 1
    except Exception as e:
        print(f"Error downloading data: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
