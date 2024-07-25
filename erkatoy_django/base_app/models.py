from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class Category(models.Model):
    name_uz = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name_uz}-{self.name_ru}"


Lang = [
    ('uz', 'Uz'),
    ('ru', 'Ru'),
]


class Content(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="contents")
    image_for_ertak = models.FileField(verbose_name="ertak uchun rasm", null=True, blank=True,
                                       default=None, upload_to="images/")
    language = models.CharField(max_length=25, choices=Lang)

    title = models.CharField(max_length=256, null=True, blank=True)
    # ertak
    text_for_ertak = RichTextUploadingField(
        verbose_name="text ertak uchun", null=True, blank=True)
    # sher
    text_for_sher = RichTextUploadingField(
        verbose_name="sher uchun text", null=True, blank=True, default=None)
    music_for_sher = models.FileField(verbose_name="sher mp3",
        upload_to="musics/", null=True, blank=True, default=None)
    # qo'shiq
    qoshiq = models.FileField(upload_to='videos',verbose_name="qo'shiq file", null= True, blank= True, default=None)

    # Oyinlar
    text_for_oyin = RichTextUploadingField(
        verbose_name="O'yinlar uchun text", null=True, blank=True, default=None)
    # Mohirlar
    video_for_mohir = models.FileField(verbose_name="mohir qo'llar uchun video", null=True, blank=True,
                                       default=None, upload_to="videos/")
    # rasm
    rasm = models.FileField(verbose_name="Rasmlar", null=True, blank=True,
                                       default=None, upload_to="images/")
    def __str__(self):
        return f"{self.title}-{self.language}"
