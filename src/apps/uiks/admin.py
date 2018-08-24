from apps.uiks.models import IkPerson, Address
from django.contrib import admin


class IkPersonInline(admin.TabularInline):
    model = IkPerson
    readonly_fields = ['person_name', 'status', 'recomend_by']
    extra = 0

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['name', 'uik_num', 'done_info']
    list_filter = ['error', 'level', 'region', 'done_info', 'done_tree']
    search_fields = ['uik_num', 'voteroom_address']
    raw_id_fields = ['parent']
    inlines = [IkPersonInline]
