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

class _test(lml.simple_base):
        
    def eval(self, ic, target):

        # lml.simple_base.start_00() has uploaded code to the mega,
        # uploaded the UI code to the raspberry PI and started the UI
        # on raspberry's console ssh1, so ssh0 is available for normal
        # commands.

        # UI is freshly started
        self.expect(
            target.capture.image_on_screenshot('canary-resp-rate.png'),
            target.capture.image_on_screenshot('canary-TV-Exp.png'),
            target.capture.image_on_screenshot('canary-TV-insp.png'),
            target.capture.image_on_screenshot('canary-bottom-right.png'),
            target.capture.image_on_screenshot('canary-button-start.png'),
            name = 'OVVE starts')
