from django import forms
from .models import Record, SubGroup, Group, Area, Flower, Farm

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('date', 'farm', 'flower', 'area', 'group', 'sub_group', 'data_type', 'really', 'theoric', 'goal')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_group'].queryset = SubGroup.objects.none()
        
        if 'group' in self.data:
            try:
                group_id = int(self.data.get('group'))
                self.fields['sub_group'].queryset = SubGroup.objects.filter(group_id=group_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty sub_group queryset
        elif self.instance.pk and self.instance.group is not None:
            self.fields['sub_group'].queryset = SubGroup.objects.filter(group=self.instance.group).order_by('name')
        
        # Filtrar grupos para excluir los eliminados
        self.fields['group'].queryset = Group.objects.filter(is_deleted=False).order_by('name')

        # Filtrar áreas para excluir las eliminadas
        self.fields['area'].queryset = Area.objects.filter(is_deleted=False).order_by('name')

        # Filtrar flores para excluir las eliminadas
        self.fields['flower'].queryset = Flower.objects.filter(is_deleted=False).order_by('name')

        # Filtrar farms para excluir las eliminadas
        self.fields['farm'].queryset = Farm.objects.filter(is_deleted=False).order_by('name')
 
        
