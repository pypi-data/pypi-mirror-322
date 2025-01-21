from django.contrib.auth.models import AbstractUser

from .abstract_pfx_base_user import AbstractPFXUser
from .pfx_models import PFXModelMixin


class PFXUser(PFXModelMixin, AbstractPFXUser):
    """The Django User with PFX mixins.
    """

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
