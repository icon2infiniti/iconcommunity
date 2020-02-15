from django import forms
from .models import PrepProject


class PrepProjectForm(forms.ModelForm):

    class Meta:
        model = PrepProject
        exclude = ['prep_address']

    def __init__(self, *args, **kwargs):
        super(PrepProjectForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.label in ['Details', 'Updates', 'Final update']:
                visible.field.widget.attrs['class'] = 'textproposalarea'                
            elif visible.label in ['Category', 'Progress', 'Status']:
                visible.field.widget.attrs['class'] = 'selectpicker'                
            else:
                visible.field.widget.attrs['class'] = 'form-control' 