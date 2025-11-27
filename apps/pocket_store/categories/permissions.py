def user_can_mutate(request, product):
    return request.user.role == "admin" or product.owner == request.user
