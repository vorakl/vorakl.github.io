Using udp-link to enhance TCP connections stability
###################################################

:summary: A UDP transport layer implementation for proxying TCP connections
:date: 2024-01-16 18:44:53
:category: article
:tags: networking, tools
:slug: udp-link

I recently discovered udp-link_, a very useful project for all those guys like
me who spend most of their working time in terminals over ssh connections.
The tool implements the UDP transport layer, which acts as a proxy for
TCP connections. It's designed to be integrated into the OpenSSH configuration.
However, with a little trick, it can also be used as a general-purpose
TCP-over-UDP proxy. *udp-link* greatly improves the stability of connections
over unreliable networks that experience packet loss and intermittent
connectivity. It also includes an IP roaming, which allows TCP connections
to remain alive even if an IP address changes.

|

udp-proxy is written in C by `Pavlo Gulchuk`_, who has a lot of experience
in running unreliable networks. Despite being a young project, the version
v0.4_ shows pretty stable results. It's quite fast, and once configured, you
don't have to think about it anymore. Unless you're surprised every time when
ssh connections don't brake, survive a laptop's sleep mode and connections
to different Wi-Fi networks.

|

The current architecture is fairly simple. The tool on the client side takes
data on the stdin and sends it via UDP to the server side where the same copy
of the tool takes that data from the network and sends it over to some TCP
service. The destination TCP service and a UDP listening port on the server
side can be specified on the client at startup. Otherwise, a TCP connection
will be established with *127.0.0.1:22* and a port is randomly chosen from
a predefined port range. Note that the server firewall should allow the
traffic to this port range on UDP. The TCP service can also reside on a remote
host, if the server side is used as a jumpbox. I consider it one of the greatest
features that *udp-link* uses a zero server-side configuration, all
configuration tweaks happen only on the client side.

|

udp-link on the server side does not run as a daemon or listen on a UDP port
all the time. Instead, the client invokes the tool in a server mode with
a randomly generated key that is used to authenticate a client connection. This
is done on demand by establishing a temporary ssh connection to the server side
and running the tool in the background, after which a connection is terminated.
This is where a secure client authentication comes into play. *udp-link* doesn't
encrypt the transferred data, which is useful when is used together with ssh
because it avoids a double encryption, but needs to be kept that in mind when
used with other configurations.

|

To start using *udp-link*, you need to clone the repository, compile, and install
the tool on both sides

.. code-block:: shell

    git clone https://github.com/pgul/udp-link.git
    cd  udp-link
    make
    sudo make install

and then make an ssh connection on the client as

.. code-block:: shell

    ssh -o ProxyCommand="udp-link %r@%h" user@host

OpenSSH supports a number of macros such as *%r* and *%p* which and can be found
in its documentation. Personally, I use ssh in a slightly different way and
never send out my public ssh keys to unknown hosts. More details on this topic
can be found in a great article '`OpenSSH client side key management for better privacy and security`_',
written by Timothée Ravier. So I'm actively using *ssh_config* files, where
I specify all connection-specific details, such as hostname, username, ssh key,
and in this case, **ProxyCommand**. My typical *ssh_config* file looks
something like this

.. code-block:: shell

    Host some-server
        user some-user
        hostname some-IP
        IdentityFile ~/.ssh/ssh-some-server.key
        ProxyCommand udp-link some-IP

    Host some-IP
        user some-user
        IdentityFile ~/.ssh/ssh-some-server.key

    Host *
        IdentitiesOnly yes
        IdentityFile /dev/null
        GSSAPIAuthentication no
        HostbasedAuthentication no
        SendEnv no

and then to connect I just run

.. code-block:: shell

    ssh some-server

The second **Host some-IP** block is needed to provide a correct ssh key to
a temporary ssh connection that *udp-link* establishes at the beginning of
the session. To debug the connection, I run

.. code-block:: shell

    ssh -o ProxyCommand="udp-link --dump some-IP" some-server

If I need to bind a connection to a specific UDP port on the server side,
I initiate a connection like this

.. code-block:: shell

    ssh -o ProxyCommand="udp-link -b 1234 some-IP" some-server

You can also bind it to a privileged port (1-1024), but *udp-link* needs root
permissions to do this, which can be achieved in a number of ways, such
as making it root-owned with the setuid bit turned on on the server-side copy
of a binary file.

.. code-block:: shell

    chown root /usr/local/bin/udp-link
    chmod u+s /usr/local/bin/udp-link

|

Unlike other projects with a similar goal, e.g. Mosh_, *udp-link* doesn't
allocate a pesudo terminal, which I consider a feature, because it opens
the possibility to use the tool for proxying any arbitrary TCP connection.
However, *udp-link* cannot currently listen on a local TCP port on the client
side. Fortunately, this can be worked around by adding *socat* and its exceptional
ability to connect things. However, *socat* cannot be paired with *udp-link* via
an unnamed pipe, because pipes provide a unidirectional interprocess
communication, while here we need a bi-directional communication to get data
back from the network. The trick is that udp-link is called by socat. Here is
an example of how to open a listening *2525/TCP* port on the client side, then
proxy a future TCP connection over a UDP channel to a remote host, and connect
it to a *25/TCP* port on the server's localhost in debug mode

.. code-block:: shell

    socat TCP-LISTEN:2525 SYSTEM:"udp-link -t 127.0.0.1\:25 --debug some-IP"

|

*udp-link* is a small, flexible and very useful tool. I hope to see further
development, adding new features and maturing the code base.


.. Links

.. _udp-link: https://github.com/pgul/udp-link
.. _repository: https://github.com/pgul/udp-link
.. _`Pavlo Gulchuk`: https://gul.kiev.ua
.. _v0.4: https://github.com/pgul/udp-link/releases/tag/v0.4
.. _`OpenSSH client side key management for better privacy and security`: https://tim.siosm.fr/blog/2023/01/13/openssh-key-management/
.. _Mosh: https://github.com/mobile-shell/mosh
