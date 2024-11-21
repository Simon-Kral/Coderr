def create_profile(type, user, customer_model, business_model):
    if type == 'customer':
        return customer_model.objects.create(user=user)
    elif type == 'business':
        return business_model.objects.create(user=user)


def get_profile_by_user_id(id, customer_model, business_model):
    if customer_model.objects.filter(user_id=id).first():
        return customer_model.objects.get(user_id=id)
    elif business_model.objects.filter(user_id=id).first():
        return business_model.objects.get(user_id=id)


def get_profile_by_user_username(username, customer_model, business_model):
    if customer_model.objects.filter(user__username=username).first():
        return customer_model.objects.get(user__username=username)
    elif business_model.objects.filter(user__username=username).first():
        return business_model.objects.get(user__username=username)


def get_user_details(user):
    data = {'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username}
    return data


def get_profile_serializer(profile, customer_serializer, business_serializer, *args, **kwargs):
    if profile.type == 'customer':
        serializer = customer_serializer(profile, **kwargs)
    elif profile.type == 'business':
        serializer = business_serializer(profile, **kwargs)
    return serializer


def get_hyperlinked_details(instance, request, serializer):
    details = instance.details
    serializer = serializer(details, many=True, context={'request': request})
    data = serializer.data
    return data


def get_min_value(details, field):
    values = details.values_list(field)
    min_value = values.order_by(field).first()[0]
    return min_value
