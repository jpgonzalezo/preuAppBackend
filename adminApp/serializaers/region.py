from rest_framework import serializers
from adminApp.models.region import Region

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id','nombre')
