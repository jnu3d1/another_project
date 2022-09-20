from rest_framework import serializers

from webapp.models import Project


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50, required=True)
    description = serializers.CharField(max_length=3000)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(read_only=True)

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
