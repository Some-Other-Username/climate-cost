from django.core.management.base import BaseCommand, CommandError
from frontend.models import UnitType, UnitConversion
from pathlib import Path
import os


def generate_missing_conversions():
    # TODO: For every conversion we have, we should generate the inverse
    # Afterwards we can generate all shortcuts as well. This way we don't need
    # to search in the graph when we convert units.
    pass


class Command(BaseCommand):
    help = "Generate all units."

    def handle(self, *args, **options):
        try:
            g, _ = UnitType.objects.get_or_create(abbreviation="g", name="Gram")
            kg, _ = UnitType.objects.get_or_create(abbreviation="kg", name="Kilogram")
            UnitConversion.objects.get_or_create(from_u_type=g, to_u_type=kg, bias_term=0, multiplication_term=1000)
            l, _ = UnitType.objects.get_or_create(abbreviation="l", name="Liter")
            w, _ = UnitType.objects.get_or_create(abbreviation="W", name="Watt")
            kw, _ = UnitType.objects.get_or_create(abbreviation="kW", name="Kilowatt")
            UnitConversion.objects.get_or_create(from_u_type=w, to_u_type=kw, bias_term=0, multiplication_term=1000)
            mw, _ = UnitType.objects.get_or_create(abbreviation="MW", name="Megawatt")
            UnitConversion.objects.get_or_create(from_u_type=kw, to_u_type=mw, bias_term=0, multiplication_term=1000)
            gw, _ = UnitType.objects.get_or_create(abbreviation="GW", name="Gigawatt")
            UnitConversion.objects.get_or_create(from_u_type=mw, to_u_type=gw, bias_term=0, multiplication_term=1000)

            generate_missing_conversions()

            print("Success!")
        except Exception as e:
            raise CommandError("Unable to generate units" + str(e))
