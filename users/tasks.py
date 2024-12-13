from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives


@shared_task
def send_login_email(subject, message, from_email, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )


@shared_task
def send_welcome_email(user_email, username):
    subject = "Welcome to Medi Track Hospital Management System"
    from_email = "codingfalsafa@example.com"
    recipient_list = [user_email]

    # Plain text fallback
    plain_message = f"""
        Dear {username},
        
        Welcome to Medi Track - Your Comprehensive Hospital Management Solution.
        
        As a User in our system, you now have access to powerful tools to streamline healthcare management:
        
        Login Credentials:
        - Username: {username}
        - Portal: http://localhost:8000/users/login
        
        For technical support, contact our IT helpdesk at support@meditrack.hospital
        
        Best regards,
        Medi Track Administration Team
        """

    # HTML message using the template
    html_message = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to Medi Track</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; background-color: #ECF0F1; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #FFFFFF; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-radius: 8px; overflow: hidden;">
                <div style="background-color: #2C3E50; color: #FFFFFF; text-align: center; padding: 25px; position: relative;">
                    <h1 style="font-size: 28px; font-weight: 300; margin: 0; letter-spacing: 1px;">Medi Track</h1>
                </div>
                <div style="padding: 30px;">
                    <p>Dear <strong>{username}</strong>,</p>
                    <p>Welcome to <strong>Medi Track - Your Comprehensive Hospital Management Solution</strong>.</p>
                    <p>As a User in our system, you now have access to powerful tools to streamline healthcare management:</p>
                    <ul style="background-color: #ECF0F1; border-left: 4px solid #2980B9; padding: 15px 15px 15px 30px; margin: 20px 0; border-radius: 0 4px 4px 0; list-style-position: inside;">
                        <li style="margin-bottom: 10px; color: #34495E;">Advanced Patient Record Management</li>
                        <li style="margin-bottom: 10px; color: #34495E;">Seamless Appointment Scheduling</li>
                        <li style="margin-bottom: 10px; color: #34495E;">Comprehensive Billing and Insurance Tracking</li>
                        <li style="margin-bottom: 10px; color: #34495E;">Intelligent Medical Inventory Management</li>
                    </ul>
                    <div style="background-color: #ECF0F1; border-left: 4px solid #2980B9; padding: 15px; margin: 20px 0; border-radius: 0 4px 4px 0;">
                        <strong>Login Credentials:</strong>
                        <p>
                            Username: <strong>{username}</strong><br>
                            Portal: <a href="http://localhost:8000/users/login" style="color: #2980B9; text-decoration: none;">Login Portal</a>
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <a href="http://localhost:8000/users/login" style="display: inline-block; background-color: #2980B9; color: #FFFFFF; text-decoration: none; padding: 12px 25px; border-radius: 6px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin: 20px 0;">Access Your Portal</a>
                    </div>
                    <p>
                        <strong>Need Assistance?</strong><br>
                        Our dedicated support team is available to help. Contact our helpdesk at 
                        <a href="mailto:support@meditrack.hospital" style="color: #2980B9; text-decoration: none;">support@meditrack.hospital</a>.
                    </p>
                    <p>
                        <strong>Our Commitment:</strong><br>
                        At Medi Track, we prioritize efficiency, security, and patient confidentiality to deliver an exceptional healthcare management experience.
                    </p>
                </div>
                <div style="background-color: #ECF0F1; padding: 20px; text-align: center; font-size: 12px; color: #34495E;">
                    <p>Medi Track Hospital Management System</p>
                    <p>
                        123 Healthcare Ave, Wellness City, HC 45678<br>
                        Phone: +1 234 567 8900 | Email: <a href="mailto:info@meditrack.hospital" style="color: #2980B9; text-decoration: none;">info@meditrack.hospital</a>
                    </p>
                    <p>&copy; 2024 Medi Track. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=from_email,
            to=recipient_list,
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        print(f"Welcome email sent successfully to {user_email}")
    except Exception as e:
        print(f"Failed to send welcome email to {user_email}: {e}")