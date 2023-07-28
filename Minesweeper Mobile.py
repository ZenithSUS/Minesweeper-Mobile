from tkinter import *
import pygame
import random
import time
from PIL import ImageTk, Image

def click(index):
    global mfield, map, fr_dbar, stack, closed, row, col, bomb, isgameover, flags, lab_flag, root, display_face, face_frame, face, lab_over, restart, menu, pressed_flag
    
    if index in closed or isgameover:
        return
    if map[index] == "b":
        face2 = ImageTk.PhotoImage(Image.open("Sad Face.png"))
        display_face.config(image = face2)
        display_face.image = face2
        stop_music()
        
        music_gameover()
        lab_over = Label(fr_dbar, text = "Game Over! You lost", fg = "#00FF00", bg = "blue", font = ("Arial", 10))
        
        lab_over.pack()
        game_over()
        restart = Button(text = "Restart", bd = 5, fg = "#00FF00", bg = "blue", font = ("Arial", 8), command = lambda : restart_btn())
        restart.place(anchor = "c", relx = 0.5, rely = 0.90)
        
        menu = Button(text = "Return to Title", bd = 5, fg = "#00FF00", bg = "blue", font = ("Arial", 8), command = lambda : return_menu())
        menu.place(anchor = "c", relx = 0.5, rely = 0.96)
        explosion()
        return
    stack.append(index)
    push_effect()
    
    while len(stack) > 0:
        cl_ind = stack[-1]
        cl_exam = examine(cl_ind)
        closed.append(cl_ind)
        stack.pop()
        
        if cl_exam == 0:
            for i in surrounding(cl_ind):
                if i not in closed and i not in stack:
                    stack.append(i)
            mfield[cl_ind].config(bg = "grey")
        else:
            if cl_exam == 1:
               color = "#00FF00"
            elif cl_exam == 2:
               color = "yellow"
            elif cl_exam == 3:
               color = "#ca4784"
            else:
               color = "#b6d718"
            mfield[cl_ind].config(text = str(cl_exam), fg = color)
            
    
    
    if len(closed) == row*col-bomb:
        music_winner()
        
        face3 = ImageTk.PhotoImage(Image.open("Heart Face.PNG"))
        display_face.config(image = face3)
        display_face.image = face3
        face_flag = False
        lab_over = Label(fr_dbar, text="You Won!", fg = "#00FF00", bg = "blue", font = ("Arial", 10, "bold"))    
        lab_over.pack()
        restart = Button(text = "Restart", bd = 5, fg = "#00FF00", bg = "blue", font = ("Arial", 8), command = lambda : restart_btn())
        restart.place(anchor = "c", relx = 0.5, rely = 0.90)
        
        menu = Button(text = "Return to Title", bd = 5, fg = "#00FF00", bg = "blue", font = ("Arial", 8), command = lambda : return_menu())
        menu.place(anchor = "c", relx = 0.5, rely = 0.96)
        game_over()


def surrounding(index):
    global row, col
    tst = []
    for c in [-col,0,col]:
        if index + c <0 or index+c >= row*col:
            continue
        for i in [-1,0,1]:
            if index//col != (index+i)//col:
                continue
            tst.append(index+c+i)
    tst.remove(index)
    return tst


def examine(index):
    tot = 0
    for i in surrounding(index):
        if map[i]=="b":
            tot+=1
    return tot



def first_click(index):
    global map, row, col, bomb, mfield, lab_flag, flags
    map = ["b" for i in range(bomb)] + ["" for i in range(row * col - bomb)]
    random.shuffle(map)
    while map[index] == "b":
        random.shuffle(map)
        
    for i in range(row * col):
        mfield[i].config(command=lambda x=i: click(x))
    lab_flag.config(text="Bombs: "+str(flags))
    click(index)


def game_over():
    global isgameover
    isgameover = True
    for i in range(row*col):
        if map[i] == "b":
            mfield[i].config(text="B", fg= "red")

def restart_btn():
   global ft_tbar, fr_game, fr_dbar, lab_flag, face_frame, face, restart, lab_over, face_flag, display_face, min, max, main_flag, menu, pressed_flag
   main_flag = False
   pressed_flag = False
   fr_tbar.destroy()
   fr_game.destroy()
   fr_dbar.destroy()
   lab_flag.destroy()
   lab_over.destroy()
   display_face.destroy() 
   face_frame.destroy()
   restart.destroy()
   menu.destroy()
   game(min, max)

def menu_play():
    pygame.mixer.music.load("Main Menu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.get_volume()
    pygame.mixer.music.play(-1)
         
         
def play():
    pygame.mixer.music.load("Minesweeper Music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.get_volume()
    pygame.mixer.music.play(-1)
    
def stop_music():
   pygame.mixer.music.stop()
   
def music_winner():
   pygame.mixer.music.load("Winner.mp3")
   pygame.mixer.music.set_volume(0.5)
   pygame.mixer.music.get_volume()
   pygame.mixer.music.play(1)
   
def music_gameover():
   pygame.mixer.music.load("Game over.mp3")
   pygame.mixer.music.set_volume(0.5)
   pygame.mixer.music.get_volume()
   pygame.mixer.music.play(1)
   
def pressed():
   pygame.mixer.music.load("Press.mp3")
   pygame.mixer.music.set_volume(0.5)
   pygame.mixer.music.get_volume()
   pygame.mixer.music.play(1)

def push_effect():
  effect = pygame.mixer.Sound("Push Effect.mp3")
  effect.play()
  
def explosion():
   global exp_flag
   exp_flag = False
   explode = pygame.mixer.Sound("Explosion.mp3")
   explode.play(0)
   

def game(MIN, MAX):
   global isgameover, row, col, bomb, flags, stack, closed, flag_map, mfield, lab_flag, fr_tbar,  fr_game, fr_dbar, root, display_face, face_frame, face, min, max, main_flag, pressed_flag
   if pressed_flag == True:
      pressed()
      time.sleep(3.5)
   
   main_flag = True
   isgameover = False
   min = MIN
   max = MAX
   row = 10
   col = 7
   bomb = random.randint(min, max)
   flags = bomb
   
   if main_flag == True:
      destroy_main()
   play() 
       
   fr_tbar = Label(root, text = "Minesweeper Mobile", bg = "blue", fg = "#00FF00", font = ("Arial", 16, "italic"))
   fr_tbar.place(anchor = "c", relx = 0.5, rely = 0.05)
   
   face_frame = Frame(root, width = 50, height = 50)
   face_frame.pack()
   face_frame.place(anchor = "c", relx = 0.5, rely = 0.15)
        
   face = ImageTk.PhotoImage(Image.open("Happy Face.PNG"))
   display_face = Label(face_frame, image = face, bg = "#1D1113")
   display_face.pack()
   
   fr_game = LabelFrame(root)
   fr_game.place(anchor = "c", relx = 0.5, rely = 0.55)
   
   fr_dbar = LabelFrame(root)
   fr_dbar.place(anchor = "c", relx = 0.5, rely = 0.85)
   
   lab_flag = Label(root, text = "Bombs: --", bd = 5, fg = "#00FF00", bg = "blue", font = ("Arial", 8))
   lab_flag.place(anchor = "c", relx = 0.5, rely = 0.25)
   
   stack = []
   closed = []
   
   mfield = []   
   for i in range(row*col):
       mfield.append(Button(fr_game, text= "   ", bg = "blue", fg = "#00FF00", bd = 5, command=lambda x=i: first_click(x)))
       mfield[i].grid(row=i//col, column= i%col)

def destroy_main():
   global fr_mtbar, fr_dfbar, easy, normal, hard, exit, creator, mine_frame, display_mine, canvas, running
   mine_frame.destroy()
   display_mine.destroy()
   fr_mtbar.destroy()
   fr_dfbar.destroy()
   easy.destroy()
   normal.destroy()
   hard.destroy()
   exit.destroy()
   creator.destroy()
   running = False
   canvas.destroy()

def return_menu():
      global main_flag, fr_tbar, fr_game, fr_dbar, lab_flag, lab_over, display_face, restart, menu, pressed_flag
      main_flag = True
      pressed_flag = True
      fr_tbar.destroy()
      fr_game.destroy()
      fr_dbar.destroy()
      lab_flag.destroy()
      lab_over.destroy()
      display_face.destroy() 
      face_frame.destroy()
      restart.destroy()
      menu.destroy()
      main()
      

      
def main():
   global fr_mtbar, fr_dfbar, easy, normal, hard, exit, creator, mine_frame, display_mine, mine, canvas, running, exp_flag, pressed_flag
   
   WIDTH = 800
   HEIGHT = 210
   xVelocity = 1
   yVelocity = 1
   running = True
   exp_flag = True
   pressed_flag = True
   
   pygame.mixer.init()
   menu_play()
   
   mine_frame = Frame(root, width = 50, height = 50)
   mine_frame.pack()
   mine_frame.place(anchor = "c", relx = 0.5, rely = 0.12)
        
   mine = ImageTk.PhotoImage(Image.open("Minebomb.PNG"))
   display_mine = Label(mine_frame, image = mine, bg = "#1D1113")
   display_mine.pack()
   
   fr_game = LabelFrame(root)
   fr_game.place(anchor = "c", relx = 0.5, rely = 0.55)
   
   fr_mtbar = Label(root, text = " Minesweeper Mobile ", bd = 5, bg = "blue", fg = "#00FF00", font = ("Arial", 16, "italic"))
   fr_mtbar.place(anchor = "c", relx = 0.5, rely = 0.26)
   
   fr_dfbar = Frame(root, background = "black", borderwidth = 10, relief = GROOVE)
   fr_dfbar.place(anchor = "c", relx = 0.5, rely = 0.52)
   
   easy = Button(fr_dfbar, text = "Easy",  fg = "#00FF00", bg = "blue", bd = 5, font = ("Arial", 12, "italic"), command = lambda : game(3, 6))
   easy.pack(padx = 10, pady = 20)
   
   normal = Button(fr_dfbar, text = "Normal",  fg = "#00FF00", bg = "blue", bd = 5, font = ("Arial", 12, "italic"), command = lambda : game(7, 12))
   normal.pack(padx = 10, pady = 20)
   
   hard = Button(fr_dfbar, text = "Hard",  fg = "#00FF00", bg = "blue", bd = 5, font = ("Arial", 12, "italic"), command = lambda : game(13, 16))
   hard.pack(padx = 10, pady = 20)
   
   exit = Button(fr_dfbar, text = "Exit",  fg = "#00FF00", bg = "blue", bd = 5, font = ("Arial", 12, "italic"), command = lambda : terminate())
   exit.pack(padx = 15, pady = 20)
   
   creator = Label(text = "Created by: ZenithSUS", fg = "#00FF00", bg = "blue", font = ("Arial", 10, "italic"))
   creator.place(anchor = "c", relx = 0.7, rely = 0.94)
   
   canvas = Canvas(root, width=WIDTH,height=HEIGHT, background = "#EC406C", highlightbackground = "#54BFC2", highlightthickness = 5)
   canvas.place(anchor = "c", relx = 0.5, rely = 0.80)
   
   am_mine = ImageTk.PhotoImage(Image.open("Minebomb.png"))
   place_mine = canvas.create_image(0, -10, image = am_mine, anchor = NW)
   
   am_face = ImageTk.PhotoImage(Image.open("Happy Face.PNG"))
   place_face = canvas.create_image(570, 30, image = am_face, anchor = NW)
   
   am_exp = ImageTk.PhotoImage(Image.open("Explode.PNG"))
   
   
   image_width = am_mine.width()
   image_height = am_mine.height()
   
   image2_width = am_face.height()
   image2_width = am_face.width()
   

   while running:
      coordinates = canvas.coords(place_mine)
      coordinates2 = canvas.coords(place_face)
      if(coordinates[0]>=(2*image2_width) or coordinates[0]<0):
         xVelocity = 0
         canvas.itemconfig(place_mine, image = am_exp)
         canvas.moveto(place_mine, 550, 30)
         canvas.delete(place_face)
         if exp_flag == True:
            explosion()
      canvas.move(place_mine ,xVelocity, 0)
      root.update()
      time.sleep(0.01)
 

def terminate():
   global running
   running = False
   root.destroy()
   
if __name__ == "__main__":
   root = Tk()
   root.geometry("500x500")  
   bg = PhotoImage(file="Background.png")
   bg_img =  Label(root, image = bg).pack()
   main()
   root.mainloop()
