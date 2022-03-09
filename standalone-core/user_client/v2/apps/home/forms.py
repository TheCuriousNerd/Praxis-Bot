from cProfile import label
from django import forms
from django.forms import ModelForm
from .models import Chyron_Entry
from .models import PraxisBot_Commands_v0
from .models import PraxisBot_Settings


class PraxisBot_Settings_Form(ModelForm):
    """
    PraxisBot Settings
    """
    class Meta:
        model = PraxisBot_Settings
        fields = ['initialSetup']

class Chyron_EntryForm(ModelForm):
    class Meta:
        model = Chyron_Entry
        fields = ('text', 'tag', 'isEnabled')

class PraxisBot_Commands_v0_Form(ModelForm):
    class Meta:
        model = PraxisBot_Commands_v0
        fields = ('command', 'response', 'isEnabled')