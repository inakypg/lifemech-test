#! /usr/bin/python
#
# Copyright (c) 2020 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#
# pylint: disable = missing-docstring
"""
"""
import os
import re

import tcfl.tc
import tcfl.tl

def vnc_start(target):
    target.shell.run(
        "if ! pgrep x11vnc; then "
        " rm -f vnc.log;"
        " sudo -u pi"
        " nohup"
        # -shared, so we can watch and take screenshots at the same time
        " x11vnc -shared -display :0 -forever -loop -q"
        # /root/vnc.sock is used as a flag that the thing is up
        " -rfbport %(vnc-tcp-port)s >& vnc.log &"
        " while ! pgrep x11vnc; do sleep 1s; done;"
        " sleep 1s;"
        "fi"
        % target.kws)


def deploy_vnc_start(ic, target):
    target.shell.prompt = re.compile("TCF-%(tc_hash)s:.*\$ " % target.kws)
    ic.power.on()
    target.pos.boot_normal()
    target.shell.up(user = 'root')
    target.input.evemu_target_setup(ic)
    target.console.disable()
    target.shell.up(user = "pi")
    # this is where we run the UI
    target.console.disable(console = "ssh1")
    target.shell.up(user = "pi", console = "ssh1")
    vnc_start(target)


def ui_sw_sync(ic, target, path):
    # Deploy the software tree to the RPI
    port = target.tunnel.add(22)
    hostname = target.rtb.parsed_url.hostname
    target.testcase.shcmd_local(
        "rsync -e 'ssh -p %s' -a %s root@%s:/home/pi"
        % (port, path, hostname))

def controller_sw_sync(target, path = "software-controller/software-controller.ino"):
    target.report_info("CONTROLLER: building")
    tcfl.app_sketch.app_sketch.configure(
        target.testcase, target, ( os.path.abspath(path), ))
    target.shcmd_local(
        "arduino-cli"
        " compile"
        " --fqbn %%(sketch_fqbn)s"
        " %s" % path)
    target.report_info("CONTROLLER: flashing")
    target.images.flash(
        {
            "kernel-arm":
            "%s.arduino.avr.mega.hex" % path
        },
        upload = True)

# need this, since the console goes through network
@tcfl.tc.interconnect("ipv4_addr")
@tcfl.tc.target("pos_capable")
class simple_base(tcfl.tc.tc_c):
    def deploy(self, ic, target):
        deploy_vnc_start(ic, target)

    def start_00(self, ic, target):
        ic.power.on()
        target.shell.prompt = re.compile("TCF-%(tc_hash)s:.*\$ " % target.kws)
        
        # Build and flash the mega
        controller_sw_sync(target, "software-controller/software-controller.ino")

        # Send the UI code, kill an existing one, start it again
        target.report_info("UI: uploading code")
        ui_sw_sync(ic, target, "software-ui")
        target.report_info("UI: restarting on console ssh1")
        # we kill any currently running UI code on the default console
        # ssh0, since we start it in foreground in console ssh1
        target.shell.run("pkill -f -9 ovve_ui.py || true")
        # note we don't use shell.run(), since it expects the prompt
        # to come back and we are running this in the foreground
        target.send(
            "DISPLAY=:0 python3 software-ui/ovve_ui/ovve_ui.py",
            console = "ssh1")
        
        # target's console:ssh1 will print something like
        ## 2020-02-14 04:17:47,135 - INFO - Successfully connected to port '/dev/ttyUSB0'.
        # meaning it connected to the mega
        target.expect(
            "INFO - Successfully connected to port",
            console = "ssh1")

    def teardown_00_check_ssh1(self, ic, target):
        # look for bad stuff in the UI output
        #
        ## 2020-02-14 04:18:09,680 - WARNING - b''
        ## 2020-02-14 04:18:09,681 - WARNING - CRC check failed! rcvd: 0 calc: 65535
        ## 2020-02-14 04:18:09,682 - WARNING - BAD PACKET: {"type": "inpkt", "bytes": "b''"}
        ## 2020-02-14 04:18:11,646 - WARNING - b'\x03\x00  \xfc     \xe0  \xf0\xfb  `   `\xff'
        ## 2020-02-14 04:18:11,647 - WARNING - CRC check failed! rcvd: 0 calc: 11770
        ## 2020-02-14 04:18:11,657 - WARNING - BAD PACKET: {"type": "inpkt", "bytes": "b'\\x03\\x00  \\xfc     \\xe0  \\xf0\\xfb  `   `\\xff'"}
        warnings = False
        errors = False
        for line in target.console.capture_iterator("ssh1"):
            if 'WARNING' in line:
                warnings = True
            if 'ERROR' in line:
                errors = True

        if errors:
            self.report_error("ERRORs found in UI output (%s)"
                              % target.console.capture_filename("ssh1"))
        if warnings:
            self.report_error("WARNINGs found in UI output (%s)"
                              % target.console.capture_filename("ssh1"))
            
    def teardown_50(self):
        tcfl.tl.console_dump_on_failure(self)

