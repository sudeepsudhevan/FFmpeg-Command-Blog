from django import forms
from .models import Command, EditRequest

class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['title', 'command_string', 'explanation']
        widgets = {
            'command_string': forms.Textarea(attrs={'rows': 3, 'class': 'code-input', 'placeholder': 'ffmpeg -i input.mp4 ...'}),
            'explanation': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Explain what each flag does...'})
        }

class EditRequestForm(forms.ModelForm):
    class Meta:
        model = EditRequest
        fields = ['suggested_command_string', 'suggested_explanation']
        widgets = {
            'suggested_command_string': forms.Textarea(attrs={'rows': 3, 'class': 'code-input'}),
            'suggested_explanation': forms.Textarea(attrs={'rows': 5})
        }
