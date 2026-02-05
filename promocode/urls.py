from django.urls import path

from promocode.api import GetPromocode, MainModelData

urlpatterns = [

    path('random-promocode/', GetPromocode.as_view(), name='random-promocode'),
    path('main/', MainModelData.as_view(), name='mainmodel-data'),

]