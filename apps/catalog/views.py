from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.catalog.models import DealerRequest
from apps.catalog.serializers import DealerRequestSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def create_dealer_request(request):
    """
    Создание новой заявки на дилерство
    
    POST /api/catalog/dealer-request/
    
    Body:
    {
        "name": "Имя",
        "company": "Название компании",
        "email": "email@example.com",
        "message": "Текст обращения"
    }
    """
    serializer = DealerRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Заявка успешно отправлена",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        {
            "success": False,
            "message": "Ошибка при отправке заявки",
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )
