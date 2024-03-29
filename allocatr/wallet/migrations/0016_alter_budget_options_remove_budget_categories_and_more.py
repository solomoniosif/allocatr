# Generated by Django 4.0.10 on 2023-04-02 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0015_alter_category_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='budget',
            options={},
        ),
        migrations.RemoveField(
            model_name='budget',
            name='categories',
        ),
        migrations.AddField(
            model_name='budget',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='wallet.category'),
        ),
        migrations.AddConstraint(
            model_name='budget',
            constraint=models.UniqueConstraint(condition=models.Q(('is_master', False)), fields=('category', 'month'), name='unique_category_month'),
        ),
        migrations.AddConstraint(
            model_name='budget',
            constraint=models.UniqueConstraint(condition=models.Q(('is_master', True)), fields=('month',), name='unique_master_month'),
        ),
    ]
