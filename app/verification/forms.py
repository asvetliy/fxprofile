from django import forms
from .models import VerificationRequest


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = VerificationRequest
        fields = ['file', 'old_file_name', 'type', 'status', 'user', 'card', ]
