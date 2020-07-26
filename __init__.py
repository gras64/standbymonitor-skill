from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message
from os.path import os, abspath, dirname
import subprocess

class Standbymonitor(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):
        self.settings["auto"] = self.settings.get('auto', True)
        self.settings["monitor"] = self.settings.get('monitor', 1)
        self.settings["timer"] = self.settings.get('timer', 60)
        if self.settings["auto"]:
            self.add_event('enclosure.mouth.reset',
                        self.handle_standby)
            self.add_event('mycroft.speech.recognition.unknown',
                        self.ex_standby)
            self.add_event('recognizer_loop:wakeword',
                        self.ex_wakeup)
            self.ex_standby()
        self.log.info("set auto mode to: "+str(self.settings["auto"]))

    def handle_standby(self):
        time = self.settings["timer"]
        self.log.info("add standby timer")
        self.schedule_event(self.ex_standby, time, name='standby')

    def ex_standby(self):
        self.log.info("handle standby")
        if int(self.settings["monitor"]) == 1:
            self.log.info(self.settings["monitor"])
            subprocess.call("/usr/bin/xset dpms force off",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.settings["monitor"]) == 2:
            subprocess.call("echo 1 > /sys/class/backlight/rpi_backlight/bl_power",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.settings["monitor"]) == 3:
            subprocess.call("usr/sbin/i2cset  -y $BUS 0x1b 0x16 0x00 0x00 0x00 0x00 i",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.settings["monitor"]) == 4:
            subprocess.call("tvservice --off",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.settings["monitor"]) == 5:
            subprocess.call("vcgencmd display_power 0",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.settings["monitor"]) == 6:
            subprocess.call("echo 'standby 0' | cec-client -s -d 1",
                                    preexec_fn=os.setsid, shell=True)
        
    def ex_wakeup(self):
        try:
            self.cancel_scheduled_event("standby")
        except:
            pass
        self.log.info("handle wakeup")
        if int(self.settings["monitor"]) == 1:
            subprocess.call("/usr/bin/xset dpms force on",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.settings["monitor"]) == 2:
            subprocess.call("echo 0 > /sys/class/backlight/rpi_backlight/bl_power",
                                    preexec_fn=os.setsid, shell=True)
            subprocess.call("echo '255' > /sys/class/backlight/rpi_backlight/brightness",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.settings["monitor"]) == 3:
            subprocess.call("/usr/sbin/i2cset -y $BUS 0x1b 0x16 0x00 0x00 0x00 0x07 i",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.settings["monitor"]) == 4:
            subprocess.call("tvservice --preferred",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.settings["monitor"]) == 5:
            subprocess.call("vcgencmd display_power 1",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.settings["monitor"]) == 6:
            subprocess.call("echo 'on 0' | cec-client -s -d 1",
                                    preexec_fn=os.setsid, shell=True)

    @intent_file_handler('standbymonitor.intent')
    def handle_standby_monitor(self, message):
        self.remove_event('recognizer_loop:wakeword')
        self.ex_standby()
        self.speak_dialog("standbymonitor")

    @intent_file_handler('wakeupmonitor.intent')
    def handle_wakeup_monitor(self, message):
        self.remove_event('recognizer_loop:audio_output_end')
        self.ex_wakeup()
        self.speak_dialog("wakeupmonitor")

    @intent_file_handler('automonitor.intent')
    def handle_auto_monitor(self, message):
        self.settings["auto"] = True
        self.add_event('recognizer_loop:audio_output_end',
                        self.handle_standby)
        self.add_event('recognizer_loop:wakeword',
                        self.ex_wakeup)
        self.speak_dialog("automonitor")

def create_skill():
    return Standbymonitor()