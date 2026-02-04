from rest_framework import serializers

from promocode.models import Promocode, MainModel, TestModel


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = "__all__"

class TestModelSerializer(serializers.ModelSerializer):
    file_path = serializers.SerializerMethodField()

    class Meta:
        model = TestModel
        fields = "__all__"

    @staticmethod
    def get_file_path(obj):
        return obj.file.path if obj.file else None

class MainModelSerializer(serializers.ModelSerializer):

    tests = TestModelSerializer( many=True,
        read_only=True)

    class Meta:
        model = MainModel
        fields = "__all__"
