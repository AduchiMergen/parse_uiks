from django.contrib.postgres.search import TrigramDistance
from django.http import JsonResponse
from django.views.generic import TemplateView

from apps.addreses.models import TreeItem
from apps.uiks.models import Address


class InputView(TemplateView):
    template_name = 'addreses/input.html'


input_view = InputView.as_view()


def query(request):
    query_string = request.GET.get('q', '').strip()
    items = []
    if query_string.isdigit():
        items = Address.objects.filter(uik_num=query_string).values('id', 'title', 'voteroom_lat', 'voteroom_lon')
        items = [
            {
                'title': item['title'],
                'subtitle': '',
                'voteroom_id': item['id'],
                'voteroom_lat': item['voteroom_lat'],
                'voteroom_lon': item['voteroom_lon'],
            }
            for item in items
        ]
    elif query_string:
        items = TreeItem.objects.prefetch_related('uik_obj').filter(
            uik_num__isnull=False
        ).annotate(
            distance=TrigramDistance('full_address', query_string),
        ).order_by('distance')[:4]
        items = [
            {
                'title': item.full_address,
                'subtitle': 'Избирательная коммисия № {}'.format(item.uik_num),
                'voteroom_id': item.uik_obj_id,
                'voteroom_lat': item.uik_obj.voteroom_lat,
                'voteroom_lon': item.uik_obj.voteroom_lon,
            }
            for item in items
        ]
    return JsonResponse({'result': items}, json_dumps_params={'ensure_ascii': False})
