from django.core.serializers.python import Serializer


class JSONSerializer(Serializer):
    def end_object(self, obj):
        self._current[obj._meta.pk.name] = obj._get_pk_val()
        self.objects.append(self._current)