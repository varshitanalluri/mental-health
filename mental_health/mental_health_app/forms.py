from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class ParentRegistrationForm(UserCreationForm):
    child_name = forms.CharField(max_length=100)
    child_username = forms.CharField(max_length=100)
    child_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Create the child user
        child_user = User.objects.create_user(
            username=self.cleaned_data['child_username'],
            password=self.cleaned_data['child_password']
        )
        child_profile = UserProfile.objects.create(user=child_user, role='child', linked_parent=user)

        # Create the parent profile
        parent_profile = UserProfile.objects.create(user=user, role='parent')

        return user

class ChildStressForm(forms.Form):
    q1 = forms.IntegerField(label='Feeling nervous, anxious or on edge', min_value=0, max_value=3)
    q2 = forms.IntegerField(label='Not being able to stop or control worrying', min_value=0, max_value=3)
    q3 = forms.IntegerField(label='Worrying too much about different things', min_value=0, max_value=3)
    q4 = forms.IntegerField(label='Trouble relaxing', min_value=0, max_value=3)
    q5 = forms.IntegerField(label='Being so restless that it is hard to sit still', min_value=0, max_value=3)
    q6 = forms.IntegerField(label='Becoming easily annoyed or irritable', min_value=0, max_value=3)
    q7 = forms.IntegerField(label='Feeling afraid as if something awful might happen', min_value=0, max_value=3)
    q8 = forms.IntegerField(label='Feeling tired or having little energy', min_value=0, max_value=3)
    q9 = forms.IntegerField(label='Poor appetite or overeating', min_value=0, max_value=3)
    q10 = forms.IntegerField(label='Feeling bad about yourself—or that you are a failure', min_value=0, max_value=3)
    q11 = forms.IntegerField(label='Trouble concentrating on things', min_value=0, max_value=3)
    q12 = forms.IntegerField(label='Moving or speaking so slowly that other people could have noticed', min_value=0, max_value=3)
    q13 = forms.IntegerField(label='Thoughts that you would be better off dead or of hurting yourself in some way', min_value=0, max_value=3)

class ParentStressForm(forms.Form):
    q1 = forms.IntegerField(label='My child seems anxious or nervous', min_value=0, max_value=3)
    q2 = forms.IntegerField(label='My child worries about school or friends', min_value=0, max_value=3)
    q3 = forms.IntegerField(label='My child appears restless or unable to relax', min_value=0, max_value=3)
    q4 = forms.IntegerField(label='My child has difficulty sleeping due to worries', min_value=0, max_value=3)
    q5 = forms.IntegerField(label='My child complains about physical symptoms (e.g., stomach aches) without a medical reason', min_value=0, max_value=3)
    q6 = forms.IntegerField(label='My child avoids certain situations due to fear or anxiety', min_value=0, max_value=3)
    q7 = forms.IntegerField(label='My child seeks excessive reassurance from me', min_value=0, max_value=3)
    q8 = forms.IntegerField(label='My child appears fatigued or low on energy', min_value=0, max_value=3)
    q9 = forms.IntegerField(label='My child has shown changes in eating habits', min_value=0, max_value=3)
    q10 = forms.IntegerField(label='My child expresses negative thoughts about themselves', min_value=0, max_value=3)
    q11 = forms.IntegerField(label='My child has difficulty concentrating on tasks', min_value=0, max_value=3)
    q12 = forms.IntegerField(label='My child seems unusually slow or withdrawn', min_value=0, max_value=3)
    q13 = forms.IntegerField(label='My child has mentioned self-harm or feeling hopeless', min_value=0, max_value=3)