#! /usr/bin/python
#
# Copyright (c) 2020 Inaky Perez-Gonzalez
#
# SPDX-License-Identifier: Apache-2.0
#
# pylint: disable = missing-docstring

import lml

class _test(lml.simple_base):
        
    def eval(self, ic, target):

        # lml.simple_base.start_00() has uploaded code to the mega,
        # uploaded the UI code to the raspberry PI and started the UI
        # on raspberry's console ssh1, so ssh0 is available for normal
        # commands.

        # UI is freshly started
        r = self.expect(
            target.capture.image_on_screenshot('canary-resp-rate.png'),
            target.capture.image_on_screenshot('canary-TV-Exp.png'),
            target.capture.image_on_screenshot('canary-TV-insp.png'),
            target.capture.image_on_screenshot('canary-bottom-right.png'),
            target.capture.image_on_screenshot('canary-button-start.png'),
            name = 'OVVE starts')

        target.input.image_click(r['canary-button-start_png'], click_time = 1)
        r = self.expect(
            target.capture.image_on_screenshot('canary-button-stop.png'),
            name = 'start button changes to stop after pressing start',
            timeout = 20)

        target.input.image_click(r['canary-button-stop_png'])
        r = self.expect(
            target.capture.image_on_screenshot('canary-confirm-stop.png'),
            target.capture.image_on_screenshot('canary-confirm-stop-confirm.png'),
            name = 'warning dialog comes up when pressing stop',
            timeout = 20)

        target.input.image_click(r['canary-confirm-stop-confirm_png'])
        r = self.expect(
            target.capture.image_on_screenshot('canary-button-start.png'),
            name = 'start button shows up again after confiriming stop',
            timeout = 20)

