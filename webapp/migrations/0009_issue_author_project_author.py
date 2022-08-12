# Generated by Django 4.0.6 on 2022-08-11 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0008_alter_issue_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='issues', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='project',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='projects', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
