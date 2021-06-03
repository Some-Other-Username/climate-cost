from django.core.management.base import BaseCommand, CommandError
from frontend.models import Region
from pathlib import Path
import os


class Command(BaseCommand):
    help = "Generate all regions."

    def handle(self, *args, **options):
        try:
            source_path = Path(__file__).resolve()
            source_dir = source_path.parent

            world, _ = Region.objects.get_or_create(
                name='World',
            )
            with open(os.path.join(source_dir, "countries.txt")) as f:
                lines = f.readlines()
                current_continent = None
                for line in lines:
                    if line.startswith("="):
                        # Continent
                        current_continent, created = Region.objects.get_or_create(
                            name=line[1:-1],
                            parent=world,
                        )
                    else:
                        Region.objects.get_or_create(
                            name=line[:-1],
                            parent=current_continent,
                        )
            print("Success!")
        except Exception as e:
            raise CommandError("Unable to generate regions" + str(e))
