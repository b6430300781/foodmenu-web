from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()   # 🥬 วัตถุดิบ
    steps = models.TextField()         # 🍳 วิธีทำ
    image = models.ImageField(upload_to='menus/', null=True, blank=True)  # 🖼️ รูป