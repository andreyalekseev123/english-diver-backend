# Generated by Django 3.2.7 on 2022-04-28 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0007_alter_word_image'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trainingtypeuserword',
            unique_together={('training_type', 'user_word')},
        ),
    ]
