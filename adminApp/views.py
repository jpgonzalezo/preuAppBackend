from django.shortcuts import render
from rest_framework import generics
from adminApp.models.region import Region
from adminApp.serializaers.region import RegionSerializer
# Create your views here.

class RegionList(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class RegionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
