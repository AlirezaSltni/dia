import random
import time
import threading
import pygame
import sys
import math
from random import randint, choice

clock = pygame.time.Clock()
nn=0
sd=60
stl= 260-sd
str= 340+sd
stu=260-sd
std=340+sd

cd=15
stlc= 260-cd
strc= 340+cd
stuc=260-cd
stdc=340+cd


v=1
int_stop=0

speeds = {'car':4*v, 'bus':3.2*v, 'truck':1.2*v, 'bike':1.5*v}  # average speeds of vehicles

# Coordinates of vehicles' start
x = {'right':[0,0,0], 'down':[264,278,290], 'left':[600,600,600], 'up':[304,316,330]}    
y = {'right':[304,316,330], 'down':[0,0,0], 'left':[264,278,290], 'up':[600,600,600]}

vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}
ArrivalVehicles = {'right': {0:[], 1:[], 2:[]}, 'down': {0:[], 1:[], 2:[]}, 'left': {0:[], 1:[], 2:[]}, 'up': {0:[], 1:[], 2:[]}}
OutboundVehicles = {'right': {0:[], 1:[], 2:[]}, 'down': {0:[], 1:[], 2:[]}, 'left': {0:[], 1:[], 2:[]}, 'up': {0:[], 1:[], 2:[]}}
vehicle_stop = {'right': 0, 'down': 0, 'left': 0, 'up': 0}
print(vehicle_stop['right'])
vehicleTypes = {0:'car', 1:'car', 2:'car', 3:'bus'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

# Coordinates of stop lines
stopLines = {'right': stl, 'down': stu, 'left': str, 'up': std}
crossLines = {'right': stlc, 'down': stuc, 'left': strc, 'up': stdc}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
# stops = {'right': [580,580,580], 'down': [320,320,320], 'left': [810,810,810], 'up': [545,545,545]}

# Gap between vehicles
stoppingGap = 16    # stopping gap
movingGap = 40   # moving gap

pygame.init()
simulation = pygame.sprite.Group()

        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.stopline=stopLines[direction]
        self.crossline=crossLines[direction]
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        vehicles[direction][lane].append(1)
        ArrivalVehicles[direction][lane].append(1)
        self.index = len(ArrivalVehicles[direction][lane]) -1
        self.first= 0
        vehicles[direction][lane][self.index]=self
        self.stop=0
        self.maxspeed=randint(3,4)
        self.inflow=0
        self.outflow=0
        

        

               
 
        #rectangle and image

        if direction_number==0 or direction_number==2:
            car=pygame.image.load('images/car.png').convert_alpha()
        else:
            car=pygame.image.load('images/car2.png').convert_alpha()
        car= pygame.transform.scale(car, (6,15))
        self.image = pygame.transform.rotate(car,(3-direction_number)*90)

        #stopping rectangle
        carstop= pygame.transform.scale(car, (6,115)) 
        self.image1 = pygame.transform.rotate(carstop,(3-direction_number)*90)
        #rectangles
#stooping
        if direction=='right':
            self.rect = self.image1.get_rect(topleft = (self.x,self.y))
        elif direction=='down':
            self.rect = self.image1.get_rect(topleft = (self.x,self.y))
        elif direction=='left':
            self.rect = self.image1.get_rect(topright = (self.x,self.y))
        elif direction=='up':
            self.rect = self.image1.get_rect(bottomleft = (self.x,self.y)) 
#fit
        if direction=='right':
            self.rectfit = self.image.get_rect(topleft = self.rect.topleft)
        elif direction=='down':
            self.rectfit = self.image.get_rect(topleft = self.rect.topleft)
        elif direction=='left':
            self.rectfit = self.image.get_rect(topright = self.rect.topright)
        elif direction=='up':
            self.rectfit = self.image.get_rect(bottomleft = self.rect.bottomleft) 

     



      
            
        # Set new starting and stopping coordinate
        # if(direction=='right'):
        #     temp = self.image.get_rect().width + stoppingGap    
        #     x[direction][lane] -= temp
        # elif(direction=='left'):
        #     temp = self.image.get_rect().width + stoppingGap
        #     x[direction][lane] += temp
        # elif(direction=='down'):
        #     temp = self.image.get_rect().height + stoppingGap
        #     y[direction][lane] -= temp
        # elif(direction=='up'):
        #     temp = self.image.get_rect().height + stoppingGap
        #     y[direction][lane] += temp
        # simulation.add(self)
        if(direction=='right'):
            temp = randint(1,40)   
            x[direction][lane] -= temp
        elif(direction=='left'):
            temp = randint(1,40)
            x[direction][lane] += temp
        elif(direction=='down'):
            temp = randint(1,40)
            y[direction][lane] -= temp
        elif(direction=='up'):
            temp = randint(1,40)
            y[direction][lane] += temp
        simulation.add(self)



    def acc(self):
        #if self.speed<=3: self.speed+=1
        #self.speed=4
        #self.ac = max( self.ac-self.ac/4 , 0)
        self.speed= min(self.speed + 1/(3*max(self.speed,1)), self.maxspeed)





    def dec(self):
        #if self.speed>=2: self.speed -= 2
        #self.speed=0
        #self.dc = min ( self.dc+self.dc/4 , 1)
        self.speed = max(self.speed - 1/(max(self.speed,0.1)) , 0)



    def FrontCheck(self):

        
        if(self.direction=='right'):
            if(self.crossed==0 and self.rectfit.right>crossLines[self.direction]):   # if the image has crossed stop line now
                self.crossed = 1
            if self.index==self.first or self.rectfit.right<(vehicles[self.direction][self.lane][self.index-1].rectfit.left - movingGap): 
                self.stop=0
            else:  
                self.stop=1
                if self.maxspeed > vehicles[self.direction][self.lane][self.index-1].maxspeed:
                    self.maxspeed=vehicles[self.direction][self.lane][self.index-1].maxspeed


        elif(self.direction=='down'):
            if(self.crossed==0 and self.rectfit.bottom>crossLines[self.direction]):
                self.crossed = 1
            if self.index==self.first or self.rectfit.bottom<(vehicles[self.direction][self.lane][self.index-1].rectfit.top - movingGap):            
                self.stop=0
            else:  
                self.stop=1
                if self.maxspeed > vehicles[self.direction][self.lane][self.index-1].maxspeed:
                    self.maxspeed=vehicles[self.direction][self.lane][self.index-1].maxspeed


        elif(self.direction=='left'):
            if(self.crossed==0 and self.rectfit.left<crossLines[self.direction]):
                self.crossed = 1
            if self.index==self.first or self.rectfit.left>(vehicles[self.direction][self.lane][self.index-1].rectfit.right + movingGap):                
                self.stop=0
            else: 
                self.stop=1
                if self.maxspeed > vehicles[self.direction][self.lane][self.index-1].maxspeed:
                    self.maxspeed=vehicles[self.direction][self.lane][self.index-1].maxspeed


        elif(self.direction=='up'):
            if(self.crossed==0 and self.rectfit.top<crossLines[self.direction]):
                self.crossed = 1
            
            if self.index==self.first or self.rectfit.top>(vehicles[self.direction][self.lane][self.index-1].rectfit.bottom  + movingGap):                                
                self.stop=0
            else: 
                self.stop=1
                if self.maxspeed > vehicles[self.direction][self.lane][self.index-1].maxspeed:
                    self.maxspeed=vehicles[self.direction][self.lane][self.index-1].maxspeed



    def move(self):
        

        
        if(self.direction=='right'):
       
            self.x += self.speed
            self.rect.x += self.speed 
            self.rectfit.x += self.speed 
            

        elif(self.direction=='down'):

            self.y += self.speed
            self.rect.y += self.speed
            self.rectfit.y += self.speed

        elif(self.direction=='left'):

            self.x -= self.speed
            self.rect.x -= self.speed 
            self.rectfit.x -= self.speed 

        elif(self.direction=='up'):

            self.y -= self.speed
            self.rect.y -= self.speed
            self.rectfit.y -= self.speed

        self.destroy()



    def destroy(self):
        if(self.direction=='right'):
            if self.rect.x > 700:
                OutboundVehicles[self.direction][self.lane].append(1) 

                self.kill()
        elif(self.direction=='left'):
            if self.rect.x < -200: 
                OutboundVehicles[self.direction][self.lane].append(1)
                self.kill()
        elif(self.direction=='down'):
            if self.rect.y > 700: 
                OutboundVehicles[self.direction][self.lane].append(1)
                self.kill()
        elif(self.direction=='up'):
            if self.rect.y < -200: 
                OutboundVehicles[self.direction][self.lane].append(1)
                self.kill()
        self.first= len(OutboundVehicles[self.direction][self.lane])
        self.outflow=0
        self.outflowtot=0
        for l in range (0,2):
            self.outflow += len(OutboundVehicles[self.direction][l])
            #print (self.outflow)
            for d in ['right', 'down', 'left', 'up']:
                self.outflowtot += len(OutboundVehicles[d][l])
                #print (self.outflowtot)



    

# Generating vehicles in the simulation
def generateVehicles():
    while(True):
        vehicle_type = random.randint(0,3)
        lane_number = random.randint(0,2)
        temp = random.randint(0,99)
        direction_number = 0
        dist = [25,50,75,100]
        if(temp<dist[0]):
            direction_number = 0
        elif(temp<dist[1]):
            direction_number = 1
        elif(temp<dist[2]):
            direction_number = 2
        elif(temp<dist[3]):
            direction_number = 3
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
        time.sleep(0.6)

class Main:

    
    
    # Colours 
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize 
    screenWidth = 600
    screenHeight = 600
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/screenshot.png')
    test_font= pygame.font.Font('font/Pixeltype.ttf', 30)
    outflow_font= pygame.font.Font(None, 22)
    MAIN_FONT = pygame.font.SysFont("comicsans", 20)
    V_font= pygame.font.Font(None, 15)
    text_surf = test_font.render('Intersection',False, 'Black')
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")


    thread = threading.Thread(name="generateVehicles",target=generateVehicles, args=())    # Generating vehicles
    thread.daemon = True
    thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0))   # display background in simulation
        #pygame.draw.rect(screen,(0,0,225),[stl,stu,str-stl,std-stu],2)
        int_rect= [stlc,stuc,strc-stlc,stdc-stuc]
        #pygame.draw.rect(screen,(200,0,10),[stlc,stuc,strc-stlc,stdc-stuc],2)
        screen.blit(text_surf,(50,100))


        #time and data
        current_time = int(pygame.time.get_ticks() / 1000)
        time_surf = MAIN_FONT.render(f'Time: {int(pygame.time.get_ticks() / 1000)} s',False, 'Black')
        screen.blit(time_surf,(10,370))

        #print(len(simulation))
        inflow = MAIN_FONT.render(f'Vehicles in simulation:{len(simulation)}',False, 'Black')
        screen.blit(inflow,(10,460))

        #vehicle_stop = {'right': 0, 'down': 0, 'left': 0, 'up': 0}
        
        
        for vehicle in simulation:
            

            

            if vehicle.direction == 'right' and vehicle.x>-50:
                screen.blit(vehicle.image, (vehicle.rect.x,vehicle.rect.y))
            if vehicle.direction == 'left' and vehicle.x<700:
                screen.blit(vehicle.image, (vehicle.rect.right-15,vehicle.rect.y))
            if vehicle.direction == 'down' and vehicle.y>-50:
                screen.blit(vehicle.image, (vehicle.rect.x,vehicle.rect.y))
            if vehicle.direction == 'up' and vehicle.y<700:
                screen.blit(vehicle.image, (vehicle.rect.x,vehicle.rect.bottom-15))
            collide = False
            for vehcol in simulation:
                if vehcol.direction != vehicle.direction and vehicle.rectfit.colliderect(vehcol.rectfit) : print(f'collide {vehicle.index} with {vehcol.index}')
                if int_stop: 
                    vehcol.crossed=0
                    vehicle.crossed=0
                if vehcol.direction != vehicle.direction:
                    
                    if (vehcol.direction =='right' and stlc<vehcol.rectfit.right) or (vehcol.direction =='left' and vehcol.rectfit.left<strc)\
                        or (vehcol.direction =='down' and stuc<vehcol.rectfit.bottom)or (vehcol.direction =='up' and vehcol.rectfit.top<stdc):

                        if vehicle.rect.colliderect(vehcol.rect):
                            if vehicle.direction == 'right' and vehicle.rectfit.right-vehicle.stopline>0:
                                if abs(vehicle.x-vehcol.x) > abs(vehcol.y-vehicle.y) or vehcol.crossed and not vehicle.crossed:
                                   collide = True
                                   #vehicle_stop[vehicle.direction] = 1

                            if  vehicle.direction== 'left' and vehicle.rectfit.left-vehicle.stopline<0:
                                if abs(vehicle.x-vehcol.x) > abs(vehcol.y-vehicle.y) or vehcol.crossed and not vehicle.crossed:
                                   collide = True
                                   #vehicle_stop[vehicle.direction] = 1
                            
                            if vehicle.direction== 'down' and vehicle.rectfit.bottom-vehicle.stopline>0:
                                if  abs(vehicle.x-vehcol.x) < abs(vehcol.y-vehicle.y) or vehcol.crossed and not vehicle.crossed:
                                    collide = True  
                                    #vehicle_stop[vehicle.direction] = 1               

                            if vehicle.direction == 'up' and vehicle.rectfit.top-vehicle.stopline<0:
                                if  abs(vehicle.x-vehcol.x) < abs(vehcol.y-vehicle.y) or vehcol.crossed and not vehicle.crossed: 
                                    collide = True
                                    #vehicle_stop[vehicle.direction] = 1



            vehicle.FrontCheck()
            if collide or vehicle.stop: 
                vehicle.dec()
            elif not collide and not vehicle.stop:
                vehicle.acc()
            vehicle.move()


            vehicle_velocity = V_font.render(f'{round(vehicle.speed*15/4,1)}',False, 'Black')
            
            if vehicle.direction == 'right':vehicle_velocity_rect=vehicle_velocity.get_rect(topright=(vehicle.rect.left-4,vehicle.rect.top))
                          
            if  vehicle.direction== 'left':vehicle_velocity_rect=vehicle_velocity.get_rect(topleft=(vehicle.rect.right+4,vehicle.rect.top))
        
            if vehicle.direction== 'down':vehicle_velocity_rect=vehicle_velocity.get_rect(bottomleft=(vehicle.rect.left-4,vehicle.rect.top-4))
      
            if vehicle.direction == 'up' :vehicle_velocity_rect=vehicle_velocity.get_rect(topleft=(vehicle.rect.left-4,vehicle.rect.bottom+4))
   

            screen.blit(vehicle_velocity,vehicle_velocity_rect)

            
            
            outflow = outflow_font.render(f'out:{round(vehicle.outflow)}',False, 'Black')
            
            if vehicle.direction == 'right':outflow_rect=outflow.get_rect(topright=(590,340))
                          
            if  vehicle.direction== 'left':outflow_rect=outflow.get_rect(topleft=(0,245))
        
            if vehicle.direction== 'down':outflow_rect=outflow.get_rect(bottomleft=(210,600))
      
            if vehicle.direction == 'up' :outflow_rect=outflow.get_rect(topleft=(340,0))
   

            screen.blit(outflow,outflow_rect)



            outflowtot = MAIN_FONT.render(f'Outflow:{round(vehicle.outflowtot)} Veh',False, 'Black')
            screen.blit(outflowtot,(10,400))


            totveh = MAIN_FONT.render(f'Inflow:{round(vehicle.outflowtot+ len(simulation))} Veh',False, 'Black')
            screen.blit(totveh,(10,430))




        


            
            
            #pygame.draw.rect(screen, (130, 130, 130), vehicle.rect, 1)
            #pygame.draw.rect(screen, (255, 0, 0), vehicle.rectfit, 1)
            
            

        clock.tick(15)
        nn+=1
        pygame.image.save(screen , f"scgridlock/screenshot{nn}.png")
        pygame.display.update()


Main()