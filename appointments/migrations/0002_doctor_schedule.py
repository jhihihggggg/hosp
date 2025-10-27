"""
Add this migration to create doctor schedules
Run: python manage.py makemigrations
     python manage.py migrate
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('MONDAY', 'Monday'), ('TUESDAY', 'Tuesday'), ('WEDNESDAY', 'Wednesday'), ('THURSDAY', 'Thursday'), ('FRIDAY', 'Friday'), ('SATURDAY', 'Saturday'), ('SUNDAY', 'Sunday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('max_patients', models.IntegerField(default=20, help_text='Maximum patients per session')),
                ('consultation_duration', models.IntegerField(default=15, help_text='Minutes per patient')),
                ('is_active', models.BooleanField(default=True)),
                ('room_number', models.CharField(blank=True, max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='accounts.user')),
            ],
            options={
                'ordering': ['day_of_week', 'start_time'],
                'unique_together': {('doctor', 'day_of_week', 'start_time')},
            },
        ),
        migrations.CreateModel(
            name='DoctorAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('max_patients', models.IntegerField(default=20)),
                ('is_available', models.BooleanField(default=True)),
                ('reason', models.CharField(blank=True, max_length=200, help_text='Reason if unavailable')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='accounts.user')),
            ],
            options={
                'ordering': ['date', 'start_time'],
                'unique_together': {('doctor', 'date', 'start_time')},
                'verbose_name_plural': 'Doctor Availabilities',
            },
        ),
    ]
