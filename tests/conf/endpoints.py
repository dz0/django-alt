from django_alt.abstract.validators import BaseValidator
from django_alt.endpoints import Endpoint
from django_alt.serializers import ValidatedModelSerializer
from django_alt.utils.shortcuts import invalid_if
from tests.conf.models import ModelA


class ModelAValidator(BaseValidator):
    pass

class ModelAValidator2(BaseValidator):
    def to_representation(self, repr_attrs, validated_attrs: dict = None):
        repr_attrs['extra'] = 'this is an extra'
        invalid_if(repr_attrs['id'] == 2, 'error', 'msg')


class ModelASerializer(ValidatedModelSerializer):
    class Meta:
        model = ModelA
        validator_class = ModelAValidator
        fields = '__all__'


class ModelASerializer2(ValidatedModelSerializer):
    class Meta:
        model = ModelA
        validator_class = ModelAValidator2
        fields = '__all__'


class ModelAEndpoint1(Endpoint):
    serializer = ModelASerializer
    config = {'get': dict(query=lambda model, **url: model.objects.all())}


class ModelAEndpoint2(Endpoint):
    serializer = ModelASerializer2
    config = {'get': dict(query=lambda model, **url: model.objects.all())}


class ModelAEndpoint3(Endpoint):
    serializer = ModelASerializer
    config = {'get': {
        'query': lambda model, **url: model.objects.all(),
        'filters': {
            'filter1': lambda queryset, param: queryset.filter(field_1=param),
            'filter2': lambda queryset, param: queryset.filter(field_2=param),
        }
    }}


class ModelAEndpoint4(Endpoint):
    serializer = ModelASerializer
    config = {'get': {
        'query': lambda model, **url: model.objects.all(),
        'filters': {
            'filter1': lambda queryset, param: queryset.filter(field_1=param),
            'filter2': lambda queryset, param: queryset.filter(field_2=param),
        }
    }}

    @classmethod
    def can_get(cls):
        return lambda request, **kwargs: False, None


class ModelAEndpoint5(Endpoint):
    serializer = ModelASerializer
    config = {'get': {
        'query': lambda model, **url: model.objects.all(),
        'filters': {
            'filter1': lambda queryset, param: queryset.filter(field_1=param),
            'filter2': lambda queryset, param: queryset.filter(field_2=param),
        }
    }}

    @classmethod
    def can_get(cls):
        return None, lambda request, qs, attrs: False


class ModelAEndpoint6(Endpoint):
    serializer = ModelASerializer
    config = {
        'post': None,
        'patch': {
            'query': lambda model_a, **_: model_a.objects.first()
        }
    }


class ModelAEndpoint7(Endpoint):
    serializer = ModelASerializer
    config = {
        'delete': {
            'query': lambda model_a, **_: model_a.objects.first()
        }
    }

class ModelAEndpoint8(Endpoint):
    serializer = ModelASerializer
    config = {
        'delete': {
            'query': lambda model_a, **_: model_a.objects.all()
        }
    }