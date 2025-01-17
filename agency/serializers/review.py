from rest_framework.serializers import ModelSerializer

from agency.models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ["text"]
