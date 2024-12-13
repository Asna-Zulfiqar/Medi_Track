from rest_framework.generics import  RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from billing.models import Accountant
from staff.models import Receptionist, SecurityGuard, Sweeper, Nurse
from staff.serializers import ReceptionistSerializer, SecurityGuardSerializer, SweeperSerializer, NurseSerializer, \
    AccountantSerializer
from staff.permissions import IsSecurityGuardGroup, IsNurseGroup, IsSweeperGroup, IsReceptionistGroup, IsAccountantGroup


# Receptionist Views
class ReceptionistDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReceptionistSerializer
    permission_classes = [IsAuthenticated, IsReceptionistGroup]

    def get_object(self):
        # Get the current logged-in user
        user = self.request.user

        # Fetch or create the Receptionist object associated with the current user
        receptionist, created = Receptionist.objects.get_or_create(user=user)

        return receptionist

    def get_queryset(self):
        return Receptionist.objects.filter(user=self.request.user)



# Security Guard Views
class SecurityGuardDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = SecurityGuardSerializer
    permission_classes = [IsAuthenticated, IsSecurityGuardGroup]

    def get_object(self):
        # Get the current logged-in user
        user = self.request.user

        # Fetch or create the SecurityGuard object associated with the current user
        security_guard, created = SecurityGuard.objects.get_or_create(user=user)

        return security_guard

    def get_queryset(self):
        return SecurityGuard.objects.filter(user=self.request.user)


# Sweeper Views
class SweeperDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = SweeperSerializer
    permission_classes = [IsAuthenticated, IsSweeperGroup]

    def get_object(self):
        # Get the current logged-in user
        user = self.request.user

        # Fetch or create the Sweeper object associated with the current user
        sweeper, created = Sweeper.objects.get_or_create(user=user)

        return sweeper

    def get_queryset(self):
       return Sweeper.objects.filter(user=self.request.user)


# Nurse Views
class NurseDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = NurseSerializer
    permission_classes = [IsAuthenticated, IsNurseGroup]

    def get_object(self):
        # Get the current logged-in user
        user = self.request.user

        # Fetch or create the Nurse object associated with the current user
        nurse, created = Nurse.objects.get_or_create(user=user)
        return nurse

    def get_queryset(self):
        return Nurse.objects.filter(user=self.request.user)


# Accountant Views
class AccountantDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AccountantSerializer
    permission_classes = [IsAuthenticated, IsAccountantGroup]

    def get_object(self):
        # Get the current logged-in user
        user = self.request.user

        # Fetch or create the Accountant object associated with the current user
        accountant, created = Accountant.objects.get_or_create(user=user)
        return accountant

    def get_queryset(self):
        return Accountant.objects.filter(user=self.request.user)
