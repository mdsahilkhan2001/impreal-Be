from rest_framework import serializers
from .models import Lead, LeadHistory


class LeadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadHistory
        fields = ['id', 'action', 'timestamp', 'user']
        read_only_fields = ['timestamp']


class LeadSerializer(serializers.ModelSerializer):
    history = LeadHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'email', 'phone', 'country', 'product_type',
            'quantity', 'budget', 'message', 'reference_images', 'status',
            'assigned_to', 'user', 'created_at', 'updated_at', 'history'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LeadCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating leads"""
    class Meta:
        model = Lead
        fields = [
            'name', 'email', 'phone', 'country', 'product_type',
            'quantity', 'budget', 'message', 'reference_images', 'user'
        ]
