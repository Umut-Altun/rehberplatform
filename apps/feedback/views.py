from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt # Sadece test için, production'da dikkatli kullanın
from .forms import ErrorReportForm
from .models import ErrorReport
from django.utils.translation import gettext_lazy as _

@require_POST
#@csrf_exempt # AJAX POST için CSRF token'ı JavaScript ile göndermeniz gerekecek
def submit_error_report(request):
    """Handles the submission of the error report form via AJAX."""
    form = ErrorReportForm(request.POST or None)
    if form.is_valid():
        try:
            report = form.save(commit=False)
            if request.user.is_authenticated:
                report.user = request.user
            report.page_url = form.cleaned_data.get('page_url', '') # URL'yi formdan al
            report.save()
            return JsonResponse({'success': True, 'message': _("Hata bildiriminiz başarıyla alındı. Teşekkür ederiz!")})
        except Exception as e:
            # Log the exception e
            return JsonResponse({'success': False, 'message': _("Bildirim kaydedilirken bir sunucu hatası oluştu.")}, status=500)
    else:
        # Form hatalarını daha detaylı döndürebiliriz
        errors = {field: error[0] for field, error in form.errors.items()}
        return JsonResponse({'success': False, 'message': _("Formda hatalar var. Lütfen kontrol edin."), 'errors': errors}, status=400)

# Bu view, modal içindeki formu yüklemek için kullanılabilir (isteğe bağlı)
# Eğer modal ilk açıldığında boş bir form gösteriyorsak buna gerek yok.
# Ama eğer formu context ile render edip modal'a göndermek istersek kullanabiliriz.
# from django.template.loader import render_to_string
# def get_error_report_form(request):
#     form = ErrorReportForm()
#     html = render_to_string('partials/_error_form_content.html', {'error_report_form': form}, request=request)
#     return JsonResponse({'html': html}) 