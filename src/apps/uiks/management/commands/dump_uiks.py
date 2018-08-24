from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        import os
        from django.conf import settings
        from apps.uiks.models import Address
        from apps.uiks.services import (
            get_init_data, update_info, write_data_json_to_file, write_address_with_children)

        Address.objects.all().delete()
        Address.objects.create(**get_init_data())
        update_info()
        file_name = os.path.join(settings.BASE_DIR, 'data', 'uiks_70.json')
        write_data_json_to_file(file_name)
        write_address_with_children(Address.objects.first())
