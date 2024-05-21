# Generated by Django 5.0.3 on 2024-05-17 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Algerie_Telecom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse_site', models.CharField(max_length=250)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('commune', models.CharField(max_length=250)),
                ('type', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Djezzy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Adresse', models.CharField(max_length=250)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('commune', models.CharField(max_length=250)),
                ('Technologie', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Mobilis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom_du_Site', models.CharField(max_length=250)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('Code_Site', models.CharField(max_length=250)),
                ('Type', models.CharField(max_length=250)),
                ('Typologie', models.CharField(max_length=250)),
                ('T_Salle_Equip', models.CharField(max_length=250)),
                ('Type_Gardiennage', models.CharField(max_length=250)),
                ('Commune', models.CharField(max_length=250)),
                ('Etat', models.CharField(max_length=250)),
                ('D_Mise_en_Air', models.DateField(null=True)),
                ('Propriétaire', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Ooredoo2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commune', models.CharField(max_length=250)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('code_site', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('adresse', models.TextField()),
                ('wilaya', models.CharField(max_length=100)),
                ('mise_en_service', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Posta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('dénomination', models.CharField(max_length=250)),
                ('commune', models.CharField(max_length=250)),
                ('Classe', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Service_Universel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localité', models.CharField(max_length=250)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('populations', models.CharField(max_length=250)),
                ('municipality', models.CharField(blank=True, max_length=255, null=True)),
                ('region', models.CharField(blank=True, max_length=255, null=True)),
                ('commune', models.CharField(max_length=250)),
            ],
        ),
    ]