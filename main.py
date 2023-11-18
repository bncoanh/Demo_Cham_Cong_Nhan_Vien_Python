############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import datetime
import numpy as np
from PIL import Image
import pandas as pd
import time
from tkinter import filedialog

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'bncoanh@gmail.com' ")

###################################################################################
# kiểm tra tệp haarcascade_frontalface_default.xml có tồn tại
def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Xác nhận lại mật khẩu mới')
            return
    else:
        mess._show(title='Sai mật khẩu', message='Vui lòng nhập đúng mật khẩu cũ')
        return
    mess._show(title='Mật khẩu đã được thay đổi', message='Đổi mật khẩu thành công!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Mật khẩu cũ',bg='white',font=('comic', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('comic', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Mật khẩu mới', bg='white', font=('comic', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('comic', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Xác nhận mật khẩu', bg='white', font=('comic', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('comic', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('comic', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#00fcca", height = 1,width=25, activebackground="white", font=('comic', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1.Chụp ảnh   >>>>    2.Lưu hồ sơ"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1.Chụp ảnh   >>>>    2.Lưu hồ sơ"
    message1.configure(text=res)

#######################################################################################

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', 'ID', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, Id,name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Nhập đúng tên"
            message.configure(text=res)

########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Hồ sơ đã được lưu thành công"
    message1.configure(text=res)
    message.configure(text='Số nhân viên đã đăng ký  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Vui lòng bấm vào Lưu hồ sơ')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Thiếu thông tin chi tiết', message='Thông tin còn thiếu, vui lòng kiểm tra')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

def merge_csv_files():
    file_paths = filedialog.askopenfilenames(title="Select CSV files to merge", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    
    if len(file_paths) == 0:
        return
    
    # Combine CSV files into a single DataFrame
    combined_data = pd.concat([pd.read_csv(file) for file in file_paths], ignore_index=True)
    
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    
    if save_path:
        combined_data.to_csv(save_path, index=False)
        result_label.config(text="Merged and saved as " + save_path)

def load_data_and_display():
    # Open a file dialog to select a CSV file
    file_path = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    
    if not file_path:
        return  # User canceled file selection

    # Load the selected CSV file and filter the data
    target_time = '09:00:00'
    df = pd.read_csv(file_path)
    filtered_data = df[df['Time'] > target_time]

    # Clear existing rows in the table
    for row in tree.get_children():
        tree.delete(row)

    # Insert filtered data into the table, including 'Id'
    for index, row in filtered_data.iterrows():
        id_value = row['Id'] if not pd.isna(row['Id']) else ""  # Use empty string if 'Id' is NaN
        tree.insert('', 'end', values=(id_value, row['Name'], row['Date'], row['Time']))

def save_data_to_csv():
    # Get the data currently displayed in the Treeview
    items = tree.get_children()
    data = []
    for item in items:
        values = tree.item(item, 'values')
        data.append({
            'Id': values[0],
            'Name': values[1],
            'Date': values[2],
            'Time': values[3]
        })
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))) 
    if save_path:
        df = pd.DataFrame(data)
        df.to_csv(save_path, index=False)

def delete_employee():
    id_to_delete = delete_id_entry.get()
    data = read_csv('StudentDetails\StudentDetails.csv')
    for row in data:
        if row[1] == id_to_delete:
            data.remove(row)
    with open('StudentDetails\StudentDetails.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['SERIAL NO.', 'ID', 'NAME'])
        csvwriter.writerows(data)
    for row in tv6.get_children():
        tv6.delete(row)
    for row in tv2.get_children():
        tv2.delete(row)
    for row in data:
        tv6.insert('', 'end', values=row)
        tv2.insert('', 'end', values=row)
def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append([row['SERIAL NO.'], row['ID'], row['NAME']])
    return data

######TIME KEEPING ###################
def read_and_display_data():
    global duplicate_counts
    file_path = filedialog.askopenfilename(title="Chọn file CSV", filetypes=[("CSV files", "*.csv")])

    if not file_path:
        return
    data = pd.read_csv(file_path, usecols=[0, 2])
    duplicate_counts = data.groupby(data.columns.tolist(), sort=False).size().reset_index(name='Số Công')
    for row in tv3.get_children():
        tv3.delete(row)
    for index, row in duplicate_counts.iterrows():
        tv3.insert('', 'end', values=(index + 1, row[0], row[1], row['Số Công']))
def save_results():
    global duplicate_counts  # Sử dụng biến toàn cục

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if not file_path:
        return
    duplicate_counts.to_csv(file_path, index=False)
    print(f"Kết quả đã được lưu vào {file_path}")
######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################
def show_frame(frame):
    notebook.select(frame)

window = tk.Tk()
window.geometry("1440x900")
window.resizable(True, False)
window.title("Attendance System")
window.configure(background='#0a3542')

# Tạo một Frame bên trái chứa các nút
button_frame = tk.Frame(window, width=1000, bg='#c79cff')
button_frame.pack(fill='y', side='left')

# Tạo nút để chuyển đổi giữa các tab
button1 = tk.Button(button_frame, text="Chấm công", command=lambda: show_frame(frame1),fg="black"  ,bg="#ff7221"  ,width=30 ,activebackground = "white" ,font=('comic', 11, ' bold '))
button1.place(x=335, y=86)
button2 = tk.Button(button_frame, text="Đăng ký thành viên mới", command=lambda: show_frame(frame2), fg="black"  ,bg="#ff7221"  ,width=30 ,activebackground = "white" ,font=('comic', 11, ' bold '))
button2.place(x=335, y=86)
button5 = tk.Button(button_frame, text="Xem thông tin nhân viên", command=lambda: show_frame(frame7), fg="black"  ,bg="#ff7221"  ,width=30 ,activebackground = "white" ,font=('comic', 11, ' bold '))
button5.place(x=335, y=86)
button4 = tk.Button(button_frame, text="Xóa thông tin nhân viên", command=lambda: show_frame(frame6), fg="black"  ,bg="#ff7221"  ,width=30 ,activebackground = "white" ,font=('comic', 11, ' bold '))
button4.place(x=335, y=86)
button3 = tk.Button(button_frame, text="Kiểm tra nhân viên đi muộn", command=lambda: show_frame(frame5), fg="black"  ,bg="#ff7221"  ,width=30 ,activebackground = "white" ,font=('comic', 11, ' bold '))
button3.place(x=335, y=86)
button6 = tk.Button(button_frame, text="Tính công nhân viên", command=lambda: show_frame(frame8), fg="black"  ,bg="#ff7221"  ,width=30 ,activebackground = "white" ,font=('comic', 11, ' bold '))
button6.place(x=335, y=86)

button1.pack(side='top', pady=10)
button2.pack(side='top', pady=10)
button5.pack(side='top', pady=10)
button4.pack(side='top', pady=10)
button3.pack(side='top', pady=10)
button6.pack(side='top', pady=10)

# Tạo một Frame bên phải chứa các tab
frame_container = tk.Frame(window)
frame_container.pack(fill='both', expand=True, side='right')

notebook = ttk.Notebook(frame_container)
notebook.pack(fill='both', expand=True)

frame1 = tk.Frame(notebook, bg="#FFE4E1")
frame1.place(relx=0.5, rely=0.5, anchor='center')
frame2 = tk.Frame(notebook, bg="#FFE4E1")
frame2.place(relx=0.5, rely=0.5, anchor='center')
frame5 = tk.Frame(notebook, bg="#FFE4E1")
frame5.place(relx=0.5, rely=0.5, anchor='center')
frame6 = tk.Frame(notebook, bg="#FFE4E1")
frame6.place(relx=0.5, rely=0.5, anchor='center')
frame7 = tk.Frame(notebook, bg="#FFE4E1")
frame7.place(relx=0.5, rely=0.5, anchor='center')
frame8 = tk.Frame(notebook, bg="#FFE4E1")
frame8.place(relx=0.5, rely=0.5, anchor='center')

notebook.add(frame1, text="Chấm công")
notebook.add(frame2, text="Đăng ký thành viên mới")
notebook.add(frame7, text="Xem thông tin nhân viên")
notebook.add(frame6, text="Xóa thông tin nhân viên")
notebook.add(frame5, text="Kiểm tra nhân viên đi muộn")
notebook.add(frame8, text="Chấm công nhân viên")
# Mặc định hiển thị frame1
show_frame(frame1)

frame3 = tk.Frame(frame_container, bg="#c4c6ce")
frame4 = tk.Frame(frame_container, bg="#c4c6ce")

frame3.pack(side='top', fill='x')
frame4.pack(side='top', fill='x')

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="#ff61e5",bg="#0a3542" ,width=55 ,height=1,font=('comic', 22, ' bold '))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3,fg="#ff61e5",bg="#0a3542" ,width=55 ,height=1,font=('comic', 22, ' bold '))
clock.pack(fill='both', expand=1)
tick()

head2 = tk.Label(frame2, text="Đăng ký thành viên mới",width=64, fg="black",bg="#FFB6C1", font=('comic', 25, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="Chấm công nhân viên", width=64, fg="black",bg="#FFB6C1" ,font=('comic', 25, ' bold ') )
head1.place(x=0,y=0)
head1 = tk.Label(frame5, text="Kiểm tra nhân viên đi muộn",width=64, fg="black",bg="#FFB6C1" ,font=('comic', 25, ' bold ') )
head1.place(x=0,y=0)
head6 = tk.Label(frame6, text="Xóa thông tin nhân viên",width=64, fg="black",bg="#FFB6C1" ,font=('comic', 25, ' bold ') )
head6.place(x=0,y=0)
head7 = tk.Label(frame7, text="Xem thông tin nhân viên",width=64, fg="black",bg="#FFB6C1" ,font=('comic', 25, ' bold ') )
head7.place(x=0,y=0)
head8 = tk.Label(frame8, text="Chấm công nhân viên",width=64, fg="black",bg="#FFB6C1" ,font=('comic', 25, ' bold ') )
head8.place(x=0,y=0)

lbl = tk.Label(frame2, text="Nhập tên id mới",width=64  ,height=1  ,fg="black"  ,bg="#FFE4E1" ,font=('comic', 17, ' bold ') )
lbl.place(x=120, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold '))
txt.place(x=350, y=88)

lbl2 = tk.Label(frame2, text="Nhập tên người dùng mới",width=64  ,fg="black"  ,bg="#FFE4E1" ,font=('comic', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold ')  )
txt2.place(x=350, y=173)

delete_id_entry = tk.Entry(frame6, width=36, fg="black", font=('comic', 15, ' bold '))
delete_id_entry.place(x=800, y=150)
message6 = tk.Label(frame6, text="Nhập id để xóa thông tin" ,bg="#FFE4E1" ,fg="black"  ,width=90 ,height=1, activebackground = "#3ffc00" ,font=('comic', 15, ' bold '))
message6.place(x=450, y=100)

message1 = tk.Label(frame2, text="1.Chụp ảnh   >>>   2.Lưu hồ sơ" ,bg="#FFE4E1" ,fg="black"  ,width=90 ,height=1, activebackground = "#3ffc00" ,font=('comic', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="#FFE4E1" ,fg="black"  ,width=39,height=1, activebackground = "#3ffc00" ,font=('comic', 16, ' bold '))
message.place(x=200, y=450)

lbl3 = tk.Label(frame1, text="Bản danh sách hôm nay",width=64  ,fg="black"  ,bg="#FFE4E1"  ,height=1 ,font=('comic', 17, ' bold '))
lbl3.place(x=100, y=115)
lbl4 = tk.Label(frame5, text="danh sách đi muộn của tháng",width=64 ,fg="black"  ,bg="#FFE4E1"  ,height=1 ,font=('comic', 17, ' bold '))
lbl4.place(x=100, y=115)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Số thành viên đã đăng ký  : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Thay đổi mật khẩu', command = change_pass)
filemenu.add_command(label='Liên hệ với UC', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Trợ giúp',font=('comic', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(330,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

tree = ttk.Treeview(frame5,height =20, columns=('Id', 'Name', 'Date', 'Time'))
tree.column('#0', width=70)

tree.column('#1', width=100)  # Adjust the width as needed
tree.column('#2', width=250)  # Adjust the width as needed
tree.column('#3', width=200)  # Adjust the width as needed
tree.column('#4', width=200)  # Adjust the width as needed
tree.grid(row=2,column=0,padx=(100,0),pady=(150,0),columnspan=4)
tree.heading('#1', text='Id')
tree.heading('#2', text='Name')
tree.heading('#3', text='Date')
tree.heading('#4', text='Time')
    
tv6 = ttk.Treeview(frame6, height=18, columns=('#1', 'ID', 'name'))
tv6.column('#0', width=70)
tv6.column('#1', width=80)
tv6.column('ID', width=100)
tv6.column('name', width=140)

tv6 = ttk.Treeview(frame6, height=18, columns=('#1', 'ID', 'name'))
tv6.column('#0', width=00)
tv6.column('#1', width=100)
tv6.column('ID', width=250)
tv6.column('name', width=300)

tv6.grid(row=2, column=0, padx=(100, 0), pady=(100, 0), columnspan=4)
tv6.heading('#1', text='STT.')
tv6.heading('ID', text='ID')
tv6.heading('name', text='NAME')
csv_file_path = 'StudentDetails\StudentDetails.csv'  

data = read_csv(csv_file_path) #Làm mới lại bảng xóa nhân viên
for row in data:
    tv6.insert('', 'end', values=row)

tv2 = ttk.Treeview(frame7, height=15, columns=('#1', 'ID', 'name'))
tv2.column('#0', width=70)
tv2.column('#1', width=100)
tv2.column('ID', width=250)
tv2.column('name', width=350)

tv2.grid(row=2, column=0, padx=(250, 0), pady=(100, 0), columnspan=4)
tv2.heading('#1', text='STT')
tv2.heading('ID', text='ID')
tv2.heading('name', text='NAME')
csv_file_path = 'StudentDetails\StudentDetails.csv'
data = read_csv(csv_file_path) #làm mới lại bảng hiển thi nhân viên
for row in data:
    tv2.insert('', 'end', values=row)

tv3 = ttk.Treeview(frame8, height=15, columns=('#0', 'ID', 'name', 'So Cong'))
tv3.column('#0', width=0)  # Đặt chiều rộng cho cột số dòng
tv3.column('ID', width=200)
tv3.column('name', width=250)
tv3.column('So Cong', width=200)

tv3.grid(row=2, column=0, padx=(180, 0), pady=(150, 0), columnspan=4)
tv3.heading('#1', text='STT')
tv3.heading('#0', text='')  # Đặt tiêu đề cho cột số dòng
tv3.heading('ID', text='ID')
tv3.heading('name', text='NAME')
tv3.heading('So Cong', text='So Cong')
###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

scroll=ttk.Scrollbar(frame5,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tree.configure(yscrollcommand=scroll.set)

scroll=ttk.Scrollbar(frame6,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(100,0),sticky='ns')
tv6.configure(yscrollcommand=scroll.set)

scroll=ttk.Scrollbar(frame7,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(100,0),sticky='ns')
tv2.configure(yscrollcommand=scroll.set)


###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#FA8072"  ,width=11 ,activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton.place(x=680, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg="#FA8072"  ,width=11 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton2.place(x=680, y=172)    
takeImg = tk.Button(frame2, text="Chụp ảnh", command=TakeImages  ,fg="white"  ,bg="#FF8C00"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
takeImg.place(x=350, y=300)
trainImg = tk.Button(frame2, text="Lưu hồ sơ", command=psw ,fg="white"  ,bg="#FF8C00"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trainImg.place(x=350, y=380)
trackImg = tk.Button(frame1, text="Bắt đầu chấm công", command=TrackImages  ,fg="black"  ,bg="#FF8C00"  ,width=35  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trackImg.place(x=350,y=50)
quitWindow = tk.Button(frame1, text="Thoát", command=window.destroy  ,fg="black"  ,bg="#FF8C00"  ,width=35 ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
quitWindow.place(x=350, y=450)
merge_button = tk.Button(frame5, text="Tổng hợp điểm danh", command=merge_csv_files, fg="white", bg="#FF8C00", width=34, height=1, activebackground="white", font=('comic', 15, ' bold '))
merge_button.place(x=350, y=50)
load_button = tk.Button(frame5, text='Nhân viên đi muộn', command=load_data_and_display, fg="white", bg="#FF8C00", width=34, height=1, activebackground="white", font=('comic', 15, ' bold '))
load_button.place(x=100, y=600)
save_button = tk.Button(frame5, text='Lưu file', command=save_data_to_csv, fg="white", bg="#FF8C00", width=34, height=1, activebackground="white", font=('comic', 15, ' bold '))
save_button.place(x=800, y=600)
delete_button = tk.Button(frame6, text="Xóa thông tin", command=delete_employee, fg="white", bg="#FF8C00", width=34, height=1, activebackground="white", font=('comic', 15, ' bold '))
delete_button.place(x=800, y=300)
gettime_button = tk.Button(frame8, text="Hiển thị và chấm công", command=read_and_display_data, fg="white", bg="#FF8C00", width=34, height=1, activebackground="white", font=('comic', 15, ' bold '))
gettime_button.place(x=800, y=600)
count_button = tk.Button(frame8, text="Lưu file", command=save_results, fg="white", bg="#FF8C00", width=34, height=1, activebackground="white", font=('comic', 15, ' bold '))
count_button.place(x=100, y=600)
                     
##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
