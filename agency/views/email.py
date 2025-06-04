from django.core.mail import send_mail
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from agency.serializers.email import EmailDataSerializer
from config.settings import EMAIL_HOST_USER as EMAIL_TARGET


class EmailView(APIView):
    authentication_classes = ()
    
    def post(self, request: Request):
        serializer = EmailDataSerializer(data=request.data)

        if serializer.is_valid():
            name: str = serializer.validated_data["name"]
            phone: str = serializer.validated_data["phone"]
            text: str = serializer.validated_data["text"]

            msg_title: str = self._get_msg_title_by_name(name=name)
            msg_text: str = self._get_msg_text_by_phone_and_text(phone=phone, text=text)

            try:
                send_mail(
                    subject=msg_title,
                    message=msg_text,
                    from_email=EMAIL_TARGET,
                    recipient_list=[EMAIL_TARGET],  # type: ignore
                )
                return Response(
                    status=status.HTTP_204_NO_CONTENT,
                )

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_msg_text_by_phone_and_text(self, phone: str, text: str) -> str:
        return f"Номер телефона: {phone}\nОписание проекта: {text}"

    def _get_msg_title_by_name(self, name: str) -> str:
        return f'Обратная связь сайта {EMAIL_TARGET} от пользователя "{name.title()}".'
