from django import forms
from .questions import QUESTIONS

class SurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

        if self.question is None:
            return

        q = self.question
        field_name = f'question_{q["number"]}'

        if q['type'] == 'text':
            self.fields[field_name] = forms.CharField(
                required=q.get('required', True),
                max_length=q.get('max_length', 50),
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': q['text']}),
            )

        elif q['type'] == 'textarea':
            self.fields[field_name] = forms.CharField(
                required=q.get('required', True),
                max_length=q.get('max_length', 1000),
                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': q['text']}),
            )

        elif q['type'] == 'number':
            self.fields[field_name] = forms.IntegerField(
                required=True,
                min_value=q.get('min', 10),
                max_value=q.get('max', 100),
                widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': q['text']}),
            )

        elif q['type'] == 'select':
            choices = [(opt, opt) for opt in q['options']]
            self.fields[field_name] = forms.ChoiceField(
                required=True,
                choices=choices,
                widget=forms.Select(attrs={'class': 'form-select'}),
            )

        elif q['type'] == 'checkbox':
            choices = [(opt, opt) for opt in q['options']]
            self.fields[field_name] = forms.MultipleChoiceField(
                required=q.get('required', True),
                choices=choices,
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            )

        elif q['type'] == 'rating':
            choices = [(str(opt['value']), f"{'⭐' * opt['value']} {opt['label']}") for opt in q['options']]
            self.fields[field_name] = forms.ChoiceField(
                required=True,
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
            )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
