# Generated manually: remove PointType model and its relations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0013_recreate_homepage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="salespoint",
            name="point_type",
        ),
        migrations.DeleteModel(
            name="PointType",
        ),
    ]

