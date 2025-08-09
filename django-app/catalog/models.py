from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta

def validate_release_date(value):
    """Validate that release_date is not more than 3 years in the future"""
    max_future_date = date.today() + timedelta(days=3*365)
    if value > max_future_date:
        raise ValidationError('Release date cannot be more than 3 years in the future.')

class MusicManagerUser(AbstractUser):
    """Custom user model with display_name and role"""
    ROLE_CHOICES = [
        ('artist', 'Artist'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]
    
    display_name = models.CharField(max_length=512)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')

    def __str__(self):
        return self.display_name

class Album(models.Model):
    """Album model with string artist field"""
    FORMAT_CHOICES = [
        ('dd', 'Digital Download'),
        ('cd', 'CD'),
        ('vi', 'Vinyl'),
    ]
    
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    artist = models.CharField(max_length=512)  # String field, not FK
    price = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(999.99)]
    )
    format = models.CharField(max_length=2, choices=FORMAT_CHOICES)
    release_date = models.DateField(validators=[validate_release_date])
    slug = models.SlugField(unique=True, blank=True)
    
    # Many-to-many relationship with Song through AlbumTracklistItem
    tracks = models.ManyToManyField('Song', through='AlbumTracklistItem', blank=True)
    
    class Meta:
        unique_together = ('title', 'artist', 'format')
        ordering = ['title']  # Default ordering to fix pagination warnings

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.artist}")
            slug = base_slug
            counter = 1
            while Album.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.artist}"
    
    @property
    def short_description(self):
        """Return first 100 characters of description"""
        if self.description:
            return self.description[:100] + '...' if len(self.description) > 100 else self.description
        return ''
    
    @property
    def release_year(self):
        """Return year of release"""
        return self.release_date.year
    
    @property
    def cover_image_url(self):
        """Return cover image URL or default"""
        if self.cover_image:
            return self.cover_image.url
        return '/static/default_album_cover.jpg'  # You should add a default image
    
    @property
    def total_playtime(self):
        """Calculate total playtime from tracks"""
        total = 0
        for track_item in self.albumtracklistitem_set.all():
            total += track_item.song.running_time
        return total
    
    @property
    def tracklist(self):
        """Return ordered tracklist"""
        return self.albumtracklistitem_set.all().order_by('position')

class Song(models.Model):
    """Song model - no direct FK to artist/album, only many-to-many through AlbumTracklistItem"""
    title = models.CharField(max_length=512)
    running_time = models.PositiveIntegerField(validators=[MinValueValidator(10)])  # seconds, minimum 10

    class Meta:
        ordering = ['title']  # Default ordering to fix pagination warnings

    def __str__(self):
        return self.title
    
class AlbumTracklistItem(models.Model):
    """
    Through model to connect Album and Song, with a track position.
    """
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['position']
        unique_together = ('album', 'song')

    def __str__(self):
        return f"{self.album.title} - Track {self.position}: {self.song.title}"