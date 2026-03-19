from graphics import *
import random
import time
import datetime
import serial
from copy import deepcopy
from csv import writer, QUOTE_MINIMAL, DictReader
from sys import setrecursionlimit, path as sys_path
from tkinter import Toplevel, Canvas, BOTH, TclError, Tk, Label, Button, \
     StringVar, OptionMenu, IntVar, Radiobutton
from os import getcwd, popen, mkdir, makedirs, path as os_path
from PIL import ImageTk, Image  
from random import choice, shuffle
from subprocess import run
import pigpio # import pi, OUTPUT
import csv

# Last edited: 2026-03-18 

def main():
        
        # Setup GPIO numbers (NOT PINS; gpio only compatible with GPIO num)
    servo_GPIO_num = 2
    hopper_light_GPIO_num = 13
    house_light_GPIO_num = 21
    string_LED_GPIO_num = 5 # Only in box 1
        
        # Setup use of pi()
    rpi_board = pigpio.pi()
        
        # Then set each pin to output 
    rpi_board.set_mode(servo_GPIO_num, pigpio.OUTPUT) # Servo motor...
    rpi_board.set_mode(hopper_light_GPIO_num, pigpio.OUTPUT) # Hopper light LED...
    rpi_board.set_mode(house_light_GPIO_num, pigpio.OUTPUT) # House light LED...
    rpi_board.set_mode(string_LED_GPIO_num, pigpio.OUTPUT) # House light LED...
        
        # Setup the servo motor 
    rpi_board.set_PWM_frequency(servo_GPIO_num, 50) # Default frequency is 50 MhZ
        
        # Next grab the up/down 
    hopper_vals_csv_path = str(os_path.expanduser('~')+"/Desktop/Box_Info/Hopper_vals.csv")
        
        # Store the proper UP/DOWN values for the hopper from csv file
    up_down_table = list(csv.reader(open(hopper_vals_csv_path)))
    hopper_up_val = up_down_table[1][0]
    hopper_down_val = up_down_table[1][1]
        
        # Lastly, run the shell script that maps the touchscreen to operant box monitor
    popen("sh /home/blaisdelllab/Desktop/Hardware_Code/map_touchscreen.sh")
                
                

    current_correct = "false"
    
    feeder = "off"
    subject_num = ""
    summary_last_correct = []
    summary_first_correct =[]
    left_clicked = "false"
    right_clicked = "false"
    middle_clicked = "false"
    trial = 0
    print("trial:", trial)
    num_correct = 0
    last_correct = 0
    first_correct = 0
    last_trials = 0
    first_trials =0
    FR = 0
    first_key = 0
    #draw window

    win = GraphWin("memory",width = 1024, height = 768)
    win.setBackground("black")
    #define left circle location
  
    lcircle = Circle(Point(412,384),30)
    lcircle.setFill("yellow")
    #define middle red circle
    mcirclered = Circle(Point(512,384),30)
    mcirclered.setFill("red")
    
    #define middle green circle
    mcirclegreen = Circle(Point(512,384),30)
    mcirclegreen.setFill("green")
    
    #define right circle
    rcircle = Circle(Point(612,384),30)
    rcircle.setFill("yellow")
    time.sleep(2)
   
    #define top circle
    tcircle = Circle(Point(512,150),30)
    tcircle.setFill("yellow")
    
    lblank = Circle(Point(412,384),30)
    rblank = Circle(Point(612,384),30)
    mblank = Circle(Point(512,384),30)
    tblank = Circle(Point(512,284),30)
    lblank.setFill("grey")
    rblank.setFill("grey")
    mblank.setFill("grey")
    tblank.setFill("grey")
    while subject_num == "":
    #draw subject# input box
        
        start_msg = Text(Point(512,284), "please enter subject number")
        start_msg.draw(win)
        input_box = Entry(Point(512,384),5)
        input_box.setText("")
        input_box.setSize(24)
        input_box.setTextColor("black")
        input_box.draw(win)
        win.getMouse()
        subject_num = input_box.getText()
        print("subject:",subject_num)    
        input_box.undraw()
        start_msg.undraw()

    input_box.undraw()
    start_msg.undraw()
    
    start_msg = Text(Point(512,384), "click to start")
    start_msg.draw(win)
    
    start_msg.undraw()
    lblank.draw(win)
    rblank.draw(win)
    mblank.draw(win)
    
    time.sleep(2)
    while trial < 20:
       
        number_correct = Text(Point(512,484), "total correct: " +str(num_correct))
        number_first_correct = Text(Point(512,504), "#F correct: " +str(first_correct))
        number_last_correct = Text(Point(512,524), "#L correct: " +str(last_correct))
        number_first_correct.setTextColor("white")
        number_last_correct.setTextColor("white")
        trial_num = Text(Point(512,544), "trials: " +str(trial))
        trial_num.draw(win)
        trial_num.setTextColor("white")
        number_first_correct.draw(win)
        number_last_correct.draw(win)
        number_correct.draw(win)
        
        if trial >0:
            if current_correct == "true":
                current_correct = "false"
                time.sleep(3)
            else:
                time.sleep(5)
            
        
        trial+=1
        
        left_clicked = "false"
        right_clicked ="false"
        middle_clicked ="false"           
        
 
        rule = select_rule(last_trials,first_trials)
        
        button = select_first_button()
        correct = correct_button(rule,button)
        
        #draw first button
        if button == 0:
            lcircle.draw(win)
        else:
            rcircle.draw(win)
            
        #wait for click
        while FR < 1:
            if left_clicked and right_clicked == "false":
                clickpos = win.getMouse()
                click_x = clickpos.getX()
                click_y = clickpos.getY()
                print("coordinate is", click_x, click_y)
            if button == 0:
                if left_clicked == "false":
                    if (click_x > 382 and click_x < 442) and (click_y > 354 and click_y < 414):
                        
                        FR+=1
                        print("pecks", FR)
                        if FR >= 1:
                            left_clicked = "true"
                            
                            print("clicked", left_clicked)
                    else:
                        clickpos = win.getMouse()
                        click_x = clickpos.getX()
                        click_y = clickpos.getY()                
                        
            elif button == 1:
                if right_clicked =="false":
                    if (click_x > 582 and click_x < 642) and (click_y > 354 and click_y < 414):
                        
                        FR+=1
                        print("pecks", FR)
                        if FR >= 1:
                            right_clicked = "true"
                           
                            print("clicked", right_clicked)
                            
                       
                    else:
                        clickpos = win.getMouse()
                        click_x = clickpos.getX()
                        click_y = clickpos.getY()                
                 
        #draw last button
        FR = 0
        print("pecks", FR)
        if button == 0 and left_clicked == "true":
            lcircle.undraw()
            rcircle.draw(win)
        elif button == 1 and right_clicked =="true":
            rcircle.undraw()
            lcircle.draw(win)
        while FR < 1:
            if left_clicked or right_clicked == "false":
                clickpos = win.getMouse()
                click_x = clickpos.getX()
                click_y = clickpos.getY()
                print("coordinate is", click_x, click_y)
     
            
                if button == 1:
                    if left_clicked == "false":
                        if (click_x > 382 and click_x < 442) and (click_y > 354 and click_y < 414):
                            FR +=1
                            print("pecks", FR)
                            if FR >= 1:
                                left_clicked = "true"
                                print("left clicked", left_clicked)
                                    
                        else:
                            clickpos = win.getMouse()
                            click_x = clickpos.getX()
                            click_y = clickpos.getY()                
                                
                elif button == 0:
                    if right_clicked =="false":
                        if (click_x > 582 and click_x < 642) and (click_y > 354 and click_y < 414):
                            FR+=1
                            print("pecks", FR)
                            if FR >= 1:
                                right_clicked = "true"
                                print("right clicked", right_clicked)
                        else:
                            clickpos = win.getMouse()
                            click_x = clickpos.getX()
                            click_y = clickpos.getY()           
                          
       
        #draw rule button
        FR = 0
        if rule == 0 and left_clicked =="true" and right_clicked =="true":
            lcircle.undraw()
            rcircle.undraw()
            mcirclered.draw(win)
            first_trials+=1
            print("number first trials:", first_trials)
        elif rule == 1 and left_clicked =="true" and right_clicked =="true":
            lcircle.undraw()
            rcircle.undraw()        
            mcirclegreen.draw(win)
            last_trials +=1
            print("number last trials:", last_trials)            
            #wait for click
        while middle_clicked == "false":
            if (click_x > 482 and click_x < 542) and (click_y > 354 and click_y< 414):
                middle_clicked = "true"
            else:
                clickpos = win.getMouse()
                click_x = clickpos.getX()
                click_y = clickpos.getY()
        if middle_clicked == "true":
            lcircle.draw(win)
            rcircle.draw(win)
           
            right_clicked ="false"
            left_clicked ="false"
       
            clickpos = win.getMouse()
            click_x = clickpos.getX()
            click_y = clickpos.getY() 
            print("correct key is", correct)
       
     
        while left_clicked == "false" and right_clicked == "false":
                       
            if correct == "left_button":
                              
                    
                if (click_x > 582 and click_x < 642) and (click_y > 354 and click_y < 414):
                    right_clicked = "true"
                 
                        
                elif (click_x > 382 and click_x < 442) and (click_y > 354 and click_y < 414):
                    left_clicked = "true"
                    current_correct = "true"
                    num_correct +=1
                    rpi_board.write(house_light_GPIO_num,
                                    False) # Turn off the house light
                    rpi_board.write(hopper_light_GPIO_num,
                                    True) # Turn off the house light
                    rpi_board.set_servo_pulsewidth(servo_GPIO_num,
                                                   hopper_up_val) # Move hopper to up position                    
                    time.sleep(2)
                    rpi_board.write(house_light_GPIO_num,
                                    False) # Turn off the house light
                    rpi_board.write(hopper_light_GPIO_num,
                                    False) # Turn off the house light
                    rpi_board.set_servo_pulsewidth(servo_GPIO_num,
                                                   hopper_down_val) # Move hopper to up position 
                    if rule == 1:
                        last_correct +=1
                        summary_last_correct.append(last_correct)
                    elif rule == 0:
                        first_correct +=1
                        summary_first_correct.append(first_correct)
                else:
                    clickpos = win.getMouse()
                    click_x = clickpos.getX()
                    click_y = clickpos.getY()                     
                                        
                                                                        
            elif correct == "right_button":
           
                   
                if (click_x > 582 and click_x < 642) and (click_y > 354 and click_y < 414):
                    right_clicked = "true"
                    current_correct = "true"
                    num_correct+=1
                    rpi_board.write(house_light_GPIO_num,
                                    False) # Turn off the house light
                    rpi_board.write(hopper_light_GPIO_num,
                                    True) # Turn off the house light
                    rpi_board.set_servo_pulsewidth(servo_GPIO_num,
                                                   hopper_up_val) # Move hopper to up position
                    time.sleep(2)
                    rpi_board.write(hopper_light_GPIO_num,
                                    False) # Turn off the house light
                    rpi_board.set_servo_pulsewidth(servo_GPIO_num,
                                                   hopper_down_val) # Move hopper to up position
                        
                    
                    if rule == 1:
                        last_correct +=1
                        summary_last_correct.append(last_correct)
                    elif rule == 0:
                        first_correct +=1
                        summary_first_correct.append(first_correct)
                                      
                elif (click_x > 382 and click_x < 442) and (click_y > 354 and click_y < 414):
                    left_clicked = "true"
                else:
                    clickpos = win.getMouse()
                    click_x = clickpos.getX()
                    click_y = clickpos.getY()           
                    
            
                                                                         
        print("total number correct:", num_correct)
        print("trials:", trial)
        print("#last correct:", last_correct)
        print("#first correct:", first_correct)
        
        lcircle.undraw()
        rcircle.undraw()
        tcircle.undraw()
        mcirclered.undraw()
        mcirclegreen.undraw() 
        lblank.undraw()
        rblank.undraw()
        mblank.undraw()
        tblank.undraw()        
        if current_correct == "true":
            time.sleep(2)
        
        number_correct.undraw()
        number_last_correct.undraw()
        number_first_correct.undraw()
        trial_num.undraw()
    if trial == 20:
        percent_last_correct = (last_correct/last_trials)*(100)
        percent_first_correct = (first_correct/first_trials)*(100)
        print(percent_last_correct)
        print(percent_first_correct)    
        file1 = open(str(subject_num)+"last.txt", "a")
        
        file1.write(str(percent_last_correct)+"\n")
        file1.close()
        file2 = open(str(subject_num)+"first.txt", "a")  
        file2.write(str(percent_first_correct)+"\n")
        file2.close()
       
        
        number_correct = Text(Point(512,484), "total correct: " +str(num_correct))
        number_first_correct = Text(Point(512,504), "#F correct: " +str(first_correct))
        number_last_correct = Text(Point(512,524), "#L correct: " +str(last_correct))
        trial_num = Text(Point(512,544), "trials: " +str(trial))        
        trial_num.draw(win)
        number_first_correct.draw(win)
        number_last_correct.draw(win)
        number_correct.draw(win)            
        time.sleep(5)
   
    session_over = Text(Point(512,334),"Session is over, click to exit AFTER bird is out")
    session_over.draw(win)
    win.getMouse()
    win.close()
def select_rule(last_trials,first_trials):
    
    print("number of last trials:", last_trials)
    if last_trials == 10:
        rule = 0
    elif first_trials == 10:
        rule = 1
    else:
        rule = random.randint(0,1)
    print("rule",rule)
    return rule
def select_first_button():
    button = random.randint(0,1)
    print("button",button)
    return button
def correct_button(rule,button):
    #decide correct button
    if rule == 0 and button == 0:
        correct = "left_button"
    elif rule == 0 and button == 1:
        correct = "right_button"
    elif rule == 1 and button == 0:
        correct = "right_button"
    elif rule == 1 and button == 1:
        correct = "left_button"      
    return correct
main()
