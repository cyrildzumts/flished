from django.utils.translation import gettext_lazy as _
from core.resources.ui_strings import HOME_META_DESCRIPTION
from flished import settings

# This file is generated automatically at 2021-12-24-23:46:57.505618
# Don't change this content unless you know what you are doing

DESCRIPTION_HOOK = _("Share experiences and ideas with others to build a better world")
HOME_TITLE = _("Write with passion")

# CATEGORIES DESCRIPTION 
HOME_DESCRIPTION = _("The place where you share passion with the world !")
CATEGORY_BUSINESS_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")
CATEGORY_CINEMA_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")
CATEGORY_CULTURE_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")
CATEGORY_FASHION_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")
CATEGORY_GAMES_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")
CATEGORY_HEALTH_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")
CATEGORY_MARKETING_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")
CATEGORY_REVIEWS_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")
CATEGORY_POLITICS_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")
CATEGORY_TECHNOLOGY_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")
CATEGORY_BEAUTY_DESCRIPTION = _("Keep up to date on business activities, startups and the like, on FLISHED.")





# CATEGORIES DESCRIPTION CONTEXTS

CATEGORY_DESCRIPTION_CONTEXT = {

    # HOME PAGE
    'home' :{'description': HOME_DESCRIPTION, 'meta-keywords':_("business, fashion, culture,health, marketing,politics"), "page-title": HOME_TITLE},

    # CATALOG PAGE

    # ROOT CATEGORIES
    "business" : {"description": CATEGORY_BUSINESS_DESCRIPTION, "meta-keywords":_("business, business topic, startups"),"page-title":_("Business | Stories about Business,Startups,E-Commerce"),"name":_("Business")},
    "culture" : {"description": CATEGORY_CULTURE_DESCRIPTION, "meta-keywords":_("culture, tv-shows, movies"),"page-title":_("Culture | TV-Shows, Movies, Music"),"name":_("Culture")},
    'fashion' :{'description': CATEGORY_FASHION_DESCRIPTION, 'meta-keywords':_("fashion, mode, beauty,perfumes"), "page-title": _("Fashion | Beauty, Cosmetics, Perfumes"),"name":_("Fashion")},
    "games" : {"description": CATEGORY_GAMES_DESCRIPTION, "meta-keywords":_("games, console"),"page-title":_("Games | Game Consoles, Mobile games"),"name":_("Games")},
    "health" : {"description": CATEGORY_HEALTH_DESCRIPTION, "meta-keywords":_("health"),"page-title":_("Health | Stories and tips on health"),"name":_("Health")},
    "marketing" : {"description": CATEGORY_MARKETING_DESCRIPTION, "meta-keywords":_("marketing"),"page-title":_("Marketing | Share your tips and stories marketing and SEO"),"name":_("Marketing")},
    "politics" : {"description": CATEGORY_POLITICS_DESCRIPTION, "meta-keywords":_("politics"),"page-title":_("Politics | News on politics around the world"),"name":_("Politics")},
    "reviews" : {"description": CATEGORY_REVIEWS_DESCRIPTION, "meta-keywords":_("reviews, products reviews"),"page-title":_("Reviews | Product reviews"),"name":_("Reviews")},
    "technology" : {"description": CATEGORY_TECHNOLOGY_DESCRIPTION, "meta-keywords":_("technology, science, engineering"),"page-title":_("Technology | Science , Engineering"),"name":_("Technology")},
}