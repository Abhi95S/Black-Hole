#To add:
#Attendance % calculator algorithm
#GSM Module
#Replace raw_input with R-pi sensor port value
#All print statements to be displayed on LCD screen using R-pi
#Create backup of all the databases

import Tkinter
from Tkinter import *
import os
import csv
import pandas as pd
import numpy as np
import datetime
import pickle

REGISTRATION = False  			  #Manually change here for toggling between Attendance mode or Registration mode.
					  #True = REGISTRATION 'ON'
					  #Changing this value will always start the program in either Attendance mode(if False)
					  #or Registration mode(if True).
					  #Default = False

flag = 0

if not os.path.exists('admin.csv'):
	print 'No admins exist. Registering admin.'
	value = raw_input('Admin, scan your left thumb: ')
	with open('admin.csv', 'w') as x:
		w = csv.writer(x, delimiter = ',')
		w.writerow(['ID', 'Name'])
		x.close

	admin = Tk()
	admin.title('Admin Registration Desk')
	admin.geometry('+450-370')
	
	a = StringVar()
	
	#Edit Variable Names below (Left Column of registration GUI):
	Label(admin, text="Name:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=1, sticky=W, padx=5, pady=5)

	#Middle Column of registration GUI:
	name = Entry(admin, textvariable=a ,font=("Times 19 bold"))
	name.grid(row=1, column=2, padx=5, pady=5)

	def Save():
		with open('admin.csv', 'a') as x:
			w = csv.writer(x, delimiter = ',')
			w.writerow([value, name.get()])
			x.close
		admin.destroy()

	def cancel():
		admin.destroy()
		os.exit()

	savebutton = Button(admin, text = ' Save ',font=("Times 17 bold"), fg='green', command= Save).grid(row=8, column=0, sticky=W, padx=10, pady=10)
	cancelbutton = Button(admin, text = 'Cancel',font=("Times 17 bold"), fg='red', command=cancel).grid(row=8, column=3, sticky=E, padx=10, pady=10)
	admin.mainloop()

if (os.path.exists('Database.csv') == False) & (os.path.exists('ProfId.csv') == False):
	print 'No databases found. Please register students and professors.'
	
	with open('Database.csv', 'w') as x:
		w = csv.writer(x, delimiter = ',')
		w.writerow(['ID', 'Name', 'Roll No.', 'Email ID', 'Phone'])
		x.close
		
	with open('ProfId.csv', 'w') as x:
		w = csv.writer(x, delimiter = ',')
		w.writerow(['ID', 'Name', 'Lecture'])
		x.close
	REGISTRATION = True

if not os.path.exists('Database.csv'):
	print 'No Student Database Found. Entering Registration Mode.'
	
	with open('Database.csv', 'w') as x:
		w = csv.writer(x, delimiter = ',')
		w.writerow(['ID', 'Name', 'Roll No.', 'Email ID', 'Phone'])
		x.close
	
	REGISTRATION = True
	
if not os.path.exists('ProfId.csv'):
	print 'No Professor Database Found. Entering Registration Mode.'
	with open('ProfId.csv', 'w') as x:
		w = csv.writer(x, delimiter = ',')
		w.writerow(['ID', 'Name', 'Lecture'])
		x.close
	
	REGISTRATION = True

if not os.path.exists('Security.csv'):
	with open('Security.csv', 'w') as f:
		w = csv.writer(f, delimiter = ',')
		w.writerow(['UID', 'Password'])
		w.writerow(['admin', '123'])
		f.close

def main(REGISTRATION):
	if REGISTRATION == True:
		def database():
			reg.register.withdraw()
			bio = Tk()
			bio.title('Registration Desk')
			bio.geometry('+450-370')

			a = StringVar()
			b = StringVar()
			c = StringVar()
			d = StringVar()

			#Edit Variable Names below (Left Column of Student GUI):
			Label(bio, text="Name:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=1, sticky=W, padx=5, pady=5)
			Label(bio, text="Roll Number:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=2, sticky=W, padx=5, pady=5)
			Label(bio, text="Parent's ID:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=3, sticky=W, padx=5, pady=5)
			Label(bio, text="Parent's Phone:", font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=4, sticky=W, padx=5, pady=5)

			#Middle Column of Student GUI:
			name = Entry(bio, textvariable=a ,font=("Times 19 bold"))
			name.grid(row=1, column=2, padx=5, pady=5)
			roll = Entry(bio, textvariable=b ,font=("Times 19 bold"))
			roll.grid(row=2, column=2, padx=5, pady=5,)
			parentid = Entry(bio, textvariable=c ,font=("Times 19 bold"))
			parentid.grid(row=3, column=2, padx=5, pady=5)
			phone = Entry(bio, textvariable=d ,font=("Times 19 bold"))
			phone.grid(row=4, column=2, padx=5, pady=5)

			def Save():
				check = 0
				with open('Database.csv', 'rU') as x:
					r = csv.DictReader(x, delimiter = ',')
					for row in r:
						n = row['Name']
						r = row['Roll No.']
						if n == name.get():
							check = 1
							print 'Invalid Name. This Name has already been taken.'
							x.close
							break
						if r == roll.get():
							check = 1
							print 'Invalid Roll number. This Roll number has already been taken.'
							x.close
							break
						x.close
				if check != 1:
					if (name.get() == '') | (roll.get() == '') | (parentid.get() == '') | (phone.get() == ''):
						print 'Please Enter ALl Fields'
					else:
						with open('Database.csv', 'a') as x:
							w = csv.writer(x, delimiter = ',')
							w.writerow([reg.value, name.get(), roll.get(), parentid.get(), phone.get()])
							x.close
						print 'Successfully registered.'
						reg.register.destroy()
						bio.destroy()

			def cancel():
				reg.register.deiconify()
				bio.destroy()

			savebutton = Button(bio, text = ' Save ',font=("Times 17 bold"), fg='green', command=Save).grid(row=8, column=0, sticky=W, padx=10, pady=10)
			cancelbutton = Button(bio, text = 'Cancel',font=("Times 17 bold"), fg='red', command=cancel).grid(row=8, column=3, sticky=E, padx=10, pady=10)
			bio.mainloop()



		def ProfReg(count):
			ProfReg.cnt += count
			with open ('Security.csv', 'rU') as f:
				r = csv.DictReader(f, delimiter = ',')
				for row in r:
					uid = row['UID']
					password = row['Password']
				f.close
			if (ProfAuth.uid.get() == uid) & (ProfAuth.password.get() == password):
				ProfAuth.auth.destroy()
				reg.register.destroy()
				bio = Tk()
				bio.title('Registration Desk')
				bio.geometry('+450-370')
	
				a = StringVar()
				b = StringVar()
	
				#Edit Variable Names below (Left Column of Prof Registration GUI):
				Label(bio, text="Name:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=1, sticky=W, padx=5, pady=5)
				Label(bio, text="Lecture:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=2, sticky=W, padx=5, pady=5)

				#Middle Column of Prof Registration GUI:
				name = Entry(bio, textvariable=a ,font=("Times 19 bold"))
				name.grid(row=1, column=2, padx=5, pady=5)
				lect = Entry(bio, textvariable=b ,font=("Times 19 bold"))
				lect.grid(row=2, column=2, padx=5, pady=5,)

				def Save():
					check = 0
					with open('ProfId.csv', 'rU') as x:
						r = csv.DictReader(x, delimiter = ',')
						for row in r:
							n = row['Name']
							if n == name.get():
								check = 1
								print 'Invalid Name. This Name has already been taken.'
								x.close
								break
							x.close
					if check != 1:
						if (name.get() == '') | (lect.get() == ''):
							print 'Please fill all the fields!'
						else:
							with open('ProfId.csv', 'a') as x:
								w = csv.writer(x, delimiter = ',')
								w.writerow([reg.value, name.get(), lect.get()])
								x.close
							print 'Sucessfully registered'
							
							if not os.path.exists(str(lect.get())+'.csv'):
								with open(str(lect.get())+'.csv', 'w') as x:
									w = csv.writer(x, delimiter = ',')
									w.writerow(['Name', 'Roll No.', 'Date', 'Attendance Status'])
									x.close
							
							bio.destroy()
							reg()

				def cancel():
					bio.destroy()
					reg()

				savebutton = Button(bio, text = ' Save ',font=("Times 17 bold"), fg='green', command= Save).grid(row=8, column=0, sticky=W, padx=10, pady=10)
				cancelbutton = Button(bio, text = 'Cancel',font=("Times 17 bold"), fg='red', command=cancel).grid(row=8, column=3, sticky=E, padx=10, pady=10)
				bio.mainloop()

			else:
				print 'Authentication Failed!'
				if ProfReg.cnt >= 3:
					ProfReg.cnt = 0
					ProfAuth.auth.destroy()

		def ProfAuth():
			reg.register.withdraw()
			ProfAuth.auth = Tk()
			ProfAuth.auth.title('Authentication Required!')
			ProfAuth.auth.geometry('+450-370')

			a = StringVar()
			b = StringVar()
	
			#Edit Variable Names below (Left Column of registration GUI):
			Label(ProfAuth.auth, text="Username:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=1, sticky=W, padx=5, pady=5)
			Label(ProfAuth.auth, text="Password:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=2, sticky=W, padx=5, pady=5)

			#Middle Column of registration GUI:
			ProfAuth.uid = Entry(ProfAuth.auth, textvariable=a ,font=("Times 19 bold"))
			ProfAuth.uid.grid(row=1, column=2, padx=5, pady=5)
			ProfAuth.password = Entry(ProfAuth.auth, textvariable=b ,font=("Times 19 bold"))
			ProfAuth.password.grid(row=2, column=2, padx=5, pady=5)

			def cancel():
				reg.register.deiconify()
				ProfAuth.auth.destroy()

			submit = Button(ProfAuth.auth, text = ' Submit ',font=("Times 17 bold"), fg='green', command=lambda: ProfReg(1)).grid(row=1, column=3, sticky=W, padx=10, pady=10)
			cancelbutton = Button(ProfAuth.auth, text = ' Cancel ',font=("Times 17 bold"), fg='red', command=cancel).grid(row=2, column=3, sticky=W, padx=10, pady=10)

			ProfAuth.auth.mainloop()

		def reg():
			while 1:
				ProfReg.cnt = 0
				reg.value = ''
				reg.value = raw_input('Scan your left thumb to register yourself: ')
				if (reg.value!=''):
					with open('admin.csv', 'rU') as f:
						r = csv.DictReader(f, delimiter=',')
						for row in r:
							admin = row['ID']
							if admin == reg.value:
								print 'Attendance Mode'
								f.close
								main(False)
								break
					f.close
					with open('ProfId.csv', 'rU') as f:
						r = csv.DictReader(f, delimiter=',')
						for row in r:
							val = row['ID']
							if val == reg.value:
								print 'Already registered as a Professor.'				
								f.close
								reg()
						f.close

					with open('Database.csv', 'rU') as f:
						r = csv.DictReader(f, delimiter=',')
						for row in r:
							val = row['ID']
							if val == reg.value:
								print 'Already registered as a Student.'				
								f.close
								reg()
						f.close

					reg.register = Tk()
					reg.register.title('Registration Desk')
					reg.register.geometry('+450-370')
					Label(reg.register, text="Register as:",font=("Times 19")).grid(row=0, column=1, sticky=W)

					def cancel():
						reg.register.destroy()

					student = Button(reg.register, text = ' Student ',font=("Times 17 bold"), fg='green', command = database).grid(row=1, column=0, sticky=W, padx=10, pady=10)
					prof = Button(reg.register, text = ' Professor ',font=("Times 17 bold"), fg='blue', command = ProfAuth).grid(row=1, column=1, sticky=W, padx=10, pady=10)
					cancelbutton = Button(reg.register, text = '   Cancel   ',font=("Times 17 bold"), fg='red', command = cancel).grid(row=1, column=2, sticky=W, padx=10, pady=10)
					reg.register.mainloop()
		reg()


	if REGISTRATION == False:
		def studattend():
			now = datetime.datetime.now()
			with open('Database.csv', 'rU') as f:
				r = csv.DictReader(f, delimiter=',')
				for row in r:
					ID = row['ID']
					if ID == action.studvalue:
						name = row['Name']
						roll = row['Roll No.']
						f.close
						
						with open(str(action.lec)+'.csv', 'a') as x:
							w = csv.writer(x, delimiter = ',')
							w.writerow([name, roll, str(now)[:10], 'P'])
							x.close
						print str(action.lec)+' attendance marked'
						break
					f.close
			if ID != action.studvalue:
				print 'Data not found! Please register yourself.'
				action(action.lec)

		def action(lec):
			action.lec = lec
			print lec
			studsearch = ''
			action.studvalue = ''
			action.studvalue = raw_input('Mark your attendance: ')

			if action.studvalue != '':
				if action.studvalue != scan.value:
					with open('Database.csv', 'rU') as f:
						r = csv.DictReader(f, delimiter=',')
						for row in r:
							studsearch = row['ID']
							if studsearch == action.studvalue:
								print 'Scanning successful'
								f.close
								for i in range(len(ProfId.list)):
									if ProfId.list[i] == action.studvalue:
										print 'Attendance already marked'
										f.close
										action(lec)
								ProfId.list.append(action.studvalue)
								print ProfId.list
								studattend()
								break
							f.close
				else:
					with open(str(lec)+'.csv', 'a') as x:
						w = csv.writer(x, delimiter = ',')
						w.writerow(['', '', '', ''])
						x.close

					scan()

			if studsearch != action.studvalue:
				print 'No match found! Please try again.'
				action(lec)
		
			else:
				action(lec)



		def ProfId():
			ProfId.list = []
			lec = 'None'
			print 'Please Wait... Scanning your ID'

			with open('ProfId.csv', 'rU') as f:
				r = csv.DictReader(f, delimiter=',')
				for row in r:
					prof = row['ID']
					if prof == scan.value:
						lec = row['Lecture']
						print 'Scanning successful'				
						f.close
						break
			f.close

			if lec == 'None':
				print 'No match found! Please try again.'
				scan()
			else:
				if not os.path.exists(str(lec)+'.csv'):
					with open(str(lec)+'.csv', 'w') as f:
						w = csv.writer(f, delimiter = ',')
						w.writerow(['ID', 'Roll No', 'Date', 'Attendance'])
						f.close
				
				action(lec)
			
		def addfunc():
			adminfunc.adminprop.withdraw()
			value = raw_input('Admin, scan your left thumb: ')
		
			with open ('admin.csv', 'rU') as f:
				r = csv.DictReader(f, delimiter = ',')
				for row in r:
					ID = row['ID']
					if value == ID:
						print 'Admin already exists.'
						f.close
						adminfunc.adminprop.deiconify()
						return
					f.close
					

			admin = Tk()
			admin.title('Admin Registration Desk')
			admin.geometry('+450-370')

			a = StringVar()

			#Edit Variable Names below (Left Column of registration GUI):
			Label(admin, text="Name:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=1, sticky=W, padx=5, pady=5)

			#Middle Column of registration GUI:
			name = Entry(admin, textvariable=a ,font=("Times 19 bold"))
			name.grid(row=1, column=2, padx=5, pady=5)

			def Save():
				with open('admin.csv', 'a') as x:
					w = csv.writer(x, delimiter = ',')
					w.writerow([value, name.get()])
					x.close
				print 'Admin added!'
				admin.destroy()
				adminfunc.adminprop.deiconify()

			def cancel():
				admin.destroy()
				adminfunc.adminprop.deiconify()
			
			savebutton = Button(admin, text = ' Save ',font=("Times 17 bold"), fg='green', command= Save).grid(row=8, column=0, sticky=W, padx=10, pady=10)
			cancelbutton = Button(admin, text = 'Cancel',font=("Times 17 bold"), fg='red', command=cancel).grid(row=8, column=3, sticky=E, padx=10, pady=10)
			admin.mainloop()
			
		def Security():
			adminfunc.adminprop.withdraw()
			Security.auth = Tk()
			Security.auth.title('Enter new User-ID and Password')
			Security.auth.geometry('+450-370')

			a = StringVar()
			b = StringVar()

			#Edit Variable Names below (Left Column of registration GUI):
			Label(Security.auth, text="Username:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=1, sticky=W, padx=5, pady=5)
			Label(Security.auth, text="Password:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=2, sticky=W, padx=5, pady=5)

			#Middle Column of registration GUI:
			Security.uid = Entry(Security.auth, textvariable=a ,font=("Times 19 bold"))
			Security.uid.grid(row=1, column=2, padx=5, pady=5)
			Security.password = Entry(Security.auth, textvariable=b ,font=("Times 19 bold"))
			Security.password.grid(row=2, column=2, padx=5, pady=5)
		
			def Save():
				if (Security.uid.get() != '') & (Security.password.get() != ''):
					with open('Security.csv', 'w') as f:
						w = csv.writer(f, delimiter = ',')
						w.writerow(['UID', 'Password'])
						w.writerow([Security.uid.get(), Security.password.get()])
						f.close
					print 'Security details changed successfully.'
					adminfunc.adminprop.deiconify()
					Security.auth.destroy()
					#adminfunc.adminprop.destroy()
					#scan.mid.destroy()
				
				else:
					print 'Please fill all the fields.'

			def cancel():
				adminfunc.adminprop.deiconify()
				Security.auth.destroy()

			savebutton = Button(Security.auth, text = ' Save ',font=("Times 17 bold"), fg='green', command=Save).grid(row=1, column=3, sticky=W, padx=10, pady=10)
			cancelbutton = Button(Security.auth, text = ' Cancel ',font=("Times 17 bold"), fg='red', command=cancel).grid(row=2, column=3, sticky=W, padx=10, pady=10)

			Security.auth.mainloop()

		def adminfunc(count):
			adminfunc.cnt += count
	
			with open ('Security.csv', 'rU') as f:
				r = csv.DictReader(f, delimiter = ',')
				for row in r:
					uid = row['UID']
					password = row['Password']
				f.close
			
			if (adminfunc.uid.get() == uid) & (adminfunc.password.get() == password):
				def cancel():
					scan.mid.deiconify()
					adminfunc.adminprop.destroy()
	
				adminfunc.auth.destroy()
				adminfunc.adminprop = Tk()
				adminfunc.adminprop.title('Registration Desk')
				adminfunc.adminprop.geometry('+450-370')
				addbutton = Button(adminfunc.adminprop, text = ' Add Admin ',font=("Times 17 bold"), fg='blue', command=addfunc).grid(row=0, column=0, sticky=W, padx=10, pady=10)
				changebutton = Button(adminfunc.adminprop, text = ' Change Security Details ',font=("Times 17 bold"), fg='green', command=Security).grid(row=0, column=1, sticky=W, padx=10, pady=10)
				cancelbutton = Button(adminfunc.adminprop, text = ' Go Back ',font=("Times 17 bold"), fg='red', command=cancel).grid(row=0, column=2, sticky=W, padx=10, pady=10)
			
			else:
				print 'Authentication Failed!'
				if adminfunc.cnt >= 3:
					adminfunc.cnt = 0
					adminfunc.auth.destroy()
					scan.mid.deiconify()
		
		def adminfuncauth():
			adminfunc.cnt = 0
			scan.mid.withdraw()
	
			adminfunc.auth = Tk()
			adminfunc.auth.title('Authentication Required!')
			adminfunc.auth.geometry('+450-370')

			a = StringVar()
			b = StringVar()

			#Edit Variable Names below (Left Column of registration GUI):
			Label(adminfunc.auth, text="Username:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=1, sticky=W, padx=5, pady=5)
			Label(adminfunc.auth, text="Password:",font=("MS_Serif 15 bold"), fg = '#000b6d').grid(row=2, sticky=W, padx=5, pady=5)

			#Middle Column of registration GUI:
			adminfunc.uid = Entry(adminfunc.auth, textvariable=a ,font=("Times 19 bold"))
			adminfunc.uid.grid(row=1, column=2, padx=5, pady=5)
			adminfunc.password = Entry(adminfunc.auth, textvariable=b ,font=("Times 19 bold"))
			adminfunc.password.grid(row=2, column=2, padx=5, pady=5)

			def cancel():
				scan.mid.deiconify()
				adminfunc.auth.destroy()

			submit = Button(adminfunc.auth, text = ' Submit ',font=("Times 17 bold"), fg='green', command=lambda: adminfunc(1)).grid(row=1, column=3, sticky=W, padx=10, pady=10)
			cancelbutton = Button(adminfunc.auth, text = ' Cancel ',font=("Times 17 bold"), fg='red', command=cancel).grid(row=2, column=3, sticky=W, padx=10, pady=10)
			
		def transition():
			scan.mid.destroy()
			main(True)
			
		def calculateattend():
			LectureList = pd.read_csv('ProfId.csv')['Lecture']
			Names = []
			Subjects = []
			attendancepercent = []
			attendancelist = ['Name', '% Attendance']
			attendancelist[1:1] = list(LectureList)
			DefList = np.empty((len(pd.read_csv('Database.csv')['Name'].index), len(attendancelist)), dtype='S10')
			k = 0
			with open('Database.csv', 'rU') as c:
				r = csv.DictReader(c, delimiter=',')
				for row in r:
					attend = row['Name']
					Names.append(attend)
					with open('ProfId.csv', 'rU') as x:
						r0 = csv.DictReader(x, delimiter=',')
						for row0 in r0:
							emptycount = 0
							attendcount = 0
							sub = row0['Lecture']
							Subjects.append(sub)
							with open(str(sub)+'.csv', 'rU') as f:
								r1 = csv.DictReader(f, delimiter=',')
								for row1 in r1:
									empty = row1['Name']
									if empty == '':
										emptycount += 1
									if attend == row1['Name']:
										attendcount += 1
									f.close
								print 'Attendance of ' + str(attend) + ' in lecture ' + str(sub) + ' is ' + str(attendcount) + ' out of ' + str(emptycount)
								percent = float(attendcount) * 100 /emptycount
								attendancepercent.append(str(percent))
								f.close
							x.close
					print ''
					c.close
			for i in np.arange(0, len(pd.read_csv('Database.csv')['Name'].index)):
				TotalAttendance = 0
				DefList[i][0] = Names[i]
				for j in np.arange(0, len(LectureList)):
					DefList[i][j+1] = attendancepercent[j+k]
					TotalAttendance += float(attendancepercent[j+k])
				k += len(LectureList)
				DefList[i][-1] = TotalAttendance/len(LectureList)
			DefListDF = pd.DataFrame(DefList)
			DefListDF.columns = attendancelist
			#print DefListDF
			DefListDF.to_csv('Defaulters List.csv', sep='\t', encoding='utf-8')
		
		def cancel():
			scan.mid.destroy()

		def scan():
			while 1:
				flag = 0
				scan.value = ''
				scan.value = raw_input('Scan your left thumb to commence lecture: ')
				if (scan.value != ''):
					with open('admin.csv', 'rU') as f:
						r = csv.DictReader(f, delimiter=',')
						for row in r:
							admin = row['ID']
							if admin == scan.value:
								print 'Registration Mode'
								f.close
								flag = 1
								f.close
								break
							f.close
							
						if flag == 1:
							scan.mid = Tk()
							scan.mid.title('Registration Desk')
							scan.mid.geometry('+450-370')
							adminbutton = Button(scan.mid, text = ' Add Admin/Security settings ',font=("Times 17 bold"), fg='#000b6d', command = adminfuncauth).grid(row=0, column=0, sticky=W, padx=10, pady=10)
							regbutton = Button(scan.mid, text = ' Registration ',font=("Times 17 bold"), fg='green', command = transition).grid(row=0, column=1, sticky=W, padx=10, pady=10)
							attendancebutton = Button(scan.mid, text = '       Calculate Attendance       ',font=("Times 17 bold"), fg='blue', command = calculateattend).grid(row=1, column=0, sticky=W, padx=10, pady=10)
							cancelbutton = Button(scan.mid, text = '     Cancel      ',font=("Times 17 bold"), fg='red', command = cancel).grid(row=1, column=1, sticky=W, padx=10, pady=10)
							scan.mid.mainloop()
						else:
							ProfId()
		scan()


	else:
		print 'Invalid Registration state. Change it to True or False.'

main(REGISTRATION)
