# Generated by Django 2.2 on 2019-06-02 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HotWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, unique=True)),
                ('meaning', models.CharField(max_length=1000)),
                ('type', models.CharField(choices=[('BZ', 'Buzzword'), ('AC', 'Acronym')], default='BZ', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='SlackMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utterer', models.CharField(max_length=15)),
                ('message', models.CharField(max_length=5000)),
                ('channel', models.CharField(max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.CharField(max_length=20)),
                ('team_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utterance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utterer', models.CharField(max_length=15)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('hot_word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.HotWord')),
                ('original_context', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.SlackMessage')),
            ],
        ),
    ]
