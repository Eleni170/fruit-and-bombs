#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import pygame
import time
import random
import sys

#initializing module
pygame.init()
pygame.mixer.music.load("introduction.wav")
crash_sound=pygame.mixer.Sound("explosion.wav")
catch_sound=pygame.mixer.Sound("success.wav")

#rgb encoding for colours
black=(0,0,0)
white=(255,255,255)

# setting width and height of window
width=500
height=500

window=pygame.display.set_mode((width,height))

pygame.display.init()
pygame.display.update()

pygame.display.set_caption('Fruits and Bombs')

clock=pygame.time.Clock()

class Background(pygame.sprite.Sprite):
    
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

background = Background('sky.png', [0,0])
fruits=[pygame.image.load('apple.png'),pygame.image.load('orange.png'),pygame.image.load('bananas.png')]
bombs=[pygame.image.load('bomb.png'),pygame.image.load('red_bomb.png'),pygame.image.load('dynamite.png')]
users=[pygame.image.load('user_left.png'),pygame.image.load('user_right.png'),pygame.image.load('user_small.png')]
pygame.display.set_icon(users[1])

def window_text(text,local_x,local_y,local_width,local_height,size):
    surface=(pygame.font.Font('freesansbold.ttf',size)).render(text,True,black)
    surface_rect=surface.get_rect()
    surface_rect.center=((local_x+local_width/2),(local_y+local_height/2))
    window.blit(surface,surface_rect)
    return

def green_button():

    mouse=pygame.mouse.get_pos()
    pygame.draw.rect(window,(0,200,0),(50,400,100,50))
    if 50+100>mouse[0]>50 and 400+50>mouse[1]>400:
        pygame.draw.rect(window,(0,255,0),(50,400,100,50))
        if pygame.mouse.get_pressed()[0]==1:
            return True

    return False 

def red_button():

    mouse=pygame.mouse.get_pos()
    pygame.draw.rect(window,(200,0,0),(350,400,100,50))
    if 350+100>mouse[0]>350 and 400+50>mouse[1]>400:
        pygame.draw.rect(window,(255,0,0),(350,400,100,50))
        if pygame.mouse.get_pressed()[0]==1:
            pygame.quit()
            sys.exit()

    window_text("Quit",350,400,100,50,15)

    return


def live(lives):
    if lives==3:
        return False,True,True
    elif lives==2:
        return False,False,True
    return False,False,False


def game_intro():
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill(white)
        window.blit(background.image, background.rect)       
        window_text("Fruit and Bombs",0,0,width,height,55)
        
        if(green_button()):break          
        window_text("Play",50,400,100,50,15)
        
        red_button()

        pygame.display.update()
        clock.tick(15)
    return

def game_over():
    pygame.mixer.music.stop()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill(white)
        window.blit(background.image, background.rect)
        window_text("Game Over",0,0,width,height,65)

        if(green_button()):break          
        window_text("Play Again",50,400,100,50,15)

        red_button()        
        
        pygame.display.update()

    pygame.mixer.music.play(-1)
    return

def paused():
    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        window.fill(white)
        window.blit(background.image, background.rect)            
        window_text("Paused",0,0,width,height,65)

        if(green_button()):break
        window_text("Continue",50,400,100,50,15)

        red_button()

        pygame.display.update()
    return

def game_loop():

    pygame.mixer.music.stop()    

    pygame.mixer.music.play(-1)

    user=users[1]
    
    x=width*0.45
    y=height*0.8

    bad_width=random.randrange(0,width)
    bad_height=-500


    good_width=random.randrange(0,width)
    good_height=-500

    fruit_or_bomb=bool(random.getrandbits(1))
    
    bomb=bombs[random.randint(0,2)]
    fruit=fruits[random.randint(0,2)]

    speed=4
    points=0.0

    small1,small2,small3=True,True,True
    lives=3

    while True:        
        #list of events that is happening on the window
        for event in pygame.event.get():
            
            if event.type==pygame.QUIT:
                return
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:                
                    paused()
        
        move_ticker = 0
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if move_ticker == 0:
                move_ticker = 10
                user=users[0]
                x+=-5
        if keys[pygame.K_RIGHT]:
            if move_ticker == 0:   
                move_ticker = 10     
                user=users[1]
                x+=5

        if move_ticker > 0:
            move_ticker -= 1

        if x<0:x=0   #if car hits on the wall
        if x+user.get_rect().size[0]>width:x=500-user.get_rect().size[0]

        window.fill(white)
        window.blit(background.image, background.rect)    
        window.blit(user,(x,y))
        window.blit(pygame.font.SysFont(None,25).render("Points : "+str(points),True,black),(0,0))
        window.blit(pygame.font.SysFont(None,25).render("Lives : ",True,black),(370,0))
        
        if(small1):window.blit(users[2],(430,0))
        if(small2):window.blit(users[2],(450,0))
        if(small3):window.blit(users[2],(470,0))
                
        if fruit_or_bomb: #bomb

            window.blit(bomb,(bad_width,bad_height))

            if bad_height>height:   #pass
                points+=speed
                speed+=0.2
                bad_width=random.randrange(0,width)
                bad_height=-500
                fruit_or_bomb=bool(random.getrandbits(1))
                bomb=bombs[random.randint(0,2)]

            if y<bad_height+bomb.get_rect().size[1]: #crash

                if x>bad_width and x<bad_width+50 or x+user.get_rect().size[0]>bad_width and x+user.get_rect().size[0]<bad_width+50:
                    pygame.mixer.Sound.play(crash_sound)
                    bad_width=random.randrange(0,width)
                    bad_height=-500
                    fruit_or_bomb=bool(random.getrandbits(1))
                    bomb=bombs[random.randint(0,2)]
                    small1,small2,small3=live(lives)
                    lives-=1
                    if(lives==0):
                        game_over()
                        game_loop()
                        break
            bad_height+=speed
        else:  #fruit
            window.blit(fruit,(good_width,good_height))

            if y<good_height+fruit.get_rect().size[1]: #catch
                if x>good_width and x<good_width+50 or x+user.get_rect().size[0]>good_width and x+user.get_rect().size[0]<good_width+50:
                    pygame.mixer.Sound.play(catch_sound)
                    points+=speed
                    speed+=0.2
                    good_width=random.randrange(0,width)
                    good_height=-500
                    fruit_or_bomb=bool(random.getrandbits(1))
                    fruit=fruits[random.randint(0,2)]

            if good_height>height: #did not catch
                points-=speed
                good_width=random.randrange(0,width)
                good_height=-500
                fruit_or_bomb=bool(random.getrandbits(1))
                fruit=fruits[random.randint(0,2)]
            good_height+=speed

        if points<0:points=0.0
        pygame.display.update()
        clock.tick(60)
    return    

game_intro()
game_loop()    
pygame.quit()


