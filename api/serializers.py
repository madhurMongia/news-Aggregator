from rest_framework.serializers import ModelSerializer
from .models import TechPost
class PostSerializer(ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields',None)
        super().__init__(*args, **kwargs)
        if(fields is not None):
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    class Meta:
        model = TechPost
        fields = '__all__'