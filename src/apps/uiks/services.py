import requests
from django.contrib.gis.geos import Point

from apps.uiks.models import Address, IkPerson


def extract_data_from_page_content(soup):
    import pendulum
    from pendulum.parsing import ParserError

    data = dict()
    center_colm = soup.find('div', class_='center-colm')
    data['title'] = center_colm.find('h2').string
    data['ik_address'] = center_colm.find('span', id='address_ik').get_text()
    data['ik_lat'] = center_colm.find(
        'span', id='view_in_map_ik').attrs['coordlat'].replace(' ', '') or None
    data['ik_lon'] = center_colm.find(
        'span', id='view_in_map_ik').attrs['coordlon'].replace(' ', '') or None
    data['ik_phone'] = center_colm.find('strong', text='Телефон: ').next_sibling
    data['fax'] = center_colm.find('strong', text='Факс: ').next_sibling
    data['email'] = center_colm.find('strong', text='Адрес электронной почты: ').next_sibling
    try:
        expired_date_raw = center_colm.find('strong', text='Срок окончания полномочий: ').next_sibling
        data['expired_date'] = pendulum.from_format(expired_date_raw, 'DD.MM.YYYY').date()
    except ParserError:
        pass
    try:
        data['voteroom_address'] = center_colm.find('span', id='address_voteroom').get_text()
    except AttributeError:
        pass
    try:
        data['voteroom_lat'] = center_colm.find(
            'span', id='view_in_map_voteroom').attrs['coordlat'].replace(' ', '') or None
    except AttributeError:
        pass
    try:
        data['voteroom_lon'] = center_colm.find(
            'span', id='view_in_map_voteroom').attrs['coordlon'].replace(' ', '') or None
    except AttributeError:
        pass

    try:
        data['voteroom_phone'] = center_colm.find(
            'strong', text='Телефон помещения для голосования: ').next_sibling
    except AttributeError:
        pass
    return data


def extract_persons(soup):
    center_colm = soup.find('div', class_='center-colm')
    persons = list()
    for row in center_colm.find('table').find_all('tr')[1:]:
        data = dict(zip(range(4), list(row.stripped_strings)))
        persons.append(dict(person_name=data.get(1, ''), status=data.get(2, ''),
                            recomend_by=data.get(3, '')))
    return persons


def process_tree(address, json=None):
    if not json:
        response = requests.get(address.tree_url)
        json = response.json()
    if address.parent:
        childrens = json
    else:
        childrens = json[0]['children']

    for children in childrens:
        Address.objects.update_or_create(
            parent=address,
            cikrf_id=children['id'],
            defaults=dict(
                name=children['text'],
                level=address.level + 1,
                region=address.region,
                reg_num=address.reg_num,
                done_tree=not children['children'],
            )
        )
    Address.objects.filter(id=address.id).update(done_tree=True)


def process_info(address, content=None):
    import bs4

    if not content:
        response = requests.get(address.info_url)
        content = response.content
    soup = bs4.BeautifulSoup(content, "html.parser")
    Address.objects.filter(id=address.id).update(
        done_info=True, **extract_data_from_page_content(soup))
    for person in extract_persons(soup):
        IkPerson.objects.update_or_create(ik=address, **person)


def update_info():
    while Address.objects.filter(done_tree=False).exists():
        for a in Address.objects.filter(done_tree=False):
            process_tree(a)

    while Address.objects.filter(done_info=False).exists():
        for a in Address.objects.filter(done_info=False):
            process_info(a)


def write_data_json_to_file(file_name: str):
    import json

    data = [a.values() for a in Address.objects.all().order_by('title')]
    with open(file_name, 'w+') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def write_address_with_children(address: Address):
    import os
    import json
    from django.conf import settings

    item = address
    path = []
    while item.parent:
        path.append(item.parent.name.replace(' ', '_'))
        item = item.parent
    path.reverse()
    dir_path = os.path.join(settings.BASE_DIR, 'data', 'split', *path)
    file_name = address.name.replace(' ', '_') + '.json'
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, file_name), 'w+') as f:
        f.write(json.dumps(address.values(), ensure_ascii=False, indent=2, sort_keys=True))
    for children in address.children.all():
        write_address_with_children(children)


def get_init_data():
    import re
    import bs4

    res = requests.get('http://www.tomsk.vybory.izbirkom.ru/region/tomsk?action=ik')
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    script_text = soup.find('div', id='tree').next_sibling.next_sibling.text
    cikrf_id = re.search(r"\d{13}", script_text).group()

    return {
        'name': 'Избирательная комиссия Томской области',
        'cikrf_id': cikrf_id,
        'region': 'tomsk',
        'reg_num': '70',
        'level': '1',
    }

