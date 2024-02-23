from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import tasks
from .serializers import CardStatusSerializer
from .models import CardStatus
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='GET',
    manual_parameters=[
        openapi.Parameter('card_id', openapi.IN_QUERY, description="Card ID", type=openapi.TYPE_STRING),
        openapi.Parameter('user_mobile', openapi.IN_QUERY, description="User Mobile", type=openapi.TYPE_STRING),
    ],
    operation_summary="Get Card Status by Card ID or User Mobile",
    responses={
        200: openapi.Response(description="Success", schema=CardStatusSerializer(many=True)),
        400: openapi.Response(description="Bad Request", schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
        })),
    }
)
@api_view(['GET'])
def get_card_status(request):
    card_id = request.query_params.get('card_id')
    user_mobile = request.query_params.get('user_mobile')
    card_status_queryset = CardStatus.objects.all()

    if not card_id and not user_mobile:
        return Response({"status": "error", "message": "Please provide either card_id or user_mobile."},
                        status=status.HTTP_400_BAD_REQUEST)

    if card_id:
        card_status_queryset = card_status_queryset.filter(card_id=card_id)
    if user_mobile:
        card_status_queryset = card_status_queryset.filter(user_mobile=user_mobile)

    serializer = CardStatusSerializer(card_status_queryset, many=True)
    return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)



csv_files = {
    "pickup": "card_status\\card-data\\Sample Card Status Info - Pickup.csv",
    "delivery_exceptions": "card_status\\card-data\\Sample Card Status Info - Delivery exceptions.csv",
    "delivered": "card_status\\card-data\\Sample Card Status Info - Delivered.csv",
    "returned": "card_status\\card-data\\Sample Card Status Info - Returned.csv"
}


@swagger_auto_schema(
    method='POST',
    operation_summary="Update Card Status Data From Delivered CSV Source using Celery Worker",
    responses={
        202: openapi.Response(description="Accepted", schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
        })),
    }
)
@api_view(['POST'])
def refresh_delivered(request):
    tasks.delivered_csv_updated.delay(csv_files['delivered'])
    return Response({"status": "success", "message": "Updating Delivered Data."}, status=status.HTTP_202_ACCEPTED)



@swagger_auto_schema(
    method='POST',
    operation_summary="Update Card Status Data From Delivery Exceptions CSV Source using Celery Worker",
    responses={
        202: openapi.Response(description="Accepted", schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
        })),
    }
)
@api_view(['POST'])
def refresh_delivery_exceptions(request):
    tasks.delivery_exceptions_csv_updated.delay(csv_files['delivery_exceptions'])
    return Response({"status": "success", "message": "Updating Delivery Exceptions Data."}, status=status.HTTP_202_ACCEPTED)



@swagger_auto_schema(
    method='POST',
    operation_summary="Update Card Status Data From Pickup CSV Source using Celery  Worker",
    responses={
        202: openapi.Response(description="Accepted", schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
        })),
    }
)
@api_view(['POST'])
def refresh_pickup(request):
    tasks.pickup_csv_updated.delay(csv_files['pickup'])
    return Response({"status": "success", "message": "Updating pickup Data."}, status=status.HTTP_202_ACCEPTED)



@swagger_auto_schema(
    method='POST',
    operation_summary="Update Card Status Data From Retuned CSV Source using Celery Worker",
    responses={
        202: openapi.Response(description="Accepted", schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
        })),
    }
)
@api_view(['POST'])
def refresh_returned(request):
    tasks.returned_csv_updated.delay(csv_files['returned'])
    return Response({"status": "success", "message": "Updating returned Data."}, status=status.HTTP_202_ACCEPTED)


