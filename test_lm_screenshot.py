#! /usr/bin/python
#
# Copyright (c) 2020 Inaky Perez-Gonzalez
#
# SPDX-License-Identifier: Apache-2.0
#
# pylint: disable = missing-docstring
import os
import re
import time

import tcfl.app_sketch
import lml

# need this, since the console goes through network
class _test(lml.simple_base):
        
    def eval(self, ic, target):

        lml.ui_sw_sync(ic, target)

        # Start OVVE UI
        target.shell.run("export DISPLAY=:0")
        target.shell.run("pkill -f -9 ovve_ui.py || true")
        target.shell.run("python3 software-ui.git/ovve_ui/ovve_ui.py >& ovve_ui.log &")

        lml.controller_sw_sync(ic, target, "software-controller.git/software-controller.ino")
        
        self.expect(
            target.capture.image_on_screenshot('canary-resp-rate.png'),
            target.capture.image_on_screenshot('canary-TV-Exp.png'),
            target.capture.image_on_screenshot('canary-TV-insp.png'),
            target.capture.image_on_screenshot('canary-bottom-right.png'),
            target.capture.image_on_screenshot('canary-button-start.png'),
            name = 'OVVE starts')
