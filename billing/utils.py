from billing.models import HospitalBill, Billing
from weasyprint import HTML
from django.template.loader import render_to_string
from medical_records.models import Surgery
from patients.models import Patient
from appointments.models import Appointment
from laboratory.models import LabTestAllocation
from pharmacy.models import MedicineAllocation
from wards.models import Ward
from billing.models import Accountant
from billing.tasks import send_bill_email_to_accountant

def generate_bill(patient_id):

    # Fetch patient and related data
    patient = Patient.objects.get(id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    surgery_details = Surgery.objects.filter(patient=patient)
    medical_record = patient.medical_record.first()
    medicines_allocations = MedicineAllocation.objects.filter(patient=patient)
    for allocation in medicines_allocations:
        allocation.total_price = allocation.medicine.price * allocation.quantity
    lab_tests_allocations = LabTestAllocation.objects.filter(patient=patient)
    ward_stay = None
    if medical_record:
        ward_stay = medical_record.ward_admitted_to

    # Check if a Billing record already exists for the patient
    billing, created = Billing.objects.get_or_create(patient=patient)

    # Trigger the recalculations and save the Billing record
    billing.save()

    # Calculate ward stay details
    ward_detail = None
    if ward_stay:
        days_stayed = (medical_record.discharge_date - medical_record.ward_admit_date).days
        ward_detail = {
            'ward_name': medical_record.ward_admitted_to.ward_type,
            'daily_fee': medical_record.ward_admitted_to.daily_bed_fee,
            'days_stayed': days_stayed,
            'total_fee': days_stayed * medical_record.ward_admitted_to.daily_bed_fee
        }

    if medical_record.ward_admitted_to.ward_type == 'ICU':
        emergency_patient = 'Yes'
    else:
        emergency_patient = 'No'

    # Fetching an Accountant
    accountant = None
    if not medical_record or not medical_record.ward_admitted_to:
        # Fetch accountant for General Ward if no specific ward is assigned
        general_ward = Ward.objects.filter(ward_type='General Ward').first()
        if general_ward:
            accountant = Accountant.objects.filter(
                ward=general_ward, is_available=True
            ).first()
    else:
        # Fetch accountant for the specific ward where the patient is admitted
        specific_ward = medical_record.ward_admitted_to
        accountant = Accountant.objects.filter(
            ward=specific_ward, is_available=True
        ).first()

    discount = billing.discount * 100

    # Check if a HospitalBill already exists for the patient
    hospital_bill = HospitalBill.objects.filter(patient=patient).first()

    if not hospital_bill:
        HospitalBill.objects.create(
            patient=patient,
            total_amount=billing.total_amount,
            status="unpaid",
        )


    # Context for rendering
    context = {
        'patient': patient,
        'emergency_patient': emergency_patient,
        'consultations': appointments,
        'ward_detail': ward_detail ,
        'medicines_allocations': medicines_allocations,
        'procedure': surgery_details,
        'tests_allocation': lab_tests_allocations,
        'subtotal': billing.amount_before_discount,
        'discount': discount,
        'total': billing.total_amount,
        'accountant': accountant,
    }

    # Render the template
    html_content = render_to_string('bill.html', context)
    pdf_file = HTML(string=html_content).write_pdf()

    # Triggering the email notification task if an accountant exists
    if accountant:
        send_bill_email_to_accountant.delay(accountant.id)
    else:
        # Log a warning or handle the absence of an accountant
        print("No accountant available to notify.")

    return pdf_file
