import requests

from apps.addreses.models import TreeItem


def get_tree_init_data():
    response = requests.get('http://www.cikrf.ru/services/lk_tree/?first=1&id=%23')
    data = response.json()
    items = data[0]['children']
    for item in items:
        if item['text'] == 'Томская область':
            return attrs_from_cikrf_data(item)


def attrs_from_cikrf_data(data):
    return {
        'cik_tree_id': int(data['id']),
        'intid': data['a_attr']['intid'],
        'levelid': int(data['a_attr']['levelid']),
        'text': data['text'],
    }


def process_tree_item(parent: TreeItem):
    import requests
    response = requests.get(parent.children_url())
    items = [attrs_from_cikrf_data(item) for item in response.json()]
    parent.children.exclude(text__in=[item['text'] for item in items]).delete()

    for item in items:
        TreeItem.objects.update_or_create(
            text=item['text'],
            parent=parent,
            defaults=item,
        )
    parent.done_tree = True
    parent.save()


def process_info_item(item: TreeItem):
    import re
    import requests
    response = requests.get(item.info_url())
    content = response.content.decode('cp1251')
    is_success = False
    if 'Участковая избирательная комиссия №' in content:
        match = re.search(r'Участковая избирательная комиссия №\s?(?P<uik_num>\d+)', content)
        item.uik_num = match.groupdict().get('uik_num')
        is_success = True
    elif 'отсутствуют' not in content:
        raise Exception('Alarm! {}'.format(item.info_url()))
    item.done_info = True
    item.save()
    return is_success


def task_process_tree_item(parent_id: int):
    from django_q.tasks import async
    tree_item = TreeItem.objects.get(id=parent_id)
    if not process_info_item(tree_item):
        process_tree_item(tree_item)
        for children_id in tree_item.children.values_list('id', flat=True):
            async(task_process_tree_item, children_id, ack_failure=True)
