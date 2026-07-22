"""Views for the user profile app."""
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/profile/ — Retrieve current user profile.
    PUT  /api/profile/ — Full update.
    PATCH /api/profile/ — Partial update.
    Auto-creates the profile if it doesn't exist yet.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True  # always allow partial updates
        return super().update(request, *args, **kwargs)
