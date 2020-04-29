#! /usr/bin/python
#
# Copyright (c) 2020 Inaky Perez-Gonzalez
#
# SPDX-License-Identifier: Apache-2.0
#
# pylint: disable = missing-docstring

import datetime

import lml

import tcfl.tc
import tcfl.tl
import tcfl.pos

class _test(tcfl.pos.tc_pos_base):
    """
    Provisiong a LifeMech RPI for testing, install the OS, boot into
    it and do the basic setup to be able to run the OVVE UI.

    This does not install the OVVE software
    """

    image_requested = "raspbian"

    def eval(self, ic, target):
        ic.power.on()
        tcfl.tl.sh_export_proxy(ic, target)

        # Some units have the time really broken
        # Don't fret about the HW clock, none in RPI
        target.shell.run("date -us '%s'" % str(datetime.datetime.utcnow()))
        
        target.shell.run("passwd -d pi")
        # base installation seems to have these packages messed up, so
        # wipe them and reinstall as deps to x11vnc
        target.shell.run(
            "dpkg --force-all -r tcl8.6 tk8.6 tk tcl x11vnc")
        target.shell.run(
            "apt install -qy evemu-tools"
            " x11vnc"
            " python3-pyqt5 python3-pyqt5.qtserialport"
            " libqt5serialport5")

        # logout and loging as user @pi
        target.shell.up(user = 'pi')
        tcfl.tl.sh_export_proxy(ic, target)
        target.shell.run(
            "pip3"
            # something is messing up the certificates...
            " --trusted-host www.piwheels.org"
            " --trusted-host files.pythonhosted.org"
            " --trusted-host pypi.org"
            " install -q --user pyqtgraph==0.10.0 crc16")

