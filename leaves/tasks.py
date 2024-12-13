from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_leave_applied_email_to_administrator(user_name, leave_reason, start_date, end_date):
    subject = "Leave Application Submitted - Action Required"
    message = f"""
    Dear Emily,

    We hope this message finds you well.

    We would like to inform you that a staff member has submitted a leave application for your review and approval. Below are the details of the application:

    - **Staff Name:** {user_name}
    - **Leave Reason:** {leave_reason}
    - **Leave Start Date:** {start_date.strftime('%B %d, %Y')}
    - **Leave End Date:** {end_date.strftime('%B %d, %Y')}
    - **Total Duration:** {(end_date - start_date).days} days

    Please review the request at your earliest convenience. If you need any further information or have any questions, feel free to reach out to the Medi Track Team.

    We appreciate your prompt attention to this matter.

    Kind regards,  
    The MediTrack Hospital Management Team

    **Note:** This is an automated notification. For any immediate assistance, please contact HR directly.
    """

    send_mail(
        subject=subject,
        message=message,
        from_email='codingfalsafa@gmail.com',
        recipient_list=['asna.zulfiqar001@gmail.com'],
        fail_silently=False,
    )


@shared_task
def send_leave_email_to_staff(user_email, user_name, start_date, end_date, status):
    if status == 'Applied':
        subject = "Leave Application Submitted Successfully"
        message = f"""
        Dear {user_name},

        Your leave application has been submitted successfully. Below are the details:

        - **Start Date:** {start_date.strftime('%B %d, %Y')}
        - **End Date:** {end_date.strftime('%B %d, %Y')}

        Our team will review your request and notify you about the decision. We appreciate your patience.

        Regards,
        HR Management System
        """
    elif status == 'Approved':
        subject = "Leave Application Approved"
        message = f"""
        Dear {user_name},

        We are pleased to inform you that your leave application has been approved. Below are the details:

        - **Start Date:** {start_date.strftime('%B %d, %Y')}
        - **End Date:** {end_date.strftime('%B %d, %Y')}
        - **Total Leave Duration:** {(end_date - start_date).days} days

        You can now proceed with your leave as scheduled. Please ensure that all pending tasks are handed over to the appropriate team members before your leave begins.

        Should you have any questions or need assistance, feel free to reach out to the HR team.

        Regards,
        HR Management System
        """
    elif status == 'Rejected':
        subject = "Leave Application Rejected"
        message = f"""
        Dear {user_name},

        We regret to inform you that your leave application has been rejected. Below are the details:

        - **Requested Start Date:** {start_date.strftime('%B %d, %Y')}
        - **Requested End Date:** {end_date.strftime('%B %d, %Y')}

        Unfortunately, your leave request does not meet the current requirements or business needs. If you have any questions or would like to discuss the decision further, please contact the HR team.

        We appreciate your understanding.

        Regards,
        HR Management System
        """

    send_mail(
        subject=subject,
        message=message,
        from_email='codingfalsafa@gmail.com',
        recipient_list=[user_email],
        fail_silently=False,
    )
