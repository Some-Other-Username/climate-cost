from django.db import models


# References are used to back up claims
class Reference(models.Model):
    url = models.URLField()
    pub_date = models.DateTimeField('published')
    access_date = models.DateTimeField('last accessed')

    def __str__(self):
        return str(self.url) + " Pub:" + str(self.pub_date) + " LastAccess" + str(self.access_date)


# A region in the world (for example Vancouver). A region can also be used
# to describe a whole country or even a continent or the whole world.
class Region(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


# A unit for measurements such as kg, kWh, ...
class UnitType(models.Model):
    abbreviation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


# This only works for simple units
class UnitConversion(models.Model):
    from_u_type = models.ForeignKey(UnitType, on_delete=models.CASCADE, related_name='convert_from')
    to_u_type = models.ForeignKey(UnitType, on_delete=models.CASCADE, related_name='convert_to')
    bias_term = models.FloatField()
    multiplication_term = models.FloatField()

    def __str__(self):
        return str(self.from_u_type) + "-->" + str(self.to_u_type)


# An emission type such as CO2, CH4, N20, ...
class EmissionType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


# Hierarchy of items, for example:
# Pepsi Light Caffeine Free -> Pepsi Cola -> Cola -> Soft Drink -> Bottled Drink -> Consumer Good -> Object
class ItemCategory(models.Model):
    name = models.CharField(max_length=100)
    # lf_stage = models.ForeignKey(LifeCycleStage, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class LifeCycleStage(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


# Every emission (conversion) can be restricted, for example an emission might only be valid for
# T-Shirts available in the UK for the year 2001
class Restriction(models.Model):
    # Null means no restriction
    item_category = models.ForeignKey(ItemCategory, blank=True, null=True, on_delete=models.CASCADE, default=None)
    lf_stage = models.ForeignKey(LifeCycleStage, blank=True, null=True, on_delete=models.CASCADE, default=None)
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.CASCADE, default=None)
    start_date = models.DateField(blank=True, null=True, default=None)
    end_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        result = "Restriction"
        if self.item_category is not None:
            result += " item:" + str(self.item_category)
        if self.lf_stage is not None:
            result += " stage:" + str(self.lf_stage)
        if self.region is not None:
            result += " region:" + str(self.region)
        if self.start_date is not None:
            result += " start:" + str(self.start_date)
        if self.end_date is not None:
            result += " end:" + str(self.end_date)
        if result == "Restriction":
            result = "No Restriction"
        return result


# A conversion from one emission type to another (such as CO2e)
# Do not convert actual CH4 into CO2 only in CO2e to avoid errors.
class EmissionConversion(models.Model):
    from_e_type = models.ForeignKey(EmissionType, on_delete=models.CASCADE, related_name='convert_from')
    to_e_type = models.ForeignKey(EmissionType, on_delete=models.CASCADE, related_name='convert_to')
    bias_term = models.FloatField()
    multiplication_term = models.FloatField()
    # If there is no restriction it means this conversion is always possible, be careful with that assumption!
    restriction = models.ForeignKey(Restriction, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.from_e_type) + "-->" + str(self.to_e_type)


class Emission(models.Model):
    e_type = models.ForeignKey(EmissionType, on_delete=models.CASCADE)
    restriction = models.ForeignKey(Restriction, blank=True, null=True, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, blank=True, null=True, on_delete=models.SET_NULL)
    e_mean = models.FloatField("Emission Mean")
    e_var = models.FloatField("Emission Variance")

    def __str__(self):
        return f"{self.e_type} emission with restriction: {self.restriction}"


# Connection between an item class and an emission
# There might be multiple connections that all need to be added up for an item class
class Connection(models.Model):
    multiplier = models.FloatField("Emission Multiplier")
    emission = models.ForeignKey(Emission, on_delete=models.CASCADE)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    add_on = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='previous')

    def __str__(self):
        return f"Connection for {self.item_category} and {self.emission}"


""""
Currently not needed
class Item(models.Model):
    identifier = models.CharField("Product Identifier", max_length=200)
    # Every item should have at least one category. The category can be the item
    # itself. The backend does not use items but item categories for everything.
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
"""
