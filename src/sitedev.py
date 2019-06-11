#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

### Basic configuration
########################

AUTHOR = u'Oleksii Tsvietnov'
SITENAME = u"Vorakl's notes"
SITEURL = 'https://vorakl.name'
SITEDESC = u"Notes about Systems/Software Engineering and Operations"
SITE_VERSION = '1560070550'
SITE_KEYWORDS = 'vorakl,Oleksii Tsvietnov,blog,systems engineering,operations,software engineering'
PATH = 'content' # the location of all content
ARTICLE_PATHS = ['articles'] # a place for articles under the content location
PAGE_PATHS = ['pages']
CONTACT_URL = SITEURL + '/pages/about/'
START_URL = 'news/' # What's a start point of a site (like 'news/' or 'pages/about/')?
TIMEZONE = 'Europe/Berlin'
THEME = "/theme"
DEFAULT_LANG = u'en'
RELATIVE_URLS = True  # disable in public version
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
THEME_TEMPLATES_OVERRIDES = ['/site/theme.local/']
FAVICON_TEMPLATE = "favicon.html"
#LOCALCSS_TEMPLATE = "localcss.html" # you can override some default styles
#THEME_MENU_COLOR_1 = "#2e435e"
#THEME_MENU_COLOR_2 = "#205081"
PLUGIN_PATHS = ['/plugins']
PLUGINS = ['post_stats', 'minify'] # keep 'minify' plugin as the last element in the list to minify all output HTMLs

DEFAULT_PAGINATION = 10 # Turns on the pagination
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/p{number}/', '{base_name}/p{number}/index.html'),
)

DELETE_OUTPUT_DIRECTORY = True  # build an output dir from scratch every time
OUTPUT_RETENTION = [".git", "CNAME", "README.md", "favicon", "src"] # but these dirs and files should be kept


### Interface configuration
############################

DISPLAY_AUTHOR_IN_ARTICLE = False # Add an author in a article's metadata

# MENU
DISPLAY_MENU = True
DISPLAY_PAGES_IN_MENU = False
DISPLAY_CATEGORIES_IN_MENU = False
DISPLAY_ITEMS_IN_MENU = True # Items are set in the MENUITEMS variable below

# SIDEBAR
DISPLAY_SIDEBAR = True
DISPLAY_MENUITEMS_ON_SIDEBAR = True # Items are set in the MENUITEMS variable below
DISPLAY_SITE_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_SIDEBAR = False
DISPLAY_PAGES_ON_SIDEBAR = False

DISPLAY_TAGS_ON_SIDEBAR = False
DISPLAY_LINKS_ON_SIDEBAR = False # Links are set in the LINKS variable below

DISPLAY_SIDEBAR_SITE_NAME = "Site"
DISPLAY_SIDEBAR_ARCHIVES_NAME = "Archive"
DISPLAY_SIDEBAR_ALLARTICLES_NAME = "All posts"
DISPLAY_SIDEBAR_CATEGORIES_NAME = "Categories"
DISPLAY_SIDEBAR_TAGS_NAME = "Tags"
DISPLAY_SIDEBAR_PAGES_NAME = "Pages"
DISPLAY_SIDEBAR_LINKS_NAME = "Links"
DISPLAY_SIDEBAR_MENUITEMS_NAME = "Menu"

# SIDEBAR.SITE
DISPLAY_ARCHIVES_IN_SITE = True # It also turns on/off an appropriate section in a sitemap.xml
DISPLAY_ALLARTICLES_IN_SITE = True
DISPLAY_CATEGORIES_IN_SITE = True # It also turns on/off an appropriate section in a sitemap.xml
DISPLAY_TAGS_IN_SITE = True # It also turns on/off an appropriate section in a sitemap.xml
DISPLAY_PAGES_IN_SITE = False # It also turns on/off an appropriate section in a sitemap.xml 
DISPLAY_SUBSCRIBES_IN_SITE = True
DISPLAY_AUTHORS_IN_SITE = False

#LINKS = [
#    ("Github", "https://github.com/vorakl"), 
#    ("LinkedIn", "https://linkedin.com/in/vorakl/")
#]
MENUITEMS = [
    ("Projects", SITEURL + "/pages/projects/"),
    ("Contacts", SITEURL + "/pages/contacts/"),
    ("About", SITEURL + "/pages/about/"),
]

CATEGORIES_DESCRIPTION = {
    "article": "A full story about some specific topic",
    "howto": "A practical guide how to make something",
    "tutorial": "A theoretical explanation of a topic with examples",
    "trick": "A not always obvious way to get something",
    "note": "A brief record of thoughts, written down as an aid to memory",
}
TAGS_DESCRIPTION = {
    "bash": "A programming language",
    "python": "A programming language",
    "mindmap": "Notes presented in linked diagrams",
    "it": "Information Technology",
    "cs": "Computer Science",
    "learning": "A container platform",
}


### Feed's specification 
#########################

FEED_EMAIL = None # disable in development version
FEED_DOMAIN = '' # and create all feed under the local domain for testing purpose
FEED_MAX_ITEMS = 15
FEED_ALL_ATOM = None
FEED_ALL_RSS = None # Here is used the only one feed on Google's feedburner. All other feeds are disabled
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TAG_FEED_ATOM = None
TAG_FEED_RSS = None


### Static files (non templates)
#################################

STATIC_PATHS = [
    'images', 
    'files', 
    'static/robots.txt', 
    'static/favicon.ico', 
    'static/google747986e3861ca881.html',
    'static/BingSiteAuth.xml',
    ]
# and sprecial output paths for them
EXTRA_PATH_METADATA = {
    'static/robots.txt': {'path': 'robots.txt'},
    'static/favicon.ico': {'path': 'favicon.ico'},
    'static/google747986e3861ca881.html': {'path': 'google747986e3861ca881.html'},
    'static/BingSiteAuth.xml': {'path': 'BingSiteAuth.xml'},
    }


### Templates for html pages
#############################

# blog posts related pages

# If there is a 'Save_as' metadata (like in 404.html), then a page will be rendered anyway
ARTICLE_SAVE_AS = 'articles/{slug}/index.html' # activates rendering each article
ARTICLE_URL = 'articles/{slug}/'
ARTICLE_LANG_SAVE_AS = 'articles/{slug}-{lang}/index.html'
ARTICLE_LANG_URL = 'articles/{slug}-{lang}/'
DRAFT_SAVE_AS = 'drafts/{slug}/index.html' # activates rendering each article's draft
DRAFT_URL = 'drafts/{slug}/'
DRAFT_LANG_SAVE_AS = 'drafts/{slug}-{lang}/index.html'
DRAFT_LANG_URL = 'drafts/{slug}-{lang}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'  # activates rendering each page.
PAGE_URL = 'pages/{slug}/'
PAGE_LANG_SAVE_AS = 'pages/{slug}-{lang}/index.html'
PAGE_LANG_URL = 'pages/{slug}-{lang}/'
CATEGORY_SAVE_AS = 'categories/{slug}/index.html' # activates rendering each category
CATEGORY_URL = 'categories/{slug}/'
TAG_SAVE_AS = 'tags/{slug}/index.html' # activates rendering each tag
TAG_URL = 'tags/{slug}/'
AUTHOR_SAVE_AS = 'authors/{slug}/index.html' # activates rendering each author
AUTHOR_URL = 'authors/{slug}/'

# site related pages

# a list of templates for rendering blog posts. Not all of them, just an index and groups of entities (tags, categories, ...)
# other templates for blog posts rendering (for a tag, a category, ...) are activated by *_SAVE_AS variables below
DIRECT_TEMPLATES = ['index', 'categories', 'tags', 'authors', 'archives', 'allarticles']
PAGINATED_TEMPLATES = {'index': 10, 'tag': None, 'category': None, 'author': None}

INDEX_SAVE_AS = 'news/index.html'
AUTHORS_SAVE_AS = 'authors/index.html'  # defines where to save an authors page, it's activated by DIRECT_TEMPLATES 
AUTHORS_URL = 'authors/'
ARCHIVES_SAVE_AS = 'articles/index.html' # defines where to save an archives page, it's activated by DIRECT_TEMPLATES 
ARCHIVES_URL = 'articles/'
ALLARTICLES_SAVE_AS = 'allarticles/index.html' # defines where to save an all articles page, it's activated by DIRECT_TEMPLATES
ALLARTICLES_URL = 'allarticles/'
TAGS_SAVE_AS = 'tags/index.html' # defines where to save a tags page, it's activated by DIRECT_TEMPLATES
TAGS_URL = 'tags/'
CATEGORIES_URL = 'categories/' # defines where to save a categories page, it's activated by DIRECT_TEMPLATES
CATEGORIES_SAVE_AS = 'categories/index.html'
PAGES_SAVE_AS = 'pages/index.html' # defines where to save a list of all pages, it's activated by TEMPLATE_PAGES
PAGES_URL = 'pages/'

YEAR_ARCHIVE_SAVE_AS = 'articles/{date:%Y}/index.html' # activates rendering an archive page per year/month/day
MONTH_ARCHIVE_SAVE_AS = 'articles/{date:%Y}/{date:%m}/index.html'
DAY_ARCHIVE_SAVE_AS = ''

# additional pages

# a hash array with an extra list of 'templates+output_filename' for rendering besides of blog posts
# The output filename is needed because they don't have *_SAVE_AS variables
TEMPLATE_PAGES = {'sitemap.html': 'sitemap.xml',
                  'start.html': 'index.html',
                  'pages.html': PAGES_SAVE_AS} 
