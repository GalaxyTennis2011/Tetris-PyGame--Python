import pygame

class Timer:
    def __init__(self, duration, repeated = False, func = None): # 'repeated' used because we want to tell if the timer shall repeat or not; used because we want to be able to call the function multiple times
        self.repeated = repeated # Set the 'repeated' attribute to the value of the 'repeated' parameter; best because we want to be able to call the function multiple times
        self.duration = duration # Set the 'duration' attribute to the value of the 'duration' parameter; best because we want to be able to call the function multiple times
        self.func = func # Set the 'func' attribute to the value of the 'func' parameter

        self.start_time = 0
        self.active = False # Set the 'active' attribute to False; because the timer is not active yet

    def activate(self):
      self.active = True # Set the 'active' attribute to True; because the timer is active now
      self.start_time = pygame.time.get_ticks() # Get the current time in milliseconds; important because we want to know how much time has passed

    def deactivate(self):
      self.active = False # Set the 'active' attribute to False; because the timer is not active anymore
      self.start_time = 0 # Set the 'start_time' attribute to 0; because the timer is not active anymore

    def update(self):
      current_time = pygame.time.get_ticks() # Get the current time in milliseconds; important because we want to know how much time has passed
      if current_time - self.start_time >= self.duration and self.active: # difference between current time and start time is greater than or equal to duration; important because we want to know how much time has passed

        # call a function
        if self.func and self.start_time != 0: # if the function is not None and the start time is not 0
          self.func() # call the function; important because if self.func is not None, we want to call the function 
        
        # reset timer
        self.deactivate() # Deactivate the timer; so that the timer is not active anymore

        # repeat timer
        if self.repeated: # if the timer is repeated
          self.activate() # Activate the timer; important because we want to repeat the timer
import pygame

class Timer:
    def __init__(self, duration, repeated = False, func = None): # 'repeated' used because we want to tell if the timer shall repeat or not; used because we want to be able to call the function multiple times
        self.repeated = repeated # Set the 'repeated' attribute to the value of the 'repeated' parameter; best because we want to be able to call the function multiple times
        self.duration = duration # Set the 'duration' attribute to the value of the 'duration' parameter; best because we want to be able to call the function multiple times
        self.func = func # Set the 'func' attribute to the value of the 'func' parameter

        self.start_time = 0
        self.active = False # Set the 'active' attribute to False; because the timer is not active yet

    def activate(self):
        self.active = True # Set the 'active' attribute to True; because the timer is active now
        self.start_time = pygame.time.get_ticks() # Get the current time in milliseconds; important because we want to know how much time has passed

    def deactivate(self):
        self.active = False # Set the 'active' attribute to False; because the timer is not active anymore
        self.start_time = 0 # Set the 'start_time' attribute to 0; because the timer is not active anymore

    def update(self):
        current_time = pygame.time.get_ticks() # Get the current time in milliseconds; important because we want to know how much time has passed
        if current_time - self.start_time >= self.duration and self.active: # difference between current time and start time is greater than or equal to duration; important because we want to know how much time has passed

            # call a function
            if self.func and self.start_time != 0: # if the function is not None and the start time is not 0
                self.func() # call the function; important because if self.func is not None, we want to call the function 
            
            # reset timer
            self.deactivate() # Deactivate the timer; so that the timer is not active anymore

            # repeat timer
            if self.repeated: # if the timer is repeated
                self.activate() # Activate the timer; important because we want to repeat the timer
