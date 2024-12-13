from celery import shared_task
from django.core.mail import send_mail
from medical_records.models import MedicinePrescription, Patient, LabPrescription

@shared_task
def send_prescription_email_to_patient(prescription_type , prescription_id, patient_id, action):
    try:
        if prescription_type.lower() == 'medicine':
            prescription = MedicinePrescription.objects.get(id=prescription_id)
            subject_prefix = 'Medicine Prescription'
            prescription_details = f"""
                    - Medicine Name: {prescription.medicine_name}
                    - Dosage: {prescription.dosage}
                    - Duration: {prescription.duration or 'As instructed by the doctor'} days
                    - Instructions: {prescription.instructions if prescription.instructions else 'No special instructions'}
                    """
        else:
            prescription = LabPrescription.objects.get(id=prescription_id)  # Adjust for lab prescription
            subject_prefix = 'Lab Test Prescription'
            prescription_details = f"""
                    - Test Name: {prescription.test_name}
                    - Instructions: {prescription.instructions if prescription.instructions else 'No special instructions'}
                    """

            # Get the patient details
        patient = Patient.objects.get(id=patient_id)

        # Email content for the patient
        email_subject = f"{subject_prefix} {action.capitalize()}: {prescription.test_name if prescription_type.lower() == 'lab' else prescription.medicine_name}"
        email_body = f"""
                Dear {patient.user.username},

                We hope this email finds you in good health. This is an official notification from MediTrack Hospital regarding your recent prescription.

                Prescription Information:
                ----------------------------
                Prescription Type: {subject_prefix}
                Action: Your prescription has been {action}.

                Prescription Details:
                {prescription_details}

                **Important Instructions:**
                Please follow the instructions provided for your prescription carefully. It is essential to adhere to the prescribed dosage, duration, and any special instructions provided by your doctor to ensure effective treatment.

                **For Medicine Prescriptions:**
                If you have received a medicine prescription, please contact your nearest pharmacy to collect the prescribed medication. Ensure that you follow the dosage and duration as mentioned. If you are unsure about any aspect of the prescription, please reach out to the pharmacy for clarification.

                **For Lab Test Prescriptions:**
                If you have been prescribed a lab test, please schedule your appointment with the designated laboratory or visit the lab as soon as possible. Ensure that you inform the lab about any special instructions related to the test.

                **Next Steps:**
                - Visit your pharmacy or lab as required.
                - Follow the instructions mentioned above.
                - If you have any questions or concerns regarding the prescription, please contact our support team or consult with your doctor.

                **Contact Support:**
                If you have any doubts or require further assistance, please don’t hesitate to reach out to our support team at:
                - Email: support@meditrack.com
                - Phone: +1-800-123-4567

                We are here to assist you at every step of your healthcare journey.

                Thank you for trusting MediTrack Hospital for your healthcare needs.

                Best regards,
                MediTrack Hospital Management
                """

        # Send email to the patient
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email="codingfalsafa@gmail.com",
            recipient_list=[patient.user.email],
            fail_silently=False,
        )

    except MedicinePrescription.DoesNotExist:
        raise Exception(f"Prescription with ID {prescription_id} does not exist.")
    except Patient.DoesNotExist:
        raise Exception(f"Patient with ID {patient_id} does not exist.")
