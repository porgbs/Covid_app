from django.contrib import admin


# Register your models here.
class BaseModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(BaseModelAdmin, self).__init__(model, admin_site)
