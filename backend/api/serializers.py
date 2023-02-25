from rest_framework import serializers

from conf import detect_item_path
from api.tools.detect_item import parse_excel
from .models import Document, DocumentResult


class BinaryField(serializers.Field):

    def to_representation(self, value):
        return value.hex()

    def to_internal_value(self, value):
        return value


class WriteDocumentSerializer(serializers.ModelSerializer):
    file = BinaryField()

    def validate_file_type(self, value: str):
        if value not in ['sol', 'zip']:
            raise serializers.ValidationError("error file type")
        return value

    def validate_file(self, value):
        if len(value) > 1024 * 1024 * 2:  # 2MB
            raise serializers.ValidationError("larger file than 2MB")
        return value

    def validate(self, attrs):
        this_time = attrs.get('date')
        user = attrs.get('user')
        last24count = Document.objects.filter(user=user, date__gte=this_time - 86400).count()
        if last24count >= 50:
            raise serializers.ValidationError("at last 24 hours, you have submit 50 contract.")
        return attrs

    class Meta:
        model = Document
        fields = '__all__'


class ReadDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ['file', 'contract', 'result']


class DetectionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file_name', 'contract_address', 'network', 'score']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        network = ret.get("network")
        if network:
            ret['network'] = network.capitalize()
        return ret


class DocumentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentResult
        fields = ('title',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        _, res = parse_excel(detect_item_path)
        item = res.get(ret.get("title"))
        if item:
            ret["id"] = f"TSP-{item.get('id')}"
            ret["level"] = item.get('confidence')
        return ret
