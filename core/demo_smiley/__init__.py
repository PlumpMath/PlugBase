dependencies = []
implements = "demo_smiley"

from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

from plugin import configargs, call_on_change

global base
global globalClock
global plugin_manager

global smiley

def init():
    global smiley
    smiley1 = DemoSmiley()
    smiley2 = DemoSmiley()
    print("Smiley obj: "+str(smiley1))
    print("Smiley obj: "+str(smiley2))
    smiley2.model.set_pos(1,0,0)

def destroy():
    global smiley
    smiley.destroy()
    smiley = None

@call_on_change("demo_smiley", "rotation_speed", "set_rotation_speed")
class DemoSmiley(DirectObject):
    @configargs(rotation_speed = ("demo_smiley", "rotation_speed", float))
    def __init__(self, rotation_speed = 0.2):
        DirectObject.__init__(self)
        self.rotation_speed = rotation_speed

        base.camera.set_pos(0, -5, 0)
        base.camera.look_at(0, 0, 0)
    
        self.model = base.loader.loadModel("models/smiley")
        self.model.reparent_to(base.render)
        
        #self.accept("config_value_changed", self.config_value_changed)
        base.taskMgr.add(self.rotate, "rotate_smiley")
    
    def rotate(self, task):
        dt = globalClock.getDt()
        self.model.set_h(self.model, self.rotation_speed * 360.0 * dt)
        return Task.cont
    
    def config_value_changed(self, section, variable, value):
        if (section, variable) == ("demo_smiley", "rotation_speed"):
            self.rotation_speed = value
    
    def set_rotation_speed(self, value):
        print("Setting rotation speed to %d" % (value, ))
        self.rotation_speed = value
    
    def destroy(self):
        # FIXME: Remove model
        pass