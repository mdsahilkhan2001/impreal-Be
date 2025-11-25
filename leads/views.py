from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Lead
from .serializers import LeadSerializer, LeadCreateSerializer


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lead management
    - List: ADMIN/SELLER only
    - Create: Any authenticated user
    - Update: ADMIN/SELLER only
    """
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return LeadCreateSerializer
        return LeadSerializer
    
    def get_queryset(self):
        user = self.request.user
        # BUYER sees only their leads
        if user.role == 'BUYER':
            return Lead.objects.filter(user=user)
        # ADMIN/SELLER see all leads
        return Lead.objects.all()
    
    def perform_create(self, serializer):
        # Auto-assign user if BUYER
        user = self.request.user
        if user.role == 'BUYER':
            serializer.save(user=user)
        elif user.role in ['SELLER', 'ADMIN']:
            # Seller can assign to themselves
            serializer.save(assigned_to=user)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def my_leads(self, request):
        """Get leads for current BUYER user"""
        leads = Lead.objects.filter(user=request.user)
        serializer = self.get_serializer(leads, many=True)
        return Response({
            'success': True,
            'count': leads.count(),
            'data': serializer.data
        })
