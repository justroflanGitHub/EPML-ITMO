"""
Monitoring and notification rules for the ML pipeline.
"""

rule generate_pipeline_report:
    """Generate comprehensive pipeline performance report."""
    input:
        metrics=expand("reports/{dataset}/{algorithm}/metrics.json",
                      dataset=config["datasets"],
                      algorithm=config["algorithms"]),
        cv_summaries=expand("reports/{dataset}/{algorithm}/cv_summary.json",
                           dataset=config["datasets"],
                           algorithm=config["algorithms"])
    output:
        report="reports/pipeline_report.md",
        summary="reports/performance_summary.json"
    shell:
        "python scripts/generate_report.py"

rule send_notifications:
    """Send notifications about pipeline completion."""
    input:
        "reports/performance_summary.json"
    output:
        "reports/notification_log.json"
    shell:
        "python scripts/send_notifications.py"

rule check_pipeline_health:
    """Check pipeline health and data integrity."""
    input:
        expand("reports/{dataset}/{algorithm}/metrics.json",
               dataset=config["datasets"],
               algorithm=config["algorithms"])
    output:
        "reports/health_check.json"
    shell:
        "python scripts/check_health.py"
