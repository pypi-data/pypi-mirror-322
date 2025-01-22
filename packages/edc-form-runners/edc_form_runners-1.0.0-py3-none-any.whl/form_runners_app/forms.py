from django import forms
from edc_form_validators import INVALID_ERROR, FormValidator, FormValidatorMixin

from .models import Member, Team, TeamWithDifferentFields


class MemberFormValidator(FormValidator):
    def clean(self) -> None:
        if self.cleaned_data.get("player_name") != "not-a-uuid":
            self.raise_validation_error({"player_name": "Cannot be a UUID"}, INVALID_ERROR)


class TeamFormValidator(FormValidator):
    def clean(self) -> None:
        if self.cleaned_data.get("name") != "not-a-uuid":
            self.raise_validation_error({"name": "Cannot be a UUID"}, INVALID_ERROR)


class MemberForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = MemberFormValidator

    class Meta:
        model = Member
        fields = "__all__"


class TeamForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = TeamFormValidator

    class Meta:
        model = Team
        fields = "__all__"


class TeamWithDifferentFieldsForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = None

    def clean(self):
        if self.cleaned_data.get("name") != "not-a-uuid":
            raise forms.ValidationError({"name": "Cannot be a UUID"}, INVALID_ERROR)

    class Meta:
        model = TeamWithDifferentFields
        fields = "__all__"
