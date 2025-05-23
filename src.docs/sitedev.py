#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import time

### Basic configuration
########################

AUTHOR = u'vorakl'
SITENAME = u"Vorakl's notes"
SITEURL = 'https://vorakl.com'
SITEDESC = u"A technical blog about Automation, Programming, Operating Systems, Clouds, Monitoring, Performance Tuning and Troubleshooting, and many other aspects of Systems and Software Engineering"
SITETITLE = u"Notes on Systems and Software Engineering"
DISCLAIMER_SHORT = u"All ideas, examples and opinions on this personal website are the result of my own practice in spare time, belong to me and don't relate to my work at any companies."
ADD_DISCLAIMER_SHORT = False
DISCLAIMER_LONG = u"This is my personal blog. All ideas, opinions, examples, and other information that can be found here are my own and belong entirely to me. This is the result of my personal efforts and activities at my free time. It doesn't relate to any professional work I've done and doesn't have correlations with any companies I worked for, I'm currently working, or will work in the future."
ADD_DISCLAIMER_LONG = True
SITE_VERSION = str(int(time.time()))
SITE_KEYWORDS = 'vorakl,blog,systems engineering,operations,software engineering'
PATH = 'content' # the location of all content
ARTICLE_PATHS = ['articles'] # a place for articles under the content location
PAGE_PATHS = ['pages']
CONTACT_URL = SITEURL + '/pages/about/'
START_URL = 'news/' # What's a start point of a site (like 'news/' or 'pages/about/')?
TIMEZONE = 'America/Los_Angeles'
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
#COUNTER_TEMPLATE = "counter.html"
TYPO_GH_URL = "https://github.com/vorakl/vorakl.github.io/blob/master/src.docs/content/articles"
PLUGIN_PATHS = ['/plugins']
PLUGINS = ['post_stats', 'minify'] # keep 'minify' plugin as the last element in the list to minify all output HTMLs

DEFAULT_PAGINATION = 10 # Turns on the pagination
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/p{number}/', '{base_name}/p{number}/index.html'),
)

DELETE_OUTPUT_DIRECTORY = True  # build an output dir from scratch every time
OUTPUT_RETENTION = [".git", "CNAME", "favicon", "src.docs", "voraklsnotes"] # but these dirs and files should be kept


### Interface configuration
############################

DISPLAY_AUTHOR_IN_ARTICLE = False # Add an author in a article's metadata

# MENU
DISPLAY_MENU = True
DISPLAY_PAGES_IN_MENU = False
DISPLAY_CATEGORIES_IN_MENU = False
DISPLAY_ITEMS_IN_MENU = True # Items are set in the MENUITEMS variable below

# SIDEBAR
DISPLAY_INDEX_SIDEBAR = True
DISPLAY_PAGE_SIDEBAR = False
DISPLAY_MENUITEMS_ON_SIDEBAR = False # Items are set in the MENUITEMS variable below
DISPLAY_SITE_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_SIDEBAR = False
DISPLAY_PAGES_ON_SIDEBAR = False

DISPLAY_TAGS_ON_SIDEBAR = False
DISPLAY_LINKS_ON_SIDEBAR = False # Links are set in the LINKS variable below

DISPLAY_SIDEBAR_SITE_NAME = "MENU"
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
    ("Contacts", SITEURL + "/pages/contacts/"),
    ("About", SITEURL + "/pages/about/"),
]

CATEGORIES_DESCRIPTION = {
    "article": "A full story about some specific topic",
    "howto": "A practical guide how to make something",
    "tutorial": "A theoretical explanation of a topic with examples",
    "trick": "A not always obvious way to do something",
    "note": "A brief record of thoughts",
    "cheatsheet": "A collection of useful facts",
}
TAGS_DESCRIPTION = {
    "bash": "A programming language",
    "python": "A programming language",
    "mindmap": "Notes in hierarchically linked diagrams",
    "it": "Information Technology",
    "cs": "Computer Science",
    "learning": "Materials about acquiring new skills",
    "ai": "Artificial Intelligence",
    "psychology": "All about the human mind and behavior",
    "programming": "Everything related to creating computer programs",
    "management": "Management, Planning, Leading, etc",
    "http": "The HyperText Transfer Protocol",
    "html": "The markup language for Web pages",
    "web": "The World Wide Web (hypertext system)",
    "math": "Topics related to mathematics",
    "binary-to-text": "Translation between binary data and text",
    "encoding": "Transformation one form of data to anoher",
    "networking": "Computer Networks and Protocols",
    "tools": "A variety of useful tools",
    "sdlc": "Software Development Life Cycle and related topics",
    "sre": "Site Reliability Engineering Practice",
    "os": "Operating Systems",
    "linux": "Linux OS",
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
    'about',
    'contacts',
    'static/robots.txt', 
    'static/favicon.ico', 
    ]
# and sprecial output paths for them
EXTRA_PATH_METADATA = {
    'static/robots.txt': {'path': 'robots.txt'},
    'static/favicon.ico': {'path': 'favicon.ico'},
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

