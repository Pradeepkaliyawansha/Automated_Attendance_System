from tkinter import *
from tkinter.font import Font
from PIL import ImageTk,Image
import cv2,os,pickle
import face_recognition as fr
from tkinter import simpledialog
from tkinter import messagebox
import datetime,face_recognition
from tkinter import filedialog
import os
import time
import glob
import datetime
from selenium import webdriver
import PIL.Image, PIL.ImageTk
import multiprocessing


root = Tk()
def Images_show():
	result=filedialog.askopenfile(initialdir=os.getcwd()+"/dataset_images/",title="Select file",filetypes=(("text",".jpg"),("all file","*.*")))
	img=os.path.abspath(result.name)
	print(img)
	#photoimg = PhotoImage(os.getcwd()+"/dataset_images/"+ img)
	top = Toplevel()
	top.title("Automated Attendant System")
	bt1=Button(top,text="Exit",bg='red',command=top.destroy)
	bt1.pack(side=BOTTOM) 
	cv_img = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)
	height, width, no_channels = cv_img.shape
	canvas = Canvas(top, width = width, height = height)
	canvas.pack()
	photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
	canvas.create_image(0, 0, image=photo, anchor=NW)
	top.mainloop()
	
def open_file():
	result=filedialog.askopenfile(initialdir=os.getcwd(),title="Select file",filetypes=(("Attendance files",".csv"),("all file","*.*")))
	dir_ = os.path.basename(result.name)
	print(dir_)
	txt=result.read()
	top = Toplevel()
	top.title(dir_)
	bt1=Button(top,text="Exit",bg='red',command=top.destroy)
	bt1.pack(side=BOTTOM)
	top.geometry("400x400+150+150")
	text_area=Text(top,undo=True)
	text_area.pack(fill=BOTH,expand=1)
	if(result != None):
		i=1
		for c in txt:
			text_area.insert(END,c)
			
		exit_file=result.name
	result.close()
def Open_new():
	#import dataset_creator
	#creating blank lists
	known_face_encodings_list=[]
	known_IDs=[]
	NUMs=[] 
	font=cv2.FONT_HERSHEY_SIMPLEX

	#creating image's directory
	try:
    		cwd=os.getcwd()
    		print(cwd)
    		os.mkdir(cwd+"/dataset_images")
	except:
    		print()
	def image_taker(dir_name,student_NUM):
		cam=cv2.VideoCapture(0)
		counter=0
		flag=0  
		while cam.isOpened():
			frame=cam.read()[1]
        
			#converting BGR frame to RGB frame
			rgb_frame=frame[:,:,::-1]
        
			#getting locations of faces present
			faces=fr.face_locations(rgb_frame)

			for (top,right,bottom,left) in faces:
            			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
			cv2.putText(frame, "Press 'C' -> capture image\n q -> Quit", (0 , 35), font, 1.0, (255, 255, 255), 2)
			cv2.imshow("live",frame)
			#handler
			if cv2.waitKey(100) & 0xFF==ord('q'):
				if flag==0:
                			#remove if image is not created to avoid any issue
					os.rmdir(dir_name)
				break	
			if cv2.waitKey(100) & 0xFF==ord('c'):
            
				#saving imaegs
				cv2.imwrite(dir_name+"/image,"+str(student_NUM)+","+str(counter)+".jpg",frame)
				flag=1
				print("captured")
				cv2.destroyAllWindows()
		cam.release()
		cv2.destroyAllWindows()

	#setting up student ID
	choice='yes'
	#getting last student NUM and creating next NUM
	try:
		with open("NUMs.txt",'rb') as file_data:
			labels=pickle.load(file_data)
		student_NUM=max(labels,default=0)+1
	except FileNotFoundError:
		student_NUM=1
  

	while(choice=='yes'):
    
		print(student_NUM)

		student_ID=simpledialog.askstring("Input string","Enter student ID: ")
		if student_ID is None:
    			break
    
		#defining directory ID where images will be stored
		cwd=os.getcwd()+"/dataset_images/"
		dir_name=cwd+student_ID+","+str(student_NUM)
		#using try to avoid error when directory is already present
		try:
			
			os.mkdir(dir_name)
			print("check")
			if(os.getcwd() == "check"):
				result=filedialog.askopenfile(initialdir=os.getcwd(),title="Select file",filetypes=(("Attendance files",".jpg"),("all file","*.*")))
				image_path=os.path.abspath(result.name)
				print(image_path)
				counter=0
				flag=0 
				frame=cv2.imread(image_path)
				rgb_frame=frame[:,:,::-1]
				faces=fr.face_locations(rgb_frame)
				for (top,right,bottom,left) in faces:
					cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
				cv2.putText(frame, '''Press 'C' -> capture image
								q -> Quit''', (0 , 35), font, 1.0, (255, 255, 255), 2)
				#cv2.imshow("live",frame)
				#if cv2.waitKey(100) & 0xFF==ord('q'):
				cv2.imwrite(dir_name+"/image,"+str(student_NUM)+","+str(counter)+".jpg",frame)
				flag=1
				print("captured")
				cv2.destroyAllWindows()
				
			else:
				image_taker(dir_name,student_NUM)
				print("check")
		except:
			messagebox.showerror("Error","Student ID already exits.")
    
		choice=messagebox.askquestion("Input string","Add another:")
		if choice=='yes':
			student_NUM=student_NUM+1
	
	dataset_dir_name=os.getcwd()+"/dataset_images"
	folder_names=os.listdir(dataset_dir_name)
	for i in folder_names:
		dir_name=dataset_dir_name+"/"+i
		face_names=os.listdir(dir_name)
		for face_name in face_names:
			image_name=dir_name+"/"+face_name
			print(image_name)

			#loading images using face_recognition library
			known_face= fr.load_image_file(image_name)
			print(known_face)
        
			#getting encodings of faces
			known_face_encoding=fr.face_encodings(known_face)
			if len(known_face_encoding) > 0:
				known_face_encoding=fr.face_encodings(known_face)[0]
			else:
				print("fail")
			student_ID=i.split(",")[0]
			student_NUM_in=int(i.split(",")[1])
        
			#appending encodings,NUMs, IDs into lists
			known_face_encodings_list.append(known_face_encoding)
			known_IDs.append(student_ID)
			NUMs.append(student_NUM_in)

	print(known_IDs)
	print(NUMs)


	#storing data in files using pickle
	with open("encodings.txt",'wb') as file_data:
		pickle.dump(known_face_encodings_list,file_data)

	with open("ID.txt",'wb') as file_data:
		pickle.dump(known_IDs,file_data)

	with open("NUMs.txt",'wb') as file_data:
		pickle.dump(NUMs,file_data)


def start():
	def save_att(student_NUM,ID_student):
		d=datetime.date.today()
		NUMs=[]
		currentDT = datetime.datetime.now()
		date=currentDT.strftime("%I:%M:%S")
		file_name=d.strftime("%d_%B"+".csv")
		try:       
			with open(file_name,'r+') as file_data:
				file_data.seek(0)
				
				for line in file_data:
					NUM,ID,state,dt=line.split(",")
					NUMs.append(int(NUM))
				if student_NUM not in NUMs:
					print("not present")
					
					file_data.write(str(student_NUM)+","+ID_student+",p,"+date+"\n")
					file_data.seek(0)
					print("marked",ID_student,"present")
	
		except FileNotFoundError:
			with open(file_name,'w') as file_data:
				
				print(date)
				file_data.write(str(student_NUM)+","+ID_student+",p,"+date+"\n")
				print("file created")
	#setting font for puttext
	font=cv2.FONT_HERSHEY_SIMPLEX

#laoding data files and storing in lists
	with open("encodings.txt",'rb') as file_data:
		known_face_encodings=pickle.load(file_data)

	with open("ID.txt",'rb') as file_data:
		known_IDs=pickle.load(file_data)
		print(known_IDs)
    
	with open("NUMs.txt",'rb') as file_data:
		student_NUMs=pickle.load(file_data)
		print(student_NUMs)
	if(k.get() == "cameraon"):
		cameraNumber =simpledialog.askstring("Input string","Camera Number or ip:port")
		print(cameraNumber)
		print(type(cameraNumber))
		if cameraNumber == '0' or cameraNumber == '1':
			camera=int(cameraNumber)
			print(camera)
			cam=cv2.VideoCapture(camera)
		
		else:
			st="http://"+cameraNumber+"/video?x.mjpg"
			print(st)
			cam=cv2.VideoCapture(st)
			
	else:
		cam=cv2.VideoCapture(0)
	if(h.get() == "check"):
		playtime =simpledialog.askinteger("Input string","Enter Time in Minutes")
		capture_duration = playtime*60
		start_time = time.time()
		timeplay=int(time.time() - start_time)
	else:
		timeplay=1
		capture_duration=2
	while (timeplay < capture_duration):
		frame=cam.read()[1]
		
			

		#converting BGR frame to RGB frame
		rgb_frame=frame[:,:,::-1]

		#gettting face locations
		face_locations=face_recognition.face_locations(rgb_frame)
    
		#getting face encodings
		current_face_encoding=face_recognition.face_encodings(rgb_frame,face_locations)
    
		for (top,right,bottom,left),face_encoding in zip(face_locations,current_face_encoding):

		#compariong face with known faces
			matches=face_recognition.compare_faces(known_face_encodings,face_encoding)
        	#print(matches)
			ID="unknown"
        	
			if True in matches:
				#getting index for matched face
				match_index=matches.index(True)
        	    
				#getting ID of the person
				ID=known_IDs[match_index]
				student_NUM_det=student_NUMs[match_index]
				save_att(student_NUM_det,ID)
			else:
				continue
			
			cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),1)
			if(h.get() == "check"):
				hk=int(time.time() - start_time)
				cv2.putText(frame,str(hk), (0 , 35), font, 1.0, (255, 255, 255), 2)
				cv2.putText(frame, ID, (left , top), font, 1.0, (255, 255, 255), 2)
			else:
				cv2.putText(frame, ID, (left , top), font, 1.0, (255, 255, 255), 2)
		if(h.get() == "check"):
			timeplay=int(time.time() - start_time)
			
		cv2.imshow("Live",frame)  	
		if cv2.waitKey(1) & 0xFF==ord('q'):
			break
	cam.release()
	cv2.destroyAllWindows()
cam=[]
def stop():
	print("hello")
	cam.release()
	cv2.destroyAllWindows()
	
def call_me():
	answer=messagebox.askquestion("exit","Do you sure to exit")
	if answer == 'yes':
		root.quit()

def Attendance_count():
	os.chdir(os.getcwd())
	wordcount={}
	top = Toplevel()
	top.title("attendance count")
	bt1=Button(top,text="Exit",bg='red',command=top.destroy)
	bt1.pack(side=BOTTOM)
	top.geometry("400x400+150+150")
	text_area=Text(top,undo=True)
	text_area.pack(fill=BOTH,expand=1)
	newlist=[]
	files_list=[]
	for all_files in glob.glob("*.csv"):
		af=all_files
		files_list.append(af)

	print(files_list)
	
	for files in files_list:
		#d=datetime.date.today()
		#file_name=d.strftime("%B")
		#print(file_name)
		print(files)
		pk=re.search(r'\d\d\w(?:Jan|Feb|March|April|May|June|Jul|Aug|Sep|Oct|Nov|December).(?:csv)',files)
		if pk == None:
			print("files not found")
		else:
			mk=pk.group()
			print(mk)
			file=open(mk,"r+")
			new=file.read().split(',')
		
		
			for l in range(1,len(new),3):
				p=new[l]
				newlist.append(p)
		
		
	print(newlist)	
	for word in newlist:
		if word not in wordcount:
			wordcount[word] = 1
				
		else:
			wordcount[word] += 1
				
	print(wordcount)

	#for l in range(0,len(wordcount)+1):
		#k = wordcount[l]
	for k,v in wordcount.items():
			#print (k , v)

	
		text_area.insert(INSERT,k)
		text_area.insert(INSERT,"=")
		text_area.insert(INSERT,v)
		text_area.insert(INSERT,"\n")
		
def Search_Attendance():
	hk1=simpledialog.askstring("Input string","Enter Search ID")
	os.chdir(os.getcwd())
	wordcount={}
	d={}
	newlist=[]
	files_list=[ ]
	for all_files in glob.glob("*.csv"):
		af=all_files
		files_list.append(af)
	print(files_list)
	for files in files_list:
		pk=re.search(r'\d\d\w(?:Jan|Feb|March|April|May|June|Jul|Aug|Sep|Oct|Nov|December).(?:csv)',files)
		if pk == None:
			print("files not found")
		else:
			mk=pk.group()
			print(mk)
			file=open(mk,"r+")
			new=file.read().split(',')
		

			for l in range(1,len(new),3):
				p=new[l]
				newlist.append(p)

		
	for word in newlist:
		if word not in wordcount:
			wordcount[word] = 1
		else:
			wordcount[word] += 1


		
	for k,v in wordcount.items():	
		d[k]=str(v)
		
	if hk1 in d:
		messagebox.showinfo("Attendance Count","Successfully count\n\n"+"         "+d[hk1])
	else:
		messagebox.showerror("Error",'   '+hk1+"\nName Not Found")	
root.title("Automated Attendent System")
topframe=Frame(root)
my_font=Font(family="Time New Roman",size=30,weight="bold",slant="italic")
label=Label(root,text="Automated Attendent System",font=my_font,foreground="#283142").pack()
topframe.pack(side=TOP)


bottomframe=Frame(root)
leftframe=Frame(bottomframe,bg='black')
canvas=Canvas(leftframe,width=627,height=663)
canvas.pack()
photo=PhotoImage(file='C:\\Users\\Gaming\\Desktop\\Automated Attendance system\\profile.png')
photo1=PhotoImage(file='C:\\Users\\Gaming\\Desktop\\Automated Attendance system\\add.png')
photo2=PhotoImage(file='C:\\Users\\Gaming\\Desktop\\Automated Attendance system\\start.png')
photo3=PhotoImage(file='C:\\Users\\Gaming\\Desktop\\Automated Attendance system\\stop.png')
photo4=PhotoImage(file='C:\\Users\\Gaming\\Desktop\\Automated Attendance system\\file.png')
photo5=PhotoImage(file='C:\\Users\\Gaming\\Desktop\\Automated Attendance system\\exit.png')
photo6=PhotoImage(file='C:\\Users\\Gaming\\Desktop\\Automated Attendance system\\clock.png')
photo7=PhotoImage(file='C:\\Users\\Gaming\\Desktop\\Automated Attendance system\\camera.png')
canvas.create_image(50,10,image=photo,anchor=NW)
leftframe.pack(side=LEFT)

rightframe=Frame(bottomframe,padx=50)
bt_font=Font(family="Time New Roman",size=45,weight="bold",slant="italic")
Bt1=Button(rightframe,text="New Entry",command=Open_new,image=photo1,activebackground="green", bd=0,width=10)
Bt1.pack(fill=X)
Bt2=Button(rightframe,text="Start",command=start,image=photo2,activebackground="green", bd=0)
Bt2.pack(fill=X,pady=10) 
Bt3=Button(rightframe,text="Stop(Press'Q')",image=photo3,activebackground="green", bd=0,command=stop)
Bt3.pack(fill=X,pady=10)
Bt4=Button(rightframe,text="files",width=10,command=open_file,image=photo4,activebackground="green", bd=0)
Bt4.pack(fill=X,pady=10)
Bt2=Button(rightframe,text="EXIT",command=call_me,image=photo5,activebackground="green", bd=0)
Bt2.pack(fill=X,pady=10)
frame1=LabelFrame(rightframe,text="Input",padx=5,pady=5)
h=StringVar()
check_bt=Checkbutton(rightframe,text="Set Time",variable=h, offvalue="uncheck",onvalue="check",activeforeground="green",width=120,image=photo6,compound=TOP)
check_bt.pack(side=LEFT)
k=StringVar()
check_bt=Checkbutton(rightframe,text="Set Camera",variable=k, offvalue="cameraoff",onvalue="cameraon",activeforeground="green",width=130,image=photo7,compound=TOP)
check_bt.pack(side=RIGHT)
#check_bt=Checkbutton(rightframe,text="Set Time",variable=h, offvalue="uncheck",onvalue="check",activeforeground="green",selectcolor="red",width=50)
#check_bt.pack()
rightframe.pack(side=RIGHT)
frame1.pack()
bottomframe.pack()

main_menu=Menu(root)
root.config(menu=main_menu)
#file menu
fileMenu=Menu(main_menu,tearoff=False)
main_menu.add_cascade(label="More Options",menu=fileMenu)
fileMenu.add_command(label="Open files",command=open_file)
fileMenu.add_separator()
fileMenu.add_command(label="Images",command=Images_show)
fileMenu.add_separator()
fileMenu.add_command(label="Attendance Count",command=Attendance_count)
fileMenu.add_command(label="Attendance Search",command=Search_Attendance)
fileMenu.add_separator()

Newfile=Menu(fileMenu,tearoff=False)
fileMenu.add_cascade(label="More options",menu=Newfile)
root.minsize(1280,800)
root.maxsize(1280,800)
root.geometry("1280x750+150+150")
root.mainloop()
