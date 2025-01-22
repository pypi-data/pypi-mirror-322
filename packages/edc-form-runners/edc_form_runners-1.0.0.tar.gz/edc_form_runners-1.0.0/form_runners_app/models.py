from uuid import uuid4

from django.db import models
from django.db.models import PROTECT
from edc_consent.managers import ConsentObjectsByCdefManager, CurrentSiteByCdefManager
from edc_consent.model_mixins.consent_version_model_mixin import (
    ConsentVersionModelMixin,
)
from edc_crf.model_mixins import CrfModelMixin, CrfWithActionModelMixin
from edc_identifier.managers import SubjectIdentifierManager
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_list_data.model_mixins import ListModelMixin
from edc_model.models import BaseUuidModel
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_screening.model_mixins import ScreeningModelMixin
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow
from edc_visit_tracking.model_mixins import SubjectVisitMissedModelMixin

from .consents import consent_v1


class DeathReport(BaseUuidModel):
    subject_identifier = models.CharField(max_length=50)


class OffStudy(BaseUuidModel):
    subject_identifier = models.CharField(max_length=50)

    offstudy_datetime = models.DateTimeField(default=get_utcnow)


class SubjectScreening(ScreeningModelMixin, BaseUuidModel):
    consent_definition = consent_v1
    objects = SubjectIdentifierManager()


class SubjectConsent(
    SiteModelMixin,
    ConsentVersionModelMixin,
    NonUniqueSubjectIdentifierModelMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    BaseUuidModel,
):
    subject_identifier = models.CharField(max_length=50)

    consent_datetime = models.DateTimeField()

    dob = models.DateField(null=True)

    version = models.CharField(max_length=10)


class SubjectConsentV1(SubjectConsent):
    objects = ConsentObjectsByCdefManager()
    on_site = CurrentSiteByCdefManager()

    class Meta:
        proxy = True


class OnSchedule(SiteModelMixin, BaseUuidModel):
    subject_identifier = models.CharField(max_length=50)

    onschedule_datetime = models.DateTimeField(default=get_utcnow)


class OffSchedule(SiteModelMixin, BaseUuidModel):
    subject_identifier = models.CharField(max_length=50)

    offschedule_datetime = models.DateTimeField(default=get_utcnow)


class SubjectVisitMissedReasons(ListModelMixin):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Subject Missed Visit Reasons"
        verbose_name_plural = "Subject Missed Visit Reasons"


class SubjectVisitMissed(
    SubjectVisitMissedModelMixin,
    CrfWithActionModelMixin,
    BaseUuidModel,
):
    missed_reasons = models.ManyToManyField(
        SubjectVisitMissedReasons, blank=True, related_name="+"
    )

    class Meta(
        SubjectVisitMissedModelMixin.Meta,
        BaseUuidModel.Meta,
    ):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"


class Team(CrfModelMixin, BaseUuidModel):

    name = models.CharField(max_length=36, default=uuid4)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class Venue(CrfModelMixin, BaseUuidModel):

    name = models.CharField(max_length=36, default=uuid4)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Venue"
        verbose_name_plural = "Venues"


class Member(SiteModelMixin, BaseUuidModel):

    team = models.ForeignKey(Team, on_delete=PROTECT)

    player_name = models.CharField(max_length=36, default=uuid4)

    skill_level = models.CharField(max_length=36, default=uuid4)

    @property
    def subject_identifier(self):
        return self.team.subject_visit.subject_identifier

    @property
    def visit_code(self):
        return self.team.subject_visit.visit_code

    @property
    def visit_code_sequence(self):
        return self.team.subject_visit.visit_code_sequence

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Member"
        verbose_name_plural = "Members"


class Prn(CrfModelMixin, BaseUuidModel):

    name = models.CharField(max_length=36, default=uuid4)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "PRN"
        verbose_name_plural = "PRN"


class TeamWithDifferentFields(CrfModelMixin, BaseUuidModel):

    size = models.IntegerField(max_length=36)

    name = models.CharField(max_length=36, null=True, blank=False)

    color = models.CharField(max_length=36, null=True, blank=False)

    mood = models.CharField(max_length=36, default="good")

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "TeamWithDifferentFields"
        verbose_name_plural = "TeamWithDifferentFields"
