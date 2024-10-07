# api/management/commands/import_techniques.py

import csv
import logging
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import (
    Technique,
    Category,
    SubCategory,
    Tag,
    AssuranceGoal,
    FairnessApproach,
    ProjectLifecycleStage,
    TechniqueFairnessApproach,
    TechniqueProjectLifecycleStage
)

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler('import_techniques.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def get_or_create_case_insensitive(model, name_field, name, defaults=None):
    """
    Performs a case-insensitive get or create for a given model and field.
    """
    if defaults is None:
        defaults = {}
    lookup = {f"{name_field}__iexact": name.strip()}
    obj = model.objects.filter(**lookup).first()
    if obj:
        return obj, False
    else:
        # Combine the name field and any extra fields required for creation
        create_kwargs = {name_field: name.strip(), **defaults}
        obj = model.objects.create(**create_kwargs)
        return obj, True

class Command(BaseCommand):
    help = 'Import techniques from a CSV file. Usage: import_techniques <csv_file> <assurance_goal>'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')
        parser.add_argument('assurance_goal', type=str, help='Name of the Assurance Goal')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        assurance_goal_name = options['assurance_goal']
        
        success_count = 0
        error_count = 0

        self.stdout.write(self.style.NOTICE(f"Starting import from '{csv_file}' for Assurance Goal '{assurance_goal_name}'"))
        logger.info(f"Starting import from '{csv_file}' for Assurance Goal '{assurance_goal_name}'")

        if not os.path.isfile(csv_file):
            error_msg = f"CSV file not found at '{csv_file}'"
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg)
            raise CommandError(error_msg)

        # Get the AssuranceGoal
        try:
            assurance_goal = AssuranceGoal.objects.get(name__iexact=assurance_goal_name)
        except AssuranceGoal.DoesNotExist:
            error_msg = f"Assurance Goal '{assurance_goal_name}' does not exist."
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg)
            raise CommandError(error_msg)

        try:
            with open(csv_file, newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                row_number = 1  # To track row numbers for logging

                for row in reader:
                    row_number += 1
                    try:
                        with transaction.atomic():
                            # Retrieve and validate Technique Name
                            technique_name = row.get('Technique Name', '').strip()
                            if not technique_name or technique_name.lower() == '???':
                                warning_msg = f"Skipping invalid row {row_number}: Technique Name is missing or invalid."
                                self.stdout.write(self.style.WARNING(warning_msg))
                                logger.warning(warning_msg)
                                error_count += 1
                                continue

                            # Process Category
                            category_name = row.get('Category', '').strip()
                            if not category_name:
                                error_msg = f"Category is missing in row {row_number}."
                                self.stdout.write(self.style.ERROR(error_msg))
                                logger.error(error_msg)
                                error_count += 1
                                continue

                            category = Category.objects.filter(name__iexact=category_name, assurance_goal=assurance_goal).first()
                            if not category:
                                error_msg = f"Category '{category_name}' not found for Assurance Goal '{assurance_goal_name}' in row {row_number}."
                                self.stdout.write(self.style.ERROR(error_msg))
                                logger.error(error_msg)
                                error_count += 1
                                continue

                            # Process SubCategory
                            sub_category_name = row.get('Sub-Category', '').strip()
                            if sub_category_name:
                                sub_category = SubCategory.objects.filter(name__iexact=sub_category_name, category=category).first()
                                if not sub_category:
                                    error_msg = f"SubCategory '{sub_category_name}' not found under Category '{category_name}' in row {row_number}."
                                    self.stdout.write(self.style.ERROR(error_msg))
                                    logger.error(error_msg)
                                    error_count += 1
                                    continue
                            else:
                                sub_category = None

                            # Prepare defaults for Technique creation/update
                            technique_defaults = {
                                'description': row.get('Description', '').strip(),
                                'assurance_goal': assurance_goal,
                                'model_dependency': row.get('Model Dependency', '').strip(),
                                'example_use_case': row.get('Example Use Case', '').strip(),
                            }

                            # Handle Scope Columns
                            scope_global = row.get('Scope Global', '').strip().lower() == 'yes'
                            scope_local = row.get('Scope Local', '').strip().lower() == 'yes'

                            if scope_global and scope_local:
                                scope = 'Both'
                            elif scope_global:
                                scope = 'Global'
                            elif scope_local:
                                scope = 'Local'
                            else:
                                scope = None

                            technique_defaults['scope'] = scope

                            # Create or update Technique with correct lookup
                            try:
                                technique = Technique.objects.get(name__iexact=technique_name)
                                # Update the Technique's fields
                                for field, value in technique_defaults.items():
                                    setattr(technique, field, value)
                                # Assign ForeignKey fields directly
                                technique.category = category
                                technique.sub_category = sub_category
                                technique.save()
                                created = False
                                success_count += 1
                                success_msg = f"Updated Technique: {technique.name}"
                                self.stdout.write(self.style.SUCCESS(success_msg))
                                logger.info(success_msg)
                            except Technique.DoesNotExist:
                                # Create a new Technique
                                technique = Technique.objects.create(
                                    name=technique_name,
                                    category=category,  # Assign ForeignKey directly
                                    sub_category=sub_category,  # Assign ForeignKey directly or leave blank
                                    **technique_defaults
                                )
                                created = True
                                success_count += 1
                                success_msg = f"Imported Technique: {technique.name}"
                                self.stdout.write(self.style.SUCCESS(success_msg))
                                logger.info(success_msg)

                            # Process Tags (assuming there's a 'Tags' column in the CSV)
                            tags = self.parse_semicolon_separated(row.get('Tags', ''))
                            for tag_name in tags:
                                if tag_name:
                                    tag, _ = get_or_create_case_insensitive(Tag, 'name', tag_name)
                                    technique.tags.add(tag)

                            # Process Fairness Approach (if column exists)
                            if 'Fairness Approach' in row:
                                fa_names = self.parse_semicolon_separated(row.get('Fairness Approach', ''))
                                for fa_name in fa_names:
                                    if fa_name:
                                        fairness_approach, _ = get_or_create_case_insensitive(FairnessApproach, 'name', fa_name)
                                        TechniqueFairnessApproach.objects.get_or_create(
                                            technique=technique, fairness_approach=fairness_approach)

                            # Process Project Lifecycle Stage (if column exists)
                            if 'Project Lifecycle Stage' in row:
                                pls_names = self.parse_semicolon_separated(row.get('Project Lifecycle Stage', ''))
                                for pls_name in pls_names:
                                    if pls_name:
                                        pls, _ = get_or_create_case_insensitive(ProjectLifecycleStage, 'name', pls_name)
                                        TechniqueProjectLifecycleStage.objects.get_or_create(
                                            technique=technique, project_lifecycle_stage=pls)

                    except Exception as e:
                        error_msg = f"Error importing row {row_number} in '{csv_file}': {e}"
                        self.stdout.write(self.style.ERROR(error_msg))
                        logger.exception("Exception occurred while importing row %d", row_number)
                        error_count += 1
                        continue  # Continue with the next row

        except Exception as e:
            error_msg = f"Failed to process file '{csv_file}': {e}"
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg)
            raise CommandError(error_msg)

        summary_msg = f"Import completed: {success_count} succeeded, {error_count} failed."
        self.stdout.write(self.style.SUCCESS(summary_msg))
        logger.info(summary_msg)

    def parse_semicolon_separated(self, value):
        """
        Helper method to parse semicolon-separated strings into a list.
        """
        return [item.strip() for item in value.split(';') if item.strip()]