How to remove a webpage from the Google index
#############################################

:summary: The approach for removing outdated or deleted content from Google search results
:date: 2019-07-18 16:39:35
:category: howto
:tags: it, web, html
:slug: remove-webpage-google

It's important to keep in mind that search engines scan websites on periodic bases and these periods may vary depending on a number of factors. In general, websites' owners don't have full control over the behavior of search engines, but instead, they can define preferences in a form of instructions. Such instructions, for example, allow excluding certain web pages from showing up in search results or preventing search engines from digging into specific paths. There are two ways to declare preferences: tweaking parameters of `robots.txt`_ in the root of a website and `HTML <meta> tag "robots"`_ in the <head> block of web pages.

|

I've recently needed to move one of my static websites to another domain. It became a complex task as I'm not able to change a server-side configuration, and the `redirection of HTTP-requests`_ is only one part of the story. Once all users are being redirected to a new location, I had to initiate and speed up a process of cleaning up the search results from links to my old website.

|

There are basically a few common ways to remove web pages from search indexes:

- remove a page completely, so clients will be getting `404 Not Found`_ HTTP response. It is clearly not my case, as the old website responses with valid and existing web pages
- restrict access to a page by asking clients to enter credentials. Then, the server will be sending `401 Unauthorized`_ HTTP response. This also won't work for me, as requires changing the configuration on the server-side
- add an HTML <meta> tag *robots* with the value `noindex`_. That's exactly what I needed and can be implemented on the client-side.

The last method allows setting different preferences per page right from the HTML code. That is, search engines must have access to a page to read it and find this instruction. This also means that all web pages with *robots* meta tag shouldn't be blocked even by a robots.txt file!

|

This solution will show a few steps for removing an entire website from Google's search results.

- check *robots.txt* (if it exists) and be sure that search bots are allowed to go through the site and read all indexed web pages. The file should either be empty or something like this (allows any bots read any webpage on a site):

.. code-block:: robots.txt

    User-agent: *
    Disallow:

- add *robots* HTML <meta> tag in the <head> block with "noindex, nofollow" value in each indexed web page:

.. code-block:: html

    <meta name="robots" content="noindex, nofollow" />

- create a `sitemap.xml`_ file and define all indexed web pages with the <lastmod> section which points to some recent time. For example:

.. code-block:: xml

    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/page1/</loc>
            <changefreq>daily</changefreq>
            <lastmod>2019-06-15</lastmod>
        </url>
        <url>
            <loc>https://example.com/page2/</loc>
            <changefreq>daily</changefreq>
            <lastmod>2019-06-15</lastmod>
        </url>
    </urlset>

- `submit this sitemap.xml file`_ to Google to let it know about recent changes. It can be done using *curl* command:

.. code-block:: bash

    curl -sSLf https://google.com/ping?sitemap=https%3A%2F%2Fexample.com%2Fsitemap.xml

- `submit a removal request`_ for each indexed web page. It may take several days for some links (and a few tries per a page's URL) to get considered "outdated" and eligible for deleting from the index


.. Links

.. _`redirection of HTTP-requests`: https://vorakl.com/articles/canonical/
.. _`404 Not Found`: https://tools.ietf.org/html/rfc2616#section-10.4.5
.. _`401 Unauthorized`: https://tools.ietf.org/html/rfc2616#section-10.4.2
.. _`HTML <meta> tag "robots"`: https://developers.google.com/search/reference/robots_meta_tag
.. _noindex: https://support.google.com/webmasters/answer/93710
.. _`robots.txt`: https://www.robotstxt.org/
.. _`sitemap.xml`: https://www.sitemaps.org/
.. _`submit this sitemap.xml file`: https://www.sitemaps.org/protocol.html#submit_ping
.. _`submit a removal request`: https://www.google.com/webmasters/tools/removals
