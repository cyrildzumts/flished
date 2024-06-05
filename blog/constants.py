from django.utils.translation import gettext_lazy as _

WEBP_QUALITY = 80
WEBP_EXT = ".webp"
IMAGE_MAX_SIZE = 10000000
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
HTTP_OK = 200
HEADERS = {
    'User-Agent': USER_AGENT
}
DB_DATETIME_FORMAT = "DD Mon YYYY HH24:MI"
CATEGORY_PAGE_TITLE_KEY = 'page-title'
CATEGORY_META_KEYWORDS_KEY = 'meta-keywords'
CATEGORY_DESCRIPTION_KEY = 'description'
MAX_RECOMMENDATION = 3
MAX_TRENDING = 3
FEED_MAX_POST = 5
SHORT_DESCRIPTION_MAX_SIZE = 164
DESCRIPTION_MAX_SIZE = 300
COMMENT_MAX_SIZE = 512
CATEGORY_DESCRIPTION_MAX_SIZE = 512
BTN_LABEL_MAX_SIZE = 32

PICK_OF_DAYS_SIZE = 3
MOST_RECENT_SIZE = 5
TRENDING_SIZE = 5
PER_CATEGORY_SIZE = 3
FEATURED_SIZE = 5

SEO_PAGE_TITLE_MAX_SIZE = 128
SEO_DESCRIPTION_MAX_SIZE = 300
SEO_META_KEYWORDS_MAX_SIZE = 128
FACEBOOK_DESCRIPTION_MAX_SIZE = 300

CACHE_CATEGORY_PATH_PREFIX = 'flished.category.path.'
CACHE_CATEGORY_DESCENDANTS_PREFIX = 'flished.category.descendants.'
CACHE_CATEGORY_POST_PREFIX = 'flished.category.posts.'
CACHE_POST_TAGS_PREFIX = 'flished.post.tags.'
CACHE_CATEGORY_MAPS_PREFIX = "flished.category.map."
CACHE_CATEGORY_ALL_PREFIX = "flished.category.categories.all"
CACHE_CATEGORY_CHILDREN_PREFIX = "flished.category.children."
CACHE_CATEGORY_ROOT_CHILDREN_KEY = CACHE_CATEGORY_CHILDREN_PREFIX + "root"
CACHE_NEWS_PREFIX = "flished.news."
CACHE_NEWS_ALL_KEY = CACHE_NEWS_PREFIX + "all"



POST_STATUS_DRAFT = 0
POST_STATUS_PUBLISHED = 1
POST_STATUS_REVIEW = 2
POST_STATUS_REVIEW_FAILED = 3
POST_STATUS_DELETED = 4
POST_STATUS_SCHEDULED = 5

POST_STATUS = (
    (POST_STATUS_DRAFT, _('draft')),
    (POST_STATUS_PUBLISHED, _('published')),
    (POST_STATUS_REVIEW, _('review')),
    (POST_STATUS_DELETED, _('deleted')),
    (POST_STATUS_SCHEDULED, _('scheduled')),
)

SEARCH_TYPE_PLAIN = "plain"
SEARCH_TYPE_PHRASE = "phrase"
SEARCH_TYPE_RAW = "raw"
SEARCH_TYPE_WEBSEARCH = "websearch"
SEARCH_ORDER_BY_RANK_ASCENDING = "rank"
SEARCH_ORDER_BY_RANK_DESCENDING = "-rank"
SEARCH_RANK_FILTER = 0.0001
# QUERIES

CATEGORY_CHILD_TO_ROOT_QUERY = """
WITH RECURSIVE CTE_CAT(id, name, parent_id, parents) AS (
SELECT id,name, parent_id, array[parent_id] FROM blog_category 
WHERE id=%s
UNION
SELECT CTE_CAT.id, CTE_CAT.name, c.parent_id, CTE_CAT.parents||c.parent_id 
FROM CTE_CAT
JOIN blog_category c ON CTE_CAT.parent_id = c.id
)
SELECT distinct on (id) id,name, parents
FROM CTE_CAT 
ORDER BY id, array_length(parents, 1) desc;
"""

### GET ANCESTOR :
CATEGORY_ANCESTOR = """
 WITH RECURSIVE
    CTE AS (
        SELECT 
            *
        FROM
            blog_category
        WHERE
            id = %s
        UNION ALL
        SELECT
            c.*
        FROM
            blog_category c
                JOIN CTE  ON c.id = CTE.parent_id
        WHERE
            CTE.parent_id IS NOT NULL
    )
    SELECT * FROM CTE;
"""

CATEGORY_ROOT_TO_CHILD_QUERY = """
WITH RECURSIVE CTE_CAT(id, name, parent_id, parents) AS (
SELECT id,name, parent_id, array[parent_id] FROM blog_category 
WHERE parent_id=%s
UNION
SELECT CTE_CAT.id, CTE_CAT.name, c.parent_id, CTE_CAT.parents||c.parent_id 
FROM CTE_CAT
JOIN blog_category c ON c.id = CTE_CAT.parent_id
)
SELECT distinct on (id) id,name, parents
FROM CTE_CAT 
ORDER BY id, array_length(parents, 1) desc;
"""


CATEGORY_DESCENDANTS_QUERY = """
WITH RECURSIVE CTE AS(
    SELECT * FROM blog_category
    WHERE id=%s AND is_active=%s
    UNION 
    SELECT c.*   
    FROM blog_category c
    JOIN CTE  ON c.parent_id = CTE.id
)
SELECT * FROM CTE;
"""


## GET ALL Product from the current category and subcategories
CATEGORY_POST_QUERY = """

WITH RECURSIVE graph(id) AS(
SELECT id FROM blog_category
WHERE id=%s AND is_active=true
UNION 
SELECT c.id FROM blog_category c, graph g WHERE c.parent_id = g.id AND c.is_active=true
)
SELECT * from blog_post p
WHERE p.category_id IN (SELECT id FROM graph ORDER BY id);
"""
