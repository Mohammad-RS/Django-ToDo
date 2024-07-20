from django import forms

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task 
        fields = ['title', 'description', 'deadline']
        labels = {'title': '', 'description': '', 'deadline': ''}
        widgets = {
            'description': forms.TextInput(),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'todo-input-title', 'placeholder': 'Title'})
        self.fields['description'].widget.attrs.update({'class': 'todo-input-description', 'placeholder': 'Description'})
        self.fields['deadline'].widget.attrs.update({'class': 'todo-input-deadline', 'placeholder': 'Deadline'})
