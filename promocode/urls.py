from django.urls import path

from promocode.api import GetPromocode, MainModelData

urlpatterns = [

    path('random-promocode/', GetPromocode.as_view()),
    path('main/', MainModelData.as_view(), name='data'),

]