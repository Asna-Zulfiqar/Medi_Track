from firebase_admin import messaging


def send_notification_to_device(token, title, body, data=None):
    """
    Sends a push notification to a specific device using Firebase Cloud Messaging.

    Args:
        token (str): The device token.
        title (str): Notification title.
        body (str): Notification body.
        data (dict, optional): Additional data payload.

    Returns:
        response: Firebase response.
    """
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            data=data or {},  # Optional additional data
        )
        response = messaging.send(message)
        return response
    except Exception as e:
        print(f"Error sending notification: {e}")
        return None
