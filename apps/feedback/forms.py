from django import forms
from .models import ErrorReport
from django.utils.translation import gettext_lazy as _

class ErrorReportForm(forms.ModelForm):
    """Form for submitting error reports."""
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}), 
        help_text=_("Lütfen hatayı detaylı açıklayın.")
    )

    page_url = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ErrorReport
        fields = ['report_type', 'description', 'page_url']
        labels = {
            'report_type': _('Hata Türü'),
            'description': _('Açıklama'),
        } 