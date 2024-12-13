from tkinter import *
from tkinter import font
import time

w=Tk()

#Using piece of code from old splash screen
width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
#w.configure(bg='#ED1B76')
w.overrideredirect(1) #for hiding titlebar

#new window to open
def new_win():
    import main
  

Frame(w, width=427, height=250, bg='#070B15').place(x=0,y=0)


label2=Label(w, text='STUTUTUTU......', fg='#E0F2FE', bg='#070B15') #decorate it 
label2.configure(font=("Futura Bold Italici", 10))
label2.place(x=10,y=215)

#making animation

image_a=PhotoImage(file='c2.png')
image_b=PhotoImage(file='c1.png')




for i in range(5): #5loops
    l1=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=180, y=125)
    l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=125)
    l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=125)
    l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=125)
    w.update_idletasks()
    time.sleep(0.1)

    l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=125)
    l2=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=200, y=125)
    l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=125)
    l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=125)
    w.update_idletasks()
    time.sleep(0.1)

    l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=125)
    l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=125)
    l3=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=220, y=125)
    l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=125)
    w.update_idletasks()
    time.sleep(0.1)

    l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=125)
    l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=125)
    l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=125)
    l4=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=240, y=125)
    w.update_idletasks()
    time.sleep(0.5)

w.destroy()
new_win()
w.mainloop()