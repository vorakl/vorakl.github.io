A few facts about POSIX
#######################

:summary: A journey to portable software 
:date: 2024-04-23 10:45:58
:category: article
:tags: it, os, programming
:slug: posix


`TLDR: quick summary of the article`_

|

How did we get there?
---------------------

|

In the early days of computing, programmers could only dream of portability. All programs were written directly in machine code for each computer architecture they were intended to run on. `Assembly languages`_ with mnemonic names for each CPU instruction and other goodies made programmers' lives a little easier, but programs were still architecture-specific. Operating systems (OS) had not yet been invented, so a program not only controlled the entire computer system, it also had to initialize and manage the peripherals. In fact, such bare-metal programs implemented drivers for every device they used. And every time a program needed to run on hardware with a different architecture, it was literally rewritten to accommodate a difference in the `CPU instruction`_ set, memory layout, and so on.

|

This is exactly what happened with Unix, which was originally written in assembly language by Ken Thompson over 50 years ago. The first versions of Unix were written for the `PDP-7`_ platform, and porting it to the `PDP-11`_ meant rewriting the code. When Dennis Ritchie created the C programming language, and `together they`_ rewrote most of the Unix code in it, software portability suddenly became possible. There are two main reasons for this. First, the code written in a high-level programming language is platform-agnostic, because compilers translate it into the assembly language for a target architecture. This is even more important for target systems based on `RISC CPUs`_, as they require writing significantly more assembly instructions than `CISC CPU`_ architecture. Even porting Unix to another platform was mostly a matter of adapting the architecture-dependent parts of the code. On the other hand, the operating system itself abstracts away all hardware specifics from a user program. Programmers don't have to implement multitasking, memory management, or drivers for different devices as they used to, because it's all part of the OS kernel and runs in the kernel address space. In contrast, user programs run in the user address space and access all of the features provided by the OS through the the system call interface. In `Real-time OSes`_, such as `Zephyr OS`_, it's `slightly different`_, but the idea of memory isolation and protection for user programs is preserved. This leads to two conclusions:

* *User programs become portable when they are written in a high-level programming language for a particular OS*. Once both requirements are met, programs are compiled into instructions for a target CPU and linked with system functions provided by the `libc`_ and OS-specific libraries to access the underlying hardware. 

* Portability is intended to be achieved **at the source code level**.

|

The birth of POSIX
------------------

|

This could have been the end of the story, but something fateful happened. Due to a legal restriction, AT&T was not allowed to sell Unix, so there was no money to be made from the newly born OS, which became increasingly popular after it was introduced to the world. However, it turned out to be possible to distribute Unix to any interested organization for the cost of the media. That's how Unix got to Berkeley in 1974 and many other places, leading to the creation of a number of OS derivatives. Some of the best known and still popular today are OSes based on the software distributed by Berkeley (BSD), e.g. FreeBSD and OpenBSD. Despite sharing the same ancestors and principles, each operating system followed its own unique path. Each of these operating systems had a unique interface (API) and implementation of kernel subsystems, syscalls, different system tools, etc. Even libc, which provides common functionality and  wrappers on top of syscalls, used to be very OS-specific. All of these OSes were Unix-like, but at the same time, it wasn't possible to take the source code of a program written for one OS and recompile it on another.

|

Over 35 years ago, these problems with software portability led to the emergence of the first `POSIX standard`_ in 1988. The acronym `was coined by Richard Stallman`_, who added "X" to the end of *Portable Operating System Interface*. The *POSIX™* trademark is currently owned by `IEEE`_, and *UNIX®* is a registered trademark of `The Open Group`_. It's meant to provide a `specification of the interface`_ that different Unix operating systems should have in common, including `programming languages and tools`_. It's important to note that **the interface is portable**, and not the implementation.

|

This was the common ground that made it possible to compile the same source code of a user program on any OS without modification, if both sides strictly followed the same standard. And this is still true to some extent today, as most modern and widely used Unix-like systems, such as Linux, and `*BSD`, do not strictly and completely follow POSIX standard, but rather use it as a guide. In addition to POSIX, there is also the `Single UNIX Specification`_ (SUS), which was consolidated with a few different POSIX standards in 2001. However, the latest SUS (SUSv4 2018) extends the latest POSIX standard (POSIX.1-2017), which is essentially its base specification, with the X/Open Curses specification. There are `a number of operating systems, such as MacOS`_, which are fully compliant with the POSIX and SUS standards, pass The Open Group  conformance tests and can therefore be called `Unix operating systems`_, not just Unix-like. Originally, POSIX was only created for Unix-like OSes, but over time it became so popular that its specification, in the form of the `Operating System Abstraction Layer (OSAL)`_, was partially implemented (some subset of the interface that applicable to the target system) in non-Unix OSes, such as Windows_, FreeRTOS_, Zephyr_, etc.

|

The POSIX spec
--------------

|

The very first standard was ratified by the IEEE in 1988 as IEEE Std 1003.1-1988, so it's called *POSIX.1-1988*. Since then, the standard has gone through several revisions, with different subsets of the specification being ratified under different names. For example, *POSIX.1-1990* (IEEE 1003.1-1990) defined *the system interface and computing environment*, *POSIX.2* (IEEE Std 1003.2-1992) defined *command language (shell) and tools*, etc. A very good and brief overview of the standard's revisions can be found in the `standards(7)`_ Linux man page. You may even come across references to some old revisions, such as POSIX.2, for example, when reading the `Bash source code`_. In 2001, POSIX.1, POSIX.2, and the Single UNIX Specification (SUS) were merged into a single document called *POSIX.1-2001*. Despite the somewhat misleading name, it does include the shell and tools specifications from POSIX.2. **The latest version of the standard is POSIX.1-2017**, also known as `IEEE Std 1003.1-2017`_, which is almost identical to POSIX.1-2008.

|

The document of the standard basically describes a specification that spans over two environments (a build-time and a run-time) and is represented by a few volumes:

* `Base Definitions`_: defines common to all volumes general terms and concepts, conformant requirements (symbolic constants, options, option groups), computing environment (locales, regexp, directory structure, tty, environment variables, etc), and C-language header files which need to be implemented by the compliant systems.

* `System Interfaces`_:  defines the C language standard (`ISO C99, ISO/IEC 9899:1999`_), system service functions, and the extension of the C standard library (libc) in terms of header files and functions.

* `Shell & Utilities`_: defines a source code-level interface to the Shell Command Language (sh) and the system utilities (awk, sed, wc, cat, ...), including behavior, command line parameters, exit statuses, etc.

* `Rationale`_: includes considerations for portability, subprofiling, option groups, and additional rationale that didn't fit any other volumes.

|

The current POSIX standard defines source code-level compatibility for `only two programming languages`_: *The C language (C99)* and *the shell command language*. However, some of the programs defined under "Utilities", such as awk_, also have their own language. Strictly speaking, the C standard library (libc) doesn't have to implement any additional functionality (functions and headers) that is not defined by the C standard (ISO C99 in this case), but most of them do. For example, the ISO C99 standard, defines 24 header files, including math functions (<math.h>), standard input/output (<stdio.h>), date and time (<time.h>), signal management (<signal.h>), string operations (<string.h>), and so on. However, the latest POSIX standard, defines 82 header files and, being fully compliant with ISO C99, extends it with with POSIX threads (<pthreads.h>), semaphores (<semaphore.h>), and many others. Modern libc implementations, e.g. `musl libc`_, are also very OS-specific, providing library functions to access operating system services (wrappers for system calls). Sometimes, the overlap with the POSIX specifications leads to difficulties in implementing the POSIX abstraction layer in the non-Unix operating systems, which also use some portable standalone libc implementations with their own POSIX support, e.g. using picolibc_ together with `Zephyr's POSIX library`_.

|

Options and Option Groups
-------------------------

|

While POSIX standardizes the system interface (C language headers and functions), shell, and utilities, it is not necessary to follow the entire specification to be `POSIX conformant`_. Some features in "POSIX System Interfaces", "POSIX Shell and Utilities", and "XSI System Interfaces" are optional. The `<unistd.h> header file`_ contains definitions of the *standard symbolic constants* for Options_, which reflect a particular feature, and `Option Groups`_ which define a set of related functions or options. Names of option groups, unlike options, typically do not begin with the underscore symbol. POSIX Conformant systems are intended to implement and support a set of mandatory options with one or more additional options. The symbolic constants for mandatory options should have specific values, e.g. *200809L*, while other options may be

* *undefined or contain -1*, which means that the option is not supported for compilation
* *0*, which means the option might or might not be supported at runtime
* *some other value*, which means the option is always supported

|

These symbolic constants are used by user applications to check the availability of a particular feature. At the C source code-level, constants may be checked either at build time (in #if preprocessing directives) or at runtime, by calling one of the *sysconf()*, *pathconf()*, *fpathconf()*, or *confstr(3)* functions. In the shell source code, the `getconf`_ utility should be used for runtime checks. A very good collection of the POSIX options, their corresponding names for use as the sysconf(3) parameters, and the list of header files and functions that these options represent can be found in the `posixoptions(7)`_ Linux man page.

|

`Subprofiling Option Groups`_ are intended for use within the systems where implementing a full POSIX specification is not reasonable. For example, real-time embedded systems are typically resource-constrained, do not have shells, user interfaces, and OS kernels are often designed to run as a single process (with multiple threads). Such systems may only implement subsets of related functions defined by option groups.

|

Summary
-------

* The development of high-level programming languages like C, along with operating systems that abstract away hardware details, enabled software portability at the source code level.
* The POSIX standard emerged in 1988 to provide a portable interface specification for Unix-like operating systems, allowing programs to be compiled across different platforms.
* The POSIX standard has evolved over time, with the latest version being POSIX.1-2017 (IEEE Std 1003.1-2017).
* Modern Unix-like systems like Linux and `*BSD` do not strictly follow the POSIX standard, but rather use it as a guide.
* POSIX standardizes a C API (header files and functions), the shell, and utilities.
* POSIX-compliant systems are expected to implement mandatory options and may support additional optional features.
* Applications can check for POSIX feature availability at both compile-time and runtime using symbolic constants and system functions.
* For resource-constrained systems like real-time embedded platforms, POSIX allows for the implementation of subsets of the full specification through "subprofile" option groups.

|

.. Links
.. _`TLDR: quick summary of the article`: Summary_
.. _`Assembly languages`: https://en.wikipedia.org/wiki/Assembly_language
.. _`CPU instruction`: https://en.wikipedia.org/wiki/Instruction_set_architecture
.. _`RISC CPUs`: https://en.wikipedia.org/wiki/Reduced_instruction_set_computer
.. _`CISC CPU`: https://en.wikipedia.org/wiki/Complex_instruction_set_computer
.. _`PDP-7`: https://en.wikipedia.org/wiki/PDP-7
.. _`PDP-11`: https://en.wikipedia.org/wiki/PDP-11
.. _`together they`: https://www.invent.org/sites/default/files/2019-02/Inductee-UNIX_Thompson_Ritchie.jpg
.. _`libc`: https://en.wikipedia.org/wiki/C_standard_library
.. _`Real-time OSes`: https://en.wikipedia.org/wiki/Real-time_operating_system
.. _`Zephyr OS`: https://www.zephyrproject.org/
.. _`slightly different`: https://www.youtube.com/watch?v=4_uL43V79xw
.. _`POSIX standard`: https://pubs.opengroup.org/onlinepubs/9699919799/nframe.html 
.. _`programming languages and tools`: https://stackoverflow.com/a/31865755
.. _`was coined by Richard Stallman`: https://opensource.com/article/19/7/what-posix-richard-stallman-explains
.. _`a number of operating systems, such as MacOS`: https://en.wikipedia.org/wiki/POSIX#POSIX-oriented_operating_systems
.. _`Unix operating systems`: https://www.opengroup.org/openbrand/register/   
.. _`Operating System Abstraction Layer (OSAL)`: https://en.wikipedia.org/wiki/Operating_system_abstraction_layer
.. _FreeRTOS: https://www.freertos.org/FreeRTOS-Plus/FreeRTOS_Plus_POSIX/index.html
.. _Zephyr: https://docs.zephyrproject.org/latest/services/portability/posix/index.html
.. _Windows: https://en.wikipedia.org/wiki/Cygwin
.. _`specification of the interface`: https://www.techtarget.com/whatis/definition/POSIX-Portable-Operating-System-Interface
.. _`Bash source code`: https://git.savannah.gnu.org/cgit/bash.git/tree/jobs.c#n4269
.. _`standards(7)`: https://man7.org/linux/man-pages/man7/standards.7.html
.. _`IEEE Std 1003.1-2017`: https://pubs.opengroup.org/onlinepubs/9699919799/nframe.html
.. _`Base Definitions`: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/toc.html
.. _`System Interfaces`: https://pubs.opengroup.org/onlinepubs/9699919799/idx/xsh.html
.. _picolibc: https://keithp.com/picolibc/
.. _`Zephyr's POSIX library`: https://docs.zephyrproject.org/latest/services/portability/posix/implementation/index.html
.. _`ISO C99, ISO/IEC 9899:1999`: http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf
.. _`musl libc`: https://musl.libc.org/about.html
.. _`Shell & Utilities`: https://pubs.opengroup.org/onlinepubs/9699919799/idx/xcu.html
.. _`Rationale`: https://pubs.opengroup.org/onlinepubs/9699919799/idx/xrat.html
.. _`POSIX conformant`: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap02.html#tag_02_01_03
.. _`<unistd.h> header file`: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/unistd.h.html
.. _Options: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap02.html#tag_02_01_06
.. _`Option Groups`: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap02.html#tag_02_01_05
.. _`getconf`: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/getconf.html
.. _`posixoptions(7)`: https://man7.org/linux/man-pages/man7/posixoptions.7.html
.. _`Subprofiling Option Groups`: https://pubs.opengroup.org/onlinepubs/9699919799/xrat/V4_subprofiles.html
.. _`Single UNIX Specification`: https://en.wikipedia.org/wiki/Single_UNIX_Specification
.. _`only two programming languages`: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap02.html#tag_02_04
.. _awk: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/awk.html
.. _`The Open Group`: https://www.opengroup.org/about-us
.. _`IEEE`: https://www.ieee.org/about/index.html
