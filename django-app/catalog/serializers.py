from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Album, Song, AlbumTracklistItem, MusicManagerUser
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        return data

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = MusicManagerUser
        fields = ['username', 'password', 'confirm_password', 'display_name', 'role']

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        if value.isnumeric():
            raise serializers.ValidationError('Password cannot be entirely numeric.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        user = MusicManagerUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            display_name=validated_data['display_name'],
            role=validated_data['role']
        )
        return user

class SongSerializer(serializers.ModelSerializer):
    """Basic Song serializer"""
    class Meta:
        model = Song
        fields = '__all__'

class AlbumTracklistItemSerializer(serializers.ModelSerializer):
    """Tracklist item serializer with song details"""
    song = SongSerializer(read_only=True)
    
    class Meta:
        model = AlbumTracklistItem
        fields = ['id', 'song', 'position']

class AlbumSerializer(serializers.ModelSerializer):
    """Album serializer with computed fields for API"""
    cover_image_url = serializers.SerializerMethodField()
    short_description = serializers.CharField(read_only=True)
    release_year = serializers.IntegerField(read_only=True)
    total_playtime = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = [
            'id', 'title', 'artist', 'short_description', 
            'release_year', 'cover_image_url', 'total_playtime'
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return request.build_absolute_uri(obj.cover_image.url)
        return None

    def get_total_playtime(self, obj):
        return obj.total_playtime

class AlbumDetailSerializer(AlbumSerializer):
    """Detailed Album serializer with full tracklist"""
    tracklist = serializers.SerializerMethodField()
    
    class Meta(AlbumSerializer.Meta):
        fields = AlbumSerializer.Meta.fields + ['description', 'price', 'format', 'release_date', 'tracklist']

    def get_tracklist(self, obj):
        track_items = obj.albumtracklistitem_set.all().order_by('position')
        return AlbumTracklistItemSerializer(track_items, many=True).data

class AlbumCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating albums with tracklist"""
    tracklist = AlbumTracklistItemSerializer(many=True, required=False)

    class Meta:
        model = Album
        fields = [
            'title', 'description', 'artist', 'price', 
            'format', 'release_date', 'cover_image'
        ]
