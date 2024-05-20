How to destroy your OS with tar
###############################

:summary: A dangerous case of tar archive unpacking
:date: 2024-05-19 20:32:42
:category: note
:tags: os, linux, tools
:slug: tar-curdir


The mistake
-----------

This is a short story about how dangerous a trivial tar unpacking might be, and what can be done to minimize the risk or completely avoid it. Recently, I was practicing an installation of `Void Linux`_ via chroot `using XBPS method`_. So, I needed the `XBPS Package Manager`_ installed on my Fedora Linux host to prepare Void Linux's base system. One of the options is to download an archive of statically built tools from the official repository. I chose https://repo-default.voidlinux.org/static/xbps-static-latest.x86_64-musl.tar.xz

|

.. code-block:: shell

    $ tar -tf xbps-static-latest.x86_64-musl.tar.xz | head

    ./
    ./usr/
    ./usr/bin/
    ./usr/bin/xbps-uunshare
    ./usr/bin/xbps-uhelper
    ./usr/bin/xbps-uchroot
    ./usr/bin/xbps-rindex
    ./usr/bin/xbps-remove
    ./usr/bin/xbps-reconfigure
    ./usr/bin/xbps-query

|

I got so used to having 0:0 as a user:group that I didn't even check the content of the file. Or, even what permissions were set. Frankly, I didn't even know about the hidden problem of the current directory in the archive at the time. I just looked at the directory structure, and that was my first big mistake. Because if I checked them, I'd see the following:

|

.. code-block:: shell

    $ tar -tvf xbps-static-latest.x86_64-musl.tar.xz | head

    drwx------ duncaen/netusers  0 2023-09-18 06:37 ./
    drwxr-xr-x duncaen/netusers  0 2023-09-18 06:37 ./usr/
    drwxr-xr-x duncaen/netusers  0 2023-09-18 06:37 ./usr/bin/
    lrwxrwxrwx duncaen/netusers  0 2023-09-18 06:37 ./usr/bin/xbps-uunshare -> xbps-uunshare.static
    lrwxrwxrwx duncaen/netusers  0 2023-09-18 06:37 ./usr/bin/xbps-uhelper -> xbps-uhelper.static
    lrwxrwxrwx duncaen/netusers  0 2023-09-18 06:37 ./usr/bin/xbps-uchroot -> xbps-uchroot.static
    lrwxrwxrwx duncaen/netusers  0 2023-09-18 06:37 ./usr/bin/xbps-rindex -> xbps-rindex.static
    lrwxrwxrwx duncaen/netusers  0 2023-09-18 06:37 ./usr/bin/xbps-remove -> xbps-remove.static
    lrwxrwxrwx duncaen/netusers  0 2023-09-18 06:37 ./usr/bin/xbps-reconfigure -> xbps-reconfigure.static
    lrwxrwxrwx duncaen/netusers  0 2023-09-18 06:37 ./usr/bin/xbps-query -> xbps-query.static

|

I quickly figured out that all the tools are conveniently located under a relative path  *"./usr/bin/"*, so my first thought was that I'll simply extract them to my root directory and they'll be immediately available in my *$PATH*. So, I ran as *root* user

|

.. code-block:: shell

    $ sudo tar -C / -xvfp xbps-static-latest.x86_64-musl.tar.xz

|

In the seconds that followed, I noticed the rapid decline of my system. The windows of my X session stopped redrawing, the X server itself shut down. I couldn't run sudo. I couldn't even boot my system successfully. It happened so quickly and unexpectedly that I could hardly believe that my last command had caused the crash. Fortunately, booting in single mode and a detailed analysis of the tar archive revealed the root cause. Basically, it was setting *"drwx------ duncaen/netusers"* permissions on my root directory /. Who could have expected that? ;)

|

How did this happen and why?
----------------------------

The tar archive contains the current directory *"./"*, which became the root directory when I used *"-C /"* to change it before extracting. Then custom owners and permissions from the archive have been restored to my directory tree, which changed its expected state. In general, it is convenient to create a new archive with a relative directory tree using a command similar to

|

.. code-block:: shell

    $ tar -C /path/to/rootfs -czf myarchive.tar.gz .

|

because you don't have to worry about the internal directory structure, and it's just one command. All files are addressed with simple *"."*. It is also useful during extraction, since *"-C /some/path/"* allows you to choose any destination directory. On the other hand, this approach adds a current directory to the archive (the top one in the output above), which takes away all convenience. For example, if an archive contains a backup of users' home directories with all the necessary permissions, it could be super easy to restore them by running something like *"tar -C /home -xpf homes.tar.gz"*. But this only works if the archive doesn't contain a current directory and the target *"/home/"* is not modified.

|

There are a few ways to create an archive without a current directory, but most of them require either a directory change beforehand, or defining all files/directories for the future archive. However, I found a way that, although it looks odd, does the job in one command:

|

.. code-block:: shell

    $ tar --transform='s|tmp/rootfs|.|' --show-transformed-names -cvf myarchive.tar /tmp/rootfs/*

    # or without a verbose mode

    $ tar --transform='s|tmp/rootfs|.|' -cf myarchive.tar /tmp/rootfs/*

|

Thanks to `Eric Radman`_ for pointing out that BSD tar has another option, `-s`_, for similar functionality.

|

Demo
----

For this little demo, I spun up a new VM. Don't try this on your running system!

|

.. code-block:: shell
   
    $ sudo chmod 700 /

    $ ls -ld /
    drwx------ 17 root root 4096 Mar 27 11:24 /

    $ sudo chown 2000:2000 /
    
    $ sudo chown 2000:2000 /usr
    -bash: /usr/bin/sudo: Permission denied

    $ sudo -s
    -bash: /usr/bin/sudo: Permission denied

    $ ls -ld /
    -bash: /usr/bin/ls: Permission denied

|

Conclusion
----------

Restoring the owner and permissions of the current (top) directory of the archive resulted in setting 700 permissions and duncaen:netusers as owner:group on the system root. As a result, my user completely lost access to the entire file system. Do not blindly extract an archive if you don't know what it contains! It could be fatal to your system.

|

.. Links
.. _`Void Linux`: https://voidlinux.org/
.. _`using XBPS method`: https://docs.voidlinux.org/installation/guides/chroot.html
.. _`XBPS Package Manager`: https://docs.voidlinux.org/xbps/index.html
.. _`-s`: https://man.openbsd.org/tar#s
.. _`Eric Radman`: http://eradman.com/
