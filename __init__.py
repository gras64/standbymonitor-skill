from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message
from mycroft.configuration import Configuration
from os.path import os, abspath, dirname
import subprocess

class Standbymonitor(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):
        self.settings["auto"] = self.settings.get('auto', True)
        self.monitor = self.settings.get('monitor', 0)
        self.settings["timer"] = self.settings.get('timer', 60)
        if self.settings["auto"]:
            self.add_event('enclosure.mouth.reset',
                        self.handle_standby)
            self.add_event('mycroft.speech.recognition.unknown',
                        self.ex_standby)
            self.add_event('recognizer_loop:wakeword',
                        self.ex_wakeup)
            self.ex_standby()
        config = Configuration.get()
        platform = config.get('enclosure').get('platform')
        if int(self.monitor) == 0:
            if platform == "mycroft_mark_1":
                self.monitor = 7
            elif platform == "mycroft_mark_2":
                self.monitor = 1
            elif os.path.isfile("/sys/class/backlight/rpi_backlight/bl_power"):
                self.monitor = 2
            elif os.path.isfile("/dev/i2c-0"):
                self.monitor = 3
            else:
                self.monitor = 1
            self.log.info("activate auto monitor and select: "+str(self.monitor))
        self.log.info("set auto mode to: "+str(self.settings["auto"]))

    def handle_standby(self):
        time = self.settings["timer"]
        self.log.info("add standby timer")
        self.schedule_event(self.ex_standby, time, name='standby')

    def ex_standby(self):
        self.log.info("handle standby")
        if int(self.monitor) == 1:
            subprocess.call("/usr/bin/xset dpms force off",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 2:
            subprocess.call("echo 1 > /sys/class/backlight/rpi_backlight/bl_power",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 3:
            subprocess.call("usr/sbin/i2cset  -y $BUS 0x1b 0x16 0x00 0x00 0x00 0x00 i",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 4:
            subprocess.call("tvservice --off",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 5:
            subprocess.call("vcgencmd display_power 0",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 6:
            subprocess.call("echo 'standby 0' | cec-client -s -d 1",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 7:
            self.bus.emit(Message('mycroft.eyes.off'))
            self.bus.emit(Message('mycroft.mouth.reset'))
        
    def ex_wakeup(self):
        try:
            self.cancel_scheduled_event("standby")
        except:
            pass
        self.log.info("handle wakeup")
        if int(self.monitor) == 1:
            subprocess.call("/usr/bin/xset dpms force on",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 2:
            subprocess.call("echo 0 > /sys/class/backlight/rpi_backlight/bl_power",
                                    preexec_fn=os.setsid, shell=True)
            subprocess.call("echo '255' > /sys/class/backlight/rpi_backlight/brightness",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 3:
            subprocess.call("/usr/sbin/i2cset -y $BUS 0x1b 0x16 0x00 0x00 0x00 0x07 i",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 4:
            subprocess.call("tvservice --preferred",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 5:
            subprocess.call("vcgencmd display_power 1",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 6:
            subprocess.call("echo 'on 0' | cec-client -s -d 1",
                                    preexec_fn=os.setsid, shell=True)
        elif int(self.monitor) == 7:
            self.bus.emit(Message('mycroft.eyes.default'))

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