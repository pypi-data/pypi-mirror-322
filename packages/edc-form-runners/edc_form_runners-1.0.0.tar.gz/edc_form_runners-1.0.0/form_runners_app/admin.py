from django.contrib import admin
from edc_model_admin.admin_site import EdcAdminSite
from edc_model_admin.dashboard import (
    ModelAdminCrfDashboardMixin,
    ModelAdminDashboardMixin,
)
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from .forms import MemberForm, TeamForm, TeamWithDifferentFieldsForm
from .models import Member, Team, TeamWithDifferentFields, Venue

my_admin_site = EdcAdminSite(name="my_admin_site")


class MemberInlineAdmin(admin.TabularInline):
    model = Member
    form = MemberForm

    extra = 0


@admin.register(Member, site=my_admin_site)
class MembersAdmin(SiteModelAdminMixin, ModelAdminDashboardMixin, SimpleHistoryAdmin):
    form = MemberForm


@admin.register(Team, site=my_admin_site)
class TeamAdmin(SiteModelAdminMixin, ModelAdminCrfDashboardMixin, SimpleHistoryAdmin):
    form = TeamForm

    inlines = [MemberInlineAdmin]

    fieldsets = ((None, ({"fields": ("name", "created", "modified")})),)


@admin.register(TeamWithDifferentFields, site=my_admin_site)
class TeamWithDifferentFieldsAdmin(
    SiteModelAdminMixin, ModelAdminCrfDashboardMixin, SimpleHistoryAdmin
):
    form = TeamWithDifferentFieldsForm

    # do not include "name" to show that the field is ignored
    # by FormRunner.run even though blank=False
    fieldsets = ((None, ({"fields": ("size", "color", "mood")})),)


@admin.register(Venue, site=my_admin_site)
class VenueAdmin(SiteModelAdminMixin, ModelAdminDashboardMixin, SimpleHistoryAdmin):
    pass
