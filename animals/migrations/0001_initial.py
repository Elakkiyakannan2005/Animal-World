from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('emoji', models.CharField(blank=True, help_text="Emoji shown before the animal's name, e.g. 🦁", max_length=10)),
                ('image_url', models.URLField(help_text='Full URL of the card image.', max_length=500)),
                ('short_description', models.CharField(help_text='Short blurb shown on the card.', max_length=200)),
                ('full_description', models.TextField(help_text="Longer fact shown in the 'Learn More' popup.")),
                ('order', models.PositiveIntegerField(default=0, help_text='Controls display order on the page (lower = first).')),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
    ]
