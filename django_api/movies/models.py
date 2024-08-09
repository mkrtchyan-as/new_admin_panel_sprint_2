import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name=_('created_at'), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(
        verbose_name=_('modified_at'), auto_now=True, blank=True, null=True)


class UUIDMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Genre(TimeStampedMixin, UUIDMixin):
    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name


class Person(TimeStampedMixin, UUIDMixin):
    class Meta:
        db_table = 'content\".\"person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    full_name = models.CharField(_('full name'), max_length=255)

    def __str__(self):
        return self.full_name


class FilmWork(TimeStampedMixin, UUIDMixin):
    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = _('Film Work')
        verbose_name_plural = _('Film Works')
        indexes = [
            models.Index(
                fields=['creation_date'],
                name='film_work_creation_date_idx')]

    FILM_WORK_TYPES = [
        ('movie', _('Movie')),
        ('tv_show', _('TV-Show')),
    ]

    creation_date = models.DateField(_('creation date'))
    description = models.TextField(_('description'), blank=True)
    file_path = models.FileField(blank=True, null=True)
    title = models.CharField(_('title'), max_length=255)
    type = models.TextField(_('type'), blank=True, choices=FILM_WORK_TYPES)
    rating = models.FloatField(
        _('rating'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)])
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through='PersonFilmWork')

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    class Meta:
        db_table = 'content\".\"genre_film_work'
        verbose_name = _('Film Work Genre')
        verbose_name_plural = _('Film Work Genres')
        unique_together = (('film_work', 'genre'),)

    created_at = models.DateTimeField(auto_now_add=True)
    film_work = models.ForeignKey(
        FilmWork,
        verbose_name=_('film work'),
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name=_('genre'),
        on_delete=models.CASCADE)


class PersonFilmWork(UUIDMixin):
    class Meta:
        db_table = 'content\".\"person_film_work'
        verbose_name = _('Film Work Person')
        verbose_name_plural = _('Film Work Persons')
        unique_together = (('film_work', 'person', 'role'),)

    PERSON_ROLES = [
        ('actor', _('Actor')),
        ('director', _('Director')),
        ('writer', _('Writer')),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    role = models.TextField(_('role'), choices=PERSON_ROLES)
    film_work = models.ForeignKey(
        FilmWork,
        verbose_name=_('film work'),
        on_delete=models.CASCADE)
    person = models.ForeignKey(
        Person,
        verbose_name=_('person'),
        on_delete=models.CASCADE)
