from wagtail.admin.views.generic.chooser import ChooseView
from wagtail.admin.ui.tables import TitleColumn


class TitleColumnExtra(TitleColumn):
    def get_link_attrs(self, instance, parent_context):
        return {
            "data-id": instance.id,
            "data-url": instance.get_absolute_url(),
            "data-string": instance.description,
            "data-chooser-modal-choice": True
        }


class TitleExtraChooseView(ChooseView):
    @property
    def title_column(self):
        if self.is_multiple_choice:
            return TitleColumn(
                "title",
                label=_("Title"),
                accessor=str,
                label_prefix="chooser-modal-select",
            )
        else:
            return TitleColumnExtra(
                "title",
                label=_("Title"),
                accessor=str,
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            )
