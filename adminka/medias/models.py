from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(verbose_name="Ism", max_length=100)
    username = models.CharField(verbose_name="Telegram username", max_length=100, null=True)
    telegram_id = models.BigIntegerField(verbose_name="Telegram ID", unique=True, default=1)

    class Meta:
        verbose_name = 'Foydalanuvchilar'
        verbose_name_plural = 'Foydalanuvchilar'


class QuranVerseModel(models.Model):
    sura_number = models.IntegerField(verbose_name="Sura tartib raqami", null=True)
    sura_name = models.CharField(verbose_name="Sura nomi", max_length=50, blank=True)
    audio_url = models.CharField(verbose_name="Sura audio url manzili", max_length=150, blank=True)
    photo_url = models.CharField(verbose_name="Sura rasmi url manzili", max_length=150, blank=True)
    zip_id = models.CharField(verbose_name="ZIP ID", max_length=150, blank=True)
    total_verses = models.IntegerField(verbose_name="Umumiy oyatlar soni", null=True)

    class Meta:
        verbose_name = 'QuranVerseByVerse'
        verbose_name_plural = 'QuranVerseByVerse'
