from rest_framework.permissions import BasePermission

class IsDoctorGroup(BasePermission):
    # Allows access only to users in the 'Doctor' group.
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Doctor').exists()

class IsReceptionistGroup(BasePermission):
    # Allows access only to users in the 'Receptionist' group.
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Receptionist').exists()

class IsPatientGroup(BasePermission):
    # Allows access only to users in the 'Patient' group.
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Patient').exists()


class CanViewMedicalRecord(BasePermission):
    """
    Permission to allow viewing and editing of medical records for specific groups.
    - Patients and Nurses can view but not edit medical records.
    - Doctors, Lab Technicians, Pharmacists, and Receptionists can view and edit medical records.
    """

    def has_permission(self, request, view):
        # Check if the user belongs to one of the allowed groups for viewing or editing medical records
        allowed_groups = ["Patient", "Nurse", "Doctor", "Lab Technician",  "Receptionist"]
        user_groups = request.user.groups.values_list("name", flat=True)

        # If the user belongs to any of the allowed groups, grant access to view or edit
        return any(group in allowed_groups for group in user_groups)

    def has_object_permission(self, request, view, obj):
        user_groups = request.user.groups.values_list("name", flat=True)

        # Patients can only view their own records, they can't modify it
        if "Patient" in user_groups:
            return obj.patient.user == request.user and request.method in ["GET", "HEAD", "OPTIONS"]

        # Nurses can view but cannot edit any medical records
        if "Nurse" in user_groups:
            return request.method in ["GET", "HEAD", "OPTIONS"]

        # Doctors, Lab Technicians, Pharmacists, and Receptionists can view and modify medical records
        if any(group in user_groups for group in ["Doctor", "Lab Technician", "Receptionist"]):
            # Allow for any method to modify (PUT, PATCH, DELETE)
            return True

        # Deny access if the user doesn't belong to any of the authorized groups
        return False

class IsStaffMember(BasePermission):
    def has_permission(self, request, view):
        staff_groups = ['Doctor', 'Nurse', 'Receptionist', 'Security Guard', 'Sweeper', 'Ward Manager' , 'Accountant']
        return request.user.is_authenticated and request.user.groups.filter(name__in=staff_groups).exists()

class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='CEO').exists()

class IsLabTechnicianGroup(BasePermission):
    # Allows access only to users in the 'Lab Technician' group.
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Lab Technician').exists()

class IsPharmacistGroup(BasePermission):
    # Allows access only to users in the 'Pharmacist' group.
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Pharmacist').exists()

class IsWardManagerGroup(BasePermission):
    # Allows access only to users in the 'Ward Manager' group.
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Ward Manager').exists()

class IsSweeperGroup(BasePermission):
    # Allows access only to users in the 'Sweeper' group.
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Sweeper').exists()

class IsNurseGroup(BasePermission):
    # Allows access only to users in the 'Nurse' group.
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Nurse').exists()

class IsSecurityGuardGroup(BasePermission):
    # Allows access only to users in the 'Security Guard' group.
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Security Guard').exists()

class IsAccountantGroup(BasePermission):
    # Allows access only to users in the 'Accountant' group.
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Accountant').exists()