#!/usr/bin/env python3
"""Send notifications about pipeline completion."""

import json
import os
from datetime import datetime


def main():
    # Load summary
    with open("reports/performance_summary.json") as f:
        summary = json.load(f)

    # Prepare notification message
    best_model = summary["best_accuracy_model"]
    notification = {
        "timestamp": datetime.now().isoformat(),
        "pipeline_status": "completed",
        "best_model": best_model,
        "total_models_trained": summary["total_models"],
        "message": f"Pipeline completed successfully. Best model: {best_model['algorithm']} with {best_model['accuracy']:.4f} accuracy",
    }

    # Log notification
    print("Pipeline Notification:")
    print(f"Status: {notification['pipeline_status']}")
    print(
        f"Best Model: {best_model['algorithm']} (Accuracy: {best_model['accuracy']:.4f})"
    )
    print(f"Models Trained: {summary['total_models']}")

    # Check for Slack webhook (if configured)
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
    if slack_webhook:
        try:
            import requests

            payload = {
                "text": "ML Pipeline Completed :white_check_mark:",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*ML Pipeline Completed Successfully*\n\nBest Model: `{best_model['algorithm']}`\nAccuracy: `{best_model['accuracy']:.4f}`\nTotal Models: `{summary['total_models_trained']}`",
                        },
                    }
                ],
            }
            response = requests.post(slack_webhook, json=payload)
            notification["slack_status"] = (
                "sent" if response.status_code == 200 else "failed"
            )
        except Exception as e:
            notification["slack_status"] = f"error: {str(e)}"
    else:
        notification["slack_status"] = "not_configured"

    # Save notification log
    with open("reports/notification_log.json", "w") as f:
        json.dump(notification, f, indent=2)

    print("Notification processing completed")


if __name__ == "__main__":
    main()
