from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user management"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user statistics"""
        user = request.user
        
        # Get prediction statistics
        from predictions.models import PredictionSession
        total_sessions = PredictionSession.objects.filter(user=user).count()
        completed_sessions = PredictionSession.objects.filter(user=user, status='completed').count()
        
        return Response({
            'total_prediction_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'success_rate': (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
        })
