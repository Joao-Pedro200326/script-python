from tkinter import *
from threading import Thread
from datetime import datetime
from time import sleep

WIDTH = 150
HEIGHT = 100

def time():
	if 400000 <float(str(datetime.today())[20:]) < 800000:
		var = 1
	else:
		var = 0
	while True: 
		if var:
			hora = str(datetime.today())[11:-7].split(':')
		else:
			hora = str(datetime.today())[11:-7]
		l1['text'] = hora
		var = not var
		sleep(0.5)
		 

janela = Tk()
janela.geometry(f"{WIDTH}x{HEIGHT}")

l1 = Label(janela, font='Arial 20')
l1.pack()

t = Thread(target=time, daemon=True)
t.start()

janela.mainloop()
exit()
