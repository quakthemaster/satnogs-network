from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins

from network.api.perms import StationOwnerCanEditPermission
from network.api import serializers, filters
from network.base.models import (Antenna, Data, Observation, Satellite,
                                 Station, Transponder)


class AntennaView(viewsets.ReadOnlyModelViewSet):
    queryset = Antenna.objects.all()
    serializer_class = serializers.AntennaSerializer


class StationView(viewsets.ReadOnlyModelViewSet):
    queryset = Station.objects.all()
    serializer_class = serializers.StationSerializer


class SatelliteView(viewsets.ReadOnlyModelViewSet):
    queryset = Satellite.objects.all()
    serializer_class = serializers.SatelliteSerializer


class TransponderView(viewsets.ReadOnlyModelViewSet):
    queryset = Transponder.objects.all()
    serializer_class = serializers.TransponderSerializer


class ObservationView(viewsets.ReadOnlyModelViewSet):
    queryset = Observation.objects.all()
    serializer_class = serializers.ObservationSerializer


class DataView(viewsets.ModelViewSet, mixins.UpdateModelMixin):
    queryset = Data.objects.all()
    serializer_class = serializers.DataSerializer
    permission_classes = [
        StationOwnerCanEditPermission
    ]


class JobView(viewsets.ReadOnlyModelViewSet):
    queryset = Data.objects.filter(payload='')
    serializer_class = serializers.JobSerializer
    filter_class = filters.DataViewFilter
    filter_fields = ('ground_station')

    def get_queryset(self):
        queryset = self.queryset.filter(start__gte=now())
        gs_id = self.request.QUERY_PARAMS.get('ground_station', None)
        if gs_id and self.request.user.is_authenticated():
            gs = get_object_or_404(Station, id=gs_id)
            if gs.owner == self.request.user:
                gs.last_seen = now()
                gs.save()
        return queryset
