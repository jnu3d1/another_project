from django.db import models


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    class Meta:
        abstract = True


class Issue(BaseModel):
    summary = models.CharField(max_length=50, verbose_name='Краткое описание')
    description = models.TextField(blank=True, max_length=3000, verbose_name='Полное описание')
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, related_name='statuses',
                               verbose_name='Статус')
    types = models.ManyToManyField('webapp.Type', related_name='issues', blank=True)

    def __str__(self):
        return f'{self.id} {self.summary} {self.status}'

    class Meta:
        db_table = 'issues'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Status(models.Model):
    name = models.CharField(max_length=12, verbose_name='Статус')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'statuses'
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(models.Model):
    name = models.CharField(max_length=12, verbose_name='Тип задачи')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'types'
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'
