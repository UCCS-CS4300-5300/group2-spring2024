from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import *


# Register your models here.
class CategoryAdmin(GuardedModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)


class TaskAdmin(GuardedModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
admin.site.register(User)
