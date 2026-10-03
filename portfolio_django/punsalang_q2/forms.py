from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Project, TechStack


class SuperuserAuthenticationForm(AuthenticationForm):
    """Login form that only lets superusers in, even if other accounts exist."""

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_superuser:
            # Same message as a wrong password, so it doesn't reveal that
            # the account exists.
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )


class ProjectForm(forms.ModelForm):
    tech_stack = forms.ModelMultipleChoiceField(
        queryset=TechStack.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Tech Stacks',
        error_messages={'required': 'Select at least one tech stack.'},
    )

    class Meta:
        model = Project
        fields = ['project_name', 'description', 'tech_stack', 'link']
        labels = {
            'project_name': 'Project Name',
            'description': 'Project Description',
            'link': 'Link',
        }
        widgets = {
            'project_name': forms.TextInput(attrs={'placeholder': 'e.g. Personal Portfolio Website'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'What does this project do?'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
        }

    def clean_project_name(self):
        name = self.cleaned_data['project_name'].strip()
        if not name:
            raise forms.ValidationError('Project name cannot be blank.')
        return name

    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        if not description:
            raise forms.ValidationError('Project description cannot be blank.')
        return description


class TechStackForm(forms.ModelForm):
    class Meta:
        model = TechStack
        fields = ['name']
        labels = {'name': 'Tech Stack Name'}
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'e.g. Python'})}

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise forms.ValidationError('Tech stack name cannot be blank.')
        # Block "python" when "Python" already exists so stacks are never duplicated.
        if TechStack.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(f'The tech stack "{name}" already exists.')
        return name
