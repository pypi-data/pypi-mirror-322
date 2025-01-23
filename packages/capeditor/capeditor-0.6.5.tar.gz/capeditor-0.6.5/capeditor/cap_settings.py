import json

from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import StreamField
from wagtail.models import Site, Orderable
from wagtailiconchooser.widgets import IconChooserWidget
from wagtailmodelchooser import register_model_chooser

from capeditor.blocks import (
    ContactBlock
)
from capeditor.forms.widgets import (
    HazardEventTypeWidget,
    MultiPolygonWidget,
    GeojsonFileLoaderWidget
)


@register_setting
class CapSetting(BaseSiteSetting, ClusterableModel):
    sender = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("CAP Sender Email"),
                              help_text=_("Email of the sending institution"))
    sender_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("CAP Sender Name"),
                                   help_text=_("Name of the sending institution"))
    wmo_oid = models.CharField(max_length=255, blank=True, null=True,
                               verbose_name=_("WMO Register of Alerting Authorities OID"),
                               help_text=_("WMO Register of Alerting Authorities "
                                           "Object Identifier (OID) of the sending institution. "
                                           "This will be used to generate CAP messages identifiers"))

    logo = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
                             verbose_name=_("Logo of the sending institution"))

    contacts = StreamField([
        ("contact", ContactBlock(label=_("Contact")))
    ], use_json_field=True, blank=True, null=True, verbose_name=_("Contact Details"),
        help_text=_("Contact for follow-up and confirmation of the alert message"))

    un_country_boundary_geojson = models.JSONField(blank=True, null=True, verbose_name=_("UN Country Boundary"),
                                                   help_text=_("GeoJSON file of the UN Country Boundary. Setting this"
                                                               " will enable the UN Country Boundary check in the alert"
                                                               "drawing tools"))

    class Meta:
        verbose_name = _("CAP Settings")

    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel("sender_name"),
            FieldPanel("sender"),
            FieldPanel("wmo_oid"),
            FieldPanel("logo"),
            FieldPanel("contacts"),
        ], heading=_("Sender Details")),
        ObjectList([
            InlinePanel("hazard_event_types", heading=_("Hazard Types"), label=_("Hazard Type"),
                        help_text=_("Hazards monitored by the institution")),
        ], heading=_("Hazard Types")),
        ObjectList([
            InlinePanel("predefined_alert_areas", heading=_("Predefined Alert Areas"), label=_("Area"),
                        help_text=_("Predefined areas for alerts")),
        ], heading=_("Predefined Areas"), classname="map-resize-trigger"),
        ObjectList([
            InlinePanel("alert_languages", heading=_("Allowed Alert Languages"), label=_("Language")),
        ], heading=_("Languages")),
        ObjectList([
            FieldPanel("un_country_boundary_geojson",
                       widget=GeojsonFileLoaderWidget(
                           attrs={"resize_trigger_selector": ".w-tabs__tab.map-resize-trigger"})),
        ], heading=_("UN Boundary"), classname="map-resize-trigger"),
    ])

    @property
    def contact_list(self):
        contacts = []
        for contact_block in self.contacts:
            contact = contact_block.value.get("contact")
            if contact:
                contacts.append(contact)
        return contacts

    @property
    def audience_list(self):
        audiences = []
        for audience_block in self.audience_types:
            audience = audience_block.value.get("audience")
            if audience:
                audiences.append(audience)
        return audiences


class HazardEventTypes(Orderable):
    setting = ParentalKey(CapSetting, on_delete=models.PROTECT, related_name="hazard_event_types")
    is_in_wmo_event_types_list = models.BooleanField(default=True,
                                                     verbose_name=_("Select from WMO list of Hazards Event Types"))
    event = models.CharField(max_length=35, unique=True, verbose_name=_("Hazard"), help_text=_("Name of Hazard"))
    icon = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Icon"), help_text=_("Matching icon"))

    panels = [
        FieldPanel("is_in_wmo_event_types_list"),
        FieldPanel("event", widget=HazardEventTypeWidget),
        FieldPanel("icon", widget=IconChooserWidget),
    ]

    def __str__(self):
        return self.event


class PredefinedAlertArea(Orderable):
    setting = ParentalKey(CapSetting, on_delete=models.PROTECT, related_name="predefined_alert_areas")
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    geom = models.MultiPolygonField(srid=4326, verbose_name=_("Area"))

    class Meta:
        verbose_name = _("Predefined Area")
        verbose_name_plural = _("Predefined Areas")

    def __str__(self):
        return self.name

    @property
    def geojson(self):
        return json.loads(self.geom.geojson)

    panels = [
        FieldPanel("name"),
        FieldPanel("geom",
                   widget=MultiPolygonWidget(attrs={"resize_trigger_selector": ".w-tabs__tab.map-resize-trigger"})),
    ]


register_model_chooser(PredefinedAlertArea)


class AlertLanguage(Orderable):
    setting = ParentalKey(CapSetting, on_delete=models.PROTECT, related_name="alert_languages")
    code = models.CharField(max_length=10, verbose_name=_("Language Code"), help_text=_("ISO 639-1 language code"))
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Language Name"))

    panels = [
        FieldPanel("code"),
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super().save(*args, **kwargs)


def get_cap_setting():
    try:
        site = Site.objects.get(is_default_site=True)
        if site:
            return CapSetting.for_site(site)
    except Exception:
        pass
    return None


def get_default_sender():
    cap_setting = get_cap_setting()
    if cap_setting and cap_setting.sender:
        return cap_setting.sender
    return None


def get_cap_contact_list(request):
    cap_settings = CapSetting.for_request(request)
    contacts_list = cap_settings.contact_list
    return contacts_list


def get_cap_audience_list(request):
    cap_settings = CapSetting.for_request(request)
    audience_list = cap_settings.audience_list
    return audience_list
