"""
A Simple Countdown Timer
"""
import sys
import subprocess
import pyglet
import os

def main():
    # This should start and launch your app!
    print(os.system('pwd'))



        
#!/usr/bin/env python
#
# A fork of Alex Holkner's countdown.py
# Changes Copyright (c) 2020 Hans Kelson
# Hacked together as a quick-fix when no suitable program could be found for a public meeting.
# Bad code quality is all on Hans, and not Alex. The file as I found it was very nice, and I'm afraid I messed it up.
# Original copyright notice is below, as instructed
# ----------------------------------------------------------------------------
# A fork of pyglet's timer.py by Luke Macken
#
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

'''A full-screen minute:second countdown timer.  Leave it in charge of your conference
lighting talks.
Once there is 5 minutes left, the timer goes red.  This limit is easily
adjustable by hacking the source code.
Press spacebar to start, stop and reset the timer.
'''




#COUNTDOWN = int(sys.argv[1])
#style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS, 

display = pyglet.canvas.get_display()
screens = display.get_screens()
window = pyglet.window.Window(fullscreen=True, resizable=True, screen = screens[-1])

KEYBINDS = "\
		Start and stop: Space\n \
		Reset: R\n \
		Toggle Fullscreen: F\n \
		Change timer length: Up/Down Arrows\n \
		Enable/Disable time turning red as 0:30: W\n \
		Enable/Disable AUDIO warning at 0:30: A\n \
		Enable/Disable AUDIO warning when time is up: S\n \
		Test Audio: T\n \
		Dismiss this splash screen: Enter\n \
		Bring back this splash screen: K\n \
		"

class Timer(object):
    def __init__(self):
        self.running = False
        self.show_keybinds()
        window.set_exclusive_mouse(False)
        #self.chime = pyglet.media.load('../Resources/app/chime.wav', streaming=False)
        self.chime = pyglet.media.load('chime.wav', streaming=False)
        self.config = {
            'Audio Warning':30,
            'Visual Warning':30
        }
      
    def show_keybinds(self):
        self.splash = True
        #self.init_timer()
        self.label = pyglet.text.Label(KEYBINDS, multiline=True, font_size=50,
                                       width=window.width,
                                       x=window.width/2, y=window.height/2,
                                       anchor_x='center', anchor_y='center')
        
        
    def init_timer(self):
        #self.chime = pyglet.media.load('chime.wav')
        self.splash = False
        self.timer_countdown = 1
        self.current = ''
        self.warning = True
        self.audiowarning = True
        self.audiowarning2 = True
        self.start = '%s:00' % self.timer_countdown
        self.label = pyglet.text.Label(self.start, font_size=360,
                                       x=window.width/2, y=window.height/2,
                                       anchor_x='center', anchor_y='center')
        self.reset()
        
    def reset(self):
        self.just_reset = True
        self.minutes = self.timer_countdown
        self.seconds = 0
        #self.time = self.timer_countdown * 60
        self.running = False
        self.label.text = '%s:00' % self.timer_countdown
        self.label.color = (255, 255, 255, 255)

    def update(self, dt):
        if self.running:
            #print(dt)
            self.seconds -= round(dt)
            if self.seconds < 0:
                self.seconds = 59
                self.minutes -= 1
            self.label.text = f'{self.minutes}:{self.seconds:02d}'
            self.seconds_remaining = (self.minutes * 60) + self.seconds
            if self.seconds_remaining == self.config['Audio Warning'] and self.audiowarning:
                self.chime.play()
                #print('playing')
            if self.seconds_remaining == self.config['Visual Warning'] and self.warning:
                self.label.color = (100,0,0,255)
            if self.seconds_remaining == 0:
                if self.audiowarning2:
                    print('thing2!!!')
                    self.chime.play()
                self.running = False
                self.label.text = '0:00'
            if self.seconds_remaining < 0:
                self.reset()

    def update_old(self, dt):
        if self.running:
            m, s = divmod(self.time, 60)
            self.time -= dt
            self.label.text = '%02d:%02d' % (m, s)
            s = round(s)
            #print(f'{m},{s}')
            if m < 1 and s == 30 and self.audiowarning:
                #print('thing')
                self.chime.play()
            if m < 1 and s < 30 and self.warning:
                self.label.color = (180, 0, 0, 255)
            if m < 0:
                self.running = False
                self.label.text = '0:00'
    
    def displayCurrent(self, dt):
        self.label.text = self.current

@window.event
def on_key_press(symbol, modifiers):
    #dismiss splash screen and inhibit other buttons if splash is up, to avoid breakage
    if symbol == pyglet.window.key.ENTER and timer.splash:
        timer.init_timer()
    elif timer.splash:
        pass
    #start and stop
    elif symbol == pyglet.window.key.SPACE:
        if timer.running:
            timer.running = False
        else:
            timer.running = True

    elif symbol == pyglet.window.key.K:
        timer.show_keybinds()
    #increment timer duration
    elif symbol == pyglet.window.key.UP:
        if timer.running:
            pass
        else:
            timer.timer_countdown += 1
            timer.reset()
    #decrement timer duration
    elif symbol == pyglet.window.key.DOWN:
        if timer.running:
            pass
        else:
            timer.timer_countdown -= 1
            timer.reset()
        #timer.chime.play()
    #reset timer        
    elif symbol == pyglet.window.key.R:
        timer.reset()
    #enter warning setting mode
    elif symbol == pyglet.window.key.W:
        timer.current = timer.label.text
        if timer.warning:
            timer.warning = False
            timer.label.text = 'RED OFF'
            pyglet.clock.schedule_once(timer.displayCurrent, .5)
        else:
            timer.warning = True
            timer.label.text = 'RED ON'
            pyglet.clock.schedule_once(timer.displayCurrent, .5)
    #enter *audio* warning setting mode
    elif symbol == pyglet.window.key.A:
        timer.current = timer.label.text
        if timer.audiowarning:
            timer.audiowarning = False
            timer.label.text = 'A OFF'
            pyglet.clock.schedule_once(timer.displayCurrent, .5)
        else:
            timer.audiowarning = True
            timer.label.text = 'A ON'
            pyglet.clock.schedule_once(timer.displayCurrent, .5)
    elif symbol == pyglet.window.key.S:
        timer.current = timer.label.text
        if timer.audiowarning2:
            timer.audiowarning2 = False
            timer.label.text = 'A2 OFF'
            pyglet.clock.schedule_once(timer.displayCurrent, .5)
        else:
            timer.audiowarning2 = True
            timer.label.text = 'A2 ON'
            pyglet.clock.schedule_once(timer.displayCurrent, .5)
    elif symbol == pyglet.window.key.D:
        timer.chime.play()
    elif symbol == pyglet.window.key.F:
        if window.fullscreen:
            window.set_fullscreen(False)
        else:
            window.set_fullscreen(True)
    elif symbol == pyglet.window.key.M:
        #timer.window.screen = 0
        window.screen = 0
        timer.reset()
    elif symbol == pyglet.window.key.T:
        timer.chime.play()
    #quit       
    elif symbol == pyglet.window.key.ESCAPE:
        window.close()

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    #print(f'x{x},y{y},dx{dx},dy{dy},buttons{buttons},modifiers{modifiers}')
    if not window.fullscreen:
        #print(modifiers)
        if modifiers == 2:
            #print(modifiers)
            win_x, win_y = window.get_location()
            #print(f'{win_x},{win_y}')
            win_x += dx 
            win_y -= dy
            #if dx or dy > 2:
            window.set_location(win_x, win_y)
        if modifiers == 1:
            win_w, win_h = window.get_size()
            win_w += dx
            win_h -= dy
            window.set_size(win_w, win_h)
    
    
@window.event
def on_resize(width, height):
    if not timer.splash:
        timer.label.font_size = height / 2.5
        timer.label.x=window.width//2
        timer.label.y=window.height//2

@window.event
def on_draw():
    window.clear()
    timer.label.draw()


timer = Timer()
pyglet.clock.schedule_interval(timer.update, 1)
pyglet.app.run()
