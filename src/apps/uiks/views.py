from apps.uiks import serializers
from apps.uiks.models import Address
from rest_framework.generics import ListAPIView
from rest_framework_gis.filters import InBBoxFilter
from rest_framework_jsonp.renderers import JSONPRenderer


class LocationList(ListAPIView):
    queryset = Address.objects.filter(voteroom_lat__isnull=False)
    serializer_class = serializers.LocationSerializer
    bbox_filter_field = 'voteroom_coord'
    filter_backends = (InBBoxFilter, )
    bbox_filter_include_overlapping = True  # Optional
    renderer_classes = (JSONPRenderer,)
