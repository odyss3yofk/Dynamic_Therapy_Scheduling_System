from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Child, Therapist, Session, TherapyProgress
from .serializers import (
    UserSerializer, ChildSerializer, TherapistSerializer,
    SessionSerializer, TherapyProgressSerializer
)
from pulp import *

User = get_user_model()


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated before accessing user_type
        return request.user.is_authenticated and request.user.user_type == 'admin'


class IsTherapist(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated before accessing user_type
        return request.user.is_authenticated and request.user.user_type == 'therapist'


class IsParent(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated before accessing user_type
        return request.user.is_authenticated and request.user.user_type == 'parent'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'parent':
            return Child.objects.filter(parent=self.request.user)
        return Child.objects.all()


class TherapistViewSet(viewsets.ModelViewSet):
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer
    permission_classes = [IsAdmin]


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'parent':
            return Session.objects.filter(child__parent=self.request.user)
        elif self.request.user.user_type == 'therapist':
            return Session.objects.filter(therapist__user=self.request.user)
        return Session.objects.all()

    @action(detail=False, methods=['post'])
    def schedule_sessions(self, request):
        # Get all available therapists and their availability
        therapists = Therapist.objects.all()
        sessions = Session.objects.filter(
            status='scheduled', therapist__isnull=True)

        # Create PuLP problem
        prob = LpProblem("Therapist_Scheduling", LpMinimize)

        # Decision variables
        x = LpVariable.dicts("assign",
                             ((s.id, t.id)
                              for s in sessions for t in therapists),
                             cat='Binary')

        # Objective function (minimize total assignments)
        prob += lpSum(x[s.id, t.id] for s in sessions for t in therapists)

        # Constraints
        # Each session must be assigned to exactly one therapist
        for s in sessions:
            prob += lpSum(x[s.id, t.id] for t in therapists) == 1

        # Each therapist can only be assigned to one session at a time
        for t in therapists:
            for s1 in sessions:
                for s2 in sessions:
                    if s1.id < s2.id and s1.date == s2.date:
                        if (s1.start_time <= s2.end_time and s2.start_time <= s1.end_time):
                            prob += x[s1.id, t.id] + x[s2.id, t.id] <= 1

        # Solve the problem
        prob.solve()

        # Update session assignments
        for s in sessions:
            for t in therapists:
                if value(x[s.id, t.id]) == 1:
                    s.therapist = t
                    s.save()

        return Response({'status': 'Sessions scheduled successfully'})


class TherapyProgressViewSet(viewsets.ModelViewSet):
    queryset = TherapyProgress.objects.all()
    serializer_class = TherapyProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'parent':
            return TherapyProgress.objects.filter(session__child__parent=self.request.user)
        elif self.request.user.user_type == 'therapist':
            return TherapyProgress.objects.filter(session__therapist__user=self.request.user)
        return TherapyProgress.objects.all()


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('login')
