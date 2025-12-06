from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(AdminUserCreationForm):

    """
    A form for creating new users.

    This form extends Django's AdminUserCreationForm to create a new CustomUser
    instance. It includes the email and username fields.
    """
    class Meta:
        """
        Meta options for the CustomUserCreationForm.

        Specifies the model to be used and the fields to be included in the form.
        """

        model = CustomUser
        fields = (
            "email",
            "username",
        )


class CustomUserChangeForm(UserChangeForm):

    """
    A form for updating existing users.

    This form extends Django's UserChangeForm to update a CustomUser instance.
    It includes the email and username fields.
    """
    class Meta:
        
        """
        Meta options for the CustomUserChangeForm.

        Specifies the model to be used and the fields to be included in the form.
        """
        model = CustomUser
        fields = (
            "email",
            "username",
        )
