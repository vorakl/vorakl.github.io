How to sort arrays natively in Bash
###################################

:summary: Sorting arrays in pure Bash with the asort built-in command
:date: 2024-02-20 18:37:45
:category: howto
:tags: bash
:slug: bash-sort


`TLDR: quick summary of the article`_

|

What would you do if, while implementing some solution in Bash, you suddenly needed to have an array in a sorted order? You might think of the *sort* tool from the *coreutils* package. Or you might even think that it's probably a good time to switch to Python or some other language? But it turns out that Bash supports sorting arrays natively! All you need is the **asort** built-in command. However, it is often not loaded by default, or even packaged on many modern Linux distributions. In this article I'll show you how to build and install Bash with all loadable modules from source, load them, and start writing faster, more advanced Bash scripts with less use of external commands.

|

First of all, check your Bash version. Version 5.2-release is the target of this article:

.. code-block:: shell

    echo ${BASH_VERSION}

|

The built-in loadable modules are loaded with the **enable** command. Bash expects to find loadable modules in one of the paths specified in the **BASH_LOADABLES_PATH** environment variable, which is a colon-separated list of directories. Setting this variable and enabling all the necessary commands can be done, for example, with *.bashrc*. If you are currently running a pre-installed Bash, check that the *asort* command is not loaded and it cannot be loaded due to its absence:

.. code-block:: shell

    enable -p | grep asort || { enable -f asort asort && enable -p | grep asort; }

|

If you see "*enable asort*" on the screen then the *asort* builtin is loaded and you can start using it, for example, by checking its help message:

.. code-block:: shell

    asort --help

|

Otherwise, let's build it from source. First of all, clone the project's official git repository and enter its directory:

.. code-block:: shell

    git clone https://git.savannah.gnu.org/git/bash.git && cd bash

|

The following procedure is pretty standard for any software written in C: you *configure* the build tools for the specific system, then you build the software, and then you install it on the system. During a configuration step, for example, you can change a default (/usr/local) installation path prefix. I'm going to override it with the same directory as the default. The loadable built-in commands can only be built after the main tool set is built:

.. code-block:: shell

    ./configure --prefix=/usr/local
    make
    make -C examples/loadables all others
    sudo make install
    sudo make -C examples/loadables install
    sudo cp -v examples/loadables/{necho,hello,cat,pushd,asort} /usr/local/lib/bash/

|

Loadable built-in commands are installed in */usr/local/lib/bash/* and Bash itself in */usr/local/bin/*. The trick with copying files is needed because the *asort* command is part of the extra commands and, as of this writing and Bash version 5.2.26, the Makefile doesn't support installing it. If all commands finished with no errors, you'll be able to find the loadable commands in the */usr/local/lib/bash/* directory. They are *shared objects* that can be analyzed in the typical way:

.. code-block:: shell

    cd /usr/local/lib/bash
    ldd asort
    file asort

|

To load built-in commands from these files, you need to know a name of the structure that was defined in the source code. Some files contain only one command, so there is only one such structure, some contain two commands and two structures. You can find out these names by checking the symbol table and looking for the pattern *<name>_struct*:

.. code-block:: shell

    objdump -t asort | grep _struct
    objdump -t truefalse | grep _struct

|

Make sure the *BASH_LOADABLES_PATH* environment variable is set and contains */usr/local/lib/bash*, the directory where we installed the built-in commands. Now, everything is ready for testing. Let's run a newly built Bash, and load some useful commands using the names we found in the symbol table:

.. code-block:: shell

    /usr/local/bin/bash
    echo ${BASH_VERSION}
    echo ${BASH_LOADABLES_PATH}
    enable -f asort asort
    enable -f truefalse true
    enable -f truefalse false
    enable -f dsv dsv
    dsv --help

|

Finally, we can perform reverse numerical sorting using only built-in functions:

.. code-block:: shell

    declare -a arr=(3 1 15 6 4 5 3)
    echo ${arr[*]}   # 3 1 15 6 4 5 3
    asort -nr arr
    echo ${arr[*]}   # 15 6 5 4 3 3 1

|

It's also worth checking out other loadable commands such as *id*, *ln*, *mkdir*, *mkfifo*, *cut*, *cat*, *stat*, *tee*, *uname*, and others (see the loadable modules directory). These are fairly common tools used in Bash scripting. They can all be loaded into the Bash itself, resulting in a significant overall performance improvement by eliminating the need to run external commands each time.

|

Summary
-------

* Bash supports sorting arrays natively using the built-in **asort** command.
* The asort and other loadable commands are not enabled by default and may need to be compiled from source.
* To build Bash and loadable commands from source, you clone the git repository, configure, make, and install it on your system.
* The enable command is used to load builtin commands using their struct names found in the symbol table.
* Common loadable commands include *asort*, *truefalse*, *dsv*, *id*, *ln*, *mkdir*, *uname*, *mkdir*, and many others.
* Loading builtins avoids running external commands, improving performance.
* Builtin commands are shared objects that can be analyzed with *ldd*, *file*, *objdump*.
* Loadable commands are installed in */usr/local/lib/bash* and need *BASH_LOADABLES_PATH* set to load.

.. Links
.. _`TLDR: quick summary of the article`: Summary_
