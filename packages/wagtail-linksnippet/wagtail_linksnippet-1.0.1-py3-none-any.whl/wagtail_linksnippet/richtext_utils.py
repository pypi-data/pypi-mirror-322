from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static
from wagtail.admin.rich_text.editors.draftail.features import EntityFeature
from wagtail import hooks
from draftjs_exporter.dom import DOM

from .richtext import GenericLinkHandler, GenericLinkElementHandler


def register_model_feature_(features, model_config):
    feature_name_ = model_config['feature_name']
    app_label_ = model_config['app_label']
    model_name_ = model_config['model_name']
    type_ = model_config['type']
    icon = model_config.get('icon', 'link-external')

    class ModelLinkHandler(GenericLinkHandler):
        identifier = feature_name_
        model_name = model_name_
        app_label = app_label_

    class ModelLinkElementHandler(GenericLinkElementHandler):
        pass

    control = {
        'type': type_,
        'description': f'Insert {model_name_}',
        'icon': icon,
    }

    features.register_link_type(ModelLinkHandler)

    features.register_editor_plugin(
        'draftail',
        feature_name_,
        EntityFeature(control)
    )

    def model_entity_decorator(props):
        selected_text = props.get('children', '')

        return DOM.create_element('a', {
            'linktype': feature_name_,
            'id': props.get('id', ''),
            "data-string": props.get("string"),
            "data-edit-link": props.get("edit_link"),
            "data-app-name": app_label_,
            "data-model-name": model_name_,
        }, selected_text)

    features.register_converter_rule('contentstate', feature_name_, {
        'from_database_format': {
            f'a[linktype="{feature_name_}"]': ModelLinkElementHandler(type_),
        },
        'to_database_format': {
            'entity_decorators': {
                type_: model_entity_decorator
            }
        }
    })

    features.default_features.append(feature_name_)


def make_editor_js(model_config):
    def editor_js():
        js_config = {
            'featureName': model_config['feature_name'],
            'chooserUrl': reverse(model_config['view_name']),
            'appName': model_config['app_label'],
            'modelName': model_config['model_name'],
            'typeName': model_config['type'],
            'iconName': model_config['icon'],
        }

        js = format_html(
            '''
            <script src="{js_file}"></script>
            <script type="text/javascript">
                window.modelChooserConfigs = window.modelChooserConfigs || [];
                window.modelChooserConfigs.push({config});
                safeInitModelChooser();
            </script>
            ''',
            js_file=static("wagtail_linksnippet/js/modelChooser.js"),
            config=mark_safe(js_config)
        )
        return js
    return editor_js


def add_snippet_link_button(chooser_viewset, feature_name=None, icon=None):
    content_type = ContentType.objects.get_for_model(chooser_viewset.model)

    app_label = content_type.app_label
    model_name = content_type.model
    feature_name = feature_name or model_name

    model_config = {
        'feature_name': feature_name.lower(),
        'view_name': f'{chooser_viewset.url_namespace}:choose',
        'type': feature_name.upper(),
        'icon': icon or chooser_viewset.icon or 'link-external',
        'app_label': app_label,
        'model_name': model_name,
    }

    @hooks.register('insert_editor_js')
    def register_editor_js():
        editor_js = make_editor_js(model_config)
        return editor_js()

    @hooks.register('register_rich_text_features')
    def register_model_feature(features):
        register_model_feature_(features, model_config)
