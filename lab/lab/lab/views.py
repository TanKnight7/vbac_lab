# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

class DocsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(
            {},                      # context
            template_name="docs.html"
        )
