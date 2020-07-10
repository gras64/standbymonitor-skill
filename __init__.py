from mycroft import MycroftSkill, intent_file_handler


class Standbymonitor(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('standbymonitor.intent')
    def handle_standbymonitor(self, message):
        self.speak_dialog('standbymonitor')


def create_skill():
    return Standbymonitor()

