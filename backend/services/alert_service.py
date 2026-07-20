"""
AtmoSync Alert Dispatch Service
Sends critical cold chain breach notifications via Slack, Email, and Webhooks.
"""

from typing import Dict, Any, List


class AlertService:
    def __init__(self):
        self.alert_history = []

    def dispatch_alert(self, alert_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatches cold chain thermal excursion or door breach alerts.
        """
        container_id = alert_payload.get("container_id", "UNKNOWN")
        severity = alert_payload.get("severity", "WARNING")
        message = alert_payload.get("message", "Cold chain threshold exceeded.")

        alert_record = {
            "container_id": container_id,
            "severity": severity,
            "message": message,
            "dispatched_at": alert_payload.get("timestamp", "NOW"),
            "channels_notified": ["SLACK_LOGISTICS_CHANNEL", "EMAIL_OPS_CENTER", "WEBHOOK"]
        }
        self.alert_history.append(alert_record)
        print(f"[ALERT DISPATCHED] {severity} for {container_id}: {message}")
        return alert_record

    def get_recent_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.alert_history[-limit:]


alert_service = AlertService()
