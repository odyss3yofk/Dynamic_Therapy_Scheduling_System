from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Child, Therapist, Session, TherapyProgress
import uuid

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChildSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = ('id', 'first_name', 'last_name', 'date_of_birth',
                  'parent', 'parent_name', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def get_parent_name(self, obj):
        return f"{obj.parent.first_name} {obj.parent.last_name}"


class TherapistSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Therapist
        fields = ('id', 'user', 'specialization', 'years_of_experience',
                  'availability', 'full_name', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        username = str(uuid.uuid4())[:30]
        user_data['username'] = username
        user = User.objects.create_user(**user_data)
        therapist = Therapist.objects.create(user=user, **validated_data)
        return therapist


class SessionSerializer(serializers.ModelSerializer):
    child_name = serializers.SerializerMethodField()
    therapist_name = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ('id', 'child', 'child_name', 'therapist', 'therapist_name', 'date',
                  'start_time', 'end_time', 'status', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def get_child_name(self, obj):
        return f"{obj.child.first_name} {obj.child.last_name}"

    def get_therapist_name(self, obj):
        return obj.therapist.user.get_full_name()


class TherapyProgressSerializer(serializers.ModelSerializer):
    session_details = SessionSerializer(source='session', read_only=True)

    class Meta:
        model = TherapyProgress
        fields = ('id', 'session', 'session_details', 'assessment',
                  'rating', 'remarks', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class TherapistRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Auto-generate a unique username
        username = str(uuid.uuid4())[:30]

        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type='therapist'
        )
        Therapist.objects.create(user=user)
        return user


class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'date_of_birth', 'parent']

    def create(self, validated_data):
        return Child.objects.create(**validated_data)
