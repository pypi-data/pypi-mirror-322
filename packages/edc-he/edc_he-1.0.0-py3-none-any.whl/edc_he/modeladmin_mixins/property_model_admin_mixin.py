from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple


class HealthEconomicsPropertyModelAdminMixin:
    form = None

    additional_instructions = _(
        "We want to learn about the household and we use these questions "
        "to get an understanding of wealth and opportunities in the community. "
    )
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Property",
            {
                "description": format_html(
                    _(
                        "<H5><B><font color='orange'>Interviewer to read</font></B></H5><p>"
                        "I would now like to know if you own any <B>land or other "
                        "property</B> – and the approximate value (amount). I know this "
                        "is sensitive information and will not share this with any persons "
                        "outside of the survey team. <B><U>There is no need to give details "
                        "or show me any of the items.</U></B></P>"
                    )
                ),
                "fields": (
                    "land_owner",
                    "land_value",
                    "land_surface_area",
                    "land_surface_area_units",
                    "land_additional",
                    "land_additional_value",
                ),
            },
        ),
        (
            "Calculated values",
            {
                "description": "To be calculated (or recalculated) when this form is saved",
                "classes": ("collapse",),
                "fields": ("calculated_land_surface_area",),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    readonly_fields = ("calculated_land_surface_area",)

    radio_fields = {
        "land_owner": admin.VERTICAL,
        "land_additional": admin.VERTICAL,
        "land_surface_area_units": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }
