#! /usr/bin/python
#
# Copyright (c) 2020 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#
# pylint: disable = missing-docstring
"""
"""
import re

import tcfl.tc

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
    vnc_start(target)


def ui_sw_sync(ic, target):
    # Deploy the software tree to the RPI
    port = target.tunnel.add(22)
    hostname = target.rtb.parsed_url.hostname
    target.testcase.shcmd_local(
        "rsync -e 'ssh -p %s' -a software-ui.git root@%s:/home/pi"
        % (port, hostname))

# need this, since the console goes through network
@tcfl.tc.interconnect("ipv4_addr")
@tcfl.tc.target("pos_capable")
class simple_base(tcfl.tc.tc_c):
    def deploy(self, ic, target):
        deploy_vnc_start(ic, target)

    def start_00(self, ic, target):
        ic.power.on()
        target.shell.prompt = re.compile("TCF-%(tc_hash)s:.*\$ " % target.kws)

        # Deploy the software tree to the RPI
        port = target.tunnel.add(22)
        hostname = target.rtb.parsed_url.hostname
        self.shcmd_local(
            "rsync -e 'ssh -p %s' -a software-ui.git root@%s:/home/pi"
            % (port, hostname))
