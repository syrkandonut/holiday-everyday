from django.db.models import CASCADE, OneToOneField, TextField

from .base import Base


class Review(Base):
    text: TextField = TextField(verbose_name="Текст отзыва")
    project: OneToOneField = OneToOneField(
        "agency.Project",
        related_name="review",
        on_delete=CASCADE,
        verbose_name="Проект",
        unique=True,
    )

    class Meta:
        db_table = "reviews"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв проекта {self.project}"
    
    def convert_text(self, text: str) -> str:
        text_list = list(text)  # Преобразуем строку в список для изменения
        for i in range(len(text_list)):
            if text_list[i] == " ":
                for j in range(1, 4):
                    try:
                        if i - j >= 0 and text_list[i - j] == " ":
                            text_list[i - j] = "&nbsp;"
                            break
                    except Exception:
                        continue                  
        return "".join(text_list) 

        
    def save(self, *args, **kwargs):
        self.text = self.convert_text(text=self.text)

        return super().save(*args, **kwargs)
    
