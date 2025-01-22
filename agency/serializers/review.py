from rest_framework.serializers import ModelSerializer, SerializerMethodField

from agency.models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ["text"]

    text = SerializerMethodField()

    def convert_text(self, text: str) -> str:
        new_text = str()
        for i in range(len(text)):
            if text[i] == " ":
                for j in range(1, 4):
                    attempt = 0
                    if i - j >= 0 and text[i - j] == " ":
                        new_text += "&nbsp;"
                        attempt += 1
                    
                if attempt == 0:
                    new_text += " "
            else:
                new_text += text[i]
                    
        return new_text


    def get_text(self, obj: Review):
        return self.convert_text(obj.text) 