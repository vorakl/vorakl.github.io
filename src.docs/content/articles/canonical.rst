How to redirect a static website on the Github Pages
####################################################

:summary: The use case for a Temporary Redirect and the Canonical Link Element
:date: 2019-07-02 11:42:34
:category: howto
:tags: it, web, html, http
:slug: canonical

I run a few static websites for my private projects on the `Github Pages`_. I'm absolutely happy with the service, as it supports custom domains, automatically redirects to HTTPS, and transparently installs SSL certificates (with automatic issuing via `Let's Encrypt`_). It is very fast (thanks to Fastly_'s content delivery network) and is extremely reliable (I haven't had any issues for years). Taking into account the fact that I get all of this for free, it perfectly matches my needs at the moment. It has, however, one important limitation: because it serves static websites only, this means no query parameters, no dynamic content generated on the server side, no options for injecting any server-side configuration (e.g., .htaccess), and the only things I can push to the website's root directory are *static assets* (e.g., HTML, CSS, JS, JPEG, etc.). In general, this is not a big issue. There are a lot of the open source  `static site generators`_ available, such as Jekyll_, which is available by default the dashboard, and Pelican_, which I prefer in most cases. Nevertheless, when you need to implement something that is traditionally solved on the server side, a whole new level of challenge begins.

|

For example, I recently had to change a custom domain name for one of my websites. Keeping the old one was ridiculously expensive, and I wasn't willing to continue wasting money. I found a cheaper alternative and immediately faced a bigger problem: all the search engines have the old name in their indexes. Updating indexes takes time, and until that happens, I would have to redirect all requests to the new location. Ideally, I would redirect each indexed resource to the equivalent on the new site, but at minimum, I needed to redirect requests to the new start page. I had access to the old domain name for enough time, and therefore, I could run the site separately on both domain names at the same time.

|

There is one proper solution to this situation that should be used whenever possible: Permanent redirect, or the `301 Moved Permanently`_ status code, is the way to redirect pages implemented in the HTTP protocol. The only issue is that it's supposed to happen on the server side within a server response's HTTP header. But the only solution I could implement resides on a client side; that is, either HTML code or JavaScript. I didn't consider the JS variant because I didn't want to rely on the script's support in web browsers. Once I defined the task, I recalled a solution: the `HTML <meta> tag`_ *<meta http-equiv>* with the 'refresh_' `HTTP header`_. Although it can be used to ask browsers to reload a page or jump to another URL after a specified number of seconds, after some research, I learned it is more complicated than I thought with some interesting facts and details.

The solution
------------

**TL;DR** (for anyone who isn't interested in all the details): In brief, this solution configures two repositories to serve as static websites with custom domain names. On the site with the old domain, I reconstructed the website's entire directory structure and put the following *index.html* in each of them (including the root): 

.. code-block:: html

    <!DOCTYPE HTML>                                                                 
    <html lang="en">                                                                
        <head>                                                                      
            <meta charset="utf-8">
            <meta name="robots" content="noindex, nofollow" />
            <meta http-equiv="refresh" content="0;url={{THE_NEW_URL}}" />       
            <link rel="canonical" href="{{THE_NEW_URL}}" />                     
        </head>                                                                                                                                                                   
        <body>                                                                      
            <h1>                                                                    
                The page been moved to <a href="{{THE_NEW_URL}}">{{THE_NEW_URL}}</a>
            </h1>                                                                   
        </body>                                                                     
    </html>

When someone opens a resource on the old domain, most web browsers "immediately" redirect to the same resource on the new website (thanks to *http-equiv="refresh"*). For any resources that were missed or nonexistent, it is helpful to create a *404.html* file in the old website's root directory with the similar content, but without *rel="canonical"* because there is no a canonical page for this case.

|

Another `HTML <meta> tag "robots"`_ tells search engines to remove a `page from search results`_. 

|

The last piece of the puzzle is the `canonical link relation`_ (*rel="canonical"*), which prevents duplicating content as long as the implemented redirect **is not permanent**. From the HTTP response's perspective, it happens when `the request has succeeded`_ and there is an indication for search engines that a resource has moved and should be associated with a new (preferred) location.

|

I have learned a few interesting facts related to *http-equiv="refresh"* and *rel="canonical"*. The HTML <meta> tag *http-equiv* is used to **simulate** the presence of an HTTP header in a server response. That is, web developers without access to the web server's configuration can get a similar result by "injecting" HTTP headers from an HTML document (the "body" of an HTTP response). It seems the *refresh* header, which has been used by all popular web browsers for many years, **doesn't really exist**. At least not as a standardized HTTP header. There was a plan to add it in the HTTP/1.1 specification that was `deferred to HTTP/1.2`_ (or later), but it never happened.

|

The task of finding the real source URL for a resource is far from trivial. There are different scheme names (HTTP, HTTPS), multiple query parameters (page.html, page.html?a=1), various hostnames that resolve to the same IP address, etc. All of these options make a webpage look different to search engines, but the page is still the same. It gets even worse when the same content is published on independent web services. In 2009, Google, Yahoo, and Microsoft announced `support for a canonical link element`_ to clean up duplicate URLs on sites by allowing webmasters to choose a canonical (preferred) URL for a group of possible URLs for the same page. This helps search engines pick up the correct URL to associate with the content and can also improve `SEO for a site`_.


.. Links

.. _`Github Pages`: https://pages.github.com/
.. _`Let's Encrypt`: https://letsencrypt.org/
.. _Fastly: https://www.fastly.com/
.. _`static site generators`: https://www.staticgen.com/
.. _Jekyll: https://jekyllrb.com/
.. _Pelican: https://github.com/getpelican/pelican
.. _`HTML <meta> tag`: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta
.. _refresh: http://www.otsukare.info/2015/03/26/refresh-http-header
.. _`HTTP header`: https://tools.ietf.org/html/rfc2616#section-14
.. _`301 Moved Permanently`: https://tools.ietf.org/html/rfc2616#section-10.3.2
.. _`404 Not Found`: https://tools.ietf.org/html/rfc2616#section-10.4.5
.. _`401 Unauthorized`: https://tools.ietf.org/html/rfc2616#section-10.4.2
.. _`the request has succeeded`: https://tools.ietf.org/html/rfc2616#section-10.2.1
.. _`HTML <meta> tag "robots"`: https://developers.google.com/search/reference/robots_meta_tag
.. _`page from search results`: {filename}/articles/remove-webpage-google.rst
.. _`canonical link relation`: https://tools.ietf.org/html/rfc6596
.. _`deferred to HTTP/1.2`: https://lists.w3.org/Archives/Public/ietf-http-wg-old/1996MayAug/0594.html
.. _`support for a canonical link element`: https://www.mattcutts.com/blog/canonical-link-tag/
.. _`SEO for a site`: https://yoast.com/rel-canonical/
