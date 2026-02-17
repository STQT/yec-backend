from rest_framework import serializers
from apps.catalog.models import DealerRequest


class DealerRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для заявок на дилерство"""
    
    class Meta:
        model = DealerRequest
        fields = ['name', 'company', 'email', 'message']
    
    def validate_email(self, value):
        """Валидация email"""
        if not value:
            raise serializers.ValidationError("Email обязателен для заполнения")
        return value
    
    def validate_name(self, value):
        """Валидация имени"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Имя должно содержать минимум 2 символа")
        return value.strip()
    
    def validate_company(self, value):
        """Валидация названия компании"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Название компании должно содержать минимум 2 символа")
        return value.strip()
    
    def validate_message(self, value):
        """Валидация сообщения"""
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Текст обращения должен содержать минимум 10 символов")
        return value.strip()
