
APP_PREFIX = 'dashboard.'

PROFESSIONALS_GROUP = "Professionals"

MAX_RECENT = 5
TOP_VIEWS_MAX = 10

DASHBOARD_GLOBALS_PREFIX = "dashboard"


DASHBOARD_TAG_CONTEXT = {
    'TAGS_URL'               : f"{DASHBOARD_GLOBALS_PREFIX}:tags",
    'TAG_URL'                : f"{DASHBOARD_GLOBALS_PREFIX}:tag-detail",
    'TAG_UPDATE_URL'         : f"{DASHBOARD_GLOBALS_PREFIX}:tag-update",
    'TAG_DELETE_URL'         : f"{DASHBOARD_GLOBALS_PREFIX}:tag-delete",
    'TAGS_DELETE_URL'        : f"{DASHBOARD_GLOBALS_PREFIX}:tags-delete",
    'TAG_CREATE_URL'         : f"{DASHBOARD_GLOBALS_PREFIX}:tag-create",
}

DASHBOARD_COUPON_CONTEXT = {
    'COUPONS_URL'               : f"{DASHBOARD_GLOBALS_PREFIX}:coupons",
    'COUPON_URL'                : f"{DASHBOARD_GLOBALS_PREFIX}:coupon-detail",
    'COUPON_UPDATE_URL'         : f"{DASHBOARD_GLOBALS_PREFIX}:coupon-update",
    'COUPON_DELETE_URL'         : f"{DASHBOARD_GLOBALS_PREFIX}:coupon-delete",
    'COUPONS_DELETE_URL'        : f"{DASHBOARD_GLOBALS_PREFIX}:coupons-delete",
    'COUPON_CREATE_URL'         : f"{DASHBOARD_GLOBALS_PREFIX}:coupon-create",
}

DASHBOARD_POST_CONTEXT = {
    'IMAGE_URL'                 : f"{DASHBOARD_GLOBALS_PREFIX}:product-image-detail",
    'IMAGE_CREATE_URL'          : f"{DASHBOARD_GLOBALS_PREFIX}:product-image-create",
    'IMAGE_DELETE_URL'          : f"{DASHBOARD_GLOBALS_PREFIX}:product-image-delete",
    'PRODUCT_CREATE_URL'        : f"{DASHBOARD_GLOBALS_PREFIX}:product-create",
    'PRODUCT_DELETE_URL'        : f"{DASHBOARD_GLOBALS_PREFIX}:product-delete",
    'PRODUCTS_DELETE_URL'       : f"{DASHBOARD_GLOBALS_PREFIX}:products-delete",
    'PRODUCT_BULK_CHANGES_URL'  : f"{DASHBOARD_GLOBALS_PREFIX}:products-changes",
    'PRODUCT_URL'               : f"{DASHBOARD_GLOBALS_PREFIX}:product-detail",
    'PRODUCTS_URL'              : f"{DASHBOARD_GLOBALS_PREFIX}:products",
    'PRODUCT_UPDATE_URL'        : f"{DASHBOARD_GLOBALS_PREFIX}:product-update",

}

DASHBOARD_HIGHLIGHT_CONTEXT = {
    'HIGHLIGHT_URL' : f"{DASHBOARD_GLOBALS_PREFIX}:highlight-detail",
    'HIGHLIGHTS_URL' : f"{DASHBOARD_GLOBALS_PREFIX}:highlights",
    'HIGHLIGHT_UPDATE_URL' : f"{DASHBOARD_GLOBALS_PREFIX}:highlight-update",
    'HIGHLIGHT_DELETE_URL' : f"{DASHBOARD_GLOBALS_PREFIX}:highlight-delete",
    'HIGHLIGHTS_DELETE_URL' : f"{DASHBOARD_GLOBALS_PREFIX}:highlights-delete",
    'HIGHLIGHT_CREATE_URL' : f"{DASHBOARD_GLOBALS_PREFIX}:highlight-create",
    'HIGHLIGHT_ADD_PRODUCTS_URL' : f"{DASHBOARD_GLOBALS_PREFIX}:highlight-add-products",
    'HIGHLIGHT_ADD_OVERVIEW_PRODUCTS_URL' : f"{DASHBOARD_GLOBALS_PREFIX}:highlight-add-overview-products"
}



DASHBOARD_VIEW_PERM = 'can_view_dashboard'
TOKEN_GENERATE_PERM = 'can_generate_token'

USER_VIEW_PERM = 'can_view_user'
USER_ADD_PERM = 'can_add_user'
USER_CHANGE_PERM = 'can_change_user'
USER_DELETE_PERM = 'can_delete_user'

ACCOUNT_VIEW_PERM = 'can_view_account'
ACCOUNT_ADD_PERM = 'can_add_account'
ACCOUNT_CHANGE_PERM = 'can_change_account'
ACCOUNT_DELETE_PERM = 'can_delete_account'


GROUP_VIEW_PERM = 'can_view_group'
GROUP_ADD_PERM = 'can_add_group'
GROUP_CHANGE_PERM = 'can_change_group'
GROUP_DELETE_PERM = 'can_delete_group'


POST_VIEW_PERM = 'can_view_post'
POST_ADD_PERM = 'can_add_post'
POST_CHANGE_PERM = 'can_change_post'
POST_DELETE_PERM = 'can_delete_post'

POLICY_VIEW_PERM = 'can_view_policy'
POLICY_ADD_PERM = 'can_add_policy'
POLICY_CHANGE_PERM = 'can_change_policy'
POLICY_DELETE_PERM = 'can_delete_policy'

POLICY_GROUP_VIEW_PERM = 'can_view_policy_group'
POLICY_GROUP_ADD_PERM = 'can_add_policy_group'
POLICY_GROUP_CHANGE_PERM = 'can_change_policy_group'
POLICY_GROUP_DELETE_PERM = 'can_delete_policy_group'

POLICY_MEMBERSHIP_VIEW_PERM = 'can_view_policy_membership'
POLICY_MEMBERSHIP_ADD_PERM = 'can_add_policy_membership'
POLICY_MEMBERSHIP_CHANGE_PERM = 'can_change_policy_membership'
POLICY_MEMBERSHIP_DELETE_PERM = 'can_delete_policy_membership'

CATEGORY_VIEW_PERM = 'can_view_category'
CATEGORY_ADD_PERM = 'can_add_category'
CATEGORY_CHANGE_PERM = 'can_change_category'
CATEGORY_DELETE_PERM = 'can_delete_category'


HIGHLIGHT_VIEW_PERM = 'can_view_highlight'
HIGHLIGHT_ADD_PERM = 'can_add_highlight'
HIGHLIGHT_CHANGE_PERM = 'can_change_highlight'
HIGHLIGHT_DELETE_PERM = 'can_delete_highlight'

COUPON_VIEW_PERM = 'can_view_coupon'
COUPON_ADD_PERM = 'can_add_coupon'
COUPON_CHANGE_PERM = 'can_change_coupon'
COUPON_DELETE_PERM = 'can_delete_coupon'
