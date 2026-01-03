from.auth import (
    RegistUserView,UserLoginView,
    PasswordResetMailView
)
from .home import HomeView

from .old_travel import (
    travel_detail, template_edit, edit_item,
    add_item, add_category_and_item, create_link
)

from .new_travel import (
    TravelStep1View, TravelStep2View,
    TemplateCreateView,TravelCopyModalView,TravelCopyApplyView
)

