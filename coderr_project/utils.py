def create_profile(type, user, customer_model, business_model):
    """
    Creates a profile for a user based on the specified type.

    Parameters:
        - type (str): The type of profile to create ('customer' or 'business').
        - user (User): The user for whom the profile is created.
        - customer_model (Model): The model class for customer profiles.
        - business_model (Model): The model class for business profiles.

    Returns:
        - An instance of the created profile (either customer or business).
    """
    if type == 'customer':
        return customer_model.objects.create(user=user)
    elif type == 'business':
        return business_model.objects.create(user=user)


def get_profile_by_user_id(id, customer_model, business_model):
    """
    Retrieves a profile (customer or business) based on the user's ID.

    Parameters:
        - id (int): The ID of the user.
        - customer_model (Model): The model class for customer profiles.
        - business_model (Model): The model class for business profiles.

    Returns:
        - The profile instance if found, otherwise None.
    """
    if customer_model.objects.filter(user_id=id).first():
        return customer_model.objects.get(user_id=id)
    elif business_model.objects.filter(user_id=id).first():
        return business_model.objects.get(user_id=id)


def get_profile_by_user_username(username, customer_model, business_model):
    """
    Retrieves a profile (customer or business) based on the user's username.

    Parameters:
        - username (str): The username of the user.
        - customer_model (Model): The model class for customer profiles.
        - business_model (Model): The model class for business profiles.

    Returns:
        - The profile instance if found, otherwise None.
    """
    if customer_model.objects.filter(user__username=username).first():
        return customer_model.objects.get(user__username=username)
    elif business_model.objects.filter(user__username=username).first():
        return business_model.objects.get(user__username=username)


def get_user_details(user):
    """
    Retrieves basic details of a user.

    Parameters:
        - user (User): The user whose details are to be retrieved.

    Returns:
        - A dictionary containing the user's first name, last name, and username.
    """
    data = {'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username}
    return data


def get_profile_serializer(profile, customer_serializer, business_serializer, *args, **kwargs):
    """
    Retrieves the appropriate serializer for a profile based on its type.

    Parameters:
        - profile (object): The profile instance.
        - customer_serializer (Serializer): The serializer class for customer profiles.
        - business_serializer (Serializer): The serializer class for business profiles.
        - *args, **kwargs: Additional arguments for the serializer.

    Returns:
        - The serializer instance for the profile.
    """
    if profile.type == 'customer':
        serializer = customer_serializer(profile, **kwargs)
    elif profile.type == 'business':
        serializer = business_serializer(profile, **kwargs)
    return serializer


def get_hyperlinked_details(instance, request, serializer):
    """
    Retrieves hyperlinked details of an instance using a specified serializer.

    Parameters:
        - instance (object): The instance whose details are to be serialized.
        - request (Request): The current HTTP request (used for context in serialization).
        - serializer (Serializer): The serializer class for the details.

    Returns:
        - A serialized representation of the instance's details.
    """
    details = instance.details
    serializer = serializer(details, many=True, context={'request': request})
    data = serializer.data
    return data


def get_min_value(details, field):
    """
    Retrieves the minimum value of a specified field from a set of details.

    Parameters:
        - details (QuerySet): A queryset of details.
        - field (str): The field for which the minimum value is to be found.

    Returns:
        - The minimum value of the specified field.
    """
    values = details.values_list(field)
    min_value = values.order_by(field).first()[0]
    return min_value
