from django.contrib.gis.db.models import PointField
from django.db import models


class Address(models.Model):
    name = models.CharField(max_length=150)
    cikrf_id = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    reg_num = models.IntegerField()

    done_tree = models.BooleanField(default=False)
    done_info = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children',
                               db_index=True, on_delete=models.CASCADE)

    uik_num = models.SmallIntegerField(null=True)

    level = models.SmallIntegerField(default=1)

    title = models.CharField(max_length=200, null=True, blank=True)
    ik_address = models.CharField(max_length=1000, null=True, blank=True)
    ik_lat = models.FloatField(null=True, blank=True)
    ik_lon = models.FloatField(null=True, blank=True)
    ik_phone = models.CharField(max_length=100, null=True, blank=True)
    fax = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    expired_date = models.DateField(null=True, blank=True)
    voteroom_address = models.CharField(max_length=1000, null=True, blank=True)
    voteroom_lat = models.FloatField(null=True, blank=True)
    voteroom_lon = models.FloatField(null=True, blank=True)
    voteroom_coord = PointField(null=True, db_index=True)
    voteroom_phone = models.CharField(max_length=100, null=True, blank=True)

    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['update_time']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if 'Участковая избирательная комиссия №' in self.name:
            import re
            match = re.search(r'Участковая избирательная комиссия №\s?(?P<uik_num>\d+)', self.name)
            self.uik_num = match.groupdict().get('uik_num')
        if self.voteroom_lat and self.voteroom_lon:
            from django.contrib.gis.geos import Point
            self.voteroom_coord = Point(self.voteroom_lat, self.voteroom_lon)

        return super().save(*args, **kwargs)

    @property
    def tree_url(self):
        url = 'http://www.{reg}.vybory.izbirkom.ru/region/{reg}' \
               '?action=ikTree&region={reg_num:02}&vrn={cikrf_id}' \
               ''.format(
                    reg=self.region, cikrf_id=self.cikrf_id, reg_num=self.reg_num,
                )
        if self.parent:
            url += '&onlyChildren=true'
        return url

    @property
    def info_url(self):
        url = 'http://www.{reg}.vybory.izbirkom.ru/region/{reg}?action=ik&vrn={cikrf_id}'.format(
            reg=self.region, cikrf_id=self.cikrf_id,
        )
        return url

    def values(self):
        from django.template.defaultfilters import default
        return {
            'title': default(self.title, '').strip(),
            'ik_address': default(self.ik_address, '').strip(),
            'ik_lat': self.ik_lat,
            'ik_lon': self.ik_lon,
            'ik_phone': default(self.ik_phone, '').strip(),
            'fax': default(self.fax, '').strip(),
            'email': default(self.email, '').strip(),
            'expired_date': str(self.expired_date),
            'voteroom_address': default(self.voteroom_address, '').strip(),
            'voteroom_lat': self.voteroom_lat,
            'voteroom_lon': self.voteroom_lon,
            'voteroom_phone': default(self.voteroom_phone, '').strip(),

            'persons': sorted(list(self.ikperson_set.values(
                'person_name', 'status', 'recomend_by'
            )), key=lambda x: x['person_name']),

            'info_url': self.info_url.strip(),
        }


class IkPerson(models.Model):
    ik = models.ForeignKey(Address, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    recomend_by = models.CharField(max_length=400)
