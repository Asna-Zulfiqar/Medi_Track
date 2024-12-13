# Medi_Track

## Description
Medi_Track is a comprehensive Hospital Management System (HMS) web application built using Django Rest Framework. It streamlines operations within hospitals and healthcare facilities by providing features for patient management, appointment scheduling, medical records management, billing, and staff management, while ensuring user authentication and role-based authorization.

## Features
### User Authentication and Authorization ( App: users )
- **Token-based authentication**: Users can authenticate by creating a token via email.
- **User roles**: Users are assigned roles according to their choice.
- **Permissions**: Specific permissions are assigned to users based on their roles.
- **Welcome Email**: Welcome email is sent upon Registering from Medi Track to user.

### Doctor Management ( App : doctors )
- **Doctor Profile**: Maintains profiles for doctors, including specialization, contact details, and availability.
- **Prescription Management**: Allow doctors to prescribe lab tests and medicines to patients, with proper record-keeping of prescriptions and associated details.
- **Patient Details**: Doctors can easily check the Patient Profile and Medical history by providing patient id in the query parameters.
- **Medical Records** : Doctors can easily change and add info to a Patient Medical Record by accessing the record using the patient id in query parameter.
 
### Patient Management ( App : patients )
- **Patient Registration**: Collects personal details (name, age, gender, contact, etc.).
- **Checking of Emergency Cases**:An email notification is automatically sent to the receptionist on duty when a new patient registers in the system to check for emergency cases.
- **Appointment Management**: Allow patients to schedule, reschedule, or cancel appointments with doctors, with notifications and reminders.
- **Prescription Tracking**: Track prescriptions issued to patients, including details of prescribed medicines and lab tests, ensuring proper follow-up.
- **Medical History**: Maintains a record of previous conditions, surgeries, allergies, and more.
- **Patient Dashboard**: A personal dashboard for patients to view and to update personal information, medical history etc.
- **Patient Portal**: Allows patients to view upcoming appointments , test results ,lab reports and request prescriptions.
- **Patient Medical Record** : Patient can easily check their medical record anytime they want.
- **Lab Test Management**: Enable patients to request and receive lab tests, with associated test results and prescribed treatments being linked to their profiles.

### Appointment Management ( App : appointments )
- **Appointment Scheduling**: Allow patients to schedule appointments with doctors, including the selection of available time slots and specialties.ors.
- **Rescheduling & Cancellations**: Enable patients to reschedule or cancel appointments with doctors, while notifying the relevant parties.
- **Appointment Notifications**: Send automated notifications and reminders to patients and doctors about upcoming appointments via email.
- **Appointment Reminders**: Appointments Reminders are send 1 hour before the appointment to the doctor and patient.
- **Appointment History**: Tracks previous and upcoming appointments for patients and doctors.
- **Appointment Status**: Set and track the status of appointments, such as "Scheduled", "Rescheduled", "Completed", or "Canceled."

### Staff Management ( App : staff )
- **Staff Profile Management**: Staff like nurses , sweepers , security guard etc can manage their profiles.
- **Shift Management**: Create shifts for staff (nurses, doctors) and assign them to specific time slots and wards.
- **Staff Leave Management**: Track leave requests and approval processes for hospital staff.

### Medical Records Management ( App : medical_records )
- **Electronic Health Records (EHR)**: Store all patient data including diagnoses, medications, lab results, and treatment plans.
- **Prescription Management**: Track and manage prescriptions issued to patients, linking them to specific doctor consultations and treatments.
- **Lab Test Records**: Record lab test results, including test names, dates, and results, and link them to patient profiles for easy reference by doctors and patients.
- **Medical Imaging**: Upload images (e.g., CT scans) related to patient records in PDF format.

### Billing and Invoicing ( App : billing )
- **Patient Billing**: Generate bills for services rendered, including consultations and tests upon user requests.
- **Payment History**: Tracks payments made by patients and outstanding balances.
- **Discounts**: Apply discounts based on patients income.
- **Track of All the Hospital Bills**: Tracking all the Hospital Bills paid or unpaid.The Accountant will be able to update the patients bill status as paid or unpaid.

### Inventory and Pharmacy Management (App : pharmacy )
- **Medicine Inventory**: Track stock of medicines, including expiration dates and reordering levels.
- **Medicine Allocations**: Allows patients to request a specific medicine from a pharmacy, checking its availability and stock. If available, the requested medicine is allocated to the patient, and the pharmacy's stock is updated accordingly.
- **Track Dispensed Medicine**: Record and track the dispensing of medicines to patients, ensuring accurate inventory management and patient records for prescriptions.
- **Inventory Alerts**: Send  email to pharmacy  when a medicine reaches low-stock.

### Laboratory Management (App: laboratory)
- **Test Inventory**: Track a list of available lab tests, including their descriptions, durations, and pricing.
- **Lab Test Allocations**: Enable patients to request specific lab tests. Allocate tests to laboratories, track the status of test requests, and ensure timely completion.
- **Patient-Laboratory Notifications**: Automatically send notifications to laboratories about test allocations and updates to patients regarding test details, laboratory assignments, and completion statuses.
- **Result Tracking**: Manage and monitor test results, ensuring they are delivered to patients promptly.

### Ward and Bed Management ( App : wards)
- **Bed Allocation**: Assign patients to beds based on room types (general, ICU).
- **Bed Availability**: Track the status of each bed (occupied, free, cleaning).
- **Ward Management**: Monitor capacity and allocate resources efficiently.
- Each ward has 3 managers that will take shifts to manage the ward. Once a ward has 3 managers no other person can be the ward manager. Each ward has 40 beds that are managed by the Ward Manager. These beds will be assigned automatically once the ward is established. A ward that is already established cannot be established again. A ward Manager can take only one shift and can exercise his authority within this shift.

### Notifications ( App : notifications )
- **Patient Alerts**: Notify patients of important events such as bill payments and discharge information.
- **Doctor Alerts** : Notify Doctors of important events such as Appointments etc.
- **Emergency Alerts** : Notify the Ward Manager in case of emergency patients.
- **Staff Alerts**: Notify staff of their work and other details accordingly.
- This was supposed to be done through firebase( firebase is not setup properly). So instead all this info will be sent through emails

### Emergency and Critical Care 
- **Emergency Services**: Track and prioritize incoming emergency patients. The receptionist will check for the emergency patients and in case of emergency patient an email will be immediately sent to the Ward Manager of ICU that is on the shift about the patient.
- **Critical Care Units**: Manage ICU or critical areas.

### Medical Staff Performance and Feedback ( App : feedback )
- **Performance Tracking**: Monitor performance through patient feedback and consultation metrics.
- **Patient Feedback System**: Collect feedback on treatment quality and service.
- **Ratings and Reviews**: Patients can rate their doctors and services.

## Project Setup

### Installation Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Asna-Zulfiqar/medi_track.git
   cd medi_track

2. **Set Up a Virtual Environment**
 Create and activate a virtual environment to manage dependencies.
 
    ```bash
   # Create a virtual environment
    python3 -m venv venv
   
   # Activate the virtual environment

    # On Windows
    venv\Scripts\activate
   
    # On macOS/Linux
    source venv/bin/activate

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

4. **Set Up the Database**
 Run the following commands to apply migrations and set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Create a Superuser**
 Create a superuser to access the Django admin panel
    ```bash
    python manage.py createsuperuser

6. **Run the Development Server**
 Start the development server to access the application
    ```bash
   python manage.py runserver
 
 Access the app at http://127.0.0.1:8000/.  
 
### Additional Notes
Start Celery Beat and Worker:

To handle background tasks with Celery, you need to run both Celery Beat and Celery Worker in separate terminals:

Start Celery Worker: In one terminal, run the following command to start the Celery worker

    celery -A medi_track worker --loglevel=info

Start Celery Beat: In another terminal, run the following command to start Celery Beat for periodic tasks

    celery -A medi_track beat --loglevel=info


