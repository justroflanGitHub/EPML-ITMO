#!/usr/bin/env python3
"""ClearML Pipeline Monitor

This script monitors ClearML pipelines and sends notifications
about pipeline status, performance, and alerts.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from clearml import Task


class PipelineMonitor:
    """Monitor for ClearML pipelines with notification system."""

    def __init__(self, project_name: str = "Iris Pipelines", check_interval: int = 60):
        """Initialize pipeline monitor.

        Args:
            project_name: ClearML project to monitor
            check_interval: Interval between checks in seconds

        """
        self.project_name = project_name
        self.check_interval = check_interval
        self.logger = logging.getLogger(__name__)

        # Monitoring state
        self.last_check_time = None
        self.monitored_pipelines = {}
        self.alert_history = []

        self.logger.info(f"Initialized pipeline monitor for project: {project_name}")

    def get_pipeline_tasks(self, status_filter: list[str] = None) -> list[Task]:
        """Get pipeline tasks from the project."""
        try:
            tasks = Task.get_tasks(
                project_name=self.project_name, task_name=None, allow_archived=False
            )

            # Filter by task types (pipelines are typically 'controller' type)
            pipeline_tasks = []
            for task in tasks:
                if hasattr(task.data, "type") and task.data.type in [
                    "controller",
                    "pipeline",
                ]:
                    if status_filter is None or task.status in status_filter:
                        pipeline_tasks.append(task)

            return pipeline_tasks

        except Exception as e:
            self.logger.error(f"Failed to get pipeline tasks: {e}")
            return []

    def get_pipeline_status(self, pipeline_task: Task) -> dict[str, Any]:
        """Get detailed status of a pipeline."""
        try:
            status_info = {
                "task_id": pipeline_task.id,
                "task_name": pipeline_task.name,
                "status": pipeline_task.status,
                "created": pipeline_task.data.created,
                "started": getattr(pipeline_task.data, "started", None),
                "completed": getattr(pipeline_task.data, "completed", None),
                "duration": None,
                "progress": 0.0,
                "steps_completed": 0,
                "total_steps": 0,
                "failed_steps": 0,
            }

            # Calculate duration
            if status_info["completed"] and status_info["started"]:
                try:
                    started_time = datetime.fromisoformat(
                        status_info["started"].replace("Z", "+00:00")
                    )
                    completed_time = datetime.fromisoformat(
                        status_info["completed"].replace("Z", "+00:00")
                    )
                    status_info["duration"] = (
                        completed_time - started_time
                    ).total_seconds()
                except:
                    pass

            # Get pipeline execution details if available
            try:
                # Get child tasks (pipeline steps)
                execution_details = pipeline_task.get_execution_details()
                if execution_details and "steps" in execution_details:
                    steps = execution_details["steps"]
                    status_info["total_steps"] = len(steps)

                    completed_count = sum(
                        1 for step in steps if step.get("status") == "completed"
                    )
                    failed_count = sum(
                        1 for step in steps if step.get("status") == "failed"
                    )

                    status_info["steps_completed"] = completed_count
                    status_info["failed_steps"] = failed_count

                    if status_info["total_steps"] > 0:
                        status_info["progress"] = (
                            completed_count / status_info["total_steps"]
                        )

            except Exception as e:
                self.logger.warning(
                    f"Could not get execution details for pipeline {pipeline_task.id}: {e}"
                )

            return status_info

        except Exception as e:
            self.logger.error(
                f"Failed to get pipeline status for {pipeline_task.id}: {e}"
            )
            return {}

    def check_pipeline_alerts(
        self, pipeline_status: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Check for alerts based on pipeline status."""
        alerts = []

        # Alert for failed pipelines
        if pipeline_status.get("status") == "failed":
            alerts.append(
                {
                    "type": "pipeline_failed",
                    "severity": "high",
                    "message": f"Pipeline '{pipeline_status['task_name']}' failed",
                    "pipeline_id": pipeline_status["task_id"],
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Alert for long-running pipelines
        if pipeline_status.get("status") in ["in_progress", "running"]:
            started = pipeline_status.get("started")
            if started:
                try:
                    started_time = datetime.fromisoformat(
                        started.replace("Z", "+00:00")
                    )
                    runtime = (datetime.now() - started_time).total_seconds()

                    # Alert if running for more than 30 minutes
                    if runtime > 1800:  # 30 minutes
                        alerts.append(
                            {
                                "type": "long_running",
                                "severity": "medium",
                                "message": f"Pipeline '{pipeline_status['task_name']}' running for {runtime / 3600:.1f} hours",
                                "pipeline_id": pipeline_status["task_id"],
                                "runtime_hours": runtime / 3600,
                                "timestamp": datetime.now().isoformat(),
                            }
                        )
                except:
                    pass

        # Alert for failed steps
        if pipeline_status.get("failed_steps", 0) > 0:
            alerts.append(
                {
                    "type": "steps_failed",
                    "severity": "high",
                    "message": f"Pipeline '{pipeline_status['task_name']}' has {pipeline_status['failed_steps']} failed steps",
                    "pipeline_id": pipeline_status["task_id"],
                    "failed_steps": pipeline_status["failed_steps"],
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return alerts

    def send_notification(self, alert: dict[str, Any]):
        """Send notification for an alert."""
        severity = alert.get("severity", "low")
        message = alert.get("message", "Unknown alert")

        # Log alert
        if severity == "high":
            self.logger.error(f"🚨 {message}")
        elif severity == "medium":
            self.logger.warning(f"⚠️ {message}")
        else:
            self.logger.info(f"ℹ️ {message}")

        # Here you could integrate with external notification systems
        # For example: email, Slack, Telegram, etc.

        # For now, just log to file
        self._log_alert_to_file(alert)

    def _log_alert_to_file(self, alert: dict[str, Any]):
        """Log alert to a file for persistence."""
        try:
            alert_log_path = Path("./logs/pipeline_alerts.jsonl")
            alert_log_path.parent.mkdir(parents=True, exist_ok=True)

            with open(alert_log_path, "a") as f:
                json.dump(alert, f)
                f.write("\n")

        except Exception as e:
            self.logger.error(f"Failed to log alert to file: {e}")

    def generate_monitoring_report(self) -> str:
        """Generate a monitoring report."""
        try:
            pipelines = self.get_pipeline_tasks()

            report_lines = []
            report_lines.append("# ClearML Pipeline Monitoring Report")
            report_lines.append(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            report_lines.append("")

            # Summary
            total_pipelines = len(pipelines)
            running_pipelines = sum(
                1 for p in pipelines if p.status in ["in_progress", "running"]
            )
            completed_pipelines = sum(1 for p in pipelines if p.status == "completed")
            failed_pipelines = sum(1 for p in pipelines if p.status == "failed")

            report_lines.append("## Summary")
            report_lines.append(f"- Total pipelines: {total_pipelines}")
            report_lines.append(f"- Running: {running_pipelines}")
            report_lines.append(f"- Completed: {completed_pipelines}")
            report_lines.append(f"- Failed: {failed_pipelines}")
            report_lines.append("")

            # Pipeline details
            if pipelines:
                report_lines.append("## Pipeline Details")
                report_lines.append(
                    "| Pipeline Name | Status | Progress | Duration | Started |"
                )
                report_lines.append(
                    "|---------------|--------|----------|----------|---------|"
                )

                for pipeline in pipelines[:10]:  # Show top 10
                    status = self.get_pipeline_status(pipeline)

                    progress = f"{status.get('progress', 0):.1%}"
                    duration = (
                        f"{status.get('duration', 0) / 3600:.1f}h"
                        if status.get("duration")
                        else "N/A"
                    )
                    started = status.get("started", "N/A")
                    if started != "N/A":
                        try:
                            started = datetime.fromisoformat(
                                started.replace("Z", "+00:00")
                            ).strftime("%H:%M:%S")
                        except:
                            pass

                    report_lines.append(
                        f"| {pipeline.name} | {pipeline.status} | {progress} | {duration} | {started} |"
                    )

                report_lines.append("")

            # Recent alerts
            if self.alert_history:
                report_lines.append("## Recent Alerts")
                recent_alerts = self.alert_history[-5:]  # Last 5 alerts

                for alert in recent_alerts:
                    severity_icon = {"high": "🚨", "medium": "⚠️", "low": "ℹ️"}.get(
                        alert.get("severity"), "ℹ️"
                    )
                    report_lines.append(
                        f"- {severity_icon} {alert.get('message', 'Unknown alert')}"
                    )

                report_lines.append("")

            return "\n".join(report_lines)

        except Exception as e:
            self.logger.error(f"Failed to generate monitoring report: {e}")
            return f"Error generating report: {e}"

    def monitor_once(self) -> dict[str, Any]:
        """Perform one monitoring cycle."""
        self.logger.info("Starting monitoring cycle...")

        # Get all pipelines
        pipelines = self.get_pipeline_tasks()
        current_time = datetime.now()

        monitoring_results = {
            "timestamp": current_time.isoformat(),
            "total_pipelines": len(pipelines),
            "pipeline_statuses": [],
            "alerts": [],
        }

        # Check each pipeline
        for pipeline in pipelines:
            status = self.get_pipeline_status(pipeline)
            monitoring_results["pipeline_statuses"].append(status)

            # Check for alerts
            alerts = self.check_pipeline_alerts(status)
            for alert in alerts:
                monitoring_results["alerts"].append(alert)
                self.alert_history.append(alert)
                self.send_notification(alert)

        self.last_check_time = current_time

        self.logger.info(
            f"Monitoring cycle completed. Checked {len(pipelines)} pipelines, {len(monitoring_results['alerts'])} alerts."
        )

        return monitoring_results

    def start_monitoring(self, duration_minutes: int = None):
        """Start continuous monitoring."""
        self.logger.info(
            f"Starting continuous monitoring (interval: {self.check_interval}s)"
        )

        start_time = datetime.now()
        cycle_count = 0

        try:
            while True:
                cycle_count += 1
                self.logger.info(f"Monitoring cycle #{cycle_count}")

                # Perform monitoring
                results = self.monitor_once()

                # Check if we should stop
                if duration_minutes:
                    elapsed = (datetime.now() - start_time).total_seconds() / 60
                    if elapsed >= duration_minutes:
                        self.logger.info(
                            f"Monitoring duration ({duration_minutes} min) reached. Stopping."
                        )
                        break

                # Wait for next cycle
                if cycle_count < 10:  # Only sleep if not the last cycle
                    time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user.")
        except Exception as e:
            self.logger.error(f"Monitoring failed: {e}")

        # Generate final report
        report = self.generate_monitoring_report()
        self.logger.info("Final monitoring report:")
        print(report)


def main():
    """Main function for pipeline monitoring."""
    import argparse

    parser = argparse.ArgumentParser(description="Monitor ClearML pipelines")
    parser.add_argument(
        "--project", default="Iris Pipelines", help="ClearML project to monitor"
    )
    parser.add_argument(
        "--interval", type=int, default=60, help="Monitoring interval in seconds"
    )
    parser.add_argument("--duration", type=int, help="Monitoring duration in minutes")
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Generate report only, do not start monitoring",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Create monitor
    monitor = PipelineMonitor(args.project, args.interval)

    if args.report_only:
        # Generate and print report only
        report = monitor.generate_monitoring_report()
        print("\n" + "=" * 80)
        print("PIPELINE MONITORING REPORT")
        print("=" * 80)
        print(report)
        print("=" * 80)
    else:
        # Start monitoring
        monitor.start_monitoring(args.duration)


if __name__ == "__main__":
    main()
