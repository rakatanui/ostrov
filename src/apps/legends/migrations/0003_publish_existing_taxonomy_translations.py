from django.db import migrations, models


def publish_existing_taxonomy_translations(apps, schema_editor):
    SeriesTranslation = apps.get_model("legends", "SeriesTranslation")
    ProvinceTranslation = apps.get_model("legends", "ProvinceTranslation")
    PatronTranslation = apps.get_model("legends", "PatronTranslation")
    TagTranslation = apps.get_model("legends", "TagTranslation")

    SeriesTranslation.objects.filter(is_published=False).update(is_published=True)
    ProvinceTranslation.objects.filter(is_published=False).update(is_published=True)
    PatronTranslation.objects.filter(is_published=False).update(is_published=True)
    TagTranslation.objects.filter(is_published=False).update(is_published=True)


class Migration(migrations.Migration):

    dependencies = [
        ("legends", "0002_alter_patron_options_alter_province_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seriestranslation",
            name="is_published",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="provincetranslation",
            name="is_published",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="patrontranslation",
            name="is_published",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name="tagtranslation",
            name="is_published",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.RunPython(
            publish_existing_taxonomy_translations,
            migrations.RunPython.noop,
        ),
    ]
