import os
from django.conf import settings
from django.views import View
from django.http import FileResponse

class IndexHtmlView(View):
    def get(self, request):
        index_path = os.path.join(settings.BASE_DIR, 'Frontend', 'index.html')
        return FileResponse(open(index_path, 'rb'), content_type='text/html')