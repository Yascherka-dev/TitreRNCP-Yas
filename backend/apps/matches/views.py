from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Match
from .serializers import MatchSerializer

class MatchListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = MatchSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')
        if date:
            return Match.objects.filter(date_heure__date=date)
        return Match.objects.all()
