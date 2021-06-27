from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    def get_object(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_field or self.lookup_url_kwarg
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg],
                         **kwargs, }
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(user=self.request.user)
        success = instance.delete()
        return Response({'success': bool(success)},
                        status=status.HTTP_200_OK)
