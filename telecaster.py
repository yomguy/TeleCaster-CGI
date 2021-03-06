#!/usr/bin/python
# -*- coding: utf-8 -*-
# *-* coding: utf-8 *-*
"""
   telecaster

   Copyright (c) 2006-2010 Guillaume Pellerin <yomguy@parisson.org>

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Author: Guillaume Pellerin <yomguy@parisson.com>
"""

version = '0.5.6'

import os
import re
import sys
import pwd
import cgi
import cgitb
import time
from tools import *
from webview import *
from station import *
cgitb.enable()


class TeleCaster:
    """Manage the calls of Station and Webview to get the network and
    disk streams"""

    def __init__(self, conf_file):
        """Main function"""
        self.conf_file = conf_file
        conf_dict = xml2dict(self.conf_file)
        self.conf = conf_dict['telecaster']
        self.title = self.conf['infos']['name']
        self.log_file = self.conf['log']
        self.logger = Logger(self.log_file)
        self.uid = os.getuid()
        self.url = self.conf['infos']['url']
        self.user = pwd.getpwuid(os.getuid())[0]
        self.user_dir = '/home' + os.sep + self.user + os.sep + '.telecaster'
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)
        self.lock_file = self.user_dir + os.sep + 'telecaster.lock'
        if os.path.exists('/usr/local/bin/deefuzzer'):
            self.deefuzzer_path = '/usr/local/bin/deefuzzer'
        elif os.path.exists('/usr/bin/deefuzzer'):
            self.deefuzzer_path = '/usr/bin/deefuzzer'

    def transition_head(self):
        html_file = open('telecaster_starting_head.html', 'r')
        html = html_file.read()
        html_file.close()
        return html

    def transition_foot(self):
        html_file = open('telecaster_starting_foot.html', 'r')
        html = html_file.read()
        html_file.close()
        return html

    def main(self):
        edcast_pid = get_pid('edcast_jack', self.uid)

        deefuzzer_pid = get_pid(self.deefuzzer_path+' '+self.user_dir+os.sep+'deefuzzer.xml', self.uid)
        writing = edcast_pid != []
        casting = deefuzzer_pid != []
        form = WebView(self.conf, version)

        if deefuzzer_pid == [] and form.has_key("action") and \
            form.has_key("department") and form.has_key("conference") and \
            form.has_key("session") and form["action"].value == "start":

            self.conference_dict = {'title': '',
                        'department': '',
                        'conference': '',
                        'session': '',
                        'professor': '',
                        'comment': ''}

            for data in self.conference_dict:
                if not form.has_key(data):
                    self.conference_dict[data] = 'Inconnu'
                else:
                    value = form.getfirst(data)
                    if '....' in value:
                        self.conference_dict[data] = 'Inconnu'
                    else:
                        value = re.sub(r'\W+', '_', value)
                        self.conference_dict[data] = value.decode('utf-8')

            self.conference_dict['title'] = self.title
            s = Station(self.conf_file, self.conference_dict, self.lock_file)
            s.start()
            time.sleep(2)
            self.logger.write_info('starting')
            self.main()

        elif deefuzzer_pid != [] and os.path.exists(self.lock_file) and not form.has_key("action"):
            self.conference_dict = get_conference_from_lock(self.lock_file)
            form.stop_form(self.conference_dict, writing, casting)

        elif deefuzzer_pid and form.has_key("action") and form["action"].value == "stop":
            self.logger.write_info('stopping')
            if os.path.exists(self.lock_file):
                self.conference_dict = get_conference_from_lock(self.lock_file)
                s = Station(self.conf_file, self.conference_dict, self.lock_file)
                s.stop()
                time.sleep(2)
                self.main()

        elif deefuzzer_pid == []:
            form.start_form(writing, casting)

	elif deefuzzer_pid != []:
	    os.system('kill -9 '+deefuzzer_pid[0])
	    self.main()

conf_file = '/etc/telecaster/telecaster.xml'

if __name__ == '__main__':
    sys.stderr = sys.stdout
    t = TeleCaster(conf_file)
    t.main()
