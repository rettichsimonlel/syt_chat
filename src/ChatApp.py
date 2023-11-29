#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import threading
from time import sleep


class ManageApp():
    def __init__(self, appname, on_press):
        self.app = ChatApp(appname, on_press)

        self.form_running = False
        self.STARTING_FORM = self.app.F
        super().__init__()

    def run(self):
        self.form_running = True
        self.app.run()
        self.form_running = False

    def on_start(self):
        self.form_running = True
        return super().on_start()

    def onCleanExit(self):
        self.form_running = False
        return super().onCleanExit()


class ChatApp(npyscreen.NPSApp):
    def __init__(self, appname, on_press) -> None:
        self.appname = appname
        self.to_call = on_press
        self.form_running = False

    def main(self):
        self.F  = npyscreen.Form(name = self.appname)
        self.read_box = self.F.add(npyscreen.MultiLineEdit, 
                              value="Loading ...",
                              editable=False,
                              max_height=-11,
                              rely=1)
        

        self.F.add(npyscreen.MultiLineEdit,
              value=f"{8*'-'}\nMessage:\n{8*'-'}",
              editable=False,
              rely=-13,
              max_height=3)

        # Create a writable Input Box
        self.write_box = self.F.add(npyscreen.MultiLineEdit, 
                               max_height=4,
                               rely=-10)
        
        self.submit = self.F.add(npyscreen.Button,
                                 name="send",
                                 value_changed_callback=self.on_press,
                                 rely=-6)

        self.F.edit()
        del(self)

    def set_read_box(self, text):
        self.read_box.value = text
        self.read_box.update()
        self.F.display()

    def on_press(self, widget):
        if self.write_box.value == "":
            return
        message = ""
        message = self.write_box.value
        self.write_box.value = ""
        self.write_box.update
        self.F.display()
        self.to_call(message)

def update(app):
    sleep(3)
    app.set_read_box("new Text")
    
if __name__ == "__main__":
    App = ChatApp("Hello World")

    app_thread = threading.Thread(target=update, kwargs={"app": App})
    app_thread.start()

    App.main()
    
