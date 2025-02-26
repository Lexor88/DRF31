import stripe
import logging
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from courses.models import Course
from .models import Payment

# Инициализация Stripe API с секретным ключом из настроек
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


class CreateStripeProductView(APIView):
    @extend_schema(
        request=inline_serializer(
            name="CreateProductRequest",
            fields={"course_id": serializers.IntegerField()},
        ),
        responses=inline_serializer(
            name="CreateProductResponse",
            fields={"product_id": serializers.CharField()},
        ),
        description="Создание продукта в Stripe для курса. Продукт будет связан с данным курсом и иметь уникальный идентификатор."
    )
    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)

        try:
            # Создание продукта в Stripe
            product = stripe.Product.create(
                name=course.name,
                description=getattr(course, "description", "")
            )
            # Сохраняем идентификатор продукта в модели курса
            course.stripe_product_id = product.id
            course.save()

            return Response({"product_id": product.id})

        except Exception as e:
            logger.error(f"Stripe product creation error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateStripePriceView(APIView):
    @extend_schema(
        request=inline_serializer(
            name="CreatePriceRequest",
            fields={"course_id": serializers.IntegerField()},
        ),
        responses=inline_serializer(
            name="CreatePriceResponse",
            fields={"price_id": serializers.CharField()},
        ),
        description="Создание цены для курса в Stripe. Цена будет связана с продуктом и указывать стоимость курса."
    )
    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)

        if not course.stripe_product_id:
            return Response({"error": "Stripe product not created for this course."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Создание цены в Stripe для курса
            price = stripe.Price.create(
                product=course.stripe_product_id,
                unit_amount=int(course.price * 100),  # Умножаем на 100, чтобы указать цену в копейках
                currency="usd",
            )
            # Сохраняем идентификатор цены в модели курса
            course.stripe_price_id = price.id
            course.save()

            return Response({"price_id": price.id})

        except Exception as e:
            logger.error(f"Stripe price creation error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateCheckoutSessionView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name="pk", description="ID курса", required=True, type=int),
        ],
        responses=inline_serializer(
            name="CheckoutSessionResponse",
            fields={"checkout_url": serializers.URLField()}
        ),
        description="Создание сессии для оплаты курса через Stripe. Создается ссылка для перехода на страницу оплаты."
    )
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        course = get_object_or_404(Course, id=self.kwargs['pk'])

        if not course.stripe_price_id:
            return Response({"error": "Stripe price not created for this course."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Создание сессии оплаты в Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': course.stripe_price_id,  # Используем ранее созданную цену
                    'quantity': 1,
                }],
                mode='payment',
                success_url="http://127.0.0.1:8000/success/",
                cancel_url="http://127.0.0.1:8000/cancel/",
            )

            # Сохраняем информацию о платеже в нашей базе данных
            Payment.objects.create(
                user=request.user,
                stripe_payment_id=checkout_session.id,
                amount=course.price
            )

            return Response({'checkout_url': checkout_session.url})

        except Exception as e:
            logger.error(f"Stripe checkout session error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)