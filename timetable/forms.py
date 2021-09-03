from django import forms
from .models import GroupModel, TeacherModel


class GroupForm(forms.Form):

    group = forms.ModelChoiceField(
        queryset=GroupModel.objects.order_by('name'),
    )
    date = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'datepicker'
    }))


class TeacherForm(forms.Form):

    teacher = forms.ModelChoiceField(
        queryset=TeacherModel.objects.order_by('name'),
    )
    date = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'datepicker'
    }))
