Hi!

Accessing the automation server
===============================

FIXME

Each target is connected to an individual network (the network is
relatively fake, in the wire they are all the same).


Running it
==========


.. _preconditions:

For the system to be able to control the boot process of the RPI, the
SD-CARD must lack the */boot* partition; this makes the boot firmware
attempt a network boot.

Checkout this repository
------------------------

::

   $ git clone https://github.com/inakypg/lifemech-test.git test.git
   $ git clone -b developer https://github.com/OVVE/software-ui.git software-ui.git
   $ git clone -b developer https://github.com/OVVE/software-controller.git software-controller.git
   
Flashing a unit from scratch
----------------------------

(the units in the server all have an empty */boot* partition)

Run::
  
  $ tcf run -vvvt "nwb or rpi3-02b" test_lm_prepare.py

This:

- boots the unit in provisioning mode and flashes the full Raspbian
  image 2020-04-13, wiping anything else

  (note it doesn't flash /boot as noted :ref:`here <preconditions>`).

- reboots into the OS itself (the full Raspbian image)
  
- sets the date, deletes @pi's password and installs the packages we
  need to run the OVVE UI.

Takes about 10minutes::
  
  $ tcf.git/tcf --trace run -vvvt "nwb or rpi3-02b" test.git/test_lm_prepare.py
  INFO2/	toplevel @local [+0.5s]: scanning for test cases
  INFO1/s5nhst	test.git/test_lm_prepare.py @5qcw-ezhc [+0.2s]: will run on target group 'ic=lifemech01/nwb target=lifemech01/rpi3-02b:armhf' (PID 6261 / TID 7f3f27c6c580)
  INFO2/s5nhstD	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/nwb [+0.6s]: powered on
  DATA2/s5nhstDPOS	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+109.8s]: TCF persistant cache usage::lifemech01/rpi3-02b:/dev/mmcblk0p2::0
  INFO1/s5nhstDPOS	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+110.1s]: POS: rsyncing raspbian:full:2020-02-13::armhf from 192.168.98.1::images to /dev/mmcblk0p2
  DATA2/s5nhstDPOS	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+530.7s]: Deployment stats image raspbian:full:2020-02-13::armhf::image rsync to lifemech01/rpi3-02b (s)::420.04
  PASS2/s5nhstD	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+534.9s]: deployed raspbian:full:2020-02-13::armhf
  PASS2/s5nhst	test.git/test_lm_prepare.py @5qcw-ezhc [+535.0s]: deploy passed

at this point (+9min), the SD-card is flashed and the automation is
rebooting into the OS itself::
  
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/nwb [+535.1s]: powered on
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+535.1s]: POS: setting target not to PXE boot Provisioning OS
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+540.8s]: power cycled
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+582.8s]: ssh0: wrote 29B (export PS1="TCF-s5nhst:$PS1"<NL>) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+583.2s]: ssh0: wrote 40B (test ! -z "$BASH" && set +o vi +o emacs<NL>) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+583.5s]: ssh0: wrote 33B (trap 'echo ERROR''-IN-SHELL' ERR<NL>) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/nwb [+583.8s]: powered on
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+583.8s]: ssh0: wrote 276B (export  http_proxy=http://192.168.98.1:8888 HTTP_P...) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+584.2s]: ssh0: wrote 38B (date -us '2020-04-26 07:10:07.444357'<NL>) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+584.5s]: ssh0: wrote 13B (passwd -d pi<NL>) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+585.4s]: ssh0: wrote 47B (dpkg --force-all -r tcl8.6 tk8.6 tk tcl x11vnc<NL>) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+586.6s]: ssh0: wrote 94B (apt install -qy evemu-tools x11vnc python3-pyqt5 p...) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+640.5s]: ssh0: wrote 29B (export PS1="TCF-s5nhst:$PS1"<NL>) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+640.8s]: ssh0: wrote 40B (test ! -z "$BASH" && set +o vi +o emacs<NL>) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+641.1s]: ssh0: wrote 33B (trap 'echo ERROR''-IN-SHELL' ERR<NL>) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+641.4s]: ssh0: wrote 276B (export  http_proxy=http://192.168.98.1:8888 HTTP_P...) to console
  INFO2/s5nhstE#1	test.git/test_lm_prepare.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+641.8s]: ssh0: wrote 141B (pip3 --trusted-host www.piwheels.org --trusted-hos...) to console
  PASS1/s5nhst	test.git/test_lm_prepare.py @5qcw-ezhc [+651.7s]: evaluation passed 
  PASS0/	toplevel @local [+652.8s]: 1 tests (1 passed, 0 error, 0 failed, 0 blocked, 0 skipped, in 0:10:51.901124) - passed 

the system has now been flashed.

Test the start and stop button
------------------------------

::

  $ tcf run -vv test_lm_start_stop
  INFO2/	toplevel @local [+0.5s]: scanning for test cases
  INFO1/id2eez	test.git/test_lm_start_stop.py @5qcw-ezhc [+0.2s]: will run on target group 'ic=lifemech01/nwb target=lifemech01/rpi3-02b:armhf' (PID 13478 / TID 7f8471eee580)
  INFO2/id2eezD	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/nwb [+0.5s]: powered on
  INFO2/id2eezD	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+0.5s]: POS: setting target not to PXE boot Provisioning OS
  INFO2/id2eezD	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+8.2s]: power cycled
  ...
  
target is being setup: input injection, VNC server started::

  ...
  INFO2/id2eezD	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+70.9s]: ssh0: wrote 182B (if ! pgrep x11vnc; then  rm -f vnc.log; sudo -u pi...) to console
  PASS2/id2eez	test.git/test_lm_start_stop.py @5qcw-ezhc [+71.3s]: deploy passed 
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/nwb [+71.4s]: powered on
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+71.4s]: tcp tunnel added from lifemech01.ra.intel.com:40098 to 192.168.98.2:22

  
  PASS2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc [+72.0s]: eval passed: 'rsync -e 'ssh -p 40098' -a software-ui.git root@lifemech01.ra.intel.com:/home/pi' @test.git/lml.py:42
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+72.0s]: ssh0: wrote 18B (export DISPLAY=:0<NL>) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+73.3s]: ssh0: wrote 31B (pkill -f -9 ovve_ui.py || true<NL>) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+73.6s]: ssh0: wrote 60B (python3 software-ui.git/ovve_ui/ovve_ui.py >& ovve...) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+81.1s]: 60.OVVE_starts/canary-resp-rate_png: detected one match
  libpng warning: iCCP: CRC error
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+81.3s]: 60.OVVE_starts/canary-TV-Exp_png: detected one match
  libpng warning: iCCP: CRC error
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+81.5s]: 60.OVVE_starts/canary-TV-insp_png: detected one match
  libpng warning: iCCP: CRC error
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+81.9s]: 60.OVVE_starts/canary-bottom-right_png: detected one match
  libpng warning: iCCP: CRC error
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+82.4s]: 60.OVVE_starts/canary-button-start_png: detected one match
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+82.4s]: mouse default_mouse: moving to (0.749375, 0.0854166666667)
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+82.5s]: ssh0: wrote 80B (cat > /tmp/evemu.data<NL>event0 EV_ABS ABS_X 49111<NL>ev...) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+82.8s]: ssh0: wrote 38B (cat /tmp/evemu.data > /tmp/evemu.fifo<NL>) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+83.1s]: mouse default_mouse: clicking at (0.749375, 0.0854166666667)
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+83.2s]: ssh0: wrote 91B (cat > /tmp/evemu.data<NL>event0 EV_KEY BTN_LEFT 1 SYN...) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+83.5s]: ssh0: wrote 38B (cat /tmp/evemu.data > /tmp/evemu.fifo<NL>) to console
  libpng warning: iCCP: CRC error
  libpng warning: iCCP: CRC error
  libpng warning: iCCP: CRC error
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+89.8s]: 65.start_button_changes_to_stop_after_pressing_start/canary-button-stop_png: detected 2 matches
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+92.8s]: mouse default_mouse: moving to (0.755, 0.102083333333)
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+92.8s]: ssh0: wrote 80B (cat > /tmp/evemu.data<NL>event0 EV_ABS ABS_X 49479<NL>ev...) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+93.2s]: ssh0: wrote 38B (cat /tmp/evemu.data > /tmp/evemu.fifo<NL>) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+93.5s]: mouse default_mouse: clicking at (0.755, 0.102083333333)
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+93.5s]: ssh0: wrote 93B (cat > /tmp/evemu.data<NL>event0 EV_KEY BTN_LEFT 1 SYN...) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+93.9s]: ssh0: wrote 38B (cat /tmp/evemu.data > /tmp/evemu.fifo<NL>) to console
  libpng warning: iCCP: CRC error
  libpng warning: iCCP: CRC error
  libpng warning: iCCP: CRC error
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+95.3s]: 70.warning_dialog_comes_up_when_pressing_stop/canary-confirm-stop_png: detected one match
  libpng warning: iCCP: CRC error
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+98.6s]: 70.warning_dialog_comes_up_when_pressing_stop/canary-confirm-stop-confirm_png: detected one match
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+98.6s]: mouse default_mouse: moving to (0.698125, 0.703125)
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+98.6s]: ssh0: wrote 81B (cat > /tmp/evemu.data<NL>event0 EV_ABS ABS_X 45752<NL>ev...) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+99.0s]: ssh0: wrote 38B (cat /tmp/evemu.data > /tmp/evemu.fifo<NL>) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+99.3s]: mouse default_mouse: clicking at (0.698125, 0.703125)
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+99.4s]: ssh0: wrote 93B (cat > /tmp/evemu.data<NL>event0 EV_KEY BTN_LEFT 1 SYN...) to console
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+99.7s]: ssh0: wrote 38B (cat /tmp/evemu.data > /tmp/evemu.fifo<NL>) to console
  libpng warning: iCCP: CRC error
  libpng warning: iCCP: CRC error
  INFO2/id2eezE#1	test.git/test_lm_start_stop.py @5qcw-ezhc|lifemech01/rpi3-02b/arm [+102.0s]: 75.start_button_shows_up_again_after_confiriming_stop/canary-button-start_png: detected one match
  PASS1/id2eez	test.git/test_lm_start_stop.py @5qcw-ezhc [+102.0s]: evaluation passed 
  PASS0/	toplevel @local [+103.2s]: 1 tests (1 passed, 0 error, 0 failed, 0 blocked, 0 skipped, in 0:01:42.151782) - passed 
  
  
    A few ways to run it

    1. Let TCF find a target, allocate it, power cycle and run the
       test for you from power cycle:: 

    2. You allocate the target and keep it allocated because you are
       developing scripts or running them manually; allocate::

         $ tcf acquire nwb rpi3-02b --hold
         allocation ID CcbPJw: [+0.4s] allocated: nwb rpi3-02b
         allocation ID CcbPJw: [+6586.9s] keeping alive during state 'active'

       note *CcbPJw*, your allocation ID; in another terminal::

         $ tcf -a CcbPJw run -vv test_lm_start_stop

       note that you don't have to do the power cycle all the time; add *-D* to
       skip the *deploy* phase if you know the target is power cycled
       and setup (VNC started, etc); this is useful when you are
       developing a script in a loop or running multiple of them.



Interactive use
===============

Acquire for exclusive use::

  $ tcf acquire nwb rpi3-02b --hold

in another console::

  $ tcf power-cycle nwb rpi3-02b
  $ tcf console-enable rpi3-02b
  $ tcf console-write -i rpi3-02b



Seeing the screen, VNC
----------------------

The scripts will start *x11vnc* so we can see and manipulate the
screen remotely (FIXME: future images start x11vnc directly?). You
need to create a tunnel to the target::

  $ tcf tunnel-add rpi3-02b 5900
  lifemech01.ra.intel.com:34667

now point your VNC client to that *hostname* and *TCF port* (note that
is a TCP port, not a VNC port--VNC ports usually are called :0, :1, :2
which correspond to ports :5900, :5901, :5902...)
