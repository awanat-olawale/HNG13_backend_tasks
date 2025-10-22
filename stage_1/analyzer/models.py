from django.db import models

from django.db import models

class AnalyzedString(models.Model):
    value = models.TextField(unique=True)           
    sha256_hash = models.CharField(max_length=64, unique=True)
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.value

