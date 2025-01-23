import json

from adminboundarymanager.models import AdminBoundarySettings
from django.contrib.gis.forms import BaseGeometryWidget
from django.contrib.gis.geometry import json_regex
from django.forms import Textarea, Widget, TextInput
from django.urls import reverse
from wagtail.models import Site
from wagtail.telepath import register
from wagtail.utils.widgets import WidgetWithScript
from wagtail.widget_adapters import WidgetAdapter

from capeditor.constants import WMO_HAZARD_EVENTS_TYPE_CHOICES


class BaseMapWidget(Widget):
    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)

        try:
            site = Site.objects.get(is_default_site=True)
            abm_settings = AdminBoundarySettings.for_site(site)
            boundary_tiles_url = abm_settings.boundary_tiles_url
            boundary_tiles_url = site.root_url + boundary_tiles_url

            boundary_detail_url = reverse("admin_boundary_detail", args=[0]).replace("/0", "")
            boundary_detail_url = site.root_url + boundary_detail_url

            context.update({
                "boundary_tiles_url": boundary_tiles_url,
                "boundary_detail_url": boundary_detail_url,
                "country_bounds": abm_settings.combined_countries_bounds
            })

        except Exception:
            pass

        return context


class UNBoundaryWidgetMixin(Widget):
    def get_context(self, *args, **kwargs):
        from capeditor.cap_settings import CapSetting
        context = super().get_context(*args, **kwargs)

        try:
            site = Site.objects.get(is_default_site=True)
            cap_settings = CapSetting.for_site(site)

            un_country_boundary_geojson = cap_settings.un_country_boundary_geojson
            context.update({
                "un_boundary_geojson": json.dumps(un_country_boundary_geojson)
            })
        except Exception as e:
            pass

        return context


class BasePolygonWidget(BaseGeometryWidget, BaseMapWidget):
    def serialize(self, value):
        return value.json if value else ""


class BoundaryPolygonWidget(WidgetWithScript, BasePolygonWidget, UNBoundaryWidgetMixin):
    template_name = "capeditor/widgets/boundary_polygon_widget.html"
    map_srid = 4326

    def __init__(self, attrs=None):
        default_attrs = {
            "class": "capeditor-widget__boundary-input",
        }
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}

        super().__init__(attrs=attrs)

    class Media:
        css = {
            "all": [
                "capeditor/css/cap_detail_page.css",
                "capeditor/css/widget/boundary-widget.css",
            ]
        }
        js = [
            "capeditor/js/maplibre-gl.js",
            "capeditor/js/turf.min.js",
            "capeditor/js/widget/boundary-polygon-widget.js",
        ]


class BoundaryPolygonWidgetAdapter(WidgetAdapter):
    js_constructor = "capeditor.widgets.BoundaryPolygonInput"

    class Media:
        js = [
            "capeditor/js/widget/boundary-polygon-widget-telepath.js",
        ]


register(BoundaryPolygonWidgetAdapter(), BoundaryPolygonWidget)


class PolygonWidget(WidgetWithScript, BasePolygonWidget, UNBoundaryWidgetMixin):
    template_name = "capeditor/widgets/polygon_widget.html"
    map_srid = 4326

    def __init__(self, attrs=None):
        default_attrs = {
            "class": "capeditor-widget__polygon-input",
        }
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}

        super().__init__(attrs=attrs)

    class Media:
        css = {
            "all": [
                "capeditor/css/maplibre-gl.css",
                "capeditor/css/mapbox-gl-draw.css",
                "capeditor/css/widget/polygon-widget.css",
            ]
        }
        js = [
            "capeditor/js/maplibre-gl.js",
            "capeditor/js/mapbox-gl-draw.js",
            "capeditor/js/turf.min.js",
            "capeditor/js/widget/polygon-widget.js",
        ]


class PolygonWidgetAdapter(WidgetAdapter):
    js_constructor = "capeditor.widgets.PolygonInput"

    class Media:
        js = [
            "capeditor/js/widget/polygon-widget-telepath.js",
        ]


register(PolygonWidgetAdapter(), PolygonWidget)


class CircleWidget(WidgetWithScript, BaseMapWidget, Textarea, UNBoundaryWidgetMixin):
    template_name = "capeditor/widgets/circle_widget.html"

    def __init__(self, attrs=None):
        default_attrs = {
            "class": "capeditor-widget__circle-input",
        }

        if attrs:
            default_attrs.update(attrs)

        super().__init__(default_attrs)

    class Media:
        css = {
            "all": [
                "capeditor/css/maplibre-gl.css",
                "capeditor/css/widget/circle-widget.css",
            ]
        }
        js = [
            "capeditor/js/maplibre-gl.js",
            "capeditor/js/turf.min.js",
            "capeditor/js/widget/circle-widget.js",
        ]


class CircleWidgetAdapter(WidgetAdapter):
    js_constructor = "capeditor.widgets.CircleInput"

    class Media:
        js = [
            "capeditor/js/widget/circle-widget-telepath.js",
        ]


register(CircleWidgetAdapter(), CircleWidget)


class HazardEventTypeWidget(WidgetWithScript, TextInput):
    template_name = "capeditor/widgets/hazard_event_type_widget.html"

    def __init__(self, attrs=None, **kwargs):
        default_attrs = {}

        if attrs:
            default_attrs.update(attrs)

        super().__init__(default_attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        options = []

        for choice in WMO_HAZARD_EVENTS_TYPE_CHOICES:
            options.append({
                "value": choice[0],
                "label": str(choice[1]),
            })

        context["widget"].update({
            "event_type_list": options
        })

        return context

    def render_js_init(self, id_, name, value):
        return "new HazardEventTypeWidget({0},{1});".format(json.dumps(id_), json.dumps(value))

    class Media:
        js = [
            "capeditor/js/widget/hazard-event-type-widget.js",
        ]


class MultiPolygonWidget(BaseGeometryWidget, BaseMapWidget, UNBoundaryWidgetMixin):
    template_name = "capeditor/widgets/multipolygon_widget.html"
    map_srid = 4326

    def __init__(self, attrs=None):
        default_attrs = {
            "class": "capeditor-widget__multipolygon-input",
        }
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}

        super().__init__(attrs=attrs)

    class Media:
        css = {
            "all": [
                "capeditor/css/maplibre-gl.css",
                "capeditor/css/mapbox-gl-draw.css",
                "capeditor/css/widget/multipolygon-widget.css",
            ]
        }
        js = [
            "capeditor/js/maplibre-gl.js",
            "capeditor/js/mapbox-gl-draw.js",
            "capeditor/js/turf.min.js",
            "capeditor/js/widget/multipolygon-widget.js",
        ]

    def serialize(self, value):
        return value.json if value else ""

    def deserialize(self, value):
        geom = super().deserialize(value)
        # GeoJSON assumes WGS84 (4326). Use the map's SRID instead.
        if geom and json_regex.match(value) and self.map_srid != 4326:
            geom.srid = self.map_srid
        return geom


class GeojsonFileLoaderWidget(BaseGeometryWidget, BaseMapWidget):
    template_name = "capeditor/widgets/geojson_file_loader_widget.html"

    def __init__(self, attrs=None):
        default_attrs = {
            "class": "capeditor-widget__polygon-draw-input",
        }
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}

        super().__init__(attrs=attrs)

    class Media:
        css = {
            "all": [
                "capeditor/css/maplibre-gl.css",
                "capeditor/css/widget/geojson-file-loader-widget.css",
            ]
        }
        js = [
            "capeditor/js/maplibre-gl.js",
            "capeditor/js/turf.min.js",
            "capeditor/js/widget/geojson-file-loader-widget.js",
        ]

    def serialize(self, value):
        return value.json if value else ""

    def deserialize(self, value):
        geom = super().deserialize(value)
        # GeoJSON assumes WGS84 (4326). Use the map's SRID instead.
        if geom and json_regex.match(value) and self.map_srid != 4326:
            geom.srid = self.map_srid
        return geom
