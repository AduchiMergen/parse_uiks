def translate_dadata_object(dadata_object):
    dadata_object = dadata_object['data']
    attrs = []
    region = ' '.join((dadata_object['region'] or '', dadata_object['region_type_full'] or '')).strip()
    if region:
        attrs.append(region)

    area = ' '.join((dadata_object['area'] or '', dadata_object['area_type_full'] or '')).strip()
    if area:
        attrs.append(area)

    if dadata_object['city_type'] == 'г':
        city = ' '.join((dadata_object['city_type_full'] or '', dadata_object['city'] or '')).strip()
    else:
        city = ' '.join((dadata_object['city'] or '', dadata_object['city_type_full'] or '')).strip()
    if city:
        attrs.append(city)

    settlement = ' '.join((dadata_object['settlement'] or '', dadata_object['settlement_type_full'] or '')).strip()
    if settlement:
        attrs.append(settlement)

    street = ' '.join((dadata_object['street'] or '', dadata_object['street_type_full'] or '')).strip()
    if street:
        attrs.append(street)

    house = (dadata_object['house'] or '').strip()
    if house:
        attrs.append(house)

    return ', '.join(attrs).lower()


def search_uik_num(query: str):
    pass
