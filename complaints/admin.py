from django.contrib import admin
from .models import Complaint 



# Register your models here.
@admin.register(Complaint)
class SeatAdmin(admin.ModelAdmin):
    
    list_display = [
        "author",
      "complaintype",
        "content",
      "answer"
    ]

