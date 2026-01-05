from.auth import (
    RegistUserView,UserLoginView,
    PasswordResetMailView
)
from .home import HomeView

from .travel import travel_detail

from .new_travel.travel_step import (
    travel_create_step1,
    travel_step2

)

from .new_travel import (
    TemplateCreateView,
    TravelCopyModalView,
    TravelCopyApplyView,
    OldTravelCopyView,
    template_edit2
)


from .old_travel import (
    travel_detail, template_edit, edit_item,
    add_item, add_category_and_item, create_link
)



