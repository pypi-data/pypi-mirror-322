# Wagtail Link Snippet

This package provides a custom implementation for adding link buttons in Wagtail’s rich text editor to link specific snippets within the Wagtail admin interface.

![How to use it](wagtail_linksnippet.gif)

## Overview

The package integrates with Wagtail’s `ChooserViewSet` ([Wagtail documentation](https://docs.wagtail.org/en/v6.2.2/extending/generic_views.html#chooserviewset)).
The package works only if the snippet has the get_absolute_url method implemented.


## Installation and Setup

pip install watail_linksnippet

Make sure to include the relevant app that contains the rich text features and handlers in your INSTALLED_APPS within settings.py.
```python
INSTALLED_APPS = [
    # Other installed apps
    'wagtail_linksnippet',
]
```

## Usage Example

You can configure the snippet choosers in your wagtail_hooks.py file by registering the chooser viewsets.

```python
from wagtail_linksnippet.richtext_utils import add_snippet_link_button

add_snippet_link_button(snippet1_chooser_viewset)
add_snippet_link_button(snippet2_chooser_viewset)
```

## Bonus TitleExtraChooseView
The package includes a view_utils.py module designed to add attributes to chooser modal links, similar to how attributes are handled in the page chooser modal.

Here’s an example of how to use the **TitleExtraChooseView** module:

```python
# views.py

from wagtail.admin.views.generic.chooser import ChooseView
from wagtail_linksnippet.views_utils import CustomChooseView

class CustomChooseView(TitleExtraChooseView):
    # Your code here
```
