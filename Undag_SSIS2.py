#================= SSIS 2 ================#
#========= Undag, Lloyd Kayle L. =========#
#============== BS Stat III ==============#


import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
import tkinter.ttk as ttk
import tkinter.messagebox
import sqlite3
import time
from PIL import ImageTk, Image




class SSIS(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Course, Student):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Course)

    def show_frame(self, page_number):

        frame = self.frames[page_number]
        frame.tkraise()
    


       


class Course(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Student Information System")
        centercolor = tk.Label(self,height = 8,width=600, bg="#003A6C")
        centercolor.place(x=0,y=5)
    
        titleheading = tk.Label(self, text="Student Information System", font=("Old English Text MT",48),bd=0,
                            fg="white",background = '#003A6C')
        titleheading.place(x=320,y=25)

        title2=Label(self, text = "SAINT CLAIRE'S ACADEMY", font = ('times', 20), foreground = 'white', background = '#003A6C')
        title2.place(x=550, y=5)

#========= BUTTONS =========#
        Coursebutton = tk.Button(self, text="Course",font=("Old English Text MT",13),bd=0,
                            width = 10,
                            bg="#003A6C", justify='center',
                            fg="white",
                            command=lambda: controller.show_frame(Course))
        Coursebutton.place(x=600,y=95)
        Coursebutton.config(cursor= "hand2")
        
        Studbutton= tk.Button(self, text="Student",font=("Old English Text MT",13),bd=0,
                            width = 10,
                            bg="#003A6C", justify='center',
                            fg="white",
                            command=lambda: controller.show_frame(Student))
        Studbutton.place(x=700,y=95)
        Studbutton.config(cursor= "hand2")

        Code = StringVar()
        Cname = StringVar()
        SearchBarVar = StringVar()


 #========= FUNCTIONS =========#
        def connectCourse():
            conn = sqlite3.connect("Undag_SSIS.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS ccode (Code TEXT PRIMARY KEY, Cname TEXT);") 
            conn.commit() 
            conn.close()
            
        def addCourse():
            if Code.get()=="" or Cname.get()=="": 
                tkinter.messagebox.showinfo("Student Information System", "Please fill up the Box correctly")
            else:
                conn = sqlite3.connect("Undag_SSIS.db")
                c = conn.cursor() 
                c.execute("INSERT INTO ccode(Code,Cname) VALUES (?,?)",\
                          (Code.get(),Cname.get()))        
                conn.commit()           
                conn.close()
                Code.set('')
                Cname.set('') 
                tkinter.messagebox.showinfo("Student Information System", "Course Recorded Successfully")
                displayCourse()
                
                
              
        def displayCourse():
            treecourse.delete(*treecourse.get_children())
            conn = sqlite3.connect("Undag_SSIS.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM ccode")
            rows = cur.fetchall()
            for row in rows:
                treecourse.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def updateCourse():
            for selected in treecourse.selection():
                conn = sqlite3.connect("Undag_SSIS.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE ccode SET Code=?, Cname=? WHERE Code=?", \
                            (Code.get(),Cname.get(), treecourse.set(selected, '#1')))                       
                conn.commit()
                tkinter.messagebox.showinfo("Student Information System", "Course Updated Successfully")
                displayCourse()
                conn.close()
                
        def editCourse():
            x = treecourse.focus()
            if x == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a record from the table.")
                return
            values = treecourse.item(x, "values")
            Code.set(values[0])
            Cname.set(values[1])
                    
        def deleteCourse(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("Student Information System", "Do you want to permanently delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("Undag_SSIS.db")
                    cur = con.cursor()
                    x = treecourse.selection()[0]
                    id_no = treecourse.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM ccode WHERE Code = ?",(id_no,))                   
                    con.commit()

                    treecourse.delete(x)
                    tkinter.messagebox.showinfo("Student Information System", "Course Deleted Successfully")
                    displayCourse()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("Student Information System", "Students are still enrolled in this course")
                
        def searchCourse():
            Code = SearchBarVar.get()                
            con = sqlite3.connect("Undag_SSIS.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM ccode WHERE Code = ?",(Code,))
            con.commit()
            treecourse.delete(*treecourse.get_children())
            rows = cur.fetchall()
            for row in rows:
                treecourse.insert("", tk.END, text=row[0], values=row[0:])
            con.close()
 
        def Refresh():
            pass
            displayCourse()
        
        def clear():
            Code.set('')
            Cname.set('') 

#========= ENTRY AND CLOCK =========#

        ManageFrame=Frame(self, relief= GROOVE, borderwidth = 5, bg="#003A6C")
        ManageFrame.place(x=0, y=130,width=400, height=600)
        
        DisplayFrame=Frame(self, relief= GROOVE, borderwidth = 5, bg="#003A6C")
        DisplayFrame.place(x=400, y=130,width=1000, height=600)

        def time1():
            time_string = time.strftime("%H:%M:%S")
            date_string = time.strftime("%d:%m:%y")
            clock.config(text="Time: "+time_string+"\n""Date: "+date_string, font =('Vogue', 15, 'bold'))
            clock.after(200, time1)

        clock = Label(DisplayFrame, font = ('vogue', 15, 'bold'), width = 15, relief = RIDGE, background = '#6C3200', foreground = 'white')
        clock.place(x = 700, y = 15, width = 150)
        time1()
        
#========= LABEL, DISPLAY AND ENTRY BOXES =========#
        
        self.lblCourseCode = Label(ManageFrame, font=("Vogue",15), justify='center',fg="white", bg="#003A6C", text="Course Code:", padx=5, pady=5)
        self.lblCourseCode.place(x=125,y=55)
        self.txtCourseCode = Entry(ManageFrame, font=("Times New Roman", 13), justify='center', textvariable=Code, width=37)
        self.txtCourseCode.place(x=40,y=85)
        

        self.lblCourseName = Label(ManageFrame, font=("Vogue",15), justify='center',fg="white", bg="#003A6C", text="Course Name:", padx=5, pady=5)
        self.lblCourseName.place(x=125,y=180)
        self.txtCourseName = Entry(ManageFrame, font=("Times New Roman", 13), justify='center', textvariable=Cname, width=37)
        self.txtCourseName.place(x=40,y=210)
        
        self.Search =  Label(DisplayFrame, font=("Vogue",13), justify='center',fg="white", bg="#003A6C", text="Course Code Search", padx=5, pady=5)
        self.Search.place(x=200, y= 28)
        self.SearchBar = Entry(DisplayFrame, font=("Times New Roman",12), justify='center', textvariable=SearchBarVar, width=25)
        self.SearchBar.place(x=400,y=30)
        



#========= TREE =========#
        
        scrollbar = Scrollbar(DisplayFrame, orient=VERTICAL)
        scrollbar.place(x=925,y=115,height=390)

        treecourse = ttk.Treeview(DisplayFrame,
                                        columns=("Course Code","Course Name"),
                                        height = 16,
                                        yscrollcommand=scrollbar.set)

        treecourse.heading("Course Code", text="Course Code", anchor=W)
        treecourse.heading("Course Name", text="Course Name",anchor=W)
        treecourse['show'] = 'headings'

        treecourse.column("Course Code", width=200, anchor=W, stretch=False)
        treecourse.column("Course Name", width=690, stretch=False)


        treecourse.place(x=30,y=115, height = 390, width = 890)
        scrollbar.config(command=treecourse.yview)
            
#========= BUTTONS =========#

        self.btnAddID = Button(ManageFrame, text="Add", font=('Vogue', 10), height=1, width=10,
                                bg="#DFE6E9", fg="#4A6274", command=addCourse)
        self.btnAddID.place(x=50,y=260)
        
        self.btnUpdate = Button(ManageFrame, text="Update", font=('Vogue', 10), height=1, width=10,
                                bg="#DFE6E9", fg="#4A6274", command=updateCourse) 
        self.btnUpdate.place(x=160,y=260)
        
        self.btnClear = Button(ManageFrame, text="Clear", font=('Vogue', 10), height=1, width=10,
                                bg="#DFE6E9", fg="#4A6274", command=clear)
        self.btnClear.place(x=270,y=260)
        
        self.btnDelete = Button(DisplayFrame, text="Delete", font=('Vogue', 10), height=1, width=10,
                                bg="#DFE6E9", fg="#4A6274", command=deleteCourse)
        self.btnDelete.place(x=850,y=70)
        
        self.btnSelect = Button(DisplayFrame, text="Select", font=('Vogue', 10), height=1, width=10,
                              bg="#DFE6E9", fg="#4A6274", command=editCourse)
        self.btnSelect.place(x=600,y=70)
        
        self.btnSearch = Button(DisplayFrame, text="Search", font=('Vogue', 10), height=1, width=10,
                               bg="#DFE6E9", fg="#4A6274", command=searchCourse)
        self.btnSearch.place(x=300,y=70)
        
        self.btnRefresh = Button(DisplayFrame, text="Show All", font=('Vogue', 10), height=1, width=10,
                              bg="#DFE6E9", fg="#4A6274", command=Refresh)
        self.btnRefresh.place(x=50,y=70)
        
        connectCourse()
        displayCourse()
        
        
        
        
        
        

class Student(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("Student Information System")
        centercolor = tk.Label(self,height = 8,width=600, bg="#003A6C")
        centercolor.place(x=0,y=5)
        apptitle = tk.Label(self, text="Student Information System", font=("Old English Text MT",48),bd=0,
                            bg="#003A6C",
                            fg="white",)
        apptitle.place(x=320,y=25)

        title2=Label(self, text = "SAINT CLAIRE'S ACADEMY", font = ('times', 20), foreground = 'white', background = '#003A6C')
        title2.place(x=550, y=5)
        

#========= INITIAL BUTTONS =========#
        Coursebutton = tk.Button(self, text="Course",font=("Old English Text MT",13),bd=0,
                                width = 10,
                                bg="#003A6C",
                                fg="white",
                                command=lambda: controller.show_frame(Course))
        Coursebutton.place(x=600,y=95)
        Coursebutton.config(cursor= "hand2")
            
        Studbutton= tk.Button(self, text="Student",font=("Old English Text MT",13),bd=0,
                                width = 10,
                                bg="#003A6C",
                                fg="white",
                                command=lambda: controller.show_frame(Student))
        Studbutton.place(x=700,y=95)
        Studbutton.config(cursor= "hand2")
        
#========= FUNCTIONS =========#
        FName = StringVar()
        ID = StringVar()
        MName = StringVar()
        SName = StringVar()
        YLevel = StringVar()
        Gender = StringVar()
        Searchbar=StringVar()
        CCode = StringVar()


        def connect():
            conn = sqlite3.connect("Undag_SSIS.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS studopt (ID  TEXT PRIMARY KEY, FName TEXT,\
                        MName TEXT, SName TEXT, CCode TEXT,\
                        YLevel TEXT, Gender TEXT,\
                        FOREIGN KEY(CCode) REFERENCES ccode(Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()  

        
        def addData():
            if ID.get() == "" or FName.get() == "" or MName.get() == "" or SName.get() == "" or CCode.get() == "" or YLevel.get() == "" or Gender.get() == "": 
                tkinter.messagebox.showinfo("Student Information System", "Please fill up the Box correctly")
            else:  
                ID1 = ID.get()
                ID1_list = []
                for i in ID1:
                    ID1_list.append(i)
                a = ID1.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID1_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("Student Information System", "ID is invalid\nIt should be in YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("Student Information System", "ID is invalid\nIt should be in YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("Student Information System", "ID is invalid\nIt should be in YYYY-NNNN")
                        else:
                            x = ID1.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("Student Information System", "ID is invalid")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("Student Information System", "ID is Invalid")
                                except:
                                    pass
                            else:
                                #try:
                                conn = sqlite3.connect("Undag_SSIS.db")
                                c = conn.cursor() 
                                c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                c.execute("INSERT INTO studopt(ID,FName,MName,SName,CCode,YLevel,Gender) VALUES (?,?,?,?,?,?,?)",\
                                              (ID.get(),FName.get(),MName.get(),SName.get(),CCode.get(),YLevel.get(),Gender.get()))                                      
                                                                       
                                tkinter.messagebox.showinfo("Student Information System", "Student Recorded")
                                conn.commit() 
                                clear()
                                displayData()
                                conn.close()
                                #except:
                                    #
                                    #tkinter.messagebox.showerror("Student Information System", "ID is Invalid")
                    else:
                        tkinter.messagebox.showerror("Student Information System", "ID is invalid")
                else:
                    tkinter.messagebox.showerror("Student Information System", "ID is Invalid")
                 
        def updateData():
            for selected in tree.selection():
                conn = sqlite3.connect("Undag_SSIS.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE studopt SET ID=?, FName=?, MName=?,SName=?,CCode=?, YLevel=?,Gender=?\
                      WHERE ID=?", ((ID.get(),FName.get(),MName.get(),SName.get(),CCode.get(),YLevel.get(),Gender.get(),\
                          tree.set(selected, '#1'))))
                conn.commit()
                tkinter.messagebox.showinfo("Student Information System", "Student Information is Updated")
                displayData()
                conn.close()
        
        def deleteData():   
            try:
                messageDelete = tkinter.messagebox.askyesno("Student Information System", "Do you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("Undag_SSIS.db")
                    cur = con.cursor()
                    x = tree.selection()[0]
                    id_no = tree.item(x)["values"][0]
                    cur.execute("DELETE FROM studopt WHERE ID = ?",(id_no,))                   
                    con.commit()
                    tree.delete(x)
                    tkinter.messagebox.showinfo("Student Information System", "Student is successfully deleted")
                    displayData()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def searchData():
            ID = Searchbar.get()
            try:  
                con = sqlite3.connect("Undag_SSIS.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM studopt WHERE ID = ?",(ID,))
                con.commit()
                tree.delete(*tree.get_children())
                rows = cur.fetchall()
                for row in rows:
                    tree.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("Student Information System", "ID is invalid")
            
                
        def displayData():
            tree.delete(*tree.get_children())
            conn = sqlite3.connect("Undag_SSIS.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM studopt")
            rows = cur.fetchall()
            for row in rows:
                tree.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
                            
        def editData():
            x = tree.focus()
            if x == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a record from the table.")
                return
            values = tree.item(x, "values")
            ID.set(values[0])
            FName.set(values[1])
            MName.set(values[2])
            SName.set(values[3])
            CCode.set(values[4])
            YLevel.set(values[5])
            Gender.set(values[6])
            
        def Refresh():
            displayData()
        
        def clear():
            ID.set('')
            FName.set('')
            MName.set('')
            SName.set('')
            CCode.set('')
            YLevel.set('')
            Gender.set('')

        con = sqlite3.connect("Undag_SSIS.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM ccode")
        books = cur.fetchall()
        bookid = []
        for book in books:
             bookid.append(book[0])




        ManageFrame=Frame(self, relief= GROOVE, borderwidth = 5, bg="#003A6C")
        ManageFrame.place(x=0, y=130,width=400, height=600)
        
        DisplayFrame=Frame(self, relief= GROOVE, borderwidth = 5, bg="#003A6C")
        DisplayFrame.place(x=400, y=130,width=1000, height=600)

        def time1():
            time_string = time.strftime("%H:%M:%S")
            date_string = time.strftime("%d:%m:%y")
            clock.config(text="Time: "+time_string+"\n""Date: "+date_string, font =('Vogue', 15, 'bold'))
            clock.after(200, time1)

        clock = Label(DisplayFrame, font = ('vogue', 15, 'bold'), width = 15, relief = RIDGE, background = '#6C3200', foreground = 'white')
        clock.place(x = 700, y = 15, width = 150)
        time1()


#========= LABEL AND ENTRY BOXES =========#
        
        self.StudentID = Label(ManageFrame, font=("Vogue",14),fg="snow", bg="#003A6C", text="STUDENT ID:", padx=5, pady=5)
        self.StudentID.place(x=150,y=8)
        self.StudentIDEntry = Entry(ManageFrame, font=("Times New Roman", 13), justify='center', textvariable=ID, width=35)
        self.StudentIDEntry.place(x=40,y=40)
        self.StudentIDEntry.insert(0,'YYYY-NNNN')
        

        self.Firstname = Label(ManageFrame, font=("Vogue",14),fg="white", bg="#003A6C", text="FIRST NAME:", padx=5, pady=5)
        self.Firstname.place(x=150,y=67)
        self.FirstnameEntry = Entry(ManageFrame, font=("Times New Roman", 13), justify='center', textvariable=FName, width=35)
        self.FirstnameEntry.place(x=40,y=100)

        self.Midname = Label(ManageFrame, font=("Vogue",14),fg="white", bg="#003A6C", text="MIDDLE INITIAL:", padx=5, pady=5)
        self.Midname.place(x=150,y=127)
        self.MidnameEntry = Entry(ManageFrame, font=("Times New Roman", 13), justify='center', textvariable=MName, width=35)
        self.MidnameEntry.place(x=40,y=160)

        self.Surname = Label(ManageFrame, font=("Vogue",14),fg="white", bg="#003A6C",text="SURNAME:", padx=5, pady=5)
        self.Surname.place(x=150,y=187)
        self.SurnameEntry = Entry(ManageFrame, font=("Times New Roman", 13), justify='center', textvariable=SName, width=35)
        self.SurnameEntry.place(x=40,y=220)

        self.Course = Label(ManageFrame, font=("Vogue",14), fg="white", bg="#003A6C",text="COURSE:", padx=5, pady=5)
        self.Course.place(x=150,y=247)
        self.CourseEntry =ttk.Combobox(ManageFrame,
                                                value=bookid,
                                                state="readonly", justify='center', font=("Times New Roman", 13), textvariable=CCode, width=33)
        self.CourseEntry.place(x=40,y=280)
        

        self.StudentYearLevel = Label(ManageFrame, font=("Vogue",14),fg="white", bg="#003A6C", text="YEAR LEVEL:", padx=5, pady=5)
        self.StudentYearLevel.place(x=150,y=312)
        self.StudentYearLevelEntry = ttk.Combobox(ManageFrame,
                                                value=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"],
                                                state="readonly", justify='center', font=("Times New Roman", 13), textvariable=YLevel,
                                                width=33)
        self.StudentYearLevelEntry.place(x=40,y=345)
        

        self.Gender = Label(ManageFrame, font=("Vogue",14),fg="white", bg="#003A6C", text="GENDER:", padx=5, pady=5)
        self.Gender.place(x=150,y=377)
        self.GenderEntry = ttk.Combobox(ManageFrame, value=["Male", "Female"], font=("Times New Roman", 13),
                                             state="readonly", justify='center', textvariable=Gender, width=33)
        self.GenderEntry.place(x=40,y=410)

        self.Search =  Label(DisplayFrame, font=("Vogue",13),fg="white", bg="#003A6C", text="Search by ID Number", padx=5, pady=5)
        self.Search.place(x=150, y= 28)
        self.SearchBar = Entry(DisplayFrame, font=("Times New Roman",12), justify='center', textvariable=Searchbar, width=29)
        self.SearchBar.place(x=350,y=30)
        self.SearchBar.insert(0,'YYYY-NNNN')
       
        

#========= TREE =========#
        
        scrollbar = Scrollbar(DisplayFrame, orient=VERTICAL)
        scrollbar.place(x=925,y=115,height=390)

        tree = ttk.Treeview(DisplayFrame,
                            columns=("ID Number", "First Name","Mid Initial","Surname", "Course", "Year Level", "Gender"),
                            height = 16,
                            yscrollcommand=scrollbar.set)

        tree.heading("ID Number", text="ID Number", anchor="center")
        tree.heading("First Name", text="First Name",anchor="center")
        tree.heading("Mid Initial", text="Middle Initial",anchor="center")
        tree.heading("Surname", text="Surname",anchor="center")
        tree.heading("Course", text="Course",anchor="center")
        tree.heading("Year Level", text="Year Level",anchor="center")
        tree.heading("Gender", text="Gender",anchor="center")
        tree['show'] = 'headings'

        tree.column("ID Number", width=127, anchor=W, stretch=False)
        tree.column("First Name", width=127, stretch=False)
        tree.column("Mid Initial", width=127, stretch=False)
        tree.column("Surname", width=127, stretch=False)
        tree.column("Course", width=127, anchor=W, stretch=False)
        tree.column("Year Level", width=127, anchor=W, stretch=False)
        tree.column("Gender", width=127, anchor=W, stretch=False)

        tree.place(x=30,y=115, height = 390, width = 890)
        scrollbar.config(command=tree.yview)
        
#========= BUTTONS =========#
        
        btnAddID = Button(ManageFrame, text="Add", font=('Vogue', 11), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=addData)
        btnAddID.place(x=50,y=450)
        btnAddID.config(cursor= "hand2")
        
        btnUpdate = Button(ManageFrame, text="Update", font=('Vogue', 11), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=updateData)
        btnUpdate.place(x=250,y=450)
        btnUpdate.config(cursor= "hand2")
        
        btnClear = Button(ManageFrame, text="Clear", font=('Vogue', 11), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=clear)
        btnClear.place(x=50,y=480)
        btnClear.config(cursor= "hand2")
        
        btnDelete = Button(ManageFrame, text="Delete", font=('Vogue', 11), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=deleteData)
        btnDelete.place(x=250,y=480)
        btnDelete.config(cursor= "hand2")
        
        btnSelect = Button(DisplayFrame, text="Select", font=('Vogue', 10), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=editData)
        btnSelect.config(cursor= "hand2")
        btnSelect.place(x=240,y=70)
        
        btnSearch = Button(DisplayFrame, text="Search", font=('Vogue', 10), height=1, width=10,
                                bg="#DFE6E9", fg="#4A6274", command=searchData)
        btnSearch.place(x=420,y=70)
        
        btnDisplay = Button(DisplayFrame, text="Show All", font=('Vogue', 10), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=Refresh)
        btnDisplay.place(x=620,y=70)
        btnDisplay.config(cursor= "hand2")
        connect()
        displayData()

ssis = SSIS()
ssis.geometry("1355x650+0+0")
ssis.resizable(False,False)
ssis.mainloop()