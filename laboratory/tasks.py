from laboratory.models import LabTestAllocation
from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from medical_records.models import TestResult


@shared_task
def send_lab_test_emails(lab_test_allocation_id):
    try:

        lab_test_allocation = LabTestAllocation.objects.get(id=lab_test_allocation_id)

        prescription = lab_test_allocation.prescription
        test_name = prescription.test.test_name
        laboratory = lab_test_allocation.laboratory
        patient = prescription.patient

        # Mock test duration (fallback if not stored in the model)
        test_duration = 3

        # Email to laboratory
        lab_subject = f"Patient Test Request: {test_name}"
        lab_message = f"""
        Dear {laboratory.lab_name},

        We are writing to inform you that a patient has requested the following test at your laboratory.
        - Test Name: {test_name}
        - Patient: {patient.user.username}
        - Patient Email: {patient.user.email}

        Test Details:
        - Test Duration: {test_duration} days
        - Prescription ID: {prescription.id}

        Please ensure that the test is conducted within the expected time frame.

        Best regards,
        MediTrack Hospital Management
        """
        send_mail(
            subject=lab_subject,
            message=lab_message,
            from_email="hospital@example.com",
            recipient_list=[laboratory.email],
            fail_silently=False
        )

        # Email to patient
        patient_subject = f"Test Request Confirmed: {test_name}"
        patient_message = f"""
        Dear {patient.user.username},

        We are pleased to inform you that your request for the {test_name} has been successfully allocated to the laboratory. The test will be conducted by {laboratory.lab_name}, and we have outlined the details below for your reference:

        **Test Details:**
        - Test Name: {test_name}
        - Test Duration: {test_duration} days
        - Laboratory: {laboratory.lab_name}
        - Laboratory Contact: {laboratory.contact}
        - Laboratory Email: {laboratory.email}
        - Expected Result Duration: {test_duration} days

        Please feel free to contact the laboratory directly should you have any inquiries or need further assistance. The test results would be sent to email so Kindly check it from time to time. If the result duration exceed
        the maximum time kindly contact the laboratory.

        Should you have any questions or concerns, our team at MediTrack Hospital is here to assist you.

        Best regards,
        MediTrack Hospital Management
        Contact: 8798-79879 
        Email: meditrack@support.com
        """
        send_mail(
            subject=patient_subject,
            message=patient_message,
            from_email="hospital@example.com",
            recipient_list=[patient.user.email],
            fail_silently=False
        )
    except Exception as e:
        raise Exception(f"Error in sending lab test emails: {str(e)}")

@shared_task
def send_test_result_email_to_patient(test_result_id):
    try:
        # Retrieve the TestResult object
        test_result = TestResult.objects.get(id=test_result_id)
        patient = test_result.patient
        lab_prescription = test_result.lab_prescription

        # Prepare email subject and message
        subject = f"Test Result for {lab_prescription.test.test_name}"
        message = f"""
        Dear {patient.user.username},

        Your test results for the {lab_prescription.test.test_name} are now available.

        Test Result:
        {test_result.result}

        You can find the detailed report attached as a PDF.

        Best regards,
        MediTrack Hospital Management
        """

        # Send email with PDF attachment
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email='codingfalsafa@gmail.com',
            to=[patient.user.email],
        )
        if test_result.file:
            email.attach_file(test_result.file.path)

        email.send()

    except Exception as e:
        print(f"Error sending email: {e}")