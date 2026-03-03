from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DoctorProfile
from patients.models import PatientProfile


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role", "phone_number", "country")
        read_only_fields = ("id", "role")


class PatientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name", "phone_number", "country")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(role=User.Roles.PATIENT, **validated_data)
        user.set_password(password)
        user.save()
        PatientProfile.objects.create(user=user)
        return user


class DoctorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    specialization = serializers.CharField(write_only=True)
    license_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "specialization",
            "license_number",
        )

    def create(self, validated_data):
        specialization = validated_data.pop("specialization")
        license_number = validated_data.pop("license_number")
        password = validated_data.pop("password")
        user = User.objects.create_user(role=User.Roles.DOCTOR, **validated_data)
        user.set_password(password)
        user.save()
        DoctorProfile.objects.create(
            user=user,
            specialization=specialization,
            license_number=license_number,
        )
        return user

