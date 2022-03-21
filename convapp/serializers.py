from rest_framework import serializers
from .models import ImgModel

class ImageSerializer(serializers.ModelSerializer):
    """
    Product serializer with all fields
    """
    class Meta:
        """
        Define your model and needed fields here
        """
        model = ImgModel
        fields = ['img']
