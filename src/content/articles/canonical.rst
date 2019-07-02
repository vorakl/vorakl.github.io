How to redirect a static website on the Github Pages
####################################################

:summary: The use case for a Temporary Redirect and the Canonical Link Element
:date: 2019-07-02 11:42:34
:category: howto
:tags: it, web, html, http
:slug: canonical

I'm running a few static web sites for my private projects on the `Github Pages`_. And, I'm absolutely happy with the service as it supports custom domains, automatically redirects to HTTPS, provides a transparent installation of SSL certificates (with automatic issuing via `Let's Encrypt`_). It works very fast (thanks to Fastly_ CDN) and absolutely reliable (I haven't had any issues for years). Taking into account the fact that this all is provided for free, I would say, it perfectly matches my needs at the moment. Of course, there is one but important limitation: it serves only static websites, which means no query parameters, no dynamic content generated on a server side, no options for injecting some server-side configuration (like with .htaccess), etc. I can 'push' to the website's root directory only *static assets* (html, css, js, jpeg, ...). In general, this is not a big issue. There are a lot of the open source  `static site generators`_ available, and one of the most popular (Jekyll_) is even provided by default, right from the dashboard. I personally, prefer Pelican_ in most cases, but sometimes it's more suitable to upload manually created and simple web pages. Nevertheless, when you need to implement something that normally used to be solved on a server side, the whole fun begins...

|

Recently, I've had to change a custom domain name for one of those my websites. A prolongation of the old one was ridiculously expensive, and I wasn't willing to continue wasting money. So, I found a cheaper alternative and immediately faced with the main problem: all search engines have the old name in their indexes. Updating indexes takes the time and obviously until it's happened, I'll need to redirect all requests to a new location. Ideally, for each indexed resource to the equivalent on the new site, but at least, any possible requests to the new start page. I'll have access to the configuration of the old domain name for enough amount of time, and therefore, I'm able to run two different sites on both domain names at the same time.

|

There is one proper solution that has to be used whenever it's possible: Permanent Redirect ('`301 Moved Permanently`_' status code), the way of redirecting implemented in the HTTP protocol. The only issue is that it's done on a server side within the HTTP header of a server response. Apparently, the only solution I could implement resides on a client side. That is, either HTML code or JavaScript. The JS variant I didn't consider at all because I didn't want to rely on the scripts support in the web browsers. Once I defined clearly the task to myself, I immediately recalled a solution: the HTML `meta tag`_ '*http-equiv*' with the 'refresh_' "`HTTP header`_". Although, it can be used for asking browsers to reload a page or jump to another URL after a specified number of seconds. Having done a little research on the topic, it turned out it is much more complicated than I thought, with interesting facts and details.

|

**TL;DR**: for all readers who think that's enough ;) here is the brief description of the solution:
two repositories are configured for being served as static websites with custom domain names. On a site with the old domain, I reconstructed all directories structure of the main website and put in each of them (including the root) this *index.html*

.. code-block:: html

    <!DOCTYPE HTML>                                                                 
    <html lang="en">                                                                
        <head>                                                                      
            <meta charset="utf-8">
            <meta http-equiv="refresh" content="0;url={{THE_NEW_URL}}" />       
            <link rel="canonical" href="{{THE_NEW_URL}}" />                     
        </head>                                                                                                                                                                   
        <body>                                                                      
            <h1>                                                                    
                The page been moved to <a href="{{THE_NEW_URL}}">{{THE_NEW_URL}}</a>
            </h1>                                                                   
        </body>                                                                     
    </html>

Once someone opens a resource on the old domain, most web browsers will "immediately" redirect to the same resource on the new website (thanks to '*http-equiv="refresh"*'). For those resources which were missed or for nonexistent ones it is helpful to create *404.html* file in the root directory of the old website with the same content. The last piece of the puzzle is the `Canonical Link Relation`_ (*rel="canonical"*). It prevents duplicating the content as long as the implemented redirect **is not permanent**. From the perspective of the HTTP response, it happens when '`the request has succeeded`_', and there has to be an indication for search engines that a resource has been moved and should be associated with a new (preferred) location.

|

I have also found out a few interesting facts related to *http-equiv="refresh"* and *rel="canonical"*. The HTML meta tag *http-equiv*, as known, is used for **simulating** the presence of an HTTP header in a server response. That is, web developers, having no access to the configuration of a web server, are able to get a similar result by "injecting" HTTP headers from an HTML document (the "body" of an HTTP response). It seems the *refresh* header is being used for many many years by all popular web browsers, but this header **doesn't really exist**. At least, as a standardized HTTP header. There was the plan to add it in HTTP/1.1 specification but then `it was deferred to HTTP/1.2 (or later)`_, which in fact has never happened.

|

The task of finding the real source URL for a resource is far from trivial. Different scheme names (http, https), query parameters (page.html, page.html?a=1), various hostnames which are resolved to the same IP address, etc. All these options make a page looks different for search engines, but the web page is still the same. It gets even worse when the same content is published on absolutely independent web services, but the content is still the same. On February 2009, '`Google, Yahoo, and Microsoft announced support for a new link element to clean up duplicate urls on sites`_'. It allows webmasters to choose a canonical (preferred) URL for the group of possible URLs of the same page. This helps search engines to pick up the correct one to associate with the content and also improve `SEO for a site`_.

.. Links

.. _`Github Pages`: https://pages.github.com/
.. _`Let's Encrypt`: https://letsencrypt.org/
.. _Fastly: https://www.fastly.com/
.. _`static site generators`: https://www.staticgen.com/
.. _Jekyll: https://jekyllrb.com/
.. _Pelican: https://github.com/getpelican/pelican
.. _`meta tag`: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta
.. _refresh: http://www.otsukare.info/2015/03/26/refresh-http-header
.. _`HTTP header`: https://tools.ietf.org/html/rfc2616#section-14
.. _`301 Moved Permanently`: https://tools.ietf.org/html/rfc2616#section-10.3.2
.. _`the request has succeeded`: https://tools.ietf.org/html/rfc2616#section-10.2.1
.. _`Canonical Link Relation`: https://tools.ietf.org/html/rfc6596
.. _`it was deferred to HTTP/1.2 (or later)`: https://lists.w3.org/Archives/Public/ietf-http-wg-old/1996MayAug/0594.html
.. _`Google, Yahoo, and Microsoft announced support for a new link element to clean up duplicate urls on sites`: https://www.mattcutts.com/blog/canonical-link-tag/
.. _`SEO for a site`: https://yoast.com/rel-canonical/
