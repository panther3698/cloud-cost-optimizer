import requests

def send_slack_alert(webhook_url: str, alert_type: str, cost: float, resource_name: str, message: str) -> bool:
    """
    Sends a formatted Slack message using an incoming webhook URL.

    Args:
        webhook_url (str): Slack webhook URL
        alert_type (str): Type of alert (e.g., "Cost Spike", "Idle Resource")
        cost (float): Cost value
        resource_name (str): Name of the resource
        message (str): Additional message

    Returns:
        bool: True if sent successfully, False otherwise
    """
    emoji = "💸" if alert_type.lower() == "cost spike" else "🟡"
    slack_message = (
        f"{emoji} *{alert_type} Alert*\n"
        f"*Resource:* `{resource_name}`\n"
        f"*Cost:* `${cost:,.2f}`\n"
        f"{message}"
    )
    payload = {"text": slack_message}
    try:
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    except Exception:
        return