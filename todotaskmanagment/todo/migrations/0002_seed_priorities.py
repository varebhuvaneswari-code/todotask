from django.db import migrations


def seed_priorities(apps, schema_editor):
    Priority = apps.get_model("todo", "Priority")
    defaults = [
        ("High", 1, "danger"),
        ("Medium", 2, "warning"),
        ("Low", 3, "success"),
    ]
    for name, level, color in defaults:
        Priority.objects.update_or_create(name=name, defaults={"level": level, "color": color})


def remove_priorities(apps, schema_editor):
    Priority = apps.get_model("todo", "Priority")
    Priority.objects.filter(name__in=["High", "Medium", "Low"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_priorities, remove_priorities),
    ]
