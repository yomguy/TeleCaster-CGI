
TeleCaster is a web controlled audio/video recording and broadcasting system.

It is written in python and freely available for Linux.


ARCHITECTURE
============

Build and install well on Debian (>= Lenny) or Ubuntu/Kubuntu (>= 10.10)


MORE INFOS
==========

GitHub: https://github.com/yomguy/TeleCaster-CGI

Twitter : @parisson_studio


INSTALLATION
=============


1. Operating System
--------------------

TeleCaster now only works on GNU/Linux systems. The installer and the following instructions
are based on Debian like software management so that it should work on Debian (>= Lenny)
or Ubuntu / Kubuntu (>= 10.4). So please install one of these OS before.


2. Install dependencies
-------------------------

Needed::

    sudo aptitude update

    sudo aptitude install python python-dev python-libxml2 python-setuptools python-twitter python-liblo python-mutagen \
                        icecast2 apache2 apache2-suexec jackd libjack-jackd2-dev vorbis-tools procps meterbridge fluxbox \
                        vnc4server vncviewer swh-plugins jack-rack libshout3 libshout3-dev libmad0-dev libogg-dev g++ \
                        libgstreamer0.10-0 gstreamer0.10-plugins-good gstreamer0.10-plugins-base gstreamer0.10-plugins-bad \
                        gstreamer-tools git-core python-pip make libmad0-dev

Cleanup::

    sudo aptitude remove --purge pulseaudio

Additional formats::

    sudo aptitude install libfaac-dev libmp3lame-dev libflac-dev

Note that obtaining and installing a preempt RT kernel is STRONGLY advised to get a good audio (JACK) stability.
Moreover, edit the pam conf file to get RT "su" pam limits at boot::

    sudo vi /etc/pam.d/su

Uncomment::

    session    required   pam_limits.so


3. Install TeleCaster
----------------------

Get the source code with Git::

    git clone https://github.com/yomguy/TeleCaster-CGI

and run the install script::

    cd TeleCaster-CGI
    sudo python install.py


4. Configuration
------------------

Edit the following files to setup TeleCaster. Please be careful with the XML syntax::

    /etc/telecaster/telecaster.xml

and tune your configuration according with your JACK setup, vnc port, icecast passwords, twitter keys, deefuzzer conf, etc...::

    /etc/default/jackd
    /etc/default/vncserver
    /etc/default/icecast2
    /etc/icecast2/icecast.xml
    /etc/telecaster/deefuzzer_safe.xml
    /etc/telecaster/deefuzzer.xml

For more infos on how to configure the deefuzzer streaming tool, see ::

    http://svn.parisson.org/deefuzzer
    https://github.com/yomguy/DeeFuzzer

5. Start audio deamons
------------------------

Just reboot your machine or start the deamons manually::

    sudo /etc/init.d/jackd start
    sudo /etc/init.d/vncserver start


6. Configure Apache2
----------------------

Configure your apache VirtualHost editing /etc/apache2/sites-available/telecaster.conf

Enable the VirtualHost::

    sudo a2enmod suexec
    sudo a2ensite telecaster.conf

Maybe remove the default VirtualHost::

    sudo rm /etc/apache2/sites-enabled/000-default

Reload Apache::

    sudo /etc/init.d/apache2 reload


7. Usage
----------

Browse the TeleCaster web control page::

    http://localhost/telecaster/telecaster.py

Fill in the form and start any free recording and broadcasting stream !

To change the form options, just edit the conf file as root::

    sudo vi /etc/telecaster/telecaster.xml

Contact
=========

Any questions, suggestions ? Please post a ticket on the dev platform::

    https://github.com/yomguy/TeleCaster-CGI

or contact the main developer::

    Guillaume Pellerin <yomguy@parisson.com>
