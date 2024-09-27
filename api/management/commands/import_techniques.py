# api/management/commands/import_techniques.py

import csv
import logging
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import (
    Techniques,
    Categories,
    SubCategories,
    Tags,
    TechniqueCategories,
    TechniqueTags,
    SubTechniques
)

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler('import_techniques.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class Command(BaseCommand):
    help = 'Import techniques from a CSV file located alongside this script'

    def handle(self, *args, **options):
        # Define the CSV filename
        CSV_FILENAME = 'techniques_data.csv'

        # Determine the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(script_dir, CSV_FILENAME)  # Fixed CSV filename

        success_count = 0
        error_count = 0

        self.stdout.write(self.style.NOTICE(f"Starting import from '{csv_file}'"))
        logger.info(f"Starting import from '{csv_file}'")

        if not os.path.isfile(csv_file):
            error_msg = f"CSV file not found at '{csv_file}'"
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg)
            raise CommandError(error_msg)

        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                row_number = 1  # To track row numbers for logging

                for row in reader:
                    row_number += 1
                    try:
                        with transaction.atomic():
                            # Skip rows with missing or invalid Technique
                            technique_name = row.get('Technique', '').strip()
                            if not technique_name or technique_name == '???':
                                warning_msg = f"Skipping invalid row {row_number}: {row}"
                                self.stdout.write(self.style.WARNING(warning_msg))
                                logger.warning(warning_msg)
                                error_count += 1
                                continue

                            # Create or get Technique
                            technique, created = Techniques.objects.get_or_create(
                                technique=technique_name,
                                defaults={
                                    'description': row.get('Description', '').strip(),
                                    'scope_global': self.str_to_bool(row.get('Scope Global', 'No')),
                                    'scope_local': self.str_to_bool(row.get('Scope Local', 'No')),
                                    'model_dependency': row.get('Model-Dependency', '').strip() or None,
                                    'example_use_case': row.get('Example Use-Case', '').strip() or None,
                                }
                            )

                            if not created:
                                # Update existing technique
                                technique.description = row.get('Description', '').strip()
                                technique.scope_global = self.str_to_bool(row.get('Scope Global', 'No'))
                                technique.scope_local = self.str_to_bool(row.get('Scope Local', 'No'))
                                technique.model_dependency = row.get('Model-Dependency', '').strip() or None
                                technique.example_use_case = row.get('Example Use-Case', '').strip() or None
                                technique.save()

                            # Process Categories
                            categories = self.parse_semicolon_separated(row.get('Categories', ''))
                            for cat_name in categories:
                                category, _ = get_or_create_case_insensitive(Categories, 'name', cat_name)
                                TechniqueCategories.objects.get_or_create(technique=technique, category=category)

                            # Process Sub-Categories
                            sub_categories = self.parse_semicolon_separated(row.get('Sub-Categories', ''))
                            for sub_cat_name in sub_categories:
                                sub_category, _ = get_or_create_case_insensitive(SubCategories, 'name', sub_cat_name)
                                SubTechniques.objects.get_or_create(technique=technique, sub_category=sub_category)

                            # Process Tags
                            tags = self.parse_semicolon_separated(row.get('Tags', ''))
                            for tag_name in tags:
                                tag, _ = get_or_create_case_insensitive(Tags, 'name', tag_name)
                                TechniqueTags.objects.get_or_create(technique=technique, tag=tag)

                            success_count += 1
                            success_msg = f"Imported Technique: {technique.technique}"
                            self.stdout.write(self.style.SUCCESS(success_msg))
                            logger.info(success_msg)

                    except Exception as e:
                        error_msg = f"Error importing row {row_number} in '{csv_file}': {e}"
                        self.stdout.write(self.style.ERROR(error_msg))
                        logger.error(error_msg)
                        error_count += 1
                        continue  # Continue with next row

        except Exception as e:
            error_msg = f"Failed to process file '{csv_file}': {e}"
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg)
            raise CommandError(f"Failed to process file '{csv_file}': {e}")

        summary_msg = f"Import completed: {success_count} succeeded, {error_count} failed."
        self.stdout.write(self.style.SUCCESS(summary_msg))
        logger.info(summary_msg)

    def parse_semicolon_separated(self, value):
        """
        Helper method to parse semicolon-separated strings into a list.
        """
        return [item.strip() for item in value.split(';') if item.strip()]

    def str_to_bool(self, value):
        """
        Helper method to convert string representations to boolean.
        """
        return value.strip().lower() in ['yes', 'true', '1']

def get_or_create_case_insensitive(model, name_field, name):
    """
    Performs a case-insensitive get or create for a given model and field.
    
    Args:
        model: The Django model to query.
        name_field: The field name to perform the lookup.
        name: The value to look for.
    
    Returns:
        Tuple of (object, created)
    """
    lookup = {f"{name_field}__iexact": name}
    obj = model.objects.filter(**lookup).first()
    if obj:
        return obj, False
    else:
        # Normalize the name by stripping whitespace
        normalized_name = name.strip()
        obj = model.objects.create(**{name_field: normalized_name})
        return obj, True