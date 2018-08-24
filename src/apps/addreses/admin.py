from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.addreses.models import TreeItem


class TreeItemInlineAdmin(admin.TabularInline):
    model = TreeItem
    fields = ['text_url', 'uik_num']
    fk_name = 'parent'
    extra = 0
    readonly_fields = ['text_url', 'uik_num']

    def text_url(self, obj):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="/admin/addreses/treeitem/{}/change/">{}</a>'.format(obj.id, obj.text))

    def has_add_permission(self, request, obj):
        return False


@admin.register(TreeItem)
class TreeItemAdmin(admin.ModelAdmin):
    list_filter = ['levelid', 'done_info', 'done_tree']
    list_display = ['text', 'info_url', 'uik_num', 'done_info']
    raw_id_fields = ['parent']

    inlines = [TreeItemInlineAdmin]

    def info_url(self, obj):
        return mark_safe('<a href="{}">Ссылка</a>'.format(obj.info_url()))
