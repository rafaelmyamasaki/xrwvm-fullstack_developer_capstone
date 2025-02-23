from django.contrib import admin
from .models import CarMake, CarModel

# Inline class for CarModel to be displayed within CarMakeAdmin
class CarModelInline(admin.StackedInline):  # or admin.TabularInline for a more compact view
    model = CarModel
    extra = 1  # Number of empty forms to display for adding new CarModels

# Admin class for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year')  # Fields to display in the list view
    list_filter = ('type', 'year')  # Add filters on the side
    search_fields = ('name', 'car_make__name')  # Enable search by name and car make name

# Admin class for CarMake with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Fields to display in the list view
    search_fields = ('name',)  # Enable search by name
    inlines = [CarModelInline]  # Include CarModelInline to manage CarModels within CarMake

# Register models with their respective admins
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
