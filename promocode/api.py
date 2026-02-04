import random

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from promocode.models import Promocode, MainModel
from promocode.serializers import MainModelSerializer


class GetPromocode(APIView):
    def get(self, request, *args, **kwargs):

        promocodes = Promocode.objects.all()

        if not promocodes.exists():
            return Response({"detail": "No promocodes available"}, status=status.HTTP_404_NOT_FOUND)

        random_promocode = random.choice(promocodes)

        return Response(random_promocode.promocode)

class MainModelData(generics.ListAPIView):
    queryset = MainModel.objects.all()
    serializer_class = MainModelSerializer