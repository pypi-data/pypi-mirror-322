from dateutil.relativedelta import relativedelta
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Crf, CrfCollection, Visit
from edc_visit_schedule.visit_schedule import VisitSchedule

from .consents import consent_v1

crfs_prn = CrfCollection(
    Crf(show_order=100, model="form_runners_app.prn", required=True),
)
crfs = CrfCollection(
    Crf(show_order=10, model="form_runners_app.team", required=True),
    Crf(show_order=20, model="form_runners_app.venue", required=True),
    Crf(show_order=30, model="form_runners_app.teamwithdifferentfields", required=True),
)

visit = Visit(
    code="1000",
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    requisitions=None,
    crfs=crfs,
    crfs_prn=crfs_prn,
    requisitions_unscheduled=None,
    crfs_unscheduled=None,
    allow_unscheduled=False,
    facility_name="5-day-clinic",
)


schedule = Schedule(
    name="schedule",
    onschedule_model="form_runners_app.onschedule",
    offschedule_model="form_runners_app.offschedule",
    appointment_model="edc_appointment.appointment",
    consent_definitions=[consent_v1],
)

visit_schedule = VisitSchedule(
    name="visit_schedule",
    offstudy_model="form_runners_app.offstudy",
    death_report_model="form_runners_app.deathreport",
    locator_model="edc_locator.subjectlocator",
)

schedule.add_visit(visit)

visit_schedule.add_schedule(schedule)
