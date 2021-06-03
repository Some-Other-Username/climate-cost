# Generated by Django 3.2.4 on 2021-06-03 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmissionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LifeCycleGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('pub_date', models.DateTimeField(verbose_name='published')),
                ('access_date', models.DateTimeField(verbose_name='last accessed')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.region')),
            ],
        ),
        migrations.CreateModel(
            name='UnitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UnitConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bias_term', models.FloatField()),
                ('multiplication_term', models.FloatField()),
                ('from_u_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convert_from', to='frontend.unittype')),
                ('to_u_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convert_to', to='frontend.unittype')),
            ],
        ),
        migrations.CreateModel(
            name='Restriction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restrictionStart', models.DateField(blank=True, default=None, null=True)),
                ('restrictionEnd', models.DateField(blank=True, default=None, null=True)),
                ('reference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.reference')),
                ('restrictRegion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.region')),
            ],
        ),
        migrations.CreateModel(
            name='LifeCycleStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.lifecyclegroup')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('lf_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.lifecyclegroup')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.itemcategory')),
            ],
        ),
        migrations.CreateModel(
            name='EmissionConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bias_term', models.FloatField()),
                ('multiplication_term', models.FloatField()),
                ('from_e_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convert_from', to='frontend.emissiontype')),
                ('restriction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.restriction')),
                ('to_e_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convert_to', to='frontend.emissiontype')),
            ],
        ),
        migrations.CreateModel(
            name='Emission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_mean', models.FloatField(verbose_name='Emission Mean')),
                ('e_var', models.FloatField(verbose_name='Emission Variance')),
                ('e_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.emissiontype')),
                ('item_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.itemcategory')),
                ('lf_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.lifecyclestage')),
                ('restriction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.restriction')),
            ],
        ),
    ]
