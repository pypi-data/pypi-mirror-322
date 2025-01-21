"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_people admin *

:details: lara_django_people admin module admin backend configuration.
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: - run "lara-django-dev forms_generator -c lara_django_people > forms.py" to update this file
________________________________________________________________________
"""

# django crispy forms s. https://github.com/django-crispy-forms/django-crispy-forms for []
# generated with django-extensions forms_generator -c  [] > forms.py (LARA-version)

from django import forms
from django.forms.widgets import DateInput, DateTimeInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit, Row, Column

from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms

from django.utils.translation import gettext_lazy as _


from .models import (
    ExtraData,
    EntityClass,
    Entity,
    EntityRole,
    EntityBankAccount,
    LaraUser,
    MeetingCalendar,
)


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = LaraUser


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = LaraUser
        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    orcid = forms.CharField(max_length=255, label="ORCID", required=False, widget=forms.TextInput(attrs={"placeholder": "ORCID"}))

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super().save(request)

        # Add your own processing here.
        user.orcid = self.cleaned_data['orcid']
        user.save()

        # You must return the original result.
        return user

    class Meta:
        fields = (
            "username",
            "email",
            "password",
            "orcid",
        )


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class ExtraDataCreateForm(forms.ModelForm):
    class Meta:
        model = ExtraData
        fields = (
            "data_type",
            "name",
            "name_full",
            "name_display",
            "namespace",
            "version",
            "hash_sha256",
            "data_json",
            "media_type",
            "iri",
            "url",
            "description",
            "file",
            "image",
            "office_room",
            "laboratory",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "data_type",
            "name",
            "name_full",
            "name_display",
            "namespace",
            "version",
            "hash_sha256",
            "data_json",
            "media_type",
            "iri",
            "url",
            "description",
            "file",
            "image",
            "office_room",
            "laboratory",
            "email",
            Submit("submit", "Create"),
        )


class ExtraDataUpdateForm(forms.ModelForm):
    class Meta:
        model = ExtraData
        fields = (
            "data_type",
            "name",
            "name_full",
            "name_display",
            "namespace",
            "version",
            "hash_sha256",
            "data_json",
            "media_type",
            "iri",
            "url",
            "description",
            "file",
            "image",
            "office_room",
            "laboratory",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "data_type",
            "name",
            "name_full",
            "name_display",
            "namespace",
            "version",
            "hash_sha256",
            "data_json",
            "media_type",
            "iri",
            "url",
            "description",
            "file",
            "image",
            "office_room",
            "laboratory",
            "email",
            Submit("submit", "Create"),
        )


class EntityClassCreateForm(forms.ModelForm):
    class Meta:
        model = EntityClass
        fields = ("name", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("name", "description", Submit("submit", "Create"))


class EntityClassUpdateForm(forms.ModelForm):
    class Meta:
        model = EntityClass
        fields = ("name", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("name", "description", Submit("submit", "Create"))


class EntityRoleCreateForm(forms.ModelForm):
    class Meta:
        model = EntityRole
        fields = ("name", "iri", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("name", "iri", "description", Submit("submit", "Create"))


class EntityRoleUpdateForm(forms.ModelForm):
    class Meta:
        model = EntityRole
        fields = ("name", "iri", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout("name", "iri", "description", Submit("submit", "Create"))


class EntityCreateForm(forms.ModelForm):
    # affiliation_start= forms.DateTimeField(widget=DateTimeInput(), label="Affl. Start", required=False)
    class Meta:
        model = Entity
        fields = (
            "slug",
            "entity_class",
            "gender",
            "title",
            "name_first",
            "names_middle",
            "name_last",
            "name_full",
            "names_last_previous",
            "name_nick",
            "acronym",
            
            "url",
            "pid",
            "orcid",
            "ror",
            "tax_no",
            "vat_no",
            "toll_no",
            "affiliation_current",
            "affiliation_start",
            "affiliation_end",
            "office_room",
            "laboratory",
            "email",
            "email_private",
            "email_permanent",
            "website",
            "phone_number_mobile",
            "phone_number_office",
            "phone_number_lab",
            "phone_number_home",
            "address",
            "date_birth",
            "date_death",
            "color",
            "icon",
            "image",
            "iri",
        )
        widgets = {
            "name_first": forms.TextInput(attrs={"placeholder": "First name", "required": True, "rows": 1}),
            "names_middle": forms.TextInput(attrs={"placeholder": "Middle names", "required": False, "rows": 1}),
            "name_last": forms.TextInput(attrs={"placeholder": "Last name", "required": False, "rows": 1}),
            "name_full": forms.TextInput(attrs={"placeholder": "Full name", "required": False, "rows": 1}),
            "names_last_previous": forms.TextInput(
                attrs={"placeholder": "Previous last names", "required": False, "rows": 1}
            ),
            "name_nick": forms.TextInput(attrs={"placeholder": "Nick name", "required": False, "rows": 1}),
            "acronym": forms.TextInput(attrs={"placeholder": "Acronym", "required": False, "rows": 1}),
            "url": forms.URLInput(),
            "pid": forms.URLInput(),
            "orcid": forms.TextInput(attrs={"placeholder": "ORCID", "required": False, "rows": 1}),
            "ror": forms.TextInput(attrs={"placeholder": "ROR", "required": False, "rows": 1}),
            "tax_no": forms.TextInput(attrs={"placeholder": "TAX no", "required": False, "rows": 1}),
            "vat_no": forms.TextInput(attrs={"placeholder": "VAT no", "required": False, "rows": 1}),
            "toll_no": forms.TextInput(attrs={"placeholder": "TOLL no", "required": False, "rows": 1}),
            "email": forms.EmailInput(),
            "email_private": forms.EmailInput(),
            "email_permanent": forms.EmailInput(),
            "website": forms.URLInput(),
            "phone_number_mobile": forms.TextInput(
                attrs={"placeholder": "Mobile phone number", "required": False, "rows": 1}
            ),
            "phone_number_office": forms.TextInput(
                attrs={"placeholder": "Office phone number", "required": False, "rows": 1}
            ),
            "phone_number_lab": forms.TextInput(
                attrs={"placeholder": "Lab phone number", "required": False, "rows": 1}
            ),
            "phone_number_home": forms.TextInput(
                attrs={"placeholder": "Home phone number", "required": False, "rows": 1}
            ),
            "affiliation_start": DateInput(attrs={"type": "date"}),
            "affiliation_end": DateInput(attrs={"type": "date"}),
            "date_birth": DateInput(attrs={"type": "date"}),
            "date_death": DateInput(attrs={"type": "date"}),
            "icon": forms.TextInput(attrs={"type": "file"}),
            "color": forms.TextInput(attrs={"type": "color"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("entity_class", css_class="form-group col-md-3 mb-0"),
                Column("gender", css_class="form-group col-md-2 mb-0"),
                Column("title", css_class="form-group col-md-2 mb-0"),
            ),
            Row(
                Column("name_first", css_class="form-group col-md-4 mb-0 pr-2"),
                Column("names_middle", css_class="form-group col-md-4 mb-0 pl-2"),
                Column("name_last", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("name_full", css_class="form-group col-md-12 mb-0"),
            ),
            Row(
                Column("name_nick", css_class="form-group col-md-4 mb-0 pr-2"),
                Column("acronym", css_class="form-group col-md-4 mb-0 pl-2"),
                Column("names_last_previous", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("email", css_class="form-group col-md-4 mb-0 pr-2"),
                Column("email_private", css_class="form-group col-md-4 mb-0 pl-2"),
                Column("email_permanent", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("website", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("phone_number_mobile", css_class="form-group col-md-6 mb-0 pr-2"),
                Column("phone_number_office", css_class="form-group col-md-6 mb-0 pl-2"),
            ),
            Row(
                Column("phone_number_lab", css_class="form-group col-md-6 mb-0 pr-2"),
                Column("phone_number_home", css_class="form-group col-md-6 mb-0 pl-2"),
            ),
            Row(
                Column("address", css_class="form-group col-md-12 mb-0"),
            ),
            Row(
                Column("orcid", css_class="form-group col-md-6 mb-0 pr-2"),
                Column("ror", css_class="form-group col-md-6 mb-0 pl-2"),
            ),
            Row(
                Column("url", css_class="form-group col-md-6 mb-0 pr-2"),
                Column("pid", css_class="form-group col-md-6 mb-0 pl-2"),
            ),
            Row(
                Column("tax_no", css_class="form-group col-md-4 mb-0 pr-2"),
                Column("vat_no", css_class="form-group col-md-4 mb-0 pl-2 pr-2"),
                Column("toll_no", css_class="form-group col-md-4 mb-0 pl-2"),
            ),
            Row(
                Column("affiliation_current", css_class="form-group col-md-4 mb-0 pr-2"),
                Column("affiliation_start", css_class="form-group col-md-4 mb-0 pl-2 pr-2"),
                Column("affiliation_end", css_class="form-group col-md-4 mb-0 pl-2"),
            ),
            Row(
                Column("office_room", css_class="form-group col-md-6 mb-0 pr-2"),
                Column("laboratory", css_class="form-group col-md-6 mb-0 pl-2"),
            ),
            Row(
                Column("date_birth", css_class="form-group col-md-6 mb-0 pr-2"),
                Column("date_death", css_class="form-group col-md-6 mb-0 pl-2"),
            ),
            Row(
                Column("color", css_class="form-group col-md-3 mb-0 pr-2"),
                Column("icon", css_class="form-group col-md-3 mb-0 pl-2 pr-2"),
                Column("image", css_class="form-group col-md-3 mb-0 pl-2"),
            ),
            Submit("submit", "Create"),
        )


class EntityUpdateForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = (
            "slug",
            "entity_class",
            "gender",
            "title",
            "name_first",
            "names_middle",
            "name_last",
            "name_full",
            "names_last_previous",
            "name_nick",
            "acronym",
            
            "url",
            "pid",
            "iri",
            "orcid",
            "ror",
            "tax_no",
            "vat_no",
            "toll_no",
            "affiliation_current",
            "affiliation_start",
            "affiliation_end",
            "office_room",
            "laboratory",
            "email",
            "email_private",
            "email_permanent",
            "website",
            "phone_number_mobile",
            "phone_number_office",
            "phone_number_lab",
            "phone_number_home",
            "address",
            "date_birth",
            "date_death",
            "color",
            "icon",
            "image",
        )
        widgets = {
            "name_first": forms.TextInput(attrs={"placeholder": "First name", "required": True, "rows": 1}),
            "names_middle": forms.TextInput(attrs={"placeholder": "Middle names", "required": False, "rows": 1}),
            "name_last": forms.TextInput(attrs={"placeholder": "Last name", "required": False, "rows": 1}),
            "name_full": forms.TextInput(attrs={"placeholder": "Full name", "required": False, "rows": 1}),
            "names_last_previous": forms.TextInput(
                attrs={"placeholder": "Previous last names", "required": False, "rows": 1}
            ),
            "name_nick": forms.TextInput(attrs={"placeholder": "Nick name", "required": False, "rows": 1}),
            "acronym": forms.TextInput(attrs={"placeholder": "Acronym", "required": False, "rows": 1}),
            "url": forms.URLInput(),
            "pid": forms.URLInput(),
            "orcid": forms.TextInput(attrs={"placeholder": "ORCID", "required": False, "rows": 1}),
            "ror": forms.TextInput(attrs={"placeholder": "ROR", "required": False, "rows": 1}),
            "tax_no": forms.TextInput(attrs={"placeholder": "TAX no", "required": False, "rows": 1}),
            "vat_no": forms.TextInput(attrs={"placeholder": "VAT no", "required": False, "rows": 1}),
            "toll_no": forms.TextInput(attrs={"placeholder": "TOLL no", "required": False, "rows": 1}),
            "email": forms.EmailInput(),
            "email_private": forms.EmailInput(),
            "email_permanent": forms.EmailInput(),
            "website": forms.URLInput(),
            "phone_number_mobile": forms.TextInput(
                attrs={"placeholder": "Mobile phone number", "required": False, "rows": 1}
            ),
            "phone_number_office": forms.TextInput(
                attrs={"placeholder": "Office phone number", "required": False, "rows": 1}
            ),
            "phone_number_lab": forms.TextInput(
                attrs={"placeholder": "Lab phone number", "required": False, "rows": 1}
            ),
            "phone_number_home": forms.TextInput(
                attrs={"placeholder": "Home phone number", "required": False, "rows": 1}
            ),
            "affiliation_start": DateInput(attrs={"type": "date"}),
            "affiliation_end": DateInput(attrs={"type": "date"}),
            "date_birth": DateInput(attrs={"type": "date"}),
            "date_death": DateInput(attrs={"type": "date"}),
            "icon": forms.TextInput(attrs={"type": "file"}),
            "color": forms.TextInput(attrs={"type": "color"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("entity_class", css_class="form-group col-md-3 mb-0"),
                Column("gender", css_class="form-group col-md-2 mb-0"),
                Column("title", css_class="form-group col-md-2 mb-0"),
                
            ),
            Row(
                Column("name_first", css_class="form-group col-md-4 mb-0", input_size="input-group-sm"),
                Column("names_middle", css_class="form-group col-md-4 mb-0"),
                Column("name_last", css_class="form-group col-md-4 mb-0"),
                # limit row height to 1 line  - currently not working
                # input_size="input-group-sm"
            ),
            Row(
                Column("name_full", css_class="form-group col-md-12 mb-0"),
            ),
            Row(
                Column("name_nick", css_class="form-group col-md-4 mb-0"),
                Column("acronym", css_class="form-group col-md-4 mb-0"),
                Column("names_last_previous", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("email", css_class="form-group col-md-4 mb-0"),
                Column("email_private", css_class="form-group col-md-4 mb-0"),
                Column("email_permanent", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("website", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("phone_number_mobile", css_class="form-group col-md-6 mb-0"),
                Column("phone_number_office", css_class="form-group col-md-6 mb-0"),
                Column("phone_number_lab", css_class="form-group col-md-6 mb-0"),
                Column("phone_number_home", css_class="form-group col-md-6 mb-0"),
                Column("address", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("orcid", css_class="form-group col-md-6 mb-0"),
                Column("ror", css_class="form-group col-md-6 mb-0"),
                Column("url", css_class="form-group col-md-6 mb-0"),
                Column("pid", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("tax_no", css_class="form-group col-md-4 mb-0"),
                Column("vat_no", css_class="form-group col-md-4 mb-0"),
                Column("toll_no", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("affiliation_current", css_class="form-group col-md-4 mb-0"),
                Column("affiliation_start", css_class="form-group col-md-4 mb-0"),
                Column("affiliation_end", css_class="form-group col-md-4 mb-0"),
            ),
            Row(
                Column("office_room", css_class="form-group col-md-6 mb-0"),
                Column("laboratory", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("date_birth", css_class="form-group col-md-6 mb-0"),
                Column("date_death", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("color", css_class="form-group col-md-3 mb-0"),
                Column("icon", css_class="form-group col-md-3 mb-0"),
                Column("image", css_class="form-group col-md-3 mb-0"),
            ),
            Submit("submit", "Update"),
        )


class EntityBankAccountCreateForm(forms.ModelForm):
    class Meta:
        model = EntityBankAccount
        fields = ("name_account", "account_no", "iban", "bic", "bank", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name_account", "account_no", "iban", "bic", "bank", "description", Submit("submit", "Create")
        )


class EntityBankAccountUpdateForm(forms.ModelForm):
    class Meta:
        model = EntityBankAccount
        fields = ("name_account", "account_no", "iban", "bic", "bank", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name_account", "account_no", "iban", "bic", "bank", "description", Submit("submit", "Update")
        )


class LaraUserCreateForm(forms.ModelForm):
    class Meta:
        model = LaraUser
        fields = (
            "entity",
            "home_screen_layout",
            "access_token",
            "access_control",
            "confirmation_token",
            "email_confirmed",
            "email_recover",
            "max_logins",
            "failed_logins",
            "ip_curr_login",
            "ip_last_login",
            "datetime_confirmed",
            "datetime_confirmation_sent",
        )
        widgets = {
            "entity": forms.TextInput(attrs={"placeholder": "Entity name"}),
            "access_token": forms.PasswordInput(attrs={"placeholder": "Access token"}),
            "confirmation_TOKEN": forms.PasswordInput(attrs={"placeholder": "Confirmation token"}),
            "email_confirmed": forms.EmailInput(attrs={"placeholder": "Confirmed email"}),
            "email_recover": forms.EmailInput(attrs={"placeholder": "Recovery email"}),
            "ip_curr_login": forms.TextInput(attrs={"placeholder": "Current IP address"}),
            "ip_last_login": forms.TextInput(attrs={"placeholder": "Last IP address"}),
            "datetime_confirmed": DateTimeInput(attrs={"type": "date"}),
            "datetime_confirmation_sent": DateTimeInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Create Lara User",
                Row(
                    Column("entity", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("access_token", css_class="form-group col-md-6 mb-0"),
                    Column("confirmation_token", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("email_confirmed", css_class="form-group col-md-6 mb-0"),
                    Column("email_recover", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("max_logins", css_class="form-group col-md-4 mb-0"),
                    Column("failed_logins", css_class="form-group col-md-4 mb-0"),
                    Column("datetime_confirmed", css_class="form-group col-md-4 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("ip_curr_login", css_class="form-group col-md-6 mb-0"),
                    Column("ip_last_login", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(Column("datetime_confirmation_sent", css_class="form-group col-md-6 mb-0"), css_class="form-row"),
                Submit("submit", "Create", css_class="btn-primary"),
            )
        )


class LaraUserUpdateForm(forms.ModelForm):
    class Meta:
        model = LaraUser
        fields = (
            "entity",
            "home_screen_layout",
            "access_token",
            "access_control",
            "confirmation_token",
            "email_confirmed",
            "email_recover",
            "max_logins",
            "failed_logins",
            "ip_curr_login",
            "ip_last_login",
            "datetime_confirmed",
            "datetime_confirmation_sent",
        )
        widgets = {
            "entity": forms.TextInput(attrs={"placeholder": "Entity name"}),
            "access_TOKEN": forms.PasswordInput(attrs={"placeholder": "Access token"}),
            "confirmation_TOKEN": forms.PasswordInput(attrs={"placeholder": "Confirmation token"}),
            "email_confirmed": forms.EmailInput(attrs={"placeholder": "Confirmed email"}),
            "email_recover": forms.EmailInput(attrs={"placeholder": "Recovery email"}),
            "ip_curr_login": forms.TextInput(attrs={"placeholder": "Current IP address"}),
            "ip_last_login": forms.TextInput(attrs={"placeholder": "Last IP address"}),
            "datetime_confirmed": DateTimeInput(attrs={"type": "date"}),
            "datetime_confirmation_sent": DateTimeInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Update Lara User",
                Row(
                    Column("entity", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("access_token", css_class="form-group col-md-6 mb-0"),
                    Column("confirmation_token", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("email_confirmed", css_class="form-group col-md-6 mb-0"),
                    Column("email_recover", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("max_logins", css_class="form-group col-md-4 mb-0"),
                    Column("failed_logins", css_class="form-group col-md-4 mb-0"),
                    Column("datetime_confirmed", css_class="form-group col-md-4 mb-0"),
                    css_class="form-row",
                ),
                Row(
                    Column("ip_curr_login", css_class="form-group col-md-6 mb-0"),
                    Column("ip_last_login", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
                Row(Column("datetime_confirmation_sent", css_class="form-group col-md-6 mb-0"), css_class="form-row"),
                Submit("submit", "Update", css_class="btn-primary"),
            )
        )


class MeetingsCalendarCreateForm(forms.ModelForm):
    class Meta:
        model = MeetingCalendar
        fields = (
            "name_display",
            "calendar_url",
            "summary",
            "description",
            "color",
            "ics",
            "datetime_start",
            "datetime_end",
            "duration",
            "all_day",
            "created",
            "datetime_last_modified",
            "timestamp",
            "location",
            "geolocation",
            "conference_url",
            "range",
            "related",
            "role",
            "tzid",
            "offset_utc",
            "alarm_repeat_json",
            "event_repeat",
            "event_repeat_json",
            "organiser",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name_display",
            "calendar_url",
            "summary",
            "description",
            "color",
            "ics",
            "datetime_start",
            "datetime_end",
            "duration",
            "all_day",
            "created",
            "datetime_last_modified",
            "timestamp",
            "location",
            "geolocation",
            "conference_url",
            "range",
            "related",
            "role",
            "tzid",
            "offset_utc",
            "alarm_repeat_json",
            "event_repeat",
            "event_repeat_json",
            "organiser",
            Submit("submit", "Create"),
        )


class MeetingsCalendarUpdateForm(forms.ModelForm):
    class Meta:
        model = MeetingCalendar
        fields = (
            "name_display",
            "calendar_url",
            "summary",
            "description",
            "color",
            "ics",
            "datetime_start",
            "datetime_end",
            "duration",
            "all_day",
            "created",
            "datetime_last_modified",
            "timestamp",
            "location",
            "geolocation",
            "conference_url",
            "range",
            "related",
            "role",
            "tzid",
            "offset_utc",
            "alarm_repeat_json",
            "event_repeat",
            "event_repeat_json",
            "organiser",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name_display",
            "calendar_url",
            "summary",
            "description",
            "color",
            "ics",
            "datetime_start",
            "datetime_end",
            "duration",
            "all_day",
            "created",
            "datetime_last_modified",
            "timestamp",
            "location",
            "geolocation",
            "conference_url",
            "range",
            "related",
            "role",
            "tzid",
            "offset_utc",
            "alarm_repeat_json",
            "event_repeat",
            "event_repeat_json",
            "organiser",
            Submit("submit", "Update"),
        )


# from .forms import ExtraDataCreateForm, EntityClassCreateForm, EntityTitleCreateForm, EntityCreateForm, EntityBankAccountCreateForm, LaraUserCreateForm, MeetingsCalendarCreateFormExtraDataUpdateForm, EntityClassUpdateForm, EntityTitleUpdateForm, EntityUpdateForm, EntityBankAccountUpdateForm, LaraUserUpdateForm, MeetingsCalendarUpdateForm
