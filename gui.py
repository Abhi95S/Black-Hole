import Tkinter
from Tkinter import *
import tkMessageBox
import subprocess
from subprocess import call
import sys
import csv
from collections import deque
from threading import Thread
#from threading import Timer
import test_rpca_ec
import os
from os.path import abspath
import Queue
import time
import PIL
from PIL import ImageTk, Image

#Error Check Initializations
errortime=[]       #Buffer for storing time-stamp of the error
faultyspnd = []    #Buffer for storing the faulty spnd number
raw = []           #Buffer for storing raw value of the faulty spnd
faultEst = []      #Buffer for storing fault estimate
cnt = 0            #Count for errors that are consecutive in time
z = 0              #Flag for incrementing cnt
l = 0              #Used for ensuring Start button works only once during runtime
f1=0
f2=0	###############################################################################################################################################################
#Initialization
def initialization():

	'''This is where the initial GUI's functions are present'''

	#Creating a log file Data.csv only once for storing all parameter values from the user, if the file does not exist
	if not os.path.exists('Data.csv'):
		with open('Data.csv', 'w') as x:
			w = csv.writer(x, delimiter = ',')
			w.writerow(['threshVarCap', 'Window Width', 'Alpha', 'rDataMat', 'cDataMat', 'Time', 'error'])
			w.writerow([0.01, 20, 0.05, 20000, 5, 1, 10])
			x.close

	#Creating a log file for storing all the outputs of the RPCA file in terms of Time, Faulty SPND, Raw Value and Fault Estimate
	with open('AllLog.csv', 'w') as v:
		w = csv.writer(v, delimiter = ',')
		w.writerow(['Time', 'Faulty SPND', 'Raw Value', 'Fault Estimate'])
		v.close()

	def Save(j):

		'''
		Here the Save button function is defined
		If all the fields are filled, 'if' condition is valid and all the values are saved in Data.csv file
		'''

		global f1
		f1 += j
		if f1 == 1:
			if ((len(threshVarCap.get())!=0)&(len(winndowWidth.get())!=0)&(len(alpha.get())!=0)&(len(rDataMat.get())!=0)&(len(cDataMat.get())!=0)&(len(Time.get())!=0)&(len(error.get())!=0)):
				with open('Data.csv', 'a') as x:
					w = csv.writer(x, delimiter = ',')
					w.writerow([threshVarCap.get(),winndowWidth.get(),alpha.get(),rDataMat.get(),cDataMat.get(),Time.get(),error.get()])
					x.close()
					initial.destroy()
				
			else:
				th=threshVarCap.get()
				ww=winndowWidth.get()
				al=alpha.get()
				rD=rDataMat.get()
				cD=cDataMat.get()
				ti=Time.get()
				er=error.get()
				
				
				with open('Data.csv', 'r') as f:
					try:
						lastrow = deque(csv.reader(f), 1)[0]
					except IndexError:  # empty file
						lastrow = None
				if(len(threshVarCap.get())==0):
					th=lastrow[0]
				if(len(winndowWidth.get())==0):
					ww=lastrow[1]
				if(len(alpha.get())==0):
					al=lastrow[2]
				if(len(rDataMat.get())==0):
					rD=lastrow[3]
				if(len(cDataMat.get())==0):
					cD=lastrow[4]
				if(len(Time.get())==0):
					ti=lastrow[5]
				if(len(error.get())==0):
					er=lastrow[6]

				with open('Data.csv', 'a') as x:
					w = csv.writer(x, delimiter = ',')
					w.writerow([th,ww,al,rD,cD,ti,er])
				x.close()

				def yes():
					confirm.destroy()
					initial.destroy()
				def no():
					global f1
					f1 = 0
					initial.attributes("-topmost", True)
					initial.attributes("-topmost", False)
					confirm.destroy()
					return f1
			
				confirm=Tk()
				confirm.attributes("-topmost", True)
				confirm.title('Are you sure?')
				#confirm.eval('tk::PlaceWindow %s center' % confirm.winfo_pathname(confirm.winfo_id()))
				confirm.geometry('+325-500')             #Adjust to bring the GUI to the center
				Label(confirm, text="             Previous value at the empty field will be used. Continue?",font=("Times 19")).grid(row=0, sticky=W)
				yesbutton = Button(confirm, text = ' Yes ', font=("Times 16"), fg='blue', command=yes).grid(row=1, column=0, sticky=W, padx=5, pady=5)
				nobutton = Button(confirm, text = ' No ', font=("Times 16"),fg='red', command=no).grid(row=1, column=1, sticky=E, padx=5, pady=5)
				confirm.mainloop()
	    
	def cancel(k):
		global f2
		f2 += k
		if f2 == 1:
			def yes():
				confirm2.destroy()
				initial.destroy()
			def no():
				global f2
				f2 = 0
				initial.attributes("-topmost", True)
				initial.attributes("-topmost", False)
				confirm2.destroy()
				return f2
				
			confirm2=Tk()
			confirm2.attributes("-topmost", True)
			confirm2.title('Are you sure?')
			#confirm.eval('tk::PlaceWindow %s center' % confirm.winfo_pathname(confirm.winfo_id()))
			confirm2.geometry('+500-500')             #Adjust to bring the GUI to the center
			Label(confirm2, text="            Proceed with default values?",font=("Times 19")).grid(row=0, sticky=W)
			yesbutton = Button(confirm2, text = ' Yes ', font=("Times 16"), fg='blue', command=yes).grid(row=1, column=0, sticky=W, padx=5, pady=5)
			nobutton = Button(confirm2, text = ' No ', font=("Times 16"),fg='red', command=no).grid(row=1, column=1, sticky=E, padx=5, pady=5)
			confirm2.mainloop()
	
	initial = Tk()
	#initial.eval('tk::PlaceWindow %s center' % initial.winfo_pathname(initial.winfo_id()))
	initial.geometry('+350-500')             #Adjust to bring the GUI to the center
	initial.title('IITB NPCIL BARC BRNS SPND Fault Diagnosal') ############CHANGE HERE FOR NAME###############

	with open('Data.csv', 'r') as f:
		try:
			lastrow = deque(csv.reader(f), 1)[0]
		except IndexError:  # empty file
			lastrow = None

	a = StringVar()
	b = StringVar()
	c = StringVar()
	d = StringVar()
	e = StringVar()
	h = StringVar()
	g = StringVar()


	a.set(str(lastrow[0]))
	b.set(str(lastrow[1]))
	c.set(str(lastrow[2]))
	d.set(str(lastrow[3]))
	e.set(str(lastrow[4]))
	h.set(str(lastrow[5]))
	g.set(str(lastrow[6]))

	#Edit Variable Names below (Left Column of Initialization GUI):
	Label(initial, text="threshVarCap:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=1, sticky=W, padx=5, pady=5)
	Label(initial, text="Window Length:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=2, sticky=W, padx=5, pady=5)
	Label(initial, text="Alpha:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=3, sticky=W, padx=5, pady=5)
	Label(initial, text="rDataMat:", font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=4, sticky=W, padx=5, pady=5)
	Label(initial, text="cDataMat:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=5, sticky=W, padx=5, pady=5)
	Label(initial, text="Error Freq (sec):",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=6, sticky=W, padx=5, pady=5)
	Label(initial, text="Error group size:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=7, sticky=W, padx=5, pady=5)

	#Right Column of Initialization GUI:
	Label(initial, text = 'Parameters',font=("Times 19 bold"), fg = 'blue').grid(row=0, sticky=W, padx=5, pady=5)
	Label(initial, text = 'Enter the Values',font=("Times 19 bold"), fg = 'blue').grid(row=0, column=2,  sticky=W, padx=5, pady=5)
	Label(initial, text = 'Previous Values',font=("Times 19 bold"), fg = 'blue').grid(row=0, column=3, sticky=W, padx=5, pady=5)
	Label(initial, text=lastrow[0],font=("Times 19 bold"), fg = 'gray').grid(row=1, sticky=E, column=3, padx=5, pady=5)
	Label(initial, text=lastrow[1],font=("Times 19 bold"), fg = 'gray').grid(row=2, sticky=E, column=3, padx=5, pady=5)
	Label(initial, text=lastrow[2],font=("Times 19 bold"), fg = 'gray').grid(row=3, sticky=E, column=3, padx=5, pady=5)
	Label(initial, text=lastrow[3],font=("Times 19 bold"), fg = 'gray').grid(row=4, sticky=E, column=3, padx=5, pady=5)
	Label(initial, text=lastrow[4],font=("Times 19 bold"), fg = 'gray').grid(row=5, sticky=E, column=3, padx=5, pady=5)
	Label(initial, text=lastrow[5],font=("Times 19 bold"), fg = 'gray').grid(row=6, sticky=E, column=3, padx=5, pady=5)
	Label(initial, text=lastrow[6],font=("Times 19 bold"), fg = 'gray').grid(row=7, sticky=E, column=3, padx=5, pady=5)

	#Middle Column of Initialization GUI:
	threshVarCap = Entry(initial, textvariable=a ,font=("Times 19 bold"))
	threshVarCap.grid(row=1, column=2, padx=5, pady=5)
	winndowWidth = Entry(initial, textvariable=b ,font=("Times 19 bold"))
	winndowWidth.grid(row=2, column=2, padx=5, pady=5,)
	alpha = Entry(initial, textvariable=c ,font=("Times 19 bold"))
	alpha.grid(row=3, column=2, padx=5, pady=5)
	rDataMat = Entry(initial, textvariable=d ,font=("Times 19 bold"))
	rDataMat.grid(row=4, column=2, padx=5, pady=5)
	cDataMat = Entry(initial, textvariable=e , font=("Times 19 bold"))
	cDataMat.grid(row=5, column=2, padx=5, pady=5)
	Time = Entry(initial, textvariable=h ,font=("Times 19 bold"))
	Time.grid(row=6, column=2, padx=5, pady=5)
	error = Entry(initial, textvariable=g ,font=("Times 19 bold"))
	error.grid(row=7, column=2, padx=5, pady=5)

	#Buttons in the Initialization GUI:
	savebutton = Button(initial, text = ' Save ',font=("Times 17 bold"), fg='green', command=lambda: Save(1)).grid(row=8, column=0, sticky=W, padx=10, pady=10)
	cancelbutton = Button(initial, text = 'Cancel',font=("Times 17 bold"), fg='red', command=lambda: cancel(1)).grid(row=8, column=3, sticky=E, padx=10, pady=10)

	#Time-out for initial GUI
	'''def timeout():
		initial.destroy()
	t = Timer(2, timeout)
	t.start()'''

	def doSomething():
		os._exit(1)
    	initial.protocol('WM_DELETE_WINDOW', doSomething)

	initial.mainloop()


#Initialization End
	###############################################################################################################################################################

#Monitor
def main():

	'''Here the GUI with Start and Exit Button lies'''

	f_path = abspath("gui.png")
	with open('Data.csv', 'r') as f:
		try:
			lastrow = deque(csv.reader(f), 1)[0]
		except IndexError:  # empty file
			lastrow = None
    	def Start(m):   

		'''Start button is defined here'''

		#Algorithm to Start the program only once then renders 'Start' button useless
		global l
		l = l + m
		if (l == 1):
			Thread(target = myfunction1).start()  #Starting thread 1: RPCA
			time.sleep(1)                         #Waiting time to start the error-detection after starting RPCA.
			Thread(target = myfunction2).start()  #Starting thread 2: Error detection

	def myfunction1():           #Thread 1: For RPCA
		test_rpca_ec.main()
 	def myfunction2():	     #Thread 2: For Error-detection and display via GUI
		errorcheck()

 	def errorcheck():
		global cnt, z

		#Initializing the LOG created for storing the error response from user.
		#(Only the Titles of the CSV files are made here once and the file is overwritten each time the code is run)
		with open('MyLog.csv', 'w+') as g:
			w = csv.writer(g, delimiter=',')
	   		w.writerow(['Time','Faulty SPND','Raw Value','Fault Estimate','Status'])
		g.close

		#Open the LOG file created by RPCA and read all columns to detect error
		with open('AllLog.csv', 'rU') as f:
		    r = csv.DictReader(f, delimiter=',')
		    for row in r:
			Fault_at_time = eval(row['Time'])
			Faulty_SPND = eval(row['Faulty SPND'])
			Raw_value_of_SPND = eval(row['Raw Value'])
			Fault_Estimate = eval(row['Fault Estimate'])
			if(Faulty_SPND!=0):
				z = 1
				errortime.append(Fault_at_time)
				faultyspnd.append(Faulty_SPND)
				raw.append(Raw_value_of_SPND)
				faultEst.append(Fault_Estimate)

			else:
				z = 0

			if (z==1):
				cnt += 1

			else:
				cnt = 0
			
			if(cnt == int(lastrow[6])):
				cnt = 0
				z = 0	
				
				time.sleep(float(lastrow[5])) #Waiting time before showing the groups of the error detected

				#Printing the errors on the GUI monitor
				text=('\n')
				edit.insert(1.0, text)
				for i in range(1, (int(lastrow[6])+1)):
					text=('\n        Faults at time: ' + str(errortime[-int(lastrow[6])+i-1]) + '   Faulty SPND: ' + str(faultyspnd[-int(lastrow[6])+i-1]) + '   Raw Value: ' + str(format(raw[-int(lastrow[6])+i-1], '+.14f')) + '   Fault Estimate:' + str(format(faultEst[-int(lastrow[6])+i-1], '+.14f')))
					edit.insert(1.0, text)
				#Error detection pop-up Yes and No Button Command Starts:						
				def ans(flag):
					if(flag == 1): #For Yes
						with open('MyLog.csv', 'a') as g:
							w = csv.writer(g, delimiter=',')
							w.writerow([Fault_at_time,Faulty_SPND,Raw_value_of_SPND,Fault_Estimate,'Y'])
							myapp.destroy()
					else:          #For No
						with open('MyLog.csv', 'a') as g:
							w = csv.writer(g, delimiter=',')
							w.writerow([Fault_at_time,Faulty_SPND,Raw_value_of_SPND,Fault_Estimate,'N'])
							myapp.destroy()               
				#Error detection pop-up Yes and No Button Commands Ends

				def doThis():
					myapp.withdraw()
					time.sleep(0.1)
					myapp.geometry('+450-265')
					myapp.deiconify()
					pass
				myapp = Tk()
				myapp.attributes("-topmost", True)     #To keep the pop-up above all open windows
				myapp.protocol('WM_DELETE_WINDOW', doThis)
				myapp.title('Fault Check')
				myapp.geometry('+450-370')             #Adjust to bring the error GUI to the center
				Label(myapp, text="      Errornous Value(s) detected. Confirm?",font=("Times 19")).grid(row=0, sticky=W)
				yesbutton = Button(myapp, text = ' Yes ',font=("Times 16"), fg='red', command=lambda: ans(1)).grid(row=1, column=0, sticky=W, padx=7, pady=7)           			       #Error detection GUI 'Yes' button
				nobutton = Button(myapp, text = ' No ', font=("Times 16"),fg='blue', command=lambda: ans(0)).grid(row=1, column=1, sticky=E, padx=7, pady=7)           			       #Error detection GUI 'No' button
				myapp.mainloop()

	#GUI with Start and Exit Button starts:
	label = Tk()
	label.title('IITB NPCIL BARC BRNS SPND Fault Diagnosal')#Change the Title of the GUI here
	label.geometry('+250-400')             		    #Adjust to bring the GUI to the center
	#edit=Text(label, height=int(lastrow[6])+2, width=120)   #Height of the text-box changes according to the error group size.
	edit=Text(label, height=12, width=120)
	edit.pack(side = BOTTOM, padx=2, pady=2)

	def Exit():					            #Exit button function
		label.destroy()
		os._exit(1)
	    
	#Banner image in the GUI:
	label.img =  ImageTk.PhotoImage(Image.open(f_path))
	label.panel1 = Label(label, image = label.img)
	label.panel1.pack(side = "top", expand = "YES", padx=10, pady=10)

	#Link below the banner:
	w = Label(label,text="http://www.ee.iitb.ac.in/%7Ebelur/spnd/", font=("Times 20 bold italic"))
	w.pack(side = "top", padx=5, pady=2)
	
	#Exit and Start Button declaration:
	exitbutton=Button(label, text = ' Exit ', fg='red',font=("Times 15"), command = Exit).pack(side=LEFT, padx=10, pady=2)
	startbutton=Button(label, text = ' Start ',font=("Times 15"), fg='green', command =lambda: Start(1)).pack(side=RIGHT, padx=10, pady=2)

	#Used to kill all threads if main GUI is closed in any way
	def doSomething():
		os._exit(1)
	label.protocol('WM_DELETE_WINDOW', doSomething)

	#Infinite loop necessary to keep GUI alive
	label.mainloop()

	#GUI with Start and Exit Button ends

if __name__ == '__main__':
	initialization()
	main()
