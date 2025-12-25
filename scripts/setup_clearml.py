#!/usr/bin/env python3
"""ClearML Setup Script.

This script sets up ClearML for the Iris Data Science Project.
It configures the connection to ClearML server and initializes the project.
"""

import argparse
import os
import sys
from pathlib import Path

import yaml
from clearml import Task


def load_config(config_path: str) -> dict:
    """Load ClearML configuration from YAML file."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def setup_clearml_config(config: dict):
    """Setup ClearML configuration from config dict."""
    # Set API credentials from environment variables if available
    api_key = os.getenv("CLEARML_API_ACCESS_KEY")
    api_secret = os.getenv("CLEARML_API_SECRET_KEY")

    if api_key and api_secret:
        os.environ["CLEARML_API_ACCESS_KEY"] = api_key
        os.environ["CLEARML_API_SECRET_KEY"] = api_secret
        print("✓ ClearML API credentials set from environment variables")
    else:
        print("⚠ No ClearML API credentials found in environment variables")
        print("  Please set CLEARML_API_ACCESS_KEY and CLEARML_API_SECRET_KEY")

    # Set basic configuration via environment variables
    os.environ["CLEARML_WEB_HOST"] = config["api"]["web_server"]
    os.environ["CLEARML_API_HOST"] = config["api"]["api_server"]
    os.environ["CLEARML_FILES_HOST"] = config["api"]["files_server"]

    print("✓ ClearML configuration updated")


def create_project(config: dict):
    """Create ClearML project if it doesn't exist."""
    try:
        # In newer versions of ClearML, Project might not be directly available
        # We'll create a project by initializing a task
        from clearml import Task

        # Try to get existing project or create via task
        task = Task.init(
            project_name=config["project"]["name"],
            task_name="project_initialization",
            task_type=Task.TaskTypes.training,
            reuse_last_task_id=False,
        )

        project_name = task.project
        task_id = task.id
        task.close()

        print(f"✓ Created/retrieved project: {project_name} (via Task ID: {task_id})")
        return {"name": project_name, "task_id": task_id}
    except Exception as e:
        print(
            f"⚠ Could not create project (this is normal without API credentials): {e}"
        )
        print(
            "  Project will be created when experiments are run with valid credentials"
        )
        return {"name": config["project"]["name"], "status": "pending"}


def test_connection(config: dict):
    """Test connection to ClearML server."""
    try:
        # Try to create a simple task to test connection
        task = Task.init(
            project_name=config["project"]["name"],
            task_name="connection_test",
            task_type=Task.TaskTypes.training,
            reuse_last_task_id=False,
            output_uri=config["storage"]["output_uri"],
        )

        print("✓ Successfully connected to ClearML server")
        print(f"  Task created: {task.name} (ID: {task.id})")

        # Clean up test task
        task.close()
        print("✓ Connection test completed")

        return True
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return False


def setup_storage(config: dict):
    """Setup storage directory for ClearML artifacts."""
    storage_path = Path(config["storage"]["output_uri"])
    storage_path.mkdir(parents=True, exist_ok=True)

    print(f"✓ Storage directory created: {storage_path.absolute()}")


def main():
    parser = argparse.ArgumentParser(
        description="Setup ClearML for Iris Data Science Project"
    )
    parser.add_argument(
        "--config",
        default="config/clearml/config.yaml",
        help="Path to ClearML configuration file",
    )
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test connection to ClearML server",
    )

    args = parser.parse_args()

    # Load configuration
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"✗ Configuration file not found: {config_path}")
        sys.exit(1)

    print(f"Loading configuration from: {config_path}")
    config = load_config(config_path)

    # Setup configuration
    setup_clearml_config(config)

    # Setup storage
    setup_storage(config)

    # Create project
    create_project(config)

    # Test connection if requested
    if args.test_connection:
        success = test_connection(config)
        if not success:
            sys.exit(1)

    print("\n✓ ClearML setup completed successfully!")
    print(f"  Project: {config['project']['name']}")
    print(f"  Server: {config['api']['web_server']}")

    if not os.getenv("CLEARML_API_ACCESS_KEY"):
        print("\n⚠ To complete setup:")
        print("  1. Go to https://app.clear.ml and create an account")
        print("  2. Get your API access key and secret from Settings > Workspace")
        print("  3. Set environment variables:")
        print("     export CLEARML_API_ACCESS_KEY='your_access_key'")
        print("     export CLEARML_API_SECRET_KEY='your_secret_key'")


if __name__ == "__main__":
    main()
