from dashboard import constants as Constants



class PermissionManager :
    """
    This Class provides a central to check for permission.
    """

    @staticmethod
    def user_has_perm(user=None, perm=None):
        flag = False
        if user and perm and hasattr(user, 'has_perm'):
            flag = user.has_perm(Constants.APP_PREFIX + perm)
        return flag


    @staticmethod
    def user_can_generate_token(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.TOKEN_GENERATE_PERM)

    @staticmethod
    def user_can_access_dashboard(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.DASHBOARD_VIEW_PERM)

    @staticmethod
    def user_can_view_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_VIEW_PERM)
    
    @staticmethod
    def user_can_change_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_CHANGE_PERM)

    @staticmethod
    def user_can_add_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_ADD_PERM)
    
    @staticmethod
    def user_can_delete_user(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.USER_DELETE_PERM)

    ## ACCOUNT PERMISSION
    @staticmethod
    def user_can_view_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_VIEW_PERM)
    
    @staticmethod
    def user_can_change_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_CHANGE_PERM)

    @staticmethod
    def user_can_add_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_ADD_PERM)
    
    @staticmethod
    def user_can_delete_account(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.ACCOUNT_DELETE_PERM)
    
    ## GROUP PERMISSION
    @staticmethod
    def user_can_view_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_VIEW_PERM)
    
    @staticmethod
    def user_can_change_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_CHANGE_PERM)

    @staticmethod
    def user_can_add_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_ADD_PERM)
    
    @staticmethod
    def user_can_delete_group(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.GROUP_DELETE_PERM)

    ## POLICY PERMISSION
    @staticmethod
    def user_can_view_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POLICY_VIEW_PERM)
    
    @staticmethod
    def user_can_change_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POLICY_CHANGE_PERM)

    @staticmethod
    def user_can_add_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POLICY_ADD_PERM)

    @staticmethod
    def user_can_delete_policy(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POLICY_DELETE_PERM)



    ## PRODUCT PERMISSION
    @staticmethod
    def user_can_change_post(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POST_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_post(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POST_ADD_PERM)
    
    @staticmethod
    def user_can_delete_post(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.POST_DELETE_PERM)

    @staticmethod
    def user_can_view_post(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.PPOST_VIEW_PERM)


    
    ## CATEGORY PERMISSION

    @staticmethod
    def user_can_change_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_ADD_PERM)
    
    @staticmethod
    def user_can_delete_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_DELETE_PERM)

    @staticmethod
    def user_can_view_category(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.CATEGORY_VIEW_PERM)

   

    
    ## COUPON

    @staticmethod
    def user_can_change_coupon(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.COUPON_CHANGE_PERM)
    
    @staticmethod
    def user_can_add_coupon(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.COUPON_ADD_PERM)
    
    @staticmethod
    def user_can_delete_coupon(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.COUPON_DELETE_PERM)

    @staticmethod
    def user_can_view_coupon(user=None):
        return PermissionManager.user_has_perm(user=user, perm=Constants.COUPON_VIEW_PERM)

    
    
    

def get_view_permissions(user=None):
    context = {
        'can_access_dashboard' : PermissionManager.user_can_access_dashboard(user),

        'can_view_user': PermissionManager.user_can_view_user(user),
        'can_add_user' : PermissionManager.user_can_add_user(user),
        'can_delete_user' : PermissionManager.user_can_delete_user(user),
        'can_change_user' : PermissionManager.user_can_change_user(user),

        'can_view_post': PermissionManager.user_can_view_post(user),
        'can_add_post' : PermissionManager.user_can_add_post(user),
        'can_delete_post' : PermissionManager.user_can_delete_post(user),
        'can_change_post' : PermissionManager.user_can_change_post(user),

        'can_view_category': PermissionManager.user_can_view_category(user),
        'can_add_category' : PermissionManager.user_can_add_category(user),
        'can_delete_category' : PermissionManager.user_can_delete_category(user),
        'can_change_category' : PermissionManager.user_can_change_category(user),


        'can_view_policy': PermissionManager.user_can_view_policy(user),
        'can_add_policy': PermissionManager.user_can_add_policy(user),
        'can_delete_policy': PermissionManager.user_can_delete_policy(user),
        'can_change_policy': PermissionManager.user_can_change_policy(user),

        'can_view_coupon': PermissionManager.user_can_view_coupon(user),
        'can_add_coupon': PermissionManager.user_can_add_coupon(user),
        'can_delete_coupon': PermissionManager.user_can_delete_coupon(user),
        'can_change_coupon': PermissionManager.user_can_change_coupon(user),

        'can_view_group' : PermissionManager.user_can_view_group(user),
        'can_add_group' : PermissionManager.user_can_add_group(user),
        'can_delete_group' : PermissionManager.user_can_delete_group(user),
        'can_change_group' : PermissionManager.user_can_change_group(user),

        'can_generate_token': PermissionManager.user_can_generate_token(user)
    }
    return context