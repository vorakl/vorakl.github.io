How to destroy your OS with tar
###############################

:summary: A dangerous case of tar archive unpacking
:date: 2024-05-19 20:32:42
:category: note
:tags: os, linux, tools
:slug: tar-curdir


This is a short story about how dangerous a trivial tar unpacking might be, and what can be done to minimize the risk or completely avoid it.

|

The mistake
-----------

Recently, I was practicing an installation of `Void Linux`_ via chroot `using XBPS method`_. I needed the `XBPS Package Manager`_ installed on my Fedora Linux host to prepare Void Linux's base system. One of the options is to download an archive of statically built tools from the official repository. I chose https://repo-default.voidlinux.org/static/xbps-static-latest.x86_64-musl.tar.xz

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

I got so used to having 0:0 as a user:group on all files in archives that I didn't even check their actual permissions and owners. I just looked at the directory structure and noticed that all the executables were conveniently located under the relative path *"./usr/bin/"*. I quickly decided to just extract them to my root directory, so they would be immediately available in my $PATH. This was a big mistake, because if I checked them, I'd see non-standard permissions (700) of a current directory "." and non-standard user:group of the entire archive content:

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

But not knowing that, I ran...

|

.. code-block:: shell

    $ sudo tar -C / -xvfp xbps-static-latest.x86_64-musl.tar.xz

|

In the seconds that followed, I noticed the rapid decline of my system. The windows of my XFCE session stopped redrawing, the X server itself shut down. I couldn't run sudo. I couldn't even boot my system again. It happened so quickly and unexpectedly that I could hardly believe that my last command had caused the crash. Fortunately, booting in a single mode and detailed analysis of the tar archive revealed the root cause.

|

The root cause
--------------

The tar archive contains the current directory "./", which became the root directory when I changed it with "tar -C / ..." to change it before extracting. Restoring the owner and permissions of the current (top) directory of the archive resulted in setting 700 permissions and 2002:2000 as owner:group on my directory tree, which changed its expected state.  Thus, my own user completely lost access to the entire file system. Who could have expected that? ;)

|

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

What can be done to prevent it?
-------------------------------

In general, it is convenient to create a new archive with a relative directory tree using a command similar to

|

.. code-block:: shell

    $ tar -C /path/to/rootfs -czf myarchive.tar.gz .

|

because you don't have to worry about the internal directory structure, and it's just one command. All files are addressed with simple *"."*. It is also useful during extraction, since *"-C /some/path/"* allows you to choose any destination directory. On the other hand, this approach adds a current directory to the archive (the top one in the output above), which takes away all convenience. The default behavior of GNU tar is *"Overwrite metadata of existing directories when extracting"*, which is equivalent to the *--overwrite-dir* option. For example, if an archive contains a backup of users' home directories with all the necessary permissions, it could be super easy to restore them by running something like *"tar -C /home -xpf homes.tar.gz"*. But this only works if the archive doesn't contain a current directory and the target *"/home/"* is not modified.

|

A good way to avoid such pitfalls is to add the **--no-overwrite-dir** option, which *"preserves metadata of existing directories"*. So, if you run something like *"tar -C /home --no-overwrite-dir -xpf homes.tar.gz"*, all existing directories (including the current one) will remain unchanged!

|

There are also a few ways to create an archive without a current directory, but most of them require either a directory change beforehand, or defining all files/directories for the future archive. However, I found a way that, although it looks odd, does the job in one command:

|

.. code-block:: shell

    $ tar --transform='s|tmp/rootfs|.|' --show-transformed-names -cvf myarchive.tar /tmp/rootfs/*

    # or without a verbose mode

    $ tar --transform='s|tmp/rootfs|.|' -cf myarchive.tar /tmp/rootfs/*

|

Thanks to `Eric Radman`_ for pointing out that BSD tar has another option, `-s`_, for similar functionality.

|

Another and pretty typical way to create such archives (packages) is to use fakeroot_. It runs as an unprivileged user and pretends that all files are owned by root. In fact, it's just an illusion. Let's have a look at the directory with the extracted original xbps tools:

|

.. code-block:: shell

    $ tree -agpu xbps-tools/ | head
    [drwxr-xr-x 2002     2000    ]  xbps-tools/
    ├── [drwxr-xr-x 2002     2000    ]  usr
    │   └── [drwxr-xr-x 2002     2000    ]  bin
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-alternatives -> xbps-alternatives.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-alternatives.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-checkvers -> xbps-checkvers.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-checkvers.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-create -> xbps-create.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-create.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-dgraph -> xbps-dgraph.static

|

And this is how it looks under *fakeroot*

|

.. code-block:: shell

    $ fakeroot /bin/bash

    root@localhost> tree -agpu xbps-tools/ | head
    [drwxr-xr-x root     root    ]  xbps-tools/
    ├── [drwxr-xr-x root     root    ]  usr
    │   └── [drwxr-xr-x root     root    ]  bin
    │       ├── [lrwxrwxrwx root     root    ]  xbps-alternatives -> xbps-alternatives.static
    │       ├── [-rwxr-xr-x root     root    ]  xbps-alternatives.static
    │       ├── [lrwxrwxrwx root     root    ]  xbps-checkvers -> xbps-checkvers.static
    │       ├── [-rwxr-xr-x root     root    ]  xbps-checkvers.static
    │       ├── [lrwxrwxrwx root     root    ]  xbps-create -> xbps-create.static
    │       ├── [-rwxr-xr-x root     root    ]  xbps-create.static
    │       ├── [lrwxrwxrwx root     root    ]  xbps-dgraph -> xbps-dgraph.static


| 

This fake environment allows you to create a tar archive with files owned by root without changing their real owners.

|

One more nice solution is to use the *cpio* tool to create or extract POSIX_ tar archives. This format can be enabled during archive creation by adding *"-H ustar"*. However, during extraction, the format is automatically detected, and it also doesn't change the permissions of the current directory, even if it exists in the archive! If you add the *"-d"* option and run *cpio* with *sudo*, all non-existing subdirectories will be created as root:root, which is also very convenient.

|

.. code-block:: shell

 
    $ tree -agpu newroot/
    [drwxr-xr-x root     root    ]  newroot/

    $ xz -cd xbps-static-latest.x86_64-musl.tar.xz | sudo cpio -D newroot -idv
    .
    ./usr
    ./usr/bin
    ./usr/bin/xbps-uunshare
    ./usr/bin/xbps-uhelper
    ./usr/bin/xbps-uchroot
    ./usr/bin/xbps-rindex
    ./usr/bin/xbps-remove
    ./usr/bin/xbps-reconfigure
    ./usr/bin/xbps-query
    ./usr/bin/xbps-pkgdb
    ./usr/bin/xbps-install
    ./usr/bin/xbps-fetch
    ./usr/bin/xbps-fbulk
    ./usr/bin/xbps-digest
    ./usr/bin/xbps-dgraph
    ./usr/bin/xbps-create
    ./usr/bin/xbps-checkvers
    ./usr/bin/xbps-alternatives
    ./usr/bin/xbps-alternatives.static
    ./usr/bin/xbps-checkvers.static
    ./usr/bin/xbps-create.static
    ./usr/bin/xbps-dgraph.static
    ./usr/bin/xbps-digest.static
    ./usr/bin/xbps-fbulk.static
    ./usr/bin/xbps-fetch.static
    ./usr/bin/xbps-install.static
    ./usr/bin/xbps-pkgdb.static
    ./usr/bin/xbps-query.static
    ./usr/bin/xbps-reconfigure.static
    ./usr/bin/xbps-remove.static
    ./usr/bin/xbps-rindex.static
    ./usr/bin/xbps-uchroot.static
    ./usr/bin/xbps-uhelper.static
    ./usr/bin/xbps-uunshare.static
    ./var
    ./var/db
    ./var/db/xbps
    ./var/db/xbps/keys
    ./var/db/xbps/keys/60:ae:0c:d6:f0:95:17:80:bc:93:46:7a:89:af:a3:2d.plist
    ./var/db/xbps/keys/3d:b9:c0:50:41:a7:68:4c:2e:2c:a9:a2:5a:04:b7:3f.plist
    179893 blocks


    $ tree -agpu newroot/ | head
    [drwxr-xr-x root     root    ]  newroot/
    ├── [drwxr-xr-x 2002     2000    ]  usr
    │   └── [drwxr-xr-x 2002     2000    ]  bin
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-alternatives -> xbps-alternatives.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-alternatives.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-checkvers -> xbps-checkvers.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-checkvers.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-create -> xbps-create.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-create.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-dgraph -> xbps-dgraph.static

|

Note that *newroot/* was left untouched and is still owned by root:root with 755 permissions. But *cpio* can do even more. You can create a POSIX tar and easily control which files go in it, because *cpio* only accepts filenames. So you can get the file list with *find* and then filter the output to remove (for this particular example) */usr*, */usr/bin*, */var/*, */var/db*, and that's it. Super safe and convenient for everyone, while maintaining a relative directory structure inside. Here is an example of how I created a tar archive with *cpio*, without any "systems" directories, and then extracted it with *tar* in the usual way:

|

.. code-block:: shell

    # Create a tar archive with 'cpio' of previously unpacked xbps tools
    $ (cd xbps-tools && find . | grep -v -e '^\.$' -e '^\./usr$' -e '^\./usr/bin$' -e '^\./var$' -e '^\./var/db$' | cpio -ov -H ustar > ../myxbps.tar)
    ./var/db/xbps/
    ./var/db/xbps/keys/
    ./var/db/xbps/keys/3d:b9:c0:50:41:a7:68:4c:2e:2c:a9:a2:5a:04:b7:3f.plist
    ./var/db/xbps/keys/60:ae:0c:d6:f0:95:17:80:bc:93:46:7a:89:af:a3:2d.plist
    ./usr/bin/xbps-uunshare.static
    ./usr/bin/xbps-uhelper.static
    ./usr/bin/xbps-uchroot.static
    ./usr/bin/xbps-rindex.static
    ./usr/bin/xbps-remove.static
    ./usr/bin/xbps-reconfigure.static
    ./usr/bin/xbps-query.static
    ./usr/bin/xbps-pkgdb.static
    ./usr/bin/xbps-install.static
    ./usr/bin/xbps-fetch.static
    ./usr/bin/xbps-fbulk.static
    ./usr/bin/xbps-digest.static
    ./usr/bin/xbps-dgraph.static
    ./usr/bin/xbps-create.static
    ./usr/bin/xbps-checkvers.static
    ./usr/bin/xbps-alternatives.static
    ./usr/bin/xbps-alternatives
    ./usr/bin/xbps-checkvers
    ./usr/bin/xbps-create
    ./usr/bin/xbps-dgraph
    ./usr/bin/xbps-digest
    ./usr/bin/xbps-fbulk
    ./usr/bin/xbps-fetch
    ./usr/bin/xbps-install
    ./usr/bin/xbps-pkgdb
    ./usr/bin/xbps-query
    ./usr/bin/xbps-reconfigure
    ./usr/bin/xbps-remove
    ./usr/bin/xbps-rindex
    ./usr/bin/xbps-uchroot
    ./usr/bin/xbps-uhelper
    ./usr/bin/xbps-uunshare
    179889 blocks

    $ file myxbps.tar
    myxbps.tar: POSIX tar archive

    # Check with 'tar' that all files have non root user/group and the archive doesn't contain . /usr /usr/bin /var /var/db
    $ tar -tvf myxbps.tar
    drwxr-xr-x 2002/2000         0 2024-05-21 16:04 var/db/xbps/
    drwxr-xr-x 2002/2000         0 2024-05-21 16:04 var/db/xbps/keys/
    -rw-r--r-- 2002/2000      1410 2024-05-21 16:04 var/db/xbps/keys/3d:b9:c0:50:41:a7:68:4c:2e:2c:a9:a2:5a:04:b7:3f.plist
    -rw-r--r-- 2002/2000      1410 2024-05-21 16:04 var/db/xbps/keys/60:ae:0c:d6:f0:95:17:80:bc:93:46:7a:89:af:a3:2d.plist
    -rwxr-xr-x 2002/2000   5623104 2024-05-21 16:04 usr/bin/xbps-uunshare.static
    -rwxr-xr-x 2002/2000   5643584 2024-05-21 16:04 usr/bin/xbps-uhelper.static
    -rwxr-xr-x 2002/2000   5631296 2024-05-21 16:04 usr/bin/xbps-uchroot.static
    -rwxr-xr-x 2002/2000   6414144 2024-05-21 16:04 usr/bin/xbps-rindex.static
    -rwxr-xr-x 2002/2000   5779264 2024-05-21 16:04 usr/bin/xbps-remove.static
    -rwxr-xr-x 2002/2000   5643904 2024-05-21 16:04 usr/bin/xbps-reconfigure.static
    -rwxr-xr-x 2002/2000   5685440 2024-05-21 16:04 usr/bin/xbps-query.static
    -rwxr-xr-x 2002/2000   5643904 2024-05-21 16:04 usr/bin/xbps-pkgdb.static
    -rwxr-xr-x 2002/2000   5787648 2024-05-21 16:04 usr/bin/xbps-install.static
    -rwxr-xr-x 2002/2000   5639488 2024-05-21 16:04 usr/bin/xbps-fetch.static
    -rwxr-xr-x 2002/2000   5631296 2024-05-21 16:04 usr/bin/xbps-fbulk.static
    -rwxr-xr-x 2002/2000   5623104 2024-05-21 16:04 usr/bin/xbps-digest.static
    -rwxr-xr-x 2002/2000   5640384 2024-05-21 16:04 usr/bin/xbps-dgraph.static
    -rwxr-xr-x 2002/2000   6402240 2024-05-21 16:04 usr/bin/xbps-create.static
    -rwxr-xr-x 2002/2000   5644032 2024-05-21 16:04 usr/bin/xbps-checkvers.static
    -rwxr-xr-x 2002/2000   5643904 2024-05-21 16:04 usr/bin/xbps-alternatives.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-alternatives -> xbps-alternatives.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-checkvers -> xbps-checkvers.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-create -> xbps-create.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-dgraph -> xbps-dgraph.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-digest -> xbps-digest.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-fbulk -> xbps-fbulk.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-fetch -> xbps-fetch.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-install -> xbps-install.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-pkgdb -> xbps-pkgdb.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-query -> xbps-query.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-reconfigure -> xbps-reconfigure.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-remove -> xbps-remove.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-rindex -> xbps-rindex.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-uchroot -> xbps-uchroot.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-uhelper -> xbps-uhelper.static
    lrwxrwxrwx 2002/2000         0 2024-05-21 16:04 usr/bin/xbps-uunshare -> xbps-uunshare.static

    # Created a new directory to emulate a root file system
    $ tree -agpu newroot2/
    [drwxr-xr-x root     root    ]  newroot2/
    ├── [drwxr-xr-x root     root    ]  usr
    │   └── [drwxr-xr-x root     root    ]  bin
    └── [drwxr-xr-x root     root    ]  var
        └── [drwxr-xr-x root     root    ]  db

    # Extract with 'tar' in a usual way
    $ sudo tar -C newroot2 -xvf myxbps.tar
    var/db/xbps/
    var/db/xbps/keys/
    var/db/xbps/keys/3d:b9:c0:50:41:a7:68:4c:2e:2c:a9:a2:5a:04:b7:3f.plist
    var/db/xbps/keys/60:ae:0c:d6:f0:95:17:80:bc:93:46:7a:89:af:a3:2d.plist
    usr/bin/xbps-uunshare.static
    usr/bin/xbps-uhelper.static
    usr/bin/xbps-uchroot.static
    usr/bin/xbps-rindex.static
    usr/bin/xbps-remove.static
    usr/bin/xbps-reconfigure.static
    usr/bin/xbps-query.static
    usr/bin/xbps-pkgdb.static
    usr/bin/xbps-install.static
    usr/bin/xbps-fetch.static
    usr/bin/xbps-fbulk.static
    usr/bin/xbps-digest.static
    usr/bin/xbps-dgraph.static
    usr/bin/xbps-create.static
    usr/bin/xbps-checkvers.static
    usr/bin/xbps-alternatives.static
    usr/bin/xbps-alternatives
    usr/bin/xbps-checkvers
    usr/bin/xbps-create
    usr/bin/xbps-dgraph
    usr/bin/xbps-digest
    usr/bin/xbps-fbulk
    usr/bin/xbps-fetch
    usr/bin/xbps-install
    usr/bin/xbps-pkgdb
    usr/bin/xbps-query
    usr/bin/xbps-reconfigure
    usr/bin/xbps-remove
    usr/bin/xbps-rindex
    usr/bin/xbps-uchroot
    usr/bin/xbps-uhelper
    usr/bin/xbps-uunshare

    $ tree -agpu newroot2/
    [drwxr-xr-x root     root    ]  newroot2/
    ├── [drwxr-xr-x root     root    ]  usr
    │   └── [drwxr-xr-x root     root    ]  bin
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-alternatives -> xbps-alternatives.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-alternatives.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-checkvers -> xbps-checkvers.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-checkvers.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-create -> xbps-create.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-create.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-dgraph -> xbps-dgraph.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-dgraph.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-digest -> xbps-digest.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-digest.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-fbulk -> xbps-fbulk.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-fbulk.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-fetch -> xbps-fetch.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-fetch.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-install -> xbps-install.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-install.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-pkgdb -> xbps-pkgdb.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-pkgdb.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-query -> xbps-query.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-query.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-reconfigure -> xbps-reconfigure.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-reconfigure.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-remove -> xbps-remove.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-remove.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-rindex -> xbps-rindex.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-rindex.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-uchroot -> xbps-uchroot.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-uchroot.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-uhelper -> xbps-uhelper.static
    │       ├── [-rwxr-xr-x 2002     2000    ]  xbps-uhelper.static
    │       ├── [lrwxrwxrwx 2002     2000    ]  xbps-uunshare -> xbps-uunshare.static
    │       └── [-rwxr-xr-x 2002     2000    ]  xbps-uunshare.static
    └── [drwxr-xr-x root     root    ]  var
        └── [drwxr-xr-x root     root    ]  db
            └── [drwxr-xr-x 2002     2000    ]  xbps
                └── [drwxr-xr-x 2002     2000    ]  keys
                    ├── [-rw-r--r-- 2002     2000    ]  3d:b9:c0:50:41:a7:68:4c:2e:2c:a9:a2:5a:04:b7:3f.plist
                    └── [-rw-r--r-- 2002     2000    ]  60:ae:0c:d6:f0:95:17:80:bc:93:46:7a:89:af:a3:2d.plist

|

Note that all "system" directories such as */usr* or */var/db* are left unmodified with their original owners and permissions.
In fact, you can get the same result with *tar* either

|

.. code-block:: shell

   $ (cd xbps-tools && find . | grep -v -e '^\.$' -e '^\./usr$' -e '^\./usr/bin$' -e '^\./var$' -e '^\./var/db$' | tar --verbatim-files-from -T - -cvf ../myxbps.tar)

|

That's how I would create such archives with files to be extracted to the root filesystem.

|

Conclusion
----------

Do not blindly extract an archive if you don't know what it contains! It could be fatal to your system.

|

.. Links
.. _`Void Linux`: https://voidlinux.org/
.. _`using XBPS method`: https://docs.voidlinux.org/installation/guides/chroot.html
.. _`XBPS Package Manager`: https://docs.voidlinux.org/xbps/index.html
.. _`-s`: https://man.openbsd.org/tar#s
.. _`Eric Radman`: http://eradman.com/
.. _fakeroot: https://wiki.debian.org/FakeRoot
.. _POSIX: {filename}/articles/posix.rst
