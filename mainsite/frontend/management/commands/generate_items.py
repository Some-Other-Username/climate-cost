from django.core.management.base import BaseCommand, CommandError
from frontend.models import *


def new_life_cycle(name, parent):
    obj, _ = LifeCycleStage.objects.get_or_create(name__iexact=name, parent=parent,
                                                  defaults={'name': name, 'parent': parent})
    return obj


def new_item_cat(name, parent):
    obj, _ = ItemCategory.objects.get_or_create(name__iexact=name, parent=parent,
                                                defaults={'name': name, 'parent': parent})
    return obj


def new_emission_type(name):
    obj, _ = EmissionType.objects.get_or_create(name__iexact=name, defaults={'name': name, })
    return obj


def new_reference(url, pub_date, access_date):
    obj, _ = Reference.objects.get_or_create(url=url.lower(),
                                             defaults={'pub_date': pub_date, 'access_date': access_date})
    return obj


def new_emission(e_type, restriction, reference, e_mean, e_var):
    obj, _ = Emission.objects.get_or_create(e_type=e_type, restriction=restriction, reference=reference,
                                            e_mean=e_mean, e_var=e_var)
    return obj


class Command(BaseCommand):
    help = "Generate all items."

    def handle(self, *args, **options):
        try:
            # Common life cycles first
            full_lf = new_life_cycle(name="Cradle to Grave", parent=None)
            production_lf = new_life_cycle(name="Production", parent=full_lf)
            production_material_lf = new_life_cycle(name="Production Material", parent=production_lf)
            production_energy_lf = new_life_cycle(name="Production Energy", parent=production_lf)
            production_waste_lf = new_life_cycle(name="Production Waste", parent=production_lf)
            packaging_lf = new_life_cycle(name="Packaging", parent=full_lf)
            transport_lf = new_life_cycle(name="Transport", parent=full_lf)
            use_lf = new_life_cycle(name="Use", parent=full_lf)
            use_dryer_lf = new_life_cycle(name="Use Dryer", parent=use_lf)
            use_iron_lf = new_life_cycle(name="Use Ironing", parent=use_lf)
            use_washing_lf = new_life_cycle(name="Use Washing", parent=use_lf)
            end_of_life_lf = new_life_cycle(name="End Of Life", parent=full_lf)

            # Some sample items groups
            i_manufactured = new_item_cat(name="Manufactured Good", parent=None)
            # Manufactured -> Consumer goods
            i_consumer = new_item_cat(name="Consumer Good", parent=i_manufactured)
            i_cloth = new_item_cat(name="Clothing", parent=i_consumer)
            i_shirt = new_item_cat(name="Shirt", parent=i_cloth)
            i_tshirt = new_item_cat(name="T-Shirt", parent=i_shirt)
            i_tshirt_cotton = new_item_cat(name="T-Shirt Cotton", parent=i_tshirt)
            i_tshirt_cotton_black = new_item_cat(name="T-Shirt Cotton Black", parent=i_tshirt_cotton)
            # Manufactured -> Materials
            i_material = new_item_cat(name="Material", parent=i_manufactured)
            # Manufactured -> Materials -> Plant
            i_plant = new_item_cat(name="Plant", parent=i_material)
            i_cotton = new_item_cat(name="Cotton", parent=i_plant)
            i_cotton_fabric = new_item_cat(name="Cotton Fabric", parent=i_cotton)
            i_cotton_yarn = new_item_cat(name="Cotton Yarn", parent=i_cotton_fabric)
            i_cotton_fibre = new_item_cat(name="Cotton Fibre", parent=i_cotton_fabric)
            # Manufactured -> Materials -> Chemicals
            i_chemical = new_item_cat(name="Chemical", parent=i_material)
            i_carbon = new_item_cat(name="Carbon", parent=i_chemical)
            i_carbon_black = new_item_cat(name="Carbon Black", parent=i_carbon)

            # Sample emissions

            e_cotton = new_emission(e_co2e, e_cotton_rest, e_cotton_ref, e_mean=3.61, e_var=0)

            # And finally the connections
            print("Success!")
        except Exception as e:
            raise CommandError("Unable to generate items" + str(e))
