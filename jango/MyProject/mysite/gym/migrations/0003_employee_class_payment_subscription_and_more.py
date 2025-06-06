# Generated by Django 5.2 on 2025-05-31 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0002_member_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('em_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('phone_num', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('cl_id', models.AutoField(primary_key=True, serialize=False)),
                ('dates', models.DateTimeField()),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('tran_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tran_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('sub_id', models.AutoField(primary_key=True, serialize=False)),
                ('avail_participations', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='member',
            old_name='reg_date',
            new_name='registration_date',
        ),
        migrations.RemoveField(
            model_name='member',
            name='id',
        ),
        migrations.RemoveField(
            model_name='member',
            name='pnumber',
        ),
        migrations.AddField(
            model_name='member',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='phone_num',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='member',
            name='user_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('h_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='histories', to='gym.member')),
                ('cl', models.ForeignKey(db_column='cl_id', on_delete=django.db.models.deletion.CASCADE, related_name='histories', to='gym.class')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('history_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='gym.history')),
                ('em_id', models.OneToOneField(db_column='em_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='booking_record', serialize=False, to='gym.employee')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('phone_num', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
            },
            bases=('gym.history',),
        ),
        migrations.CreateModel(
            name='Cancellation',
            fields=[
                ('history_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='gym.history')),
                ('em_id', models.OneToOneField(db_column='em_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='cancellation_record', serialize=False, to='gym.employee')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('phone_num', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Cancellation',
                'verbose_name_plural': 'Cancellations',
            },
            bases=('gym.history',),
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('employee_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gym.employee')),
            ],
            options={
                'verbose_name': 'Coach',
                'verbose_name_plural': 'Coaches',
            },
            bases=('gym.employee',),
        ),
        migrations.CreateModel(
            name='Secretary',
            fields=[
                ('employee_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gym.employee')),
            ],
            options={
                'verbose_name': 'Secretary',
                'verbose_name_plural': 'Secretaries',
            },
            bases=('gym.employee',),
        ),
        migrations.AddField(
            model_name='member',
            name='tran',
            field=models.ForeignKey(blank=True, db_column='tran_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='gym.payment'),
        ),
        migrations.AddField(
            model_name='payment',
            name='sub',
            field=models.ForeignKey(db_column='sub_id', on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='gym.subscription'),
        ),
        migrations.AddField(
            model_name='member',
            name='sub',
            field=models.ForeignKey(blank=True, db_column='sub_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='gym.subscription'),
        ),
        migrations.AddField(
            model_name='class',
            name='em',
            field=models.ForeignKey(db_column='em_id', on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='gym.coach'),
        ),
    ]
