from apps.uiks.models import Address
from rest_framework.fields import SerializerMethodField
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class LocationSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    clusterCaption = SerializerMethodField()
    balloonContent = SerializerMethodField()
    balloonContentHeader = SerializerMethodField()

    class Meta:
        model = Address
        geo_field = "voteroom_coord"
        auto_bbox = True

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('id', 'title', 'voteroom_address', 'clusterCaption',
                  'balloonContent', 'balloonContentHeader')

    def get_clusterCaption(self, obj):
        return obj.title

    def get_balloonContent(self, obj):
        return ', '.join([s.replace(' ', '\xa0') for s in obj.voteroom_address.split(', ')[2:]])

    def get_balloonContentHeader(self, obj):
        return obj.title
