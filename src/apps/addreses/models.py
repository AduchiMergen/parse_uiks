from django.db import models
from mptt.models import MPTTModel

SKIP_LEVELS = ['2', '13']


class TreeItem(models.Model):
    cik_tree_id = models.BigIntegerField()
    intid = models.CharField(max_length=100)
    levelid = models.CharField(max_length=100)
    text = models.CharField(max_length=200)
    uik_num = models.IntegerField(null=True)
    uik_obj = models.ForeignKey('uiks.Address', null=True, on_delete=models.SET_NULL)
    full_address = models.CharField(max_length=500, default='', blank=True, db_index=True)

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children',
                               db_index=True, on_delete=models.CASCADE)
    done_tree = models.BooleanField(default=False)
    done_info = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ['text']

    def __str__(self):
        if self.levelid in SKIP_LEVELS:
            return self.text
        return self.full_address or self.text

    def children_url(self):
        return 'http://www.cikrf.ru/services/lk_tree/?id={}'.format(self.cik_tree_id)

    def info_url(self):
        return 'http://www.cikrf.ru/services/lk_address/{}?do=result'.format(self.intid)

    def save(self, *args, **kwargs):
        if not self.full_address:
            parent = ''
            if self.parent and self.parent.full_address:
                parent = '{}, '.format(self.parent.full_address)
            if self.levelid not in SKIP_LEVELS:
                self.full_address = '{}{}'.format(parent, self.text.capitalize())
            else:
                if self.parent:
                    self.full_address = self.parent.full_address
        if not self.uik_obj and self.uik_num:
            from apps.uiks.models import Address
            self.uik_obj = Address.objects.filter(uik_num=self.uik_num).first()
        return super(TreeItem, self).save(*args, **kwargs)
