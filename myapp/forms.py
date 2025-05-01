from .models import Organization
#Auth from
from django import forms
from django.contrib.auth.hashers import make_password
from .models import Organization, State, City,CompanyCategory,Positions,Member,Agency,Login
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
import re


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'solid-line-input', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'solid-line-input', 'placeholder': 'Password'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if not email or not password:
            raise forms.ValidationError("Both fields are required.")

        return self.cleaned_data


class OrganizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Dynamically set the city queryset when state is selected
        if 'state' in self.data:
            state_id = self.data.get('state')
            self.fields['city'].queryset = City.objects.filter(state_id=state_id)
        elif self.instance and self.instance.pk:
            self.fields['city'].queryset = City.objects.filter(state=self.instance.state)

        # Set initial values for state and city if an instance exists
        if self.instance and self.instance.pk:
            self.fields['state'].initial = self.instance.state
            self.fields['city'].initial = self.instance.city

        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f'{field.label} <span class="required-field">*</span>')

    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'state-dropdown'}),
        label="State"
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.none(),  # Initially empty, filled dynamically
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'city-dropdown'}),
        label="City"
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    
    # ✅ Use ModelChoiceField for ccid with Bootstrap dropdown styling
    ccid = forms.ModelChoiceField(
        queryset=CompanyCategory.objects.all(),
        empty_label="Select Company Category",
        widget=forms.Select(attrs={'class': 'form-select'}),  # Bootstrap 5 dropdown
        label="Company Category"
    )

    class Meta:
        model = Organization
        fields = ['cmpname', 'strmobileno', 'stremail', 'state', 'city', 'website', 'status', 'logo', 'cmp_strength', 'password','ccid']

        labels = {  # ✅ Custom Labels
            'cmpname': "Company Name",
            'strmobileno': "Mobile Number",
            'stremail': "Email Address",
            'state': "State",
            'city': "City",
            'website': "Company Website",
            'strstatus': "Status",
            'logo': "Company Logo",
            'cmp_strength': "Company Strength",
            'password': "Password",
            'ccid': "Company Category",
        }
        
        widgets = {
            'cmpname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'strmobileno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'stremail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'state': forms.Select(attrs={'class': 'form-control'}),  # Dropdown
            'city': forms.Select(attrs={'class': 'form-control'}),  # Dropdown
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'strstatus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Status'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'cmp_strength': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Company Strength'}),
        }

    def clean_cmpname(self):
        """Validate that company name contains only alphabets and spaces."""
        cmpname = self.cleaned_data.get('cmpname')
        if not re.match(r'^[A-Za-z\s]+$', cmpname):  # Only letters and spaces
            raise ValidationError("Company name can only contain alphabets and spaces.")
        return cmpname

    def clean_strmobileno(self):
        """Validate that mobile number contains only numeric characters and is exactly 10 digits."""
        strmobileno = self.cleaned_data.get('strmobileno')
        if not re.match(r'^\d{10}$', strmobileno):  # Ensures exactly 10 digits
            raise ValidationError("Mobile number must be exactly 10 digits and numeric.")
        return strmobileno

    def clean_stremail(self):
        """Validate that email ends with @gmail.com."""
        stremail = self.cleaned_data.get('stremail')
        if not stremail.endswith("@gmail.com"):
            raise ValidationError("Email must be a valid Gmail address (e.g., example@gmail.com).")
        return stremail

    def clean_website(self):
        """Validate that the website starts with 'https://' and ends with '.com'."""
        website = self.cleaned_data.get('website')
        if not re.match(r'^https:\/\/.*\.com$', website):
            raise ValidationError("Website URL must start with 'https://' and end with '.com'.")
        return website

    def clean_logo(self):
        """Validate that logo is in JPG, JPEG, or PNG format."""
        logo = self.cleaned_data.get('logo')
        if logo:
            allowed_extensions = ['jpg', 'jpeg', 'png']
            ext = logo.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise ValidationError("Only JPG, JPEG, and PNG files are allowed for the logo.")
        return logo

    def clean_password(self):
        """Validate password complexity: at least 8 characters, one uppercase, one lowercase, one number, and one special character."""
        password = self.cleaned_data.get('password')
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise ValidationError(
                "Password must be at least 8 characters long and contain at least one uppercase letter, "
                "one lowercase letter, one digit, and one special character (@$!%*?&)."
            )
        return password
    

class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f'{field.label} <span class="required-field">*</span>')

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gender'}),
        label="Gender"
    )

    position = forms.ModelChoiceField(
        queryset=Positions.objects.all(),
        empty_label="Select Position",
        required=False
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

    address = forms.CharField(
        label="Address",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': '4'})
    )

    class Meta:
        model = Member
        fields = [
            'firstname', 'lastname', 'gender', 'dateofbirth', 'address', 
            'profile', 'eemail', 'phoneno', 'password', 'position'
        ]

        labels = {
            'firstname': "First Name",
            'lastname': "Last Name",
            'gender': "Gender",
            'address': 'Address',
            'dateofbirth': "Date of Birth",
            'eemail': "Email Address",
            'phoneno': "Contact Number",
            'position': "Position",
            'password': "Password",
            'profile': "Profile Picture"
        }

        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'dateofbirth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth', 'type': 'date'}),
            'profile': forms.FileInput(attrs={'class': 'form-control'}),
            'eemail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phoneno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
        }

    def clean_firstname(self):
        firstname = self.cleaned_data.get('firstname')
        if not re.match(r'^[A-Za-z\s]+$', firstname):
            raise ValidationError("First name can only contain alphabets and spaces.")
        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if not re.match(r'^[A-Za-z\s]+$', lastname):
            raise ValidationError("Last name can only contain alphabets and spaces.")
        return lastname

    def clean_phoneno(self):
        phoneno = self.cleaned_data.get('phoneno')
        if not re.match(r'^\d{10}$', phoneno):
            raise ValidationError("Mobile number must be exactly 10 digits and numeric.")
        return phoneno

    def clean_eemail(self):
        eemail = self.cleaned_data.get('eemail')
        if eemail and not eemail.endswith("@gmail.com"):
            raise ValidationError("Email must be a valid Gmail address (e.g., example@gmail.com).")
        return eemail

    def clean_profile(self):
        profile = self.cleaned_data.get('profile')
        if profile:
            allowed_extensions = ['jpg', 'jpeg', 'png']
            ext = profile.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise ValidationError("Only JPG, JPEG, and PNG files are allowed for the profile picture.")
        return profile

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise ValidationError(
                "Password must be at least 8 characters long, with one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        return password

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not re.match(r'^[\w\s,.-/]+$', address):
            raise ValidationError(
                "Address can only contain letters, numbers, spaces, commas, dots, hyphens, and slashes."
            )
        if len(address) < 5:
            raise ValidationError("Address must be at least 5 characters long.")
        return address



class AgencyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f'{field.label} <span class="required-field">*</span>')
    
        # ✅ Dynamically set the city queryset when state is selected
        if 'state' in self.data:
            state_id = self.data.get('state')
            self.fields['city'].queryset = City.objects.filter(state_id=state_id)
        elif self.instance and self.instance.pk:
            self.fields['city'].queryset = City.objects.filter(state=self.instance.state)

        # Set initial values for state and city if an instance exists
        if self.instance and self.instance.pk:
            self.fields['state'].initial = self.instance.state
            self.fields['city'].initial = self.instance.city

        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f'{field.label} <span class="required-field">*</span>')

    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'state-dropdown'}),
        label="State"
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.none(),  # Initially empty, filled dynamically
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'city-dropdown'}),
        label="City"
    )
        
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )


    class Meta:
        model = Agency # ✅ Fixed model name
        fields = ['agency_name', 'email_address', 'state', 'city', 'date_of_establishment', 'contact_number','website', 'logo', 'status', 'password']

        labels = {
            'agency_name': "Agency Name",
            'email_address': "Email Address",
            'date_of_establishment': "Date Of Establishment",
            'contact_number': 'Contact Number',
            'website': "Wensite URL",
            'logo': "Agency Logo",
            'status': "Active/Not Active",
            'password': "Password",
        }

        widgets = {
            'agency_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agency Name'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'date_of_establishment': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Establishment', 'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Contact Number'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Agency Logo'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Active/Not Active'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }

    def clean_agency_name(self):
        agency_name = self.cleaned_data.get('agency_name')
        if not re.match(r'^[A-Za-z\s]+$', agency_name):  # ✅ Use raw string
            raise ValidationError("Agency name can only contain alphabets and spaces.")
        return agency_name

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not re.match(r'^\d{10}$', contact_number):
            raise ValidationError("Mobile number must be exactly 10 digits and numeric.")
        return contact_number

    def clean_email_address(self):
        email_address = self.cleaned_data.get('email_address')
        if not email_address.endswith("@gmail.com"):
            raise ValidationError("Email must be a valid Gmail address (e.g., example@gmail.com).")
        return email_address

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo:
            allowed_extensions = ['jpg', 'jpeg', 'png']
            ext = logo.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise ValidationError("Only JPG, JPEG, and PNG files are allowed for the profile picture.")
        return logo

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise ValidationError(
                "Password must be at least 8 characters long, with one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        return password

#cv_builder
from django import forms
from django.forms import modelformset_factory
from .models import MemberEducation, MemberSkills, MemberExperience, MemberLanguage, MemberLink,Summary

# 🔹 MemberEducation Form
class MemberEducationForm(forms.ModelForm):
    class Meta:
        model = MemberEducation
        fields = ['passingyear', 'institute', 'grade', 'remark']
        widgets = {
            'passingyear': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Passing Year'}),
            'institute': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Institute Name'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Grade'}),
            'remark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Any Remark'}),
        }

# 🔹 MemberSkills Form
class MemberSkillsForm(forms.ModelForm):
    class Meta:
        model = MemberSkills
        fields = ['skills', 'details']
        widgets = {
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Skill'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skill Details'}),
        }

# 🔹 MemberExperience Form
class MemberExperienceForm(forms.ModelForm):
    class Meta:
        model = MemberExperience
        fields = ['organizationname', 'worktitle', 'workdetails', 'startdate', 'enddate']  # removed totalmonthexperience
        widgets = {
            'organizationname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'}),
            'worktitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'workdetails': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe Your Work', 'rows': 3}),
            'startdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'enddate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# 🔹 MemberLanguage Form
class MemberLanguageForm(forms.ModelForm):
    class Meta:
        model = MemberLanguage
        fields = ['language']
        widgets = {
            'language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Language'}),
        }

# 🔹 MemberLink Form
class MemberLinkForm(forms.ModelForm):
    class Meta:
        model = MemberLink
        fields = ['link_name', 'link_url']
        widgets = {
            'link_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link Name (e.g., Portfolio, LinkedIn)'}),
            'link_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
        }
class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ['summary']
        '''widgets = {
            'summary': forms.TextInput(attrs={'class':'form-control','placeholder':'Add your summary here...'})           
        }'''

# ✅ Use `modelformset_factory` to support deletion of objects
MemberEducationFormSet = modelformset_factory(
    MemberEducation, form=MemberEducationForm, extra=1, can_delete=True
)

MemberSkillsFormSet = modelformset_factory(
    MemberSkills, form=MemberSkillsForm, extra=1, can_delete=True
)

MemberExperienceFormSet = modelformset_factory(
    MemberExperience, form=MemberExperienceForm, extra=1, can_delete=True
)

MemberLanguageFormSet = modelformset_factory(
    MemberLanguage, form=MemberLanguageForm, extra=1, can_delete=True
)

MemberLinkFormSet = modelformset_factory(
    MemberLink, form=MemberLinkForm, extra=1, can_delete=True
)
SummaryFormSet = modelformset_factory(
    Summary, form=SummaryForm, extra=1, can_delete=True
)

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['posttitle', 'postcontent', 'postdesc']
        widgets = {
            'posttitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'}),
            'postcontent': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'postdesc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a caption...', 'rows': 4}),
        }
