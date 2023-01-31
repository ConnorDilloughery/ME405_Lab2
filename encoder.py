import pyb

class Encoder:
    ''' @brief This class sets up an encoder using the given parameters during initilization. Allows for reading operations annd zero reset

        '''
    def __init__(self,PinIn1, PinIn2, timer):
    ''' @brief This initializes the encoder with the given parameters
        @self A place holder for objects that will eventually be orientated
        @PinIn1 Corresponds to the first timer channel pin being used
        @PinIn2 Correponds to the second timer channel pin being used
        @timer Corresponds to the timer sharesd between PinIn1 and PinIn2
    '''
        ##Initializing count. variable for the encoder. This contains the encoder count
        self.Count=0
        ##Initilizing the Previous variable for the encoder. Used to figure out change in position
        self.Previous =0
        ##Setting up the first timer pin
        self.Pin1 = pyb.Pin(PinIn1, pyb.Pin.IN)
        ##Setting up the second timer pin
        self.Pin2 = pyb.Pin(PinIn2, pyb.Pin.IN)
        ##Setting up the timer for pin 1
        self.ENC_Timer1= pyb.Timer(timer, prescaler=0, period =0xFFFF)
        ##Setting up the timer for pin 2
        self.ENC_Timer2= pyb.Timer(timer, prescaler=0, period =0xFFFF)
        ##Setting up the channel and timer to encoder count
        self.ENC_CHANNEL1=self.ENC_Timer1.channel(1, pyb.Timer.ENC_AB, pin=self.Pin1)
        ##Setting up the channel and timer to encoder count
        self.ENC_CHANNEL2=self.ENC_Timer1.channel(2, pyb.Timer.ENC_AB, pin=self.Pin2)
    
    
    def read(self):
    '''@brief This returns the overall timer position after finding it through set conditions
       @self A place holder for objects that will eventually be orientated
       @return This returns the current position of the motor 
       '''
        ##Reads the current value for the encoder count
        self.readd= self.ENC_Timer1.counter()
        ##Calculates the change with the previous
        self.delta= self.readd-self.Previous
        ##Determining if the delta change was positive
        if self.delta> 0:
         ##If positive, the change is compared to compared to (AR +1)/2
         if self.delta> (0xFFFF+1)/2:
          ##If a reset is true, subract the AR + 1
          self.delta -= (0xFFFF+1)
          ##Add the result to count
          self.Count+= self.delta
         ##Determining if the change was less than (AR+1)/2
         elif self.delta<(0xFFFF+1)/2:
          ##If true, add the delta
          self.Count+= self.delta
        ##Determining if the change was negative
        if self.delta< 0:
         ##Determining if delta is less than -(AR+1)/2
         if self.delta< -(0xFFFF+1)/2:
          ##If true, add AR+1 to delta
          self.delta += (0xFFFF+1)
          ##Subtracting delta from Count
          self.Count-= self.delta
         ##Determining if delta was greater than -(AR+1)/2
         elif self.delta>-(0xFFFF+1)/2:
          ##If true, add delta to Count
          self.Count+= self.delta
                
        ##Changing the Previous value to match the current read value
        self.Previous= self.readd
          
        
        return self.Count

    
    def zero(self):
    '''@brief This command will reset the coutn to 0, resetting the home position
       @self A place holder for objects that will eventually be orientated
     '''
    ##Sets Count to 0
    self.Count=0
     

