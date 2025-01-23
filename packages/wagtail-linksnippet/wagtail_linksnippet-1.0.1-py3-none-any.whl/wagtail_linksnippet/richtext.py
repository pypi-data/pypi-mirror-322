from django.conf import settings
from django.apps import apps
from wagtail.rich_text import LinkHandler
from wagtail.admin.rich_text.converters.html_to_contentstate import LinkElementHandler
from .utils import encode_message


encrypt_enabled = getattr(settings, 'WAGTAIL_LINKSNIPPET_ENCRYPT', False)
process_message = encode_message if encrypt_enabled else lambda message: message


class GenericLinkHandler(LinkHandler):
    identifier = None
    model_name = None
    app_label = None

    @classmethod
    def get_model(cls):
        return apps.get_model(cls.app_label, cls.model_name)

    @classmethod
    def get_instance(cls, attrs):
        id = attrs.get("id", None)
        if id:
            model = cls.get_model()
            qs = model.objects.filter(id=id)
            return qs.first()
        return None

    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            obj = cls.get_instance(attrs)
            url = obj.get_absolute_url()
            obj_id = process_message(obj.id)
            link_type = process_message(cls.model_name)
            return f'<a href="{url}" data-link-type="{link_type}" data-link-object-id="{obj_id}" class="link-metrics">'
        except Exception:
            return "<a>"


class GenericLinkElementHandler(LinkElementHandler):
    def get_attribute_data(self, attrs):
        return {
            'id': attrs.get('id'),
            'string': attrs.get('data-string'),
            "edit-link": attrs.get("data-edit_link"),
            "app_name": attrs.get("data-app-name"),
            "model_name": attrs.get("data-model-name"),
        }
