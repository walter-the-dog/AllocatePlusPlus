import datetime
#for date time calculations and fetching the current time
import email
#for email related functions
import os
#os is used for running shell commands and for deleteing files
import random
#random is used for OTP
import re
#regex is used for checking for appended "BOUND:" or "ENROLLED:" , this saves processing power of having to itirate the entire enrolement list
import sys
#sys is used to exit the program
import tkinter
#tkinter is used for all gui related functions
import urllib
#urllib is used to fetch data from the internet
import time
#time is used to make the program wait for a certain duration of seconds
from email.mime.multipart import MIMEMultipart
#email related function
from email.mime.text import MIMEText
#email related function
from time import localtime, strftime
#localtime provides the current time and strftime provides formatting options
from tkinter import messagebox, ttk
#ttk is used for combo boxes and other Newer tkinter objects. messageboxes are used to generate messages to the users using a gui interface
import smtplib
#smtplib is used to connect to email servers using SMTP protocol
import ctypes
#ctypes is used to communicate with windows and fetch window titles
import poplib
#poplib is used to connect to email servers using POP protocol
from email import parser
#email related function
from email.parser import Parser
#email related function
from email.header import decode_header
#email related function
from email.utils import parseaddr
#email related function
import subprocess
#sub process is used to run shell commands and get the output without opening the shell as a gui
import urllib.request
'''
file explanations
users.csv = username,password,subject.class,role,email
subjects.csv = subjectname,classname,max,DD:MM:YYYY(dayfrom).DD:MM:YYYY(dayto).HH:MM(timefrom).HH:MM(timeto).RepeatState,restrictedcheck,teacherbound
roles.csv = rolename,rolelevel,canbindtoclass.canmanageroles.canaddusers.candeleteusers.canjoinrestricted.canmanageclass
waitlist.csv = username , subject name , classname

--------------------------------------------------------------------------------------------------------------------------------
Date Created :- 28th May 2020 , 9:41PM
Project Name:- Allocate++
Project Owner:- walter-the-dog
Purpose:- A system designed to enrol students to subjects and also check for class clashes
--------------------------------------------------------------------------------------------------------------------------------
'''
#Approved text in usernames , role names, subject names, class names
approved_text = set("abcdefghijlkmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
#row length globals
userLEN = 5
subjectLEN = 6
roleLEN = 3
waitlistLEN = 3
#Almost all single letter variables are itirables
CRED = '\033[91m'
CEND = '\033[0m'
CGREEN = '\33[32m'
'''
Module Name:-QuickieSort
Module Purpose:- Sorts a list
Module Arguments:- lst(List to sort)
Module Inputs:- list
Module Outputs:- sorted list
'''
def QuickieSort(lst):
    #list sorting is more messy than category. Subjects and classes needs to be passed as SubjectClass ie MathsS9. Categorical would be defaulted
    def partition(sort_list, low, high):
        i = (low -1)
        pivot = sort_list[high]
        for j in range(low, high):
            if sort_list[j] <= pivot:
                i += 1
                sort_list[i], sort_list[j] = sort_list[j], sort_list[i]
        sort_list[i+1],sort_list[high] = sort_list[high], sort_list[i+1]
        return (i+1)
            
    def quick_sort(sort_list, low, high):
        if low < high:
            pi = partition(sort_list, low, high)
            quick_sort(sort_list, low, pi-1)
            quick_sort(sort_list, pi+1, high)
    low = 0
    high = len(lst) - 1
    quick_sort(lst, low, high)
    return lst
'''
Module Name:- CheckOpen
Module Purpose:- Retrieves a list of open windows and checks whether a certain window is open
Module Arguments:- windowtitle(The title of the window to look for)
Module Inputs:- Window title
Module Outputs:- True or False
'''
def CheckOpen(windowtitle):
    #gets windows using ctypes
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    #gets the titles
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    #gets the windows that are accessible by the user
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    
    titles = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    k = 0
    while k < len(titles):
        if titles[k] == "":
            del titles[k]
            continue
        if titles[k] == windowtitle:
            print(CRED+"Windows already open!!"+CEND)
            return True
        k+=1
    return False
'''
Module Name:- binarySearchAppr
Module Purpose:- To conduct a binary search for a peice of data in a array
Module Arguments:- arr(array to search) , start(the location to start searching from) , end(location to stop searching to) , x (the item to look for)
Module Inputs:- array and what to search for
Module Outputs:- true or false
'''
def binarySearchAppr (arr, start, end, x): 
                    
    # check condition
    if end >= start:

        mid = start + (end- start)//2

        # If element is present at the middle
        try:
            if arr[mid] == x: 
                
                return True

            # If element is smaller than mid
            elif arr[mid] > x: 
                return binarySearchAppr(arr, start, mid-1, x) 

            # Else the element greator than mid
            else: 
                return binarySearchAppr(arr, mid+1, end, x) 
        except:
            return False
    else: 
        # Element is not found in the array 
        return False
'''
Module Name:- AuthMod
Module Purpose:- To authenticate a user and checks whether they have permissions
Module Arguments:- user(the username) and perm(the permission number)
Module Inputs:- Username and permission id , User data information , Role permission information
Module Outputs:- True or False
'''
def AuthMod(user,perm):
    #this module is used to authenticate modules and check whether the user has enough permissions to access the module
    #user = username
    #perm = Perm Number to check. not list count but normal count starting from 1
    file=open("users.csv","r+")
    userLines=file.readlines()
    file.close()
    print(CGREEN+f"Checking perm id:{perm} for {user}"+CEND)
    file = open("roles.csv","r+")
    roleLines=file.readlines()
    file.close()
    #admin user has all perms by default
    if user == "admin":
        return True
    i = 0
    tempRole = ""
    while i<len(userLines):
        
        if len(userLines[i].split(',')) != userLEN:
            i+=1
            continue

        if userLines[i].split(',')[0] == user:
            tempRole = userLines[i].split(',')[3].strip()
            break
        i+=1
    i = 0
    while i<len(roleLines):
        if len(roleLines[i].split(',')) != roleLEN:
            i+=1
            continue
        if roleLines[i].split(',')[0] == tempRole:
            rol = int(roleLines[i].split(',')[2].split(".")[perm-1])
            if bool(rol):
                return True
            else:
                return False
        i+=1
    #this messagebox is used for debugging purposes , normally a invalid user cannot be passed onto this module
    messagebox.showerror("Error","User not defined. User given:"+user)
    return False
'''
Module Name:- manageClass
Module Purpose:- To show the options related to managing classes
Module Arguments:- The current user who is logged in
Module Inputs:- Current logged in
Module Outputs:- Manage Class tkinter window which acts as a portal to AddClass , EditClass and DeleteClass
'''
def manageClass(user):
    #Manage Class Screen
    #This screen is used to display 3 options to modify classes, add , edit , delete.
    if CheckOpen("Manage Classes"):
        return False
    manageClassWindow = tkinter.Toplevel(loginScreen)
    manageClassWindow.title("Manage Classes")
    manageClassWindow.resizable(0,0)
    tkinter.Label(manageClassWindow,text="Click on the buttons to perform a action",fg="blue").grid(column=1,row=0)
    print(CGREEN+"Manage class window intialised!"+CEND)
    #Add Class Module
    '''
    Module Name:- AddClass
    Module Purpose:- To open a dialog to add a class to the system
    Module Arguments:- None
    Module Inputs:- None
    Module Outputs:- Tkinter window with a add class form
    '''
    def AddClass():
        #This module is used to add classes to the system. Takes no arguments
        global selectedTeacher
        global closeAddClassScreen
        #Globals used to close
        if CheckOpen("Add Class"):
            return False
        selectedTeacher = ""
        #initializes global selected teacher which is modified by Bind User To Class
        AddClassScreen = tkinter.Toplevel(loginScreen)
        AddClassScreen.resizable(0,0)
        AddClassScreen.title("Add Class")
        print(CGREEN+"Add Class screen initialised!"+CEND)
        #Initialize window elements        
        tkinter.Label(AddClassScreen,text="Fill out the form to add a class",fg="green").grid(column=1,row=0)
        tkinter.Label(AddClassScreen,text="A subject would be\nmade if it doesnt exist").grid(column=2,row=2)
        tkinter.Label(AddClassScreen,text="Subject:").grid(column=0,row=1)
        SubjectEntry = tkinter.Entry(AddClassScreen,width=23)
        SubjectEntry.grid(column=1,row=1)

        tkinter.Label(AddClassScreen,text="Class:").grid(column=0,row=2)
        ClassEntry = tkinter.Entry(AddClassScreen,width=23)
        ClassEntry.grid(column=1,row=2)

        tkinter.Label(AddClassScreen,text="Maximum Space:").grid(column=0,row=3)
        MaxEntry = tkinter.Entry(AddClassScreen,width=23)
        MaxEntry.grid(column=1,row=3)

        tkinter.Label(AddClassScreen,text="Restricted?").grid(column=0,row=4)
        RestrictedCheck = ttk.Checkbutton(AddClassScreen)
        RestrictedCheck.state(['!alternate'])
        RestrictedCheck.grid(column=1,row=4)

        tkinter.Label(AddClassScreen,text="From Date(DD/MM/YYYY):").grid(column=0,row=5)

        FromDayCombo = ttk.Combobox(AddClassScreen,state='readonly')
        FromDayCombo.grid(column=1,row=5)

        FromMonthCombo = ttk.Combobox(AddClassScreen,state='readonly',values=list(range(1,13)))
        FromMonthCombo.grid(column=2,row=5)

        FromYearCombo = ttk.Combobox(AddClassScreen,state='readonly')
        FromYearCombo.grid(column=3,row=5)

        
        tkinter.Label(AddClassScreen,text="To Date(DD/MM/YYY):").grid(column=0,row=6)
        ToDayCombo = ttk.Combobox(AddClassScreen,state='readonly')
        ToDayCombo.grid(column=1,row=6)

        ToMonthCombo = ttk.Combobox(AddClassScreen,state='readonly',values=list(range(1,13)))
        ToMonthCombo.grid(column=2,row=6)

        ToYearCombo = ttk.Combobox(AddClassScreen,state='readonly')
        ToYearCombo.grid(column=3,row=6)

        tkinter.Label(AddClassScreen,text="Time From(HH:MM)").grid(column=0,row=7)
        FromHourCombo = ttk.Combobox(AddClassScreen,state='readonly',value=list(range(0,24)))
        FromHourCombo.grid(column=1,row=7)

        FromMinuteCombo = ttk.Combobox(AddClassScreen,state='readonly',values=list(range(0,60)))
        FromMinuteCombo.grid(column=2,row=7)

        tkinter.Label(AddClassScreen,text="Time To(HH:MM)").grid(column=0,row=8)
        ToHourCombo = ttk.Combobox(AddClassScreen,state='readonly',values=list(range(0,24)))
        ToHourCombo.grid(column=1,row=8)

        ToMinuteCombo = ttk.Combobox(AddClassScreen,state='readonly',values=list(range(0,60)))
        ToMinuteCombo.grid(column=2,row=8)

        tkinter.Label(AddClassScreen,text="Repeat On:").grid(column=0,row=9)
        RepeatCombo = ttk.Combobox(AddClassScreen,values=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","Everyday"],state='readonly')
        RepeatCombo.grid(column=1,row=9)
        tkinter.Label(AddClassScreen,text="Teacher Bind:").grid(column=0,row=10)
        '''
        Module Name:- BindUserToClass
        Module Purpose:- To bind a user to a new class
        Module Arguments :- None
        Module inputs:- user information and class information
        Module outputs:- A window with a table of potential users that can be bound to a class
        '''
        def BindUserToClass():
            #this function allows the user to bind a teacher to a new class , all in one window.
            global BindUserToClassScreen
            global closeBindUser
            #check open is used to prevent duplicate windows from being spammed
            if CheckOpen("Bind a Teacher"):return False
            BindUserToClassScreen = tkinter.Toplevel(loginScreen)
            BindUserToClassScreen.resizable(0,0)
            BindUserToClassScreen.title("Bind a Teacher")

            tkinter.Label(BindUserToClassScreen,text="Double Click to Bind",fg='purple').grid(column=1,row=0)
            print(CGREEN+"Bind user to class screen intiailised"+CEND)
            #frame is used to store the x scroll and y scroll and treeview. These needs to use pack features which cannot be done in a screen(the screen uses grid)
            BindUserToClassTreeFrame = tkinter.Frame(BindUserToClassScreen)
            BindUserToClassTree = ttk.Treeview(BindUserToClassTreeFrame)
            BindUserToClassTree.heading("#0",text="User/Role")

            YScrollBindUser = tkinter.Scrollbar(BindUserToClassTreeFrame,orient=tkinter.VERTICAL,command=BindUserToClassTree.yview)
            BindUserToClassTree.configure(yscrollcommand=YScrollBindUser.set)
            XScrollBindUser = tkinter.Scrollbar(BindUserToClassTreeFrame,orient=tkinter.HORIZONTAL,command=BindUserToClassTree.xview)
            BindUserToClassTree.configure(xscrollcommand=XScrollBindUser.set)
            
            #these elements are packed to provide the intuitive x and y scroll bar
            YScrollBindUser.pack(side=tkinter.RIGHT,fill=tkinter.Y)
            XScrollBindUser.pack(side=tkinter.BOTTOM,fill=tkinter.X)
            BindUserToClassTree.pack(side=tkinter.TOP,expand='false')

            BindUserToClassTreeFrame.grid(column=1,row=1)
            '''
            name:RefreshBindUserTree
            purpose:Refreshes the bind user table with data of potential users that can bind
            args:none
            inputs:user data , authmod
            outputs:refreshed table
            '''
            def RefreshBindUserTree():
                #Purpose is to wipe and refresh table
                BindUserToClassTree.delete(*BindUserToClassTree.get_children())

                file = open("users.csv","r+")
                userLines = file.readlines()
                file.close()

                i = 0
                toInsert = []
                while i<len(userLines):
                    row = userLines[i].split(',')
                    if len(row)!=userLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t]=row[t].strip()
                    givenUser = row[0]
                    givenRole = row[3]
                    if AuthMod(givenUser,1):
                        #uses authmod to check whether the user has permissions to bind to a class
                        toInsert.append((givenUser,givenRole))
                    i+=1
                i = 0
                while i<len(toInsert):
                    #gets existing parents
                    existingRoles = BindUserToClassTree.get_children()
                    name,role = toInsert[i]
                    print(CGREEN+f"Inserted {name} to table"+CEND)
                    if len(existingRoles) == 0:
                        #used to optimize the algo by executing this peice of code to skip the first run
                        tempID = BindUserToClassTree.insert("",tkinter.END,text=role)
                        BindUserToClassTree.insert(tempID,tkinter.END,text=name)
                        i+=1
                        continue
                    k= 0
                    t=False
                    while k<len(existingRoles):
                        if BindUserToClassTree.item(existingRoles[k])['text'] == role:
                            #itirates and if a  parent is found , inserts a child onto that parent row.
                            BindUserToClassTree.insert(existingRoles[k],tkinter.END,text=name)
                            #t is used to continue to loop
                            t = True
                            break
                        k+=1
                    if t:
                        i+=1
                        continue
                    else:
                        tempID = BindUserToClassTree.insert("",tkinter.END,text=role)
                        BindUserToClassTree.insert(tempID,tkinter.END,text=name)
                    i+=1
                print(CGREEN+"Bind Tree refreshed!"+CEND)
            RefreshBindUserTree()
            '''
            name:SearchBindTree
            purpose:provide a form to search the bind tree
            args:none
            inputs:none
            outputs:window with a form to search bind tree
            '''
            def SearchBindUserTree():
                #search function to look up roles and users
                global SearchBindTreeScreen
                if CheckOpen("Search BindUserTree3"):
                    return False
                SearchBindTreeScreen = tkinter.Toplevel(loginScreen)
                SearchBindTreeScreen.resizable(0,0)
                SearchBindTreeScreen.title("Search BindUserTree3")
                #initializing elements
                tkinter.Label(SearchBindTreeScreen,text="Fill the Form",fg='blue').grid(column=1,row=0)
                tkinter.Label(SearchBindTreeScreen,text="Search What:").grid(column=0,row=1)
                SearchWhatEntry = tkinter.Entry(SearchBindTreeScreen,width=23)
                SearchWhatEntry.grid(column=1,row=1)
                tkinter.Label(SearchBindTreeScreen,text="Search Where:").grid(column=0,row=2)
                SearchWhereCombo = ttk.Combobox(SearchBindTreeScreen,values=["Users","Roles"],state='readonly')
                SearchWhereCombo.set("Users")
                SearchWhereCombo.grid(column=1,row=2)
                tkinter.Label(SearchBindTreeScreen,text="Search How:").grid(column=0,row=3)
                SearchHowCombo = ttk.Combobox(SearchBindTreeScreen,values=["Binary","Linear"],state='readonly')
                SearchHowCombo.set("Linear")
                SearchHowCombo.grid(column=1,row=3)
                print(CGREEN+"Search Bind Tree Screen Initialised!"+CEND)
                '''
                name:SearchConfirmUserBind
                purpose:searches the bind user tree using provided criteria in the form
                args:none
                inputs:search what(what to look for) , search where(where to look for the data(users/roles)) , search how(binary/linear)
                outputs:item highlighted or error thrown
                '''
                def SearchConfirmUserBind():
                    #search algorithm for BindUserToClassTree
                    SearchWhat = SearchWhatEntry.get()
                    SearchWhere = SearchWhereCombo.get()
                    SearchHow = SearchHowCombo.get()
                    #GIGO prevention
                    if SearchWhat == "" or SearchWhere == "" or SearchHow == "":
                        print(CRED+"Missing data!"+CEND)
                        messagebox.showerror("Error","Fill the form and try again")
                        return False
                    #gets the parents
                    existingRoles = BindUserToClassTree.get_children()
                    if SearchHow == "Linear":
                        if SearchWhere == "Users":
                            i = 0
                            while i<len(existingRoles):
                                #gets the children
                                existingUsers = BindUserToClassTree.get_children(existingRoles[i])
                                k = 0
                                while k<len(existingUsers):
                                    if BindUserToClassTree.item(existingUsers[k])['text'] == SearchWhat:
                                        print(CGREEN+"item found"+CEND)
                                        #Highlights item in table
                                        BindUserToClassTree.item(existingRoles[i],open=True)
                                        BindUserToClassTree.focus(existingUsers[k])
                                        BindUserToClassTree.selection_set(existingUsers[k])
                                        SearchWhatEntry.delete(0,tkinter.END)
                                        messagebox.showinfo("Success","Item has been highlighted in the treeview")
                                        return False
                                    k+=1
                                i+=1
                            #Shows a error if the loop was unable to find user
                            print(CRED+"Item not found!"+CEND)
                            messagebox.showerror("Error","Unable to find user")
                            SearchWhatEntry.delete(0,tkinter.END)
                            return False
                        else:
                            i = 0
                            while i<len(existingRoles):
                                if BindUserToClassTree.item(existingRoles[i])['text'] == SearchWhat:
                                    #Highlighted in table
                                    print(CGREEN+"item found"+CEND)
                                    BindUserToClassTree.focus(existingRoles[i])
                                    BindUserToClassTree.selection_set(existingRoles[i])
                                    SearchWhatEntry.delete(0,tkinter.END)
                                    messagebox.showinfo("Sucess","Item has been highlighted in the treeview")
                                    return False
                                i+=1
                            #Throws error if the loop cannot find criteria
                            print(CRED+"Unable to find role"+CEND)
                            messagebox.showerror("Error","Unable to find role")
                            SearchWhatEntry.delete(0,tkinter.END)
                            return False
                    else:
                        if SearchWhere == "Users":
                            i = 0
                            while i<len(existingRoles):
                                existingChildren = BindUserToClassTree.get_children(existingRoles[i])
                                newExistingChildren = []
                                for t in range(len(existingChildren)):newExistingChildren.append(BindUserToClassTree.item(existingChildren[t])['text'])
                                newExistingChildren = QuickieSort(newExistingChildren)
                                #binarysearchAppr returns true if item is found and false if the item is not found
                                if binarySearchAppr(newExistingChildren,0,len(newExistingChildren)-1,SearchWhat):
                                    print(CGREEN+"User found"+CEND)
                                    for p in existingChildren:
                                        if BindUserToClassTree.item(p)['text'] == SearchWhat:
                                            #executes a quick linear search to get id and highlight in table
                                            BindUserToClassTree.item(existingRoles[i],open=True)
                                            BindUserToClassTree.focus(p)
                                            BindUserToClassTree.selection_set(p)
                                            SearchWhatEntry.delete(0,tkinter.END)
                                            messagebox.showinfo("Success","User has been highlighted in treeview")
                                            return False
                                i+=1
                            #throws error if the loop cannot find user
                            print(CRED+"Unable to find user"+CEND)
                            messagebox.showerror("Error","Unable to find user")
                            SearchWhatEntry.delete(0,tkinter.END)
                            return False
                        else:
                            newExistingRoles = []
                            #newExistingRoles contains the 
                            for t in range(len(existingRoles)):newExistingRoles.append(BindUserToClassTree.item(existingRoles[t])['text'])
                            newExistingRoles = QuickieSort(newExistingRoles)
                            #binarySearchAppr returns true and false if the item exists
                            if binarySearchAppr(newExistingRoles,0,len(newExistingRoles)-1,SearchWhat):
                                print(CRED+"")
                                for t in existingRoles:
                                    if BindUserToClassTree.item(t)['text'] == SearchWhat:
                                        messagebox.showinfo("Success","Role has been highlighted in treeview")
                                        BindUserToClassTree.focus(t)
                                        BindUserToClassTree.selection_set(t)
                                        return False
                            else:
                                #throws error if it doesnt exist
                                messagebox.showerror("Error","Unable to find role")
                                SearchWhatEntry.delete(0,tkinter.END)
                                return False
                tkinter.Button(SearchBindTreeScreen,text="Search..",fg='blue',command=SearchConfirmUserBind).grid(column=1,row=4)
            tkinter.Button(BindUserToClassScreen,text="Search..",fg='blue',bd=0,command=SearchBindUserTree).grid(column=0,row=2)
            '''
            name:SortBindUserTree
            purpose:sort the bind user tree
            inputs:bind user data columns
            outputs:bind user data columns sorted
            '''
            def SortBindUserTree():
                #Sorts the items using QuickSort
                existingRoles = BindUserToClassTree.get_children()
                newExistingRoles = []
                for t in range(len(existingRoles)):newExistingRoles.append(BindUserToClassTree.item(existingRoles[t])['text'])
                newExistingRoles=QuickieSort(newExistingRoles)
                finalInsert = []
                for o in newExistingRoles:
                    for n in existingRoles:
                        if BindUserToClassTree.item(n)['text'] == o:
                            #o is the true role name and n is the itirated row id.
                            existingChildren = BindUserToClassTree.get_children(n)
                            #gets children of n(users of role o)
                            newExistingChildren = []
                            for t in range(len(existingChildren)):newExistingChildren.append(BindUserToClassTree.item(existingChildren[t])['text'])
                            newExistingChildren = QuickieSort(newExistingChildren)
                            #appends them to final insert
                            finalInsert.append((o,newExistingChildren))
                i = 0
                BindUserToClassTree.delete(*BindUserToClassTree.get_children())
                #wipes table and prepares to insert
                while i<len(finalInsert):
                    #role :- str
                    #children :-list
                    role,children = finalInsert[i]
                    #gets existingRoles
                    existingRoles = BindUserToClassTree.get_children()
                    if len(existingRoles) == 0:
                        #gets tempID(id returned by Insert) of the role that was just inserted
                        tempID=BindUserToClassTree.insert("",tkinter.END,text=role)
                        k = 0
                        while k<len(children):
                            #inserts the children to that role
                            BindUserToClassTree.insert(tempID,tkinter.END,text=children[k])
                            k+=1
                        i+=1
                        continue
                    k = 0
                    a = False
                    #existing roles are itirated to check whether the role already exists or not
                    while k<len(existingRoles):
                        if BindUserToClassTree.item(existingRoles[k])['text'] == role:
                            j = 0
                            while j<len(children):
                                BindUserToClassTree.insert(existingRoles[k],tkinter.END,text=children[j])
                                j+=1
                            a = True
                        k+=1
                    if a:
                        i+=1
                        continue
                    else:
                        #if not found , insert a new one
                        tempID = BindUserToClassTree.insert("",tkinter.END,text=role)
                        k = 0
                        while k<len(children):
                            BindUserToClassTree.insert(tempID,tkinter.END,text=children[k])
                            k+=1
                    i+=1
                messagebox.showinfo("Success","Sorted using QuickSort")
            tkinter.Button(BindUserToClassScreen,text="Sort..",fg='blue',bd=0,command=SortBindUserTree).grid(column=2,row=2)
            '''
            name:CloseBindUser
            purpose:close the child windows
            inputs:none
            outputs:close commands sent to all children
            '''
            def closeBindUser():
                #used to imitate parent-children inheritance by closing Search screen when the parent is closed
                global SearchBindTreeScreen
                try:
                    SearchBindTreeScreen.destroy()
                except:
                    pass
                BindUserToClassScreen.destroy()
            BindUserToClassScreen.protocol("WM_DELETE_WINDOW",closeBindUser)
            '''
            name:BindUserToClassCONFIRM
            purpose:Bind a user to class
            inputs:Authmod
            outputs:user bound to global
            '''
            def BindUserToClassCONFIRM(event):
                #Bind user to class confirmation that occurs when the user is double clicked
                global selectedTeacher
                try:
                    #checks whether a user was clicked or not. The <Double-1> event triggers when the table is clicked , therefore , checks are required to see whether a user is clicked and not a role or a blank space
                    givenUser = BindUserToClassTree.item(BindUserToClassTree.focus())['text']
                    if BindUserToClassTree.parent(BindUserToClassTree.focus()) == "":
                        return False
                except:
                    return False
                #Uses regex to check whether BOUND: is appended at the start of the given user string.
                if re.search("^BOUND:",givenUser):
                    if messagebox.askyesno("Confirm","Are you sure you want to unbind this user?"):
                        #clears Selected Teacher global
                        selectedTeacher = ""
                        #returns user to normal and removes append
                        past = BindUserToClassTree.item(BindUserToClassTree.focus())['text']
                        past = re.sub("^BOUND:","",past)
                        BindUserToClassTree.item(BindUserToClassTree.focus(),text=past)
                        messagebox.showinfo("Success","Successfully completed")
                        return False
                    else:
                        return False
                existingRoles=BindUserToClassTree.get_children()
                existingChildren = []
                ids = []
                i = 0
                while i<len(existingRoles):
                    #gets ids
                    existingTemp=BindUserToClassTree.get_children(existingRoles[i])
                    for t in range(len(existingTemp)):
                        existingChildren.append(BindUserToClassTree.item(existingTemp[t])['text'])
                        ids.append(existingTemp[t])
                    i+=1
                i=0
                while i<len(existingChildren):
                    if re.search("^BOUND:",existingChildren[i]):
                        if messagebox.askyesno("Confirm","A user is already bound to this class. Do you want to unbind him?"):
                            #You cannot bind more than 1 teacher to a class. This is used to prevent that from happening
                            BindUserToClassTree.item(ids[i],text=selectedTeacher)
                            past = BindUserToClassTree.item(BindUserToClassTree.focus())['text']
                            BindUserToClassTree.item(BindUserToClassTree.focus(),text="BOUND:"+past)
                            selectedTeacher = past
                            #binds new user and unbinds 
                            messagebox.showinfo("Success","User unbound and new user has been bounded!")
                            return False
                        else:
                            return False
                    i+=1
                #binds user
                selectedTeacher = givenUser
                past = BindUserToClassTree.item(BindUserToClassTree.focus())['text']
                BindUserToClassTree.item(BindUserToClassTree.focus(),text="BOUND:"+past)
                messagebox.showinfo("Success","User has been selected as teacher. Finish the setup to add the teacher")
            BindUserToClassTree.bind("<Double-1>",BindUserToClassCONFIRM)
        BindButton = tkinter.Button(AddClassScreen,text="Bind..",fg='blue',command=BindUserToClass,bd=0)
        BindButton.grid(column=1,row=10)
        '''
        Module Name :- Refresh_AddClass
        Module Purpose:- Clears and refreshes form
        Module Arguments:- None
        Module Inputs:- current date and time
        Module outputs:- cleared boxes and reconfigured combo boxes.
        '''
        def Refresh_AddClass():
            #refresh function used to clear form.
            SubjectEntry.delete(0,tkinter.END)
            ClassEntry.delete(0,tkinter.END)
            MaxEntry.delete(0,tkinter.END)
            #datetime.datetime.now() returns a dictionary and strftime reads that dictionary with a key(eg:- "%d")
            currentDay = datetime.datetime.now().strftime("%d")
            currentMonth = datetime.datetime.now().strftime("%m")
            currentYear = datetime.datetime.now().strftime("%Y")
            currentWeekday = datetime.datetime.now().strftime("%A")
            currentHour = datetime.datetime.now().strftime("%H")
            currentMinute = datetime.datetime.now().strftime("%M")
            print(CGREEN+f"Current time {currentYear}/{currentMonth}/{currentDay} , {currentHour}:{currentMinute}. {currentWeekday}"+CEND)
            #setting the combo boxes is vital to prevent null input
            FromMinuteCombo.set(str(int(currentMinute)))
            FromHourCombo.set(str(int(currentHour)))
            FromYearCombo.set(str(int(currentYear)))
            FromDayCombo.set(str(int(currentDay)))
            FromMonthCombo.set(str(int(currentMonth)))
            MonthsWith31 = [1,3,5,7,8,10,12]
            #date max is used to figure out the days in the month, this changes depending on leap years , february and 31 months
            datemax = 30
            if int(currentMonth) in MonthsWith31:
                datemax=31
            elif int(currentMonth) == 2:
                if int(FromYearCombo)%4==0:
                    datemax=29
                else:
                    datemax=28
            #proceeds to add 5 minutes to the initial time. This 5 minutes is added onto the current Minute.
            '''
            if the current minute is larger than 60 , it adds 1 to current hours 
            but if current hours is larger than 24 , it adds 1 to current day
            but if current day is larger than date max(months in the year) it adds 1 to current month 
            but if the current month is larger than 12 , it adds 1 to the current year
            '''
            if int(currentMinute)+5>=60:
                if int(currentHour)+1>=24:
                    if int(currentDay)+1>datemax:
                        if int(currentMonth)+1>12:
                            currentYear = int(currentYear)+1
                            currentDay = 1
                            currentMonth = 1
                            currentMinute = int(currentMinute)-55
                            currentHour = int(currentHour)-23
                        else:
                            currentMonth = int(currentMonth)+1
                            currentDay = 1
                            currentMinute = int(currentMinute)-55
                            currentHour = int(currentHour)-23
                    else:
                        currentDay=int(currentDay)+1
                        currentMinute=int(currentMinute)-55
                        currentHour=int(currentHour)-23
                else:
                    currentHour=int(currentHour)+1
                    currentMinute=int(currentMinute)-55
            else:
                currentMinute=int(currentMinute)+5
            #setting future dates that we calculated above
            ToMinuteCombo.set(str(int(currentMinute)))
            ToHourCombo.set(str(int(currentHour)))
            ToDayCombo.set(str(int(currentDay)))
            ToMonthCombo.set(str(int(currentMonth)))
            ToYearCombo.set(str(int(currentYear)))
            RepeatCombo.set(str(currentWeekday))
            #setting the ranges for date selection.
            #a range function is from inclusive to exclusive , ie , range(1,3) would return [1,2]
            FromDayCombo.config(values=list(range(1,32)))
            ToDayCombo.config(values=list(range(1,32)))
            ToYearCombo.config(values=list(range(int(currentYear),2100)))
            FromYearCombo.config(values=list(range(int(currentYear),2100)))        
        Refresh_AddClass()
        '''
        Module Name :- Confirm_AddClass
        Module Purpose:- Checks whether the user has provided correct class information and then proceeds to write that information to a csv
        Module Args:- none
        Module Inputs:- classname,subjectname,time data
        Module Outputs:- confirmation messages , error messages , CSV class information
        '''
        def Confirm_AddClass():
            #this function is used to confirm a class to be added and verifies and adds that information to a csv file
            #no params
            global selectedTeacher
            #selected teacher is modified by the bind function
            #obtains and freezes data in variables to prevent manipulation during messageboxes(messageboxes temporarily pause the script , allowing the user to make changes and possibly cause logic issues)
            givenClassName = ClassEntry.get()
            givenSubjectName = SubjectEntry.get()
            FromMinute = FromMinuteCombo.get()
            FromHour = FromHourCombo.get()
            FromDay = FromDayCombo.get()
            FromYear = FromYearCombo.get()
            FromMonth = FromMonthCombo.get()
            ToMinute = ToMinuteCombo.get()
            ToHour = ToHourCombo.get()
            ToDay = ToDayCombo.get()
            ToYear = ToYearCombo.get()
            ToMonth = ToMonthCombo.get()
            RepeatState = RepeatCombo.get()
            MaxSpots = MaxEntry.get()
            ToRestrict = RestrictedCheck.instate(['selected'])
            #checks whether a class name is inserted and only contains approved characters
            if givenClassName == "" or not(set(givenClassName).issubset(approved_text)):
                print(CRED+"Class Name not valid"+CEND)
                ClassEntry.delete(0,tkinter.END)
                messagebox.showerror("Error","Class name contains invalid characters")
                return False
            #checks whether a subject name is inserted and only contains approved characters
            if givenSubjectName == "" or not(set(givenSubjectName)).issubset(approved_text):
                print(CRED+"Subject Name not valid"+CEND)
                SubjectEntry.delete(0,tkinter.END)
                messagebox.showerror("Error","Subject name contains invalid characters")
                return False
            try:
                #int conversion checks for whether max spots is a integer
                MaxSpots = int(MaxSpots)
                #classes cannot have 0 spaces
                if MaxSpots<=0:
                    print(CRED+"Cannot be less than or equal to 0 max spots"+CEND)
                    messagebox.showerror("Error","Invalid Max Spaces")
                    MaxEntry.delete(0,tkinter.END)
                    return False
            except:
                print(CRED+"Not a number Max Spots"+CEND)
                messagebox.showerror("Error","Insert a number as Max Spots")
                return False
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
            i = 0
            newSub = []
            while i<len(subjectLines):
                row = subjectLines[i].split(',')
                if len(row)!=subjectLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                #checks for whether a class with this name and subject already exists
                if row[0] == givenSubjectName and row[1] == givenClassName:
                    print(CRED+"Cannot overwrite classes"+CEND)
                    messagebox.showerror("Error","This name has been taken by a different class. Edit that class and try again")
                    Refresh_AddClass()
                    return False
                i+=1
            '''
            -time1 would be like "09:15"
            -time2 would be "09:50"
            -repeatstate? would be the day of the week or all(dates between date 1 and date2)
            -date1 would be "2020:04:10"
            -date2 would be "2020:09:10"'''
            toWriteSchedulerInfo = ""
            #daysFromYear stores each minute that has occured till the given date , this might be not the most optimum method of calculating dates but modern day systems are really optimized for heavy tasks
            daysFromYear = 0
            monthswith31Days = [1,3,5,7,8,10,12]
            february = 0
            #date and time calculation is very heavy on a system.
            i=0
            #years are itirated starting from 0 until current year(2020 as of dev). Adds the amount of minutes in each year to a integer
            while i<int(FromYear):
                if i%4 == 0:
                    daysFromYear+=366*24*60
                else:
                    daysFromYear+=365*24*60
                i+=1
            #sets the february max for the current year
            if int(FromYear)%4 == 0:
                february = 29
            else:
                february=28
            if not(int(FromMonth) in monthswith31Days):
                #checks whether the day is below 30 as this month is not part of the months with 31 days
                if int(FromMonth) == 2:
                    if int(FromDay)>february:
                        messagebox.showerror("Error","Februrary only has "+str(february)+" days.")
                        ToDayCombo.set(february)
                        return False
                elif int(FromDay)>30:
                    messagebox.showerror("Error","The "+FromMonth+" month does not have "+FromDay+" days.")
                    FromDayCombo.set("1")
                    return False
                tempMath = 0
                i = 1
                #itirates and adds the days of each month to the date variable
                while i<int(FromMonth):
                    if i in monthswith31Days:
                        tempMath+=31
                    elif i == 2:
                        tempMath+=int(february)
                    else:
                        tempMath+=30
                    i+=1
                daysFromYear = daysFromYear+tempMath*24*60+int(FromDay)*24*60+int(FromMinute)+int(FromHour)*60
            else:
                tempMath = 0
                i = 1
                while i<int(FromMonth):
                    if i in monthswith31Days:
                        tempMath+=31
                    elif i == 2:
                        tempMath+=int(february)
                    else:
                        tempMath+=30
                    i+=1
                daysFromYear = daysFromYear+tempMath*24*60+int(FromDay)*24*60+int(FromMinute)+int(FromHour)*60
            daysToYear = 0
            i = 0
            while i<int(ToYear):
                if i%4 == 0:
                    daysToYear+=366*24*60
                else:
                    daysToYear+=365*24*60
                i+=1
            if int(ToYear)%4 == 0:
                february=29
            else:
                february=28
            if not(int(ToMonth) in monthswith31Days):
                if int(ToMonth) == 2:
                    if int(ToDay)>february:
                        messagebox.showerror("Error","Februrary only has "+february+" days.")
                        ToDayCombo.set(february)
                        return False
                elif int(ToDay)>30:
                    messagebox.showerror("Error","The "+ToMonth+" month does not have "+ToDay+" days.")
                    FromDayCombo.set("1")
                    return False
                tempMath = 0
                i = 1
                while i<int(ToMonth):
                    if i in monthswith31Days:
                        tempMath+=31
                    elif i == 2:
                        tempMath+=int(february)
                    else:
                        tempMath+=30
                    i+=1
                daysToYear = daysToYear+tempMath*24*60+int(ToDay)*24*60+int(ToHour)*60+int(ToMinute)
            else:
                tempMath = 0
                i = 1
                while i<int(ToMonth):
                    if i in monthswith31Days:
                        tempMath+=31
                    elif i == 2:
                        tempMath+=int(february)
                    else:
                        tempMath+=30
                    i+=1
                daysToYear = daysToYear+tempMath*24*60+int(ToDay)*24*60+int(ToHour)*60+int(ToMinute)
            if daysFromYear>=daysToYear:
                messagebox.showerror("Error","Your times are illogical. Make sure the end date is actually after the start date")
                return False
            #calculates current date and checks whether the class has already finished or not
            currentYear = strftime("%Y",localtime())
            currentMonth = strftime("%m",localtime())
            currentDay = strftime("%d",localtime())
            currentHour = strftime("%H",localtime())
            currentMinute = strftime("%M",localtime())
            currentTime = 0
            i = 0
            while i<int(currentYear):
                if i%4 == 0:
                    currentTime+=366*24*60
                else:
                    currentTime+=365*24*60
                i+=1
            if int(currentYear)%4 == 0:
                february=29
            else:
                february=28
            tempMath = 0
            i = 1
            while i<int(currentMonth):
                if i in monthswith31Days:
                    tempMath+=31
                elif i == 2:
                    tempMath+=int(february)
                else:
                    tempMath+=30
                i+=1
            currentTime = currentTime+tempMath*24*60+int(currentDay)*24*60+int(currentHour)*60+int(currentMinute)
            if currentTime>daysToYear:
                print(CRED+"Class already ended"+CEND)
                messagebox.showerror("Error","This class has already ended as of now")                
                return False
            toWriteSchedulerInfo = FromDay+":"+FromMonth+":"+FromYear+"."+ToDay+":"+ToMonth+":"+ToYear+"."+FromHour+":"+FromMinute+"."+ToHour+":"+ToMinute+"."+RepeatState
            file = open("subjects.csv","r+")
            subjectLines=file.readlines()
            file.close()
            if ToRestrict:
                ToRestrict="1"
            else:
                ToRestrict="0"
            if ToRestrict == "1":
                if selectedTeacher != "":
                    #if the user doesnot have the ability to join a restricted class, he cannot be bound as teacher
                    if not AuthMod(selectedTeacher,5):
                        print(CRED+"Cannot bind to class due to missing permissions"+CEND)
                        messagebox.showwarning("Warning","The user that has been bound does not have the permissions required to bind to this restricted class. Bound user ignored")
                        selectedTeacher=""
            
            subjectLines.append(givenSubjectName+","+givenClassName+","+str(MaxSpots)+","+toWriteSchedulerInfo+","+ToRestrict+","+selectedTeacher+"\n")
            file = open("subjects.csv","w+")
            file.writelines(subjectLines)
            file.close()
            print(CGREEN+"Class added"+CEND)
            messagebox.showinfo("Success","Class added to the system")
            Refresh_AddClass()
        tkinter.Button(AddClassScreen,text="Add Class",fg='green',bd=0,command=Confirm_AddClass).grid(column=1,row=11)
        tkinter.Button(AddClassScreen,text="Clear Form..",fg='red',command=Refresh_AddClass,bd=0).grid(column=2,row=11)
        '''
        Module Name:- closeAddClassScreen
        Module Purpose:- Checks whether any child windows are open and closes them when the parent window is closed
        Module args:- none
        Module Inputs:- Currently Open window list
        Module Output:- window close command
        '''
        def closeAddClassScreen():
            #close functions are used as a method to "imitate" inheritance behaviour
            #these functions close child windows when the WM_DELETE_WINDOW event happens
            global closeBindUser
            print(CRED+"Close command receieved"+CEND)
            try:
                BindUserToClassScreen.destroy()
            except:
                pass
            try:
                closeBindUser()
            except:
                pass
            AddClassScreen.destroy()
        AddClassScreen.protocol("WM_DELETE_WINDOW",closeAddClassScreen)
    tkinter.Button(manageClassWindow,text="Add Class",fg="green",command=AddClass,bd=0).grid(column=1,row=1)
    '''
    Module Name:- DeleteClass
    Module Purpose:- To open a dialog to delete a class from the system
    Module Arguments:- None
    Module Inputs:- None
    Module Outputs:- Tkinter window with a delete class table
    '''
    def DeleteClass():
        global CloseDeleteClassWindow
        if CheckOpen("Delete Class Screen"):
            return False
        #this function is used for the user to delete a class
        DeleteClassWindow = tkinter.Toplevel(loginScreen)
        DeleteClassWindow.title("Delete Class Screen")
        DeleteClassWindow.resizable(0,0)
        tkinter.Label(DeleteClassWindow,text="Double Click to Delete",fg='violet').grid(column=1,row=0)
        print(CGREEN+"Delete class windows closed"+CEND)
        DeleteClassFrame = tkinter.Frame(DeleteClassWindow)
        DeleteClassFrame.grid(column=1,row=1)
        DeleteClassTree = ttk.Treeview(DeleteClassFrame,columns=["Teacher"])
        DeleteClassTree.heading("#0",text="Subject/Class")
        DeleteClassTree.heading("Teacher",text="Teacher")
        XScrollDelete = tkinter.Scrollbar(DeleteClassFrame,orient=tkinter.HORIZONTAL,command=DeleteClassTree.xview)
        DeleteClassTree.configure(xscrollcommand=XScrollDelete.set)
        YScrollDelete = tkinter.Scrollbar(DeleteClassFrame,orient=tkinter.VERTICAL,command=DeleteClassTree.yview)
        DeleteClassTree.configure(yscrollcommand=YScrollDelete.set)
        YScrollDelete.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        XScrollDelete.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        DeleteClassTree.pack(side=tkinter.TOP,expand='false')
        '''
        Module Name:-RefreshDeleteClassTree
        Module Purpose:- Refresh the Delete Class Tree to display latest changes
        Module Arguments:- None
        Module Inputs:- Table columns , class information
        Module outputs:- refreshed table
        '''
        def RefreshDeleteClassTree():
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
            DeleteClassTree.delete(*DeleteClassTree.get_children())

            i = 0
            toIns = []
            while i<len(subjectLines):
                row = subjectLines[i].split(',')
                if len(row)!=subjectLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                #reads each subject and adds it to a list
                toIns.append((row[0],row[1],row[5]))
                i+=1
            i = 0
            while i<len(toIns):
                sub,clas,teacher = toIns[i]
                #unpacks data
                existingRows= DeleteClassTree.get_children()
                k = 0
                t = False
                '''
                Inserts the data onto the table by scanning for a existing parent.
                if a parent is found , it inserts the child under the parent
                If a parent is not found , a parent is created and a child is inserted
                '''
                while k<len(existingRows):
                    if DeleteClassTree.item(existingRows[k])['text'] == sub:
                        DeleteClassTree.insert(existingRows[k],tkinter.END,text=clas,values=[teacher])
                        t = True
                        break
                    k+=1
                if t:
                    i+=1
                    continue
                else:
                    p = DeleteClassTree.insert("",tkinter.END,text=sub)
                    DeleteClassTree.insert(p,tkinter.END,text=clas,values=[teacher])
                i+=1
            print(CGREEN+"Refreshed delete class tree"+CEND)
        RefreshDeleteClassTree()
        '''
        Module Name:- DeleteClassSearch
        Module Purpose:- Opens a window with a form, this form is used to search Delete Class Tree
        Module Arguments:- None
        Module Inputs:- None
        Module Outputs:- tkinter window with a search form
        '''
        def DeleteClassSearch():
            global DeleteClassSearchWindow
            if CheckOpen("Delete Class Search Window"):
                return False
            
            DeleteClassSearchWindow = tkinter.Toplevel(loginScreen)
            DeleteClassSearchWindow.title("Delete Class Search Window")
            DeleteClassSearchWindow.resizable(0,0)
            tkinter.Label(DeleteClassSearchWindow,text="Fill the Form").grid(column=1,row=0)
            tkinter.Label(DeleteClassSearchWindow,text="Search What:").grid(column=0,row=1)
            SearchWhatEntry = tkinter.Entry(DeleteClassSearchWindow,width=23)
            SearchWhatEntry.grid(column=1,row=1)
            tkinter.Label(DeleteClassSearchWindow,text="Search Where:").grid(column=0,row=2)
            SearchWhereCombo = ttk.Combobox(DeleteClassSearchWindow,values=["Subjects","Classes"],state='readonly')
            SearchWhereCombo.set("Subjects")
            SearchWhereCombo.grid(column=1,row=2)
            tkinter.Label(DeleteClassSearchWindow,text="Search How:").grid(column=0,row=3)
            SearchHowCombo = ttk.Combobox(DeleteClassSearchWindow,values=["Linear","Binary"],state='readonly')
            SearchHowCombo.set("Linear")
            SearchHowCombo.grid(column=1,row=3)
            print(CGREEN+"Delete class search window initialised"+CEND)
            '''
            Module Name:- SearchDeleteClassConfirm
            Module Purpose:- Grabs the data from the form and reads the table for matching data
            Module Arguments:- none
            Module Inputs:- Search What(Item to look for) , Search Where(Place to look for) , Search How(Method to search)
            Module Output:- Messagebox with status and item highlighted in table
            '''
            def SearchDeleteClassConfirm():

                SearchWhat = SearchWhatEntry.get()
                SearchWhere = SearchWhereCombo.get()
                SearchHow = SearchHowCombo.get()
                
                existingSubjects = DeleteClassTree.get_children()
                #Filters out bad input
                if SearchWhat == "" or SearchWhere == "" or SearchHow == "":
                    print(CRED+"Missing data for search"+CEND)
                    messagebox.showerror("Error","Fill the form")
                    return False
                
                if SearchHow == "Linear":
                    if SearchWhere == "Subjects":
                        i = 0
                        while i<len(existingSubjects):
                            if DeleteClassTree.item(existingSubjects[i])['text'] == SearchWhat:
                                #Highlights result in table and shows messagebox with result
                                print(CGREEN+"Subject found"+CEND)
                                DeleteClassTree.focus(existingSubjects[i])
                                DeleteClassTree.selection_set(existingSubjects[i])
                                messagebox.showinfo("Success","Item highlighted in the table")
                                return False
                            i+=1
                        print(CRED+"Missing subject"+CEND)
                        messagebox.showerror("Error","Unable to find item")
                        return False
                    else:
                        i = 0
                        while i<len(existingSubjects):
                            existingChildren = DeleteClassTree.get_children(existingSubjects[i])
                            k = 0
                            while k<len(existingChildren):
                                if DeleteClassTree.item(existingChildren[k])['text'] == SearchWhat:
                                    #Highlights result in table and shows messagebox with result
                                    print(CGREEN+"Item Found"+CEND)
                                    DeleteClassTree.item(existingSubjects[i],open=True)
                                    DeleteClassTree.focus(existingChildren[k])
                                    DeleteClassTree.selection_set(existingChildren[k])
                                    messagebox.showinfo("Success","Item highlighted in the table")
                                    return False
                                k+=1
                            i+=1
                        print(CRED+"Cannot find Item"+CEND)
                        messagebox.showerror("Error","Unable to find item")
                        return False
                else:
                    if SearchWhere == "Subjects":
                        newExistingSubjects = []
                        for t in existingSubjects:newExistingSubjects.append(DeleteClassTree.item(t)['text'])
                        newExistingSubjects = QuickieSort(newExistingSubjects)
                        if binarySearchAppr(newExistingSubjects,0,len(newExistingSubjects)-1,SearchWhat):
                            print(CGREEN+"Subject found"+CEND)
                            for t in existingSubjects:
                                if DeleteClassTree.item(t)['text'] == SearchWhat:
                                    #Highlights result in table and shows messagebox with result
                                    DeleteClassTree.selection_set(t)
                                    DeleteClassTree.focus(t)
                                    messagebox.showinfo("Success","Item highlighted in the table")
                                    return False
                        else:
                            print(CRED+"Subject not found"+CEND)
                            messagebox.showerror("Error","Unable to find item")
                            return False
                    else:
                        i = 0
                        while i<len(existingSubjects):
                            existingChildren = DeleteClassTree.get_children(existingSubjects[i])
                            newExistingChildren = []
                            for t in existingChildren: newExistingChildren.append(DeleteClassTree.item(t)['text'])
                            newExistingChildren = QuickieSort(newExistingChildren)
                            if binarySearchAppr(newExistingChildren,0,len(newExistingChildren)-1,SearchWhat):
                                print(CGREEN+"Class found"+CEND)
                                for t in existingChildren:
                                    if DeleteClassTree.item(t)['text'] == SearchWhat:
                                        DeleteClassTree.item(existingSubjects[i],open=True)
                                        DeleteClassTree.focus(t)
                                        DeleteClassTree.selection_set(t)
                                        messagebox.showinfo("Success","Item Highlighted in table")
                                        return False
                            i+=1
                        print(CRED+"Class not found"+CEND)
                        messagebox.showerror("Error","Unable to find item")
                        return False
            tkinter.Button(DeleteClassSearchWindow,text="Search..",fg='blue',bd=0,command=SearchDeleteClassConfirm).grid(column=1,row=4)
        tkinter.Button(DeleteClassWindow,text="Search..",fg='blue',command=DeleteClassSearch,bd=0).grid(column=0,row=2)
        '''
        Module Name:- DeleteClassSort
        Module Purpose:- Sorts the delete class tree
        Module Arguments:- None
        Module Inputs:- Data in table
        Module Output:- Sorted Table
        '''
        def DeleteClassSort():
            #gets all the columns
            existingSubjects=DeleteClassTree.get_children()
            newExistingSubjects = []
            #converts all the ids, to text
            for t in existingSubjects:newExistingSubjects.append(DeleteClassTree.item(t)['text'])
            #sorts text
            newExistingSubjects = QuickieSort(newExistingSubjects)
            finalIns = []
            #itirates sorted text and checks whether it matches an id , if it matches , obtain the children and append to Array
            for newS in newExistingSubjects:
                for oldS in existingSubjects:
                    if DeleteClassTree.item(oldS)['text'] == newS:
                        existingChildren = DeleteClassTree.get_children(oldS)
                        newExistingChildren = []
                        tempDataChildren = []
                        for oldC in existingChildren:
                            newExistingChildren.append(DeleteClassTree.item(oldC)['text'])
                        newExistingChildren = QuickieSort(newExistingChildren)
                        for newC in newExistingChildren:
                            for oldC in existingChildren:
                                if DeleteClassTree.item(oldC)['text'] == newC:
                                    tempDataChildren.append((newC,DeleteClassTree.item(oldC)['values'][0]))
                        finalIns.append((newS,tempDataChildren))
            i = 0
            DeleteClassTree.delete(*DeleteClassTree.get_children())
            #insert normally
            while i<len(finalIns):
                s,cl = finalIns[i]
                p = DeleteClassTree.insert("",tkinter.END,text=s)
                k = 0
                while k<len(cl):
                    clN , clV = cl[k]
                    DeleteClassTree.insert(p,tkinter.END,text=clN,values=[clV])
                    k+=1
                i+=1
            print(CGREEN+"Sorted"+CEND)
            messagebox.showinfo("Success","Sorted using QuickSort")
        tkinter.Button(DeleteClassWindow,text="Sort..",fg='blue',command=DeleteClassSort,bd=0).grid(column=2,row=2)
        '''
        Module Name:- DeleteClassConfirm
        Module Purpose:- Sorts the delete class tree
        Module Arguments:- event(this argument is passed by python by default for bind functions. it is ignored)
        Module Inputs:- Selected item in table(subject and class)
        Module Outputs:- Modified csv and refreshed table
        '''
        def DeleteClassConfirm(event):
            try:
                #checks to see whether the user actually clicked on a class
                selectedClass = DeleteClassTree.item(DeleteClassTree.focus())['text']
                if DeleteClassTree.parent(DeleteClassTree.focus()) == "":
                    return False
                selectedSubject = DeleteClassTree.item(DeleteClassTree.parent(DeleteClassTree.focus()))['text']
            except:
                return False
            #deletes the entry of the class from the subjects csv
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
            i = 0
            newSubjectLines = []
            while i<len(subjectLines):
                row = subjectLines[i].split(',')
                if len(row)!=subjectLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == selectedSubject and row[1] == selectedClass:
                    i+=1
                    continue
                newSubjectLines.append(subjectLines[i])
                i+=1
            file = open("subjects.csv","w+")
            file.writelines(newSubjectLines)
            file.close()
            print(CRED+"Subject Removed for SDatabase"+CEND)
            #deletes all the enrolements to that class
            file = open("users.csv","r+")
            userLines = file.readlines()
            file.close()
            newULines = []
            i = 0
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                tempSubU = row[2].split('.')
                k = 0
                while k<len(tempSubU):
                    try:
                        if tempSubU[k] == selectedSubject and tempSubU[k+1] == selectedClass:
                            del tempSubU[k]
                            del tempSubU[k]
                        else:
                            k+=1
                    except:
                        break
                tempSubsUW = ""
                k = 0
                while k<len(tempSubU):
                    if k == len(tempSubU)-1:
                        tempSubsUW = tempSubsUW+tempSubU[k]
                    else:
                        tempSubsUW = tempSubsUW+tempSubU[k]+"."
                    k+=1
                #TODO
                newULines.append(row[0]+","+row[1]+","+tempSubsUW+","+row[3]+","+row[4]+"\n")
                i+=1
            file = open("users.csv","w+")
            file.writelines(newULines)
            file.close()
            print(CRED+"Enrolements made to the class has been wiped!"+CEND)
            #deletes all waitlists made to that class
            file = open("waitlist.csv","r+")
            waitlistLines = file.readlines()
            file.close()
            i = 0
            newWaitlistLines = []
            while i<len(waitlistLines):
                row = waitlistLines[i].split(',')
                if len(row)!=waitlistLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[1] == selectedSubject and row[2] == selectedClass:
                    i+=1
                    continue
                newWaitlistLines.append(waitlistLines[i])
                i+=1
            file = open("waitlist.csv","w+")
            file.writelines(newWaitlistLines)
            file.close()
            print(CRED+"Waitlists made to the class has been wiped!"+CEND)
            print(CGREEN+"Class successfully wiped!"+CEND)
            messagebox.showinfo("Success","Class wiped from the system")
            RefreshDeleteClassTree()
        DeleteClassTree.bind("<Double-1>",DeleteClassConfirm)
        '''
        Module Name:- CloseDeleteClassWindow
        Module Purpose:- Imitates window inheritace
        Module arguments:- none
        Module Inputs:- Currently Open Windows
        Module Outputs:- Appropriate window close commands
        '''
        def CloseDeleteClassWindow():
            print(CRED+"Close command receieved"+CEND)
            global DeleteClassSearchWindow
            try:
                DeleteClassSearchWindow.destroy()
            except:
                pass
            DeleteClassWindow.destroy()
        tkinter.Button(DeleteClassWindow,text="Exit",fg='red',command=CloseDeleteClassWindow,bd=0).grid(column=1,row=2)
        DeleteClassWindow.protocol("WM_DELETE_WINDOW",CloseDeleteClassWindow)
    tkinter.Button(manageClassWindow,text="Delete Class",fg="green",command=DeleteClass,bd=0).grid(column=1,row=3)
    '''
    Module Name:- EditClass
    Module Purpose:- To open a dialog with a table to select a class to edit
    Module Arguments:- None
    Module Inputs:- None
    Module Outputs:- Tkinter window with a edit class table
    '''
    def EditClass():
        global EditClassScreen
        global SearchEditTreeScreen
        global CloseEditTree
        global CloseBindTree
        #this function is used to display a window that allows the user to select a class to edit
        if CheckOpen("Edit Class"):return False
        EditClassScreen = tkinter.Toplevel()
        EditClassScreen.title("Edit Class")
        EditClassScreen.resizable(0,0)
        tkinter.Label(EditClassScreen,text="Double Click to Edit",fg='blue').grid(column=1,row=0)
        EditTreeFrame = tkinter.Frame(EditClassScreen)
        EditTree = ttk.Treeview(EditTreeFrame)
        EditTree.heading("#0",text="Subject/Class")
        EditTreeY = tkinter.Scrollbar(EditTreeFrame,orient=tkinter.VERTICAL,command=EditTree.yview)
        EditTree.configure(yscrollcommand=EditTreeY.set)
        EditTreeX = tkinter.Scrollbar(EditTreeFrame,orient=tkinter.HORIZONTAL,command=EditTree.xview)
        EditTree.configure(xscrollcommand=EditTreeX.set)
        EditTreeY.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        EditTreeX.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        EditTree.pack(side=tkinter.TOP,expand='false')
        EditTreeFrame.grid(column=1,row=1)
        print(CGREEN+"Edit class window initialised"+CEND)
        '''
        Module Name:- RefreshEditTree
        Module Purpose:- To Refresh the edit class table to reflect the latest content of the file
        Module Arguments:- None
        Module Inputs:- Subject information
        Module Outputs:- Refreshed table
        '''
        def RefreshEditTree():
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
            i = 0
            EditTree.delete(*EditTree.get_children())
            toIns = []
            while i<len(subjectLines):
                row = subjectLines[i].split(',')
                if len(row)!=subjectLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                toIns.append((row[0],row[1]))
                i+=1
            i = 0
            while i<len(toIns):
                subject,class_ = toIns[i]
                existingSubs = EditTree.get_children()
                k = 0
                t = False
                while k<len(existingSubs):
                    if EditTree.item(existingSubs[k])['text'] == subject:
                        EditTree.insert(existingSubs[k],tkinter.END,text=class_)
                        t = True
                    k+=1
                if not t:
                    print(CGREEN+f"Inserted {subject}:{class_}"+CEND)
                    id2 = EditTree.insert("",tkinter.END,text=subject)
                    EditTree.insert(id2,tkinter.END,text=class_)
                i+=1
        RefreshEditTree()
        '''
        Module Name:- CloseEditTree
        Module Purpose:- Imitate window inheritance
        Module Inputs:- Current Windows
        Module Outputs:- Appropriate close commands
        '''
        def CloseEditTree():
            print(CRED+"Close command received"+CEND)
            global SearchEditTreeScreen
            global EditClassConfirmScreen
            global CloseBindTree
            try:
                SearchEditTreeScreen.destroy()
            except:
                pass
            try:
                EditClassConfirmScreen.destroy()
            except:
                pass
            try:
                CloseBindTree()
            except:
                pass
            EditClassScreen.destroy()
        tkinter.Button(EditClassScreen,text="Finish",fg='green',bd=0,command=CloseEditTree).grid(column=1,row=2)
        '''
        Module Name:- SearchEditTree
        Module Purpose:- Search the Edit Table
        Module Inputs:- None
        Module Outputs:- Window with a form that is capable of searching Edit table
        '''
        def SearchEditTree():
            global SearchEditTreeScreen
            if CheckOpen("Search Edit Tree Screen"):
                return False
            #initialize window elements
            SearchEditTreeScreen = tkinter.Toplevel(loginScreen)
            SearchEditTreeScreen.resizable(0,0)
            SearchEditTreeScreen.title("Search Edit Tree Screen")
            tkinter.Label(SearchEditTreeScreen,text="Fill the form",fg='blue').grid(column=1,row=0)

            tkinter.Label(SearchEditTreeScreen,text="Search What:").grid(column=0,row=1)
            SearchWhatEntry = tkinter.Entry(SearchEditTreeScreen,width=23)
            SearchWhatEntry.grid(column=1,row=1)

            tkinter.Label(SearchEditTreeScreen,text="Search Where:").grid(column=0,row=2)
            SearchWhereCombo = ttk.Combobox(SearchEditTreeScreen,values=["Subjects","Classes"],state='readonly')
            SearchWhereCombo.set("Subjects")
            SearchWhereCombo.grid(column=1,row=2)

            tkinter.Label(SearchEditTreeScreen,text="Search How:").grid(column=0,row=3)
            SearchHowCombo = ttk.Combobox(SearchEditTreeScreen,values=['Binary',"Linear"],state='readonly')
            SearchHowCombo.set("Linear")
            SearchHowCombo.grid(column=1,row=3)
            print(CGREEN+"Search window initialised"+CEND)
            ''' 
            Module Name:- SearchEditConfirm
            Module Purpose:- Use appropraite search algorithms to find a item that matches the search criteria
            Module Arguments:- None
            Module Inputs:- SearchWhat(Criteria to look for) , SearchHow(Method that should be used to search) , Search Where(The location to search)
            '''
            def SearchEditConfirm():
                SearchWhat = SearchWhatEntry.get()
                SearchHow = SearchHowCombo.get()
                SearchWhere = SearchWhereCombo.get()
                #filter out null input
                if SearchWhat == "" or SearchHow == "" or SearchWhere == "":
                    print(CRED+"Missing data"+CEND)
                    messagebox.showerror("Error","Fill the form completely and try again.")
                    return False
                if SearchHow == "Linear":
                    if SearchWhere == "Subjects":
                        #gets existing columns
                        existingSubjects = EditTree.get_children()
                        i = 0
                        while i<len(existingSubjects):
                            if EditTree.item(existingSubjects[i])['text'] == SearchWhat:
                                #if item found , it highlights it in the table.
                                EditTree.focus(existingSubjects[i])
                                print(CGREEN+"Subject found"+CEND)
                                EditTree.selection_set(existingSubjects[i])
                                SearchWhatEntry.delete(0,tkinter.END)
                                messagebox.showinfo("Success","Item highlighted in the table")
                                return False
                            i+=1
                        print(CRED+"Unable to find subject"+CEND)
                        messagebox.showerror("Error","Unable to find subject")
                        SearchWhatEntry.delete(0,tkinter.END)
                        return False
                    else:
                        existingSubjects = EditTree.get_children()
                        i = 0
                        #gets existing columns
                        while i<len(existingSubjects):
                            existingChildren = EditTree.get_children(existingSubjects[i])
                            k = 0
                            while k<len(existingChildren):
                                if EditTree.item(existingChildren[k])['text'] == SearchWhat:
                                    print(CGREEN+"Class found"+CEND)
                                    EditTree.item(existingSubjects[i],open=True)
                                    EditTree.focus(existingChildren[k])
                                    EditTree.selection_set(existingChildren[k])
                                    SearchWhatEntry.delete(0,tkinter.END)
                                    messagebox.showinfo("Success","Item highlighted in the table")
                                    return False
                                k+=1
                            i+=1
                        print(CRED+"Unable to find class"+CEND)
                        messagebox.showerror("Error","Unable to find class")
                        SearchWhatEntry.delete(0,tkinter.END)
                        return False
                else:
                    #binary search begins
                    if SearchWhere == "Subjects":
                        existingSubjects = EditTree.get_children()
                        newExistingSubjects = []
                        for t in range(len(existingSubjects)):newExistingSubjects.append(EditTree.item(existingSubjects[t])['text'])
                        newExistingSubjects = QuickieSort(newExistingSubjects)
                        if binarySearchAppr(newExistingSubjects,0,len(newExistingSubjects)-1,SearchWhat):
                            print(CGREEN+"Subject found"+CEND)
                            i = 0
                            while i<len(existingSubjects):
                                if EditTree.item(existingSubjects[i])['text'] == SearchWhat:
                                    EditTree.focus(existingSubjects[i])
                                    EditTree.selection_set(existingSubjects[i])
                                    SearchWhatEntry.delete(0,tkinter.END)
                                    messagebox.showinfo("Success","Item highlighted in the table")
                                    return False
                                i+=1
                        else:
                            print(CRED+"Subject not found"+CEND)
                            SearchWhatEntry.delete(0,tkinter.END)
                            messagebox.showerror("Error","Subject not found")
                            return False
                    else:
                        existingSubjects = EditTree.get_children()
                        i = 0
                        while i<len(existingSubjects):
                            existingChildren = EditTree.get_children(existingSubjects[i])
                            newExistingChildren = []
                            for t in range(len(existingChildren)):newExistingChildren.append(EditTree.item(existingChildren[t])['text'])
                            #sorts before binary search
                            newExistingChildren=QuickieSort(newExistingChildren)
                            if binarySearchAppr(newExistingChildren,0,len(newExistingChildren)-1,SearchWhat):
                                print(CGREEN+"Class found"+CEND)
                                k = 0
                                while k<len(existingChildren):
                                    if EditTree.item(existingChildren[k])['text'] == SearchWhat:
                                        EditTree.item(existingSubjects[i],open=True)
                                        EditTree.focus(existingChildren[k])
                                        EditTree.selection_set(existingChildren[k])
                                        SearchWhatEntry.delete(0,tkinter.END)
                                        messagebox.showinfo("Success","Class highlighted in the table")
                                        return False
                                    k+=1
                            i+=1
                        print(CRED+"Class Not found"+CEND)
                        messagebox.showerror("Error","Unable to find class")
                        SearchWhatEntry.delete(0,tkinter.END)
                        return False
            tkinter.Button(SearchEditTreeScreen,text="Search..",fg='blue',command=SearchEditConfirm,bd=0).grid(column=1,row=4)
        tkinter.Button(EditClassScreen,text="Search..",fg='blue',bd=0,command=SearchEditTree).grid(column=0,row=2)
        '''
        Module Name:-SortEditTree
        Module Purpose:- Sort the Edit Table
        Module Inputs:- Table Data
        Module Outputs:- sorted table
        '''
        def SortEditTree():
            existingSubjects = EditTree.get_children()
            newExistingSubjects = []
            for t in range(len(existingSubjects)):newExistingSubjects.append(EditTree.item(existingSubjects[t])['text'])
            newExistingSubjects = QuickieSort(newExistingSubjects)
            #QuickSort is used for sorting
            finalIns = []
            for t in newExistingSubjects:
                for p in existingSubjects:
                    if EditTree.item(p)['text'] == t:
                        existingChildren = EditTree.get_children(p)
                        newExistingChildren = []
                        for j in range(len(existingChildren)):newExistingChildren.append(EditTree.item(existingChildren[j])['text'])
                        newExistingChildren = QuickieSort(newExistingChildren)
                        finalIns.append((t,newExistingChildren))
            i = 0
            EditTree.delete(*EditTree.get_children())
            #sorted parents and children are inserted
            while i<len(finalIns):
                parent,child = finalIns[i]
                p =EditTree.insert("",tkinter.END,text=parent)
                k = 0
                while k<len(child):
                    EditTree.insert(p,tkinter.END,text=child[k])
                    k+=1
                i+=1
            messagebox.showinfo("Success","Sorted using QuickSort")
            print(CGREEN+"Sorted"+CEND)
        tkinter.Button(EditClassScreen,text="Sort..",fg='blue',command=SortEditTree,bd=0).grid(column=2,row=2)
        '''
        Module Name:-EditClassConfirm
        Module Purpose:-Used to display a form capable of editing the selected class
        Module Arguments:- event(this is passed by default by python for bind functions. this is ignored)
        Module Inputs:- Selected Class, selected subject
        Module Outputs:- Form with the data of the class(name,max spots,time data,restricted state)
        '''
        def EditClassConfirm(event):
            global EditClassConfirmScreen
            global CloseBindTree
            global TeacherBound
            if CheckOpen("Edit Class Confirm Screen"):
                return False
            try:
                #Ensure that the user clicked on a class
                givenClass = EditTree.item(EditTree.focus())['text']
                if EditTree.item(EditTree.parent(EditTree.focus()))['text'] == "":
                    return False
                givenSubject = EditTree.item(EditTree.parent(EditTree.focus()))['text']
            except:
                return False
            SchedulerInfo = ""
            MaxSpots = ""
            TeacherBound = ""
            RestrictedState = ""
            #initiazlize form
            EditClassConfirmScreen = tkinter.Toplevel(loginScreen)
            EditClassConfirmScreen.title("Edit Class Confirm Screen")
            EditClassConfirmScreen.resizable(0,0)
            print(CGREEN+"Edit class confirm screen initialised"+CEND)
            tkinter.Label(EditClassConfirmScreen,text="Edit..",fg='blue').grid(column=1,row=0)
            tkinter.Label(EditClassConfirmScreen,text="Subject:").grid(column=0,row=1)
            
            SubjectEntry = tkinter.Entry(EditClassConfirmScreen,width=23)
            SubjectEntry.grid(column=1,row=1)
            
            tkinter.Label(EditClassConfirmScreen,text="Class:").grid(column=0,row=2)
            
            ClassEntry = tkinter.Entry(EditClassConfirmScreen,width=23)
            ClassEntry.grid(column=1,row=2)
            
            tkinter.Label(EditClassConfirmScreen,text="Restricted:").grid(column=0,row=3)
            
            RestrictedCheck = ttk.Checkbutton(EditClassConfirmScreen)
            RestrictedCheck.state(['!alternate'])
            RestrictedCheck.grid(column=1,row=3)
            
            tkinter.Label(EditClassConfirmScreen,text="From Day(DD/MM/YYYY):").grid(column=0,row=4)
            
            FromDayCombo = ttk.Combobox(EditClassConfirmScreen,values=list(range(0,32)),state='readonly')
            FromDayCombo.grid(column=1,row=4)
            
            FromMonthCombo = ttk.Combobox(EditClassConfirmScreen,values=list(range(0,13)),state='readonly')
            FromMonthCombo.grid(column=2,row=4)
            
            FromYearCombo = ttk.Combobox(EditClassConfirmScreen,state='readonly',values=list(range(2000,2100)))
            FromYearCombo.grid(column=3,row=4)
            
            tkinter.Label(EditClassConfirmScreen,text="To Day(DD/MM/YYYY):").grid(column=0,row=5)
            
            ToDayCombo = ttk.Combobox(EditClassConfirmScreen,values=list(range(0,32)),state='readonly')
            ToDayCombo.grid(column=1,row=5)
            
            ToMonthCombo = ttk.Combobox(EditClassConfirmScreen,values=list(range(0,13)),state='readonly')
            ToMonthCombo.grid(column=2,row=5)
            
            ToYearCombo = ttk.Combobox(EditClassConfirmScreen,state='readonly',values=list(range(2000,2100)))
            ToYearCombo.grid(column=3,row=5)
            
            tkinter.Label(EditClassConfirmScreen,text="From Time(HH:MM):").grid(column=0,row=6)
            
            FromHourCombo = ttk.Combobox(EditClassConfirmScreen,values=list(range(0,24)),state='readonly')
            FromHourCombo.grid(column=1,row=6)
            
            FromMinuteCombo = ttk.Combobox(EditClassConfirmScreen,values=list(range(0,60)),state='readonly')
            FromMinuteCombo.grid(column=2,row=6)
            
            tkinter.Label(EditClassConfirmScreen,text="To Time(HH:MM):").grid(column=0,row=7)
            
            ToHourCombo = ttk.Combobox(EditClassConfirmScreen,values=list(range(0,24)),state='readonly')
            ToHourCombo.grid(column=1,row=7)
            
            ToMinuteCombo = ttk.Combobox(EditClassConfirmScreen,values=list(range(0,60)),state='readonly')
            ToMinuteCombo.grid(column=2,row=7)
            
            tkinter.Label(EditClassConfirmScreen,text="Repeat Day:").grid(column=0,row=8)
            
            RepeatCombo = ttk.Combobox(EditClassConfirmScreen,values=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","Everyday"],state='readonly')
            RepeatCombo.grid(column=1,row=8)
            
            tkinter.Label(EditClassConfirmScreen,text="Max Spots:").grid(column=0,row=9)
            
            MaxSpotsEntry = tkinter.Entry(EditClassConfirmScreen,width=23)
            MaxSpotsEntry.grid(column=1,row=9)
            
            tkinter.Label(EditClassConfirmScreen,text="Bind/Unbinds:").grid(column=0,row=10)
            '''
            Module Name:- BindMang
            Module Purpose:- Allows the user to change the user who is bound to a class(or assign a user if the class hasnt been bound at all)
            Module Arguments:-None
            Module Inputs:- Previously bound user
            Module Outputs:- Window to select a new user to bind to
            '''
            def BindMang():
                global CloseBindTree
                if CheckOpen("Bind Mang Screen"):
                    return False
                global SearchBindTreeS2
                
                BindMangScreen = tkinter.Toplevel(loginScreen)
                BindMangScreen.title("Bind Mang Screen")
                BindMangScreen.resizable(0,0)
                
                tkinter.Label(BindMangScreen,text="Bind/Unbind by double clicking on a user",fg='purple').grid(column=1,row=0)
                
                TreeFrameBind = tkinter.Frame(BindMangScreen)
                TreeFrameBind.grid(column=1,row=1)
                
                TreeBind = ttk.Treeview(TreeFrameBind)
                TreeBind.heading("#0",text="Role/User")
                
                YScrollBind = tkinter.Scrollbar(TreeFrameBind,orient=tkinter.VERTICAL,command=TreeBind.yview)
                TreeBind.configure(yscrollcommand=YScrollBind.set)
                XScrollBind = tkinter.Scrollbar(TreeFrameBind,orient=tkinter.HORIZONTAL,command=TreeBind.xview)
                TreeBind.configure(xscrollcommand=XScrollBind.set)
                YScrollBind.pack(side=tkinter.RIGHT,fill=tkinter.Y)
                XScrollBind.pack(side=tkinter.BOTTOM,fill=tkinter.X)
                TreeBind.pack(side=tkinter.TOP,expand='false')
                '''
                Module Name:- RefreshBindTree
                Module Purpose:- Refresh the Bind Tree and reinsert latest data from users
                Module Arguments:- None
                Module Inputs:- User database , previously selected teacher(if any)
                Module Outputs:- Refreshed table
                '''
                def RefreshBindTree():
                    file = open("users.csv","r+")
                    userLines = file.readlines()
                    file.close()
                    i = 0
                    toIns = []
                    while i<len(userLines):
                        row = userLines[i].split(',')
                        if len(row)!=userLEN:
                            i+=1
                            continue
                        for t in range(len(row)):row[t] = row[t].strip()
                        givenUser = row[0]
                        givenRole = row[3]
                        if AuthMod(givenUser,1):
                            #checks whether the user can bind to the class using AuthMod then proceeds to append to a list to insert
                            toIns.append((givenUser,givenRole))
                        i+=1
                    i = 0
                    TreeBind.delete(*TreeBind.get_children())
                    while i<len(toIns):
                        u,r = toIns[i]
                        #appends bound if the user is a teacher
                        if u == TeacherBound:
                            u = "BOUND:"+u
                        existingR = TreeBind.get_children()
                        k = 0
                        t = False
                        while k<len(existingR):
                            if TreeBind.item(existingR[k])['text'] == r:
                                TreeBind.insert(existingR[k],tkinter.END,text=u)
                                t=True
                                break
                            k+=1
                        if t:
                            i+=1
                            continue
                        else:
                            p = TreeBind.insert("",tkinter.END,text=r)
                            TreeBind.insert(p,tkinter.END,text=u)
                        i+=1
                RefreshBindTree()
                '''
                Module Name:- SearchBindTree
                Module Purpose:- Provide a form capable of searching the Bind Tree
                Module Arguments:- None
                Module Inputs:- Tree Bind data
                Module Outputs:- Tkinter window that provides a search form
                '''
                def SearchBindTree():
                    global SearchBindTreeS2
                    if CheckOpen("Search Bind Tree S2"):
                        return False
                    SearchBindTreeS2 = tkinter.Toplevel(loginScreen)
                    SearchBindTreeS2.title("Search Bind Tree S2")
                    SearchBindTreeS2.resizable(0,0)
                    
                    tkinter.Label(SearchBindTreeS2,text="Search..",fg='blue').grid(column=1,row=0)
                    tkinter.Label(SearchBindTreeS2,text="Search What:").grid(column=0,row=1)
                    SearchWhatEntry = tkinter.Entry(SearchBindTreeS2,width=23)
                    SearchWhatEntry.grid(column=1,row=1)
                    tkinter.Label(SearchBindTreeS2,text="Search Where:").grid(column=0,row=2)
                    SearchWhereCombo = ttk.Combobox(SearchBindTreeS2,values=["Users","Roles"],state='readonly')
                    SearchWhereCombo.set("Users")
                    SearchWhereCombo.grid(column=1,row=2)
                    tkinter.Label(SearchBindTreeS2,text="Search How:").grid(column=0,row=3)
                    SearchHowCombo = ttk.Combobox(SearchBindTreeS2,values=["Linear","Binary"],state='readonly')
                    SearchHowCombo.grid(column=1,row=3)
                    SearchHowCombo.set("Linear")
                    print(CGREEN+"Search window loaded"+CEND)
                    '''
                    Module Name:- SearchBindTreeS2Confirm
                    Module purpose:- Uses the preffered algorithm to search for criteria
                    Module args:- None
                    Module inputs:- Table data , search what(what to look for) , search where(where to look for) , search how(how to find that item)
                    Module Outputs:- Highlighted entry in table which is the criteria that is being looked for
                    '''
                    def SearchBindTreeS2Confirm():
                        #data is always passed as string ,therefore no  type checks required
                        existingRows = TreeBind.get_children()
                        SearchWhat = SearchWhatEntry.get()
                        SearchWhere = SearchWhereCombo.get()
                        SearchHow = SearchHowCombo.get()
                        #existence verifs
                        if SearchWhat=="" or SearchWhere == "" or SearchHow == "":
                            messagebox.showerror("Error","Fill the form")
                            return False
                        if SearchHow == "Linear":
                            if SearchWhere == "Roles":
                                i = 0
                                while i<len(existingRows):
                                    if TreeBind.item(existingRows[i])['text'] == SearchWhat:
                                        #searches for item using linear search then highlights on table
                                        print(CGREEN+"Item found"+CEND)
                                        TreeBind.focus(existingRows[i])
                                        TreeBind.selection_set(existingRows[i])
                                        messagebox.showinfo("Success","Item has been highlighted in the table")
                                        SearchWhatEntry.delete(0,tkinter.END)
                                        return False
                                    i+=1
                                print(CRED+"Item not found"+CEND)
                                messagebox.showerror("Error","Unable to find the role")
                                SearchWhatEntry.delete(0,tkinter.END)
                                return False
                            else:
                                i = 0
                                while i<len(existingRows):
                                    existingChildren = TreeBind.get_children(existingRows[i])
                                    k = 0
                                    while k<len(existingChildren):
                                        if TreeBind.item(existingChildren[k])['text'] == SearchWhat:
                                            print(CGREEN+"Item found"+CEND)
                                            #searches for item using linear search then highlights on table
                                            TreeBind.item(existingRows[i],open=True)
                                            TreeBind.focus(existingChildren[k])
                                            TreeBind.selection_set(existingChildren[k])
                                            messagebox.showinfo("Success","Item highlighted in table")
                                            SearchWhatEntry.delete(0,tkinter.END)
                                            return False
                                        k+=1    
                                    i+=1
                                print(CRED+"Item Not Found"+CEND)
                                messagebox.showerror("Error","Unable to find item")
                                SearchWhatEntry.delete(0,tkinter.END)
                                return False
                        else:
                            if SearchWhere == "Roles":
                                newExistingRows = []
                                for t in range(len(existingRows)):newExistingRows.append(TreeBind.item(existingRows[t])['text'])
                                newExistingRows = QuickieSort(newExistingRows)
                                if binarySearchAppr(newExistingRows,0,len(newExistingRows)-1,SearchWhat):
                                    for t in existingRows:
                                        if TreeBind.item(t)['text'] == SearchWhat:
                                            #searches for item using binary and highlights on table
                                            TreeBind.focus(t)
                                            TreeBind.selection_set(t)
                                            messagebox.showinfo("Success","Item highlighted in the table")
                                            SearchWhatEntry.delete(0,tkinter.END)
                                            return False
                                else:
                                    print(CRED+"Item not found"+CEND)
                                    messagebox.showerror("Error","Unable to find item in table")
                                    SearchWhatEntry.delete(0,tkinter.END)
                                    return False
                            else:
                                i = 0
                                while i<len(existingRows):
                                    existingChildren = TreeBind.get_children(existingRows[i])
                                    NewExistingChildren = []
                                    for t in existingChildren:NewExistingChildren.append(TreeBind.item(t)['text'])
                                    NewExistingChildren = QuickieSort(NewExistingChildren)
                                    if binarySearchAppr(NewExistingChildren,0,len(NewExistingChildren)-1,SearchWhat):
                                        for t in existingChildren:
                                            if TreeBind.item(t)['text'] == SearchWhat:
                                                #searches for item using binary and highlights on table
                                                TreeBind.item(existingRows[i],open=True)
                                                TreeBind.focus(t)
                                                TreeBind.selection_set(t)
                                                messagebox.showinfo("Success","Item highlighted in the table")
                                                SearchWhatEntry.delete(0,tkinter.END)
                                                return False
                                    i+=1
                                print(CRED+"Item not found"+CEND)
                                messagebox.showerror("Error","Unable to find item")
                                SearchWhatEntry.delete(0,tkinter.END)
                                return False
                            
                    tkinter.Button(SearchBindTreeS2,text="Search",fg='green',command=SearchBindTreeS2Confirm,bd=0).grid(column=1,row=4)
                tkinter.Button(BindMangScreen,text="Search..",fg='blue',command=SearchBindTree,bd=0).grid(column=0,row=2)
                '''
                Module Name:- SortBindTree
                Module Purpose:- Sort The table using quicksort
                Module Arguments:- None
                Module Inputs:- all rows in the table
                Module Outputs:- Sorted table rows
                '''
                def SortBindTree():
                    existingRows = TreeBind.get_children()
                    newExistingRows = []
                    for t in existingRows: newExistingRows.append(TreeBind.item(t)['text'])
                    newExistingRows = QuickieSort(newExistingRows)
                    toIns = []
                    for sub in newExistingRows:
                        #sub is the row that has been sorted and its true name
                        for subP in existingRows:
                            #subP is a row id of a unsorted table entry
                            if TreeBind.item(subP)['text'] == sub:
                                #if the "TEXT" columns matches sub , then the children of subP is obtained and sorted
                                existingChildren = TreeBind.get_children(subP)
                                newExistingChildren = []
                                for t in existingChildren:newExistingChildren.append(TreeBind.item(t)['text'])
                                newExistingChildren =QuickieSort(newExistingChildren)
                                #finally , the data is put in a array for insertion
                                toIns.append((sub,newExistingChildren))
                    i = 0
                    TreeBind.delete(*TreeBind.get_children())
                    #table clears and data will be inserted
                    while i<len(toIns):
                        sub,children = toIns[i]
                        a=TreeBind.insert("",tkinter.END,text=sub)
                        k = 0
                        while k<len(children):
                            TreeBind.insert(a,tkinter.END,text=children[k])
                            k+=1
                        i+=1
                    print(CGREEN+"Sorted"+CEND)
                tkinter.Button(BindMangScreen,text="Sort..",fg='blue',command=SortBindTree,bd=0).grid(column=2,row=2)
                '''
                Module Name:- CloseBindTree
                Module Purpose:- Imitate children inheritance
                Module Arguments:- None
                Module Inputs:-  All windows currently open
                Module Outputs:- Appropriate close commands for the child windows
                '''
                def CloseBindTree():
                    print(CRED+"Close command recieved"+CEND)
                    global SearchBindTreeS2
                    #the only child of this window is SearchBindTreeS2
                    try:
                        SearchBindTreeS2.destroy()
                    except:
                        pass
                    BindMangScreen.destroy()
                BindMangScreen.protocol("WM_DELETE_WINDOW",CloseBindTree)
                tkinter.Button(BindMangScreen,text="Exit..",fg='red',command=CloseBindTree,bd=0).grid(column=1,row=2)
                '''
                Module name:- ConfirmBind
                Module Purpose:- Binds the user once some checks are executed
                Module Arguments:- None
                Module Inputs:- Currently selected user
                Module Outputs:- User bound
                '''
                def ConfirmBind(event):
                    global TeacherBound
                    try:
                        selectedUser = TreeBind.item(TreeBind.focus())['text']
                        if TreeBind.parent(TreeBind.focus())=="":
                            return False
                    except:
                        return False
                    #checks whether the OVERuser is attempting to unbind this user
                    if re.search("^BOUND:",selectedUser):
                        print(CRED+"Bind detected"+CEND)
                        if messagebox.askyesno("Confirm","Are you sure you want to unbind this user?"):
                            print(CGREEN+"Unbound"+CEND)
                            TreeBind.item(TreeBind.focus(),text=TeacherBound)
                            TeacherBound = ""
                            return False
                        else:
                            return False                  
                    existingRows = TreeBind.get_children()
                    i = 0
                    #this algoritm checks for whether any other user has already bound to this class. 
                    while i<len(existingRows):
                        existingChildren = TreeBind.get_children(existingRows[i])
                        k = 0
                        t=False
                        while k<len(existingChildren):
                            if re.search("^BOUND:",TreeBind.item(existingChildren[k])['text']):
                                #if a bound user is found , proceed to prompt the user, asking for unbind or cancel
                                if messagebox.askyesno("Confirm","This class has been already bound to a user. Do you want to unbind and rebind to a new user?"):
                                    #if the user agrees to unbind , the already bound user would be unbound and the setup would move to step 3
                                    TreeBind.item(existingChildren[k],text=TeacherBound)
                                    TeacherBound = ""
                                    t = True
                                    break
                                else:
                                    return False
                            k+=1
                        if t:
                            break
                        i+=1
                    #last stage in which the teacher is bound to selectedUser
                    TreeBind.item(TreeBind.focus(),text="BOUND:"+selectedUser)
                    messagebox.showinfo("Success","User bound to class. Remember to save changes")
                    print(CGREEN+"Bound"+CEND)
                    TeacherBound = selectedUser
                TreeBind.bind("<Double-1>",ConfirmBind)
            tkinter.Button(EditClassConfirmScreen,text="Bind Mang.",command=BindMang,bd=0,fg='blue',).grid(column=1,row=10)
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
            i=0
            while i<len(subjectLines):
                row= subjectLines[i].split(',')
                if len(row)!=subjectLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == givenSubject and row[1] == givenClass:
                    SchedulerInfo = row[3]
                    TeacherBound=row[5]
                    MaxSpots=row[2]
                    RestrictedState=row[4]
                    break
                i+=1
            SubjectEntry.delete(0,tkinter.END)
            ClassEntry.delete(0,tkinter.END)
            SubjectEntry.insert(0,givenSubject)
            ClassEntry.insert(0,givenClass)
            MaxSpotsEntry.delete(0,tkinter.END)
            MaxSpotsEntry.insert(0,MaxSpots)
            try:
                SchedulerInfo = SchedulerInfo.split('.')
                #unpacking data like this is risky , but its useful in this situation where we are checking for correct and full time arguments
                DayFromD,DayFromM,DayFromY = SchedulerInfo[0].split(':')
                DayToD,DayToM,DayToY = SchedulerInfo[1].split(':')
                TimeFromH,TimeFromM = SchedulerInfo[2].split(':')
                TimeToH,TimeToM = SchedulerInfo[3].split(":")
            except:
                messagebox.showerror("Error","This class is corrupted or missing some arguments in time settings. Unable to load sys.edit")
                return False
            RepeatCombo.set(SchedulerInfo[4])
            
            FromDayCombo.set(DayFromD)
            FromMonthCombo.set(DayFromM)
            FromYearCombo.set(DayFromY)

            ToDayCombo.set(DayToD)
            ToMonthCombo.set(DayToM)
            ToYearCombo.set(DayToY)

            FromHourCombo.set(TimeFromH)
            FromMinuteCombo.set(TimeFromM)

            ToHourCombo.set(TimeToH)
            ToMinuteCombo.set(TimeToM)
            if RestrictedState == "1":
                RestrictedCheck.state(['selected'])
            else:
                RestrictedCheck.state(['!selected'])
            '''
            Module Name:- SaveChangesEditConfirmed
            Module Purpose:- Save Changes that has occured in the form and the bind class sub menu
            Module Args:- None
            Module inputs:- all the form data , selected teacher
            Module Outputs:- Changes saved to subject database
            '''
            def SaveChangesEditConfirmed():
                global TeacherBound
                newSub = SubjectEntry.get()
                newClass = ClassEntry.get()

                newToD = ToDayCombo.get()
                newToMo = ToMonthCombo.get()
                newToMi = ToMinuteCombo.get()
                newToY = ToYearCombo.get()
                newToH = ToHourCombo.get()
                
                newFromD = FromDayCombo.get()
                newFromMo = FromMonthCombo.get()
                newFromM = FromMinuteCombo.get()
                newFromH = FromHourCombo.get()
                newFromY = FromYearCombo.get()
                
                newMax = MaxSpotsEntry.get()
                newRes = RestrictedCheck.instate(['selected'])
                newRep = RepeatCombo.get()           
                #all data is fetched and frozen to prevent user manipulation
                if newClass == "" or not(set(newClass).issubset(approved_text)):
                    #existence and validation
                    print(CRED+"Validation Fail"+CEND)
                    ClassEntry.delete(0,tkinter.END)
                    messagebox.showerror("Error","Class name contains invalid characters")
                    return False
                if newSub == "" or not(set(newSub)).issubset(approved_text):
                    #existence and validation
                    print(CRED+"Validation Fail"+CEND)
                    SubjectEntry.delete(0,tkinter.END)
                    messagebox.showerror("Error","Subject name contains invalid characters")
                    return False
                try:
                    newMax = int(newMax)
                    #type and range check
                    if newMax<=0:
                        print(CRED+"Validation Fail"+CEND)
                        messagebox.showerror("Error","Invalid Max Spaces")
                        MaxSpotsEntry.delete(0,tkinter.END)
                        return False
                except:
                    print(CRED+"Validation Fail"+CEND)
                    messagebox.showerror("Error","Insert a number as Max Spots")
                    MaxSpotsEntry.delete(0,tkinter.END)
                    return False
                '''
                -time1 would be like "09:15"
                -time2 would be "09:50"
                -repeatstate? would be the day of the week or all(dates between date 1 and date2)
                -date1 would be "2020:04:10"
                -date2 would be "2020:09:10"'''
                toWriteSchedulerInfo = ""
                #years
                daysFromYear = 0
                monthswith31Days = [1,3,5,7,8,10,12]
                february = 0
                #daysFromYear is each minute that has passed since year 0 until the from date, even though it is unoptimized , range() functions are irreliable
                i = 0
                while i<int(newFromY):
                    if i%4 == 0:
                        daysFromYear+=366*24*60
                    else:
                        daysFromYear+=365*24*60
                    i+=1
                if int(newFromY)%4 == 0:
                    february = 29
                else:
                    february = 28
                #start from here
                if not(int(newFromMo) in monthswith31Days):
                    if int(newFromMo) == 2:
                        if int(newFromD)>february:
                            messagebox.showerror("Error","Februrary only has "+february+" days.")
                            ToDayCombo.set(february)
                            return False
                    elif int(newFromD)>30:
                        messagebox.showerror("Error","The "+newFromMo+" month does not have "+newFromD+" days.")
                        FromDayCombo.set("1")
                        return False
                    tempMath = 0
                    i = 1
                    while i<int(newFromMo):
                        if i in monthswith31Days:
                            tempMath+=31
                        elif i == 2:
                            tempMath+=int(february)
                        else:
                            tempMath+=30
                        i+=1
                    daysFromYear = daysFromYear+tempMath*24*60+int(newFromD)*24*60+int(newFromM)+int(newFromH)*60
                else:
                    tempMath = 0
                    i = 1
                    while i<int(newFromMo):
                        if i in monthswith31Days:
                            tempMath+=31
                        elif i == 2:
                            tempMath+=int(february)
                        else:
                            tempMath+=30
                        i+=1
                    daysFromYear = daysFromYear+tempMath*24*60+int(newFromD)*24*60+int(newFromH)*60+int(newFromM)
                daysToYear = 0
                i = 0
                #days to year contains each minute that has passed from year 0 until the to date.
                while i<int(newToY):
                    if i%4 == 0:
                        daysToYear+=366*24*60
                    else:
                        daysToYear+=365*24*60
                    i+=1
                if int(newToY)%4 == 0:
                    february=29
                else:
                    february=28
                if not(int(newToMo) in monthswith31Days):
                    if int(newToMo) == 2:
                        if int(newToD)>february:
                            messagebox.showerror("Error","Februrary only has "+february+" days.")
                            ToDayCombo.set(february)
                            return False
                    elif int(newToD)>30:
                        messagebox.showerror("Error","The "+newToMo+" month does not have "+newToD+" days.")
                        FromDayCombo.set("1")
                        return False
                    tempMath = 0
                    i = 1
                    while i<int(newToMo):
                        if i in monthswith31Days:
                            tempMath+=31
                        elif i == 2:
                            tempMath+=int(february)
                        else:
                            tempMath+=30
                        i+=1
                    daysToYear = daysToYear+tempMath*24*60+int(newToD)*24*60+int(newToH)*60+int(newToMi)
                else:
                    tempMath = 0
                    i = 1
                    while i<int(newToMo):
                        if i in monthswith31Days:
                            tempMath+=31
                        elif i == 2:
                            tempMath+=int(february)
                        else:
                            tempMath+=30
                        i+=1
                    daysToYear = daysToYear+tempMath*24*60+int(newToD)*24*60+int(newToH)*60+int(newToMi)
                #checks whether the from date is larger than the to date which means that the from time is in the future of the to time, if it is , a error would be shown
                if daysFromYear>=daysToYear:
                    messagebox.showerror("Error","Your times are illogical. Make sure the end date is actually after the start date")
                    return False
                #current times are fetched from PC
                currentYear = strftime("%Y",localtime())
                currentMonth = strftime("%m",localtime())
                currentDay = strftime("%d",localtime())
                currentHour = strftime("%H",localtime())
                currentMinute = strftime("%M",localtime())
                currentTime = 0
                i = 0
                while i<int(currentYear):
                    if i%4 == 0:
                        currentTime+=366*24*60
                    else:
                        currentTime+=365*24*60
                    i+=1
                if int(currentYear)%4 == 0:
                    february=29
                else:
                    february=28
                tempMath = 0
                i = 1
                while i<int(currentMonth):
                    if i in monthswith31Days:
                        tempMath+=31
                    elif i == 2:
                        tempMath+=int(february)
                    else:
                        tempMath+=30
                    i+=1
                currentTime = currentTime+tempMath*24*60+int(currentDay)*24*60+int(currentHour)*60+int(currentMinute)
                #current time is used to check whether the class has already ended in the past(ie , the to date has happened in the past)
                if currentTime>daysToYear:
                    #this system allows the creation of these subjects for debugging purposes
                    if messagebox.askyesno("Error","This class has already ended as of now. Do you still want to continue?"):
                        pass
                    else:
                        return False
                #once all the scheduler info is verified , it is compiled to a program understandable format , ready for writing
                toWriteSchedulerInfo = newFromD+":"+newFromMo+":"+newFromY+"."+newToD+":"+newToMo+":"+newToY+"."+newFromH+":"+newFromM+"."+newToH+":"+newToMi+"."+newRep
                file = open("subjects.csv","r+")
                subjectLines = file.readlines()
                file.close()
                i = 0
                while i<len(subjectLines):
                    row = subjectLines[i].split(',')
                    if len(row)!=subjectLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    #this removes the ability of the user to wipe all the other classes by editing to them , causing a overwrite clash
                    if (row[0] == newSub and row[1] == newClass) and (row[0]!=givenSubject or row[1] != givenClass):
                        messagebox.showerror("Error","Error. This class name is already taken. Edit/Delete the other class and try again")
                        return False
                    i+=1
                if newRes:
                    newRes="1"
                else:
                    newRes="0"
                if newRes == "1":
                    if TeacherBound != "":
                        #checks whether the user is capable of joining to restricted class, if he cannot join to a restricted class , he cannot bind to it either
                        if not AuthMod(TeacherBound,5):
                            messagebox.showwarning("Warning","The user that has been bound does not have the permissions required to bind to this restricted class. Bound user ignored")
                            TeacherBound=""
                file = open("users.csv","r+")
                userLines = file.readlines()
                file.close()
                enrolledCount = 0
                i = 0
                while i<len(userLines):
                    row = userLines[i].split(',')
                    if len(row)!=userLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    tempE = row[2].split('.')
                    k = 0
                    while k<len(tempE):
                        try:
                            if tempE[k] == givenSubject and tempE[k+1] == givenClass:
                                enrolledCount+=1
                        except:
                            break
                        k+=2
                    i+=1
                #performs a quick check to see whether there are enough spaces for the existing users. if not , it will throw a error
                if enrolledCount>newMax:
                    messagebox.showerror("Error","There isnt enough space in this class to keep all the students who have already enrolled. Please set a space higher than "+str(enrolledCount))
                    MaxSpotsEntry.delete(0,tkinter.END)
                    MaxSpotsEntry.insert(0,str(enrolledCount))
                    return False
                i = 0
                newSLines = []
                while i<len(subjectLines):
                    row = subjectLines[i].split(',')
                    if len(row)!=subjectLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    if row[0] == givenSubject and row[1] == givenClass:
                        #these todo's mark important lines that might need revising if the file length is to be changed
                        #TODO
                        newSLines.append(newSub+","+newClass+","+str(newMax)+","+toWriteSchedulerInfo+","+newRes+","+TeacherBound+"\n")
                        i+=1
                        continue
                    newSLines.append(subjectLines[i])
                    i+=1
                file = open("users.csv","r+")
                userLines=file.readlines()
                file.close()
                #the subject is finally saved

                #all users that are already enrolled gets their enrolements renamed(if necessary) to reflect the subject changes
                i = 0
                newUserLines = []
                while i<len(userLines):
                    row = userLines[i].split(',')
                    if len(row)!=userLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    oldSubjects = row[2].split('.')
                    newSubjects = []
                    k = 0
                    if row[2] == "":
                        i+=1
                        continue
                    while k<len(oldSubjects):
                        try:
                            if oldSubjects[k] == givenSubject and oldSubjects[k+1] == givenClass:
                                newSubjects.append(newSub)
                                newSubjects.append(newClass)
                            else:
                                newSubjects.append(oldSubjects[k])
                                newSubjects.append(oldSubjects[k+1])
                        except:
                            break
                        k+=2
                    newSubjectsW = ""
                    k = 0
                    while k<len(newSubjects):
                        if k == len(newSubjects)-1:
                            newSubjectsW = newSubjectsW+newSubjects[k]
                        else:
                            newSubjectsW = newSubjectsW+newSubjects[k]+"."
                        k+=1
                    #TODO
                    newUserLines.append(row[0]+","+row[1]+","+newSubjectsW+","+row[3]+","+row[4]+"\n")
                    i+=1
                file = open('users.csv',"w+")
                file.writelines(newUserLines)
                file.close()
                print(CGREEN+"Enrolements updated"+CEND)
                #any waitlists would get renamed to reflect subject name changes as well
                file = open("waitlist.csv","r+")
                waitlistLines = file.readlines()
                file.close()
                i = 0
                newWLines = []
                while i<len(waitlistLines):
                    row=waitlistLines[i].split(',')
                    if len(row)!=waitlistLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    if row[1] == givenSubject and row[2] == givenClass:
                        newWLines.append(row[0]+","+newSub+","+newClass+"\n")
                    else:
                        newWLines.append(waitlistLines[i])
                    i+=1
                print(CGREEN+"Waitlists modified"+CEND)
                file = open("waitlist.csv","w+")
                file.writelines(newWLines)
                file.close()
                file = open("subjects.csv","w+")
                file.writelines(newSLines)
                file.close()
                print(CGREEN+"Class edited"+CEND)
                #changes saved to subject database
                messagebox.showinfo("Success","Class edited")
                RefreshEditTree()
                #the edit tree table is refreshed to reflect any changes
                CloseEditClass()
                #Once saved , the edit class window will automatically close
            def CloseEditClass():
                print(CRED+"Close command recieved"+CEND)
                global CloseBindTree
                try:
                    CloseBindTree()
                except:
                    pass
                EditClassConfirmScreen.destroy()
            EditClassConfirmScreen.protocol("WM_DELETE_WINDOW",CloseEditClass)
            tkinter.Button(EditClassConfirmScreen,text="Save Any Changes",fg='green',command=SaveChangesEditConfirmed,bd=0).grid(column=1,row=11)
        EditTree.bind("<Double-1>",EditClassConfirm)
        EditClassScreen.protocol("WM_DELETE_WINDOW",CloseEditTree)
    tkinter.Button(manageClassWindow,text="Edit Class",fg="green",command=EditClass,bd=0).grid(column=1,row=2)
    '''
    Module Name:- closeManageClassWindow
    Module Purpose:- To imitate child/parent inheritance
    Module Arguments:- None
    Module Inputs:- All Open windows
    Module Outputs:- Close commands for all children windows
    '''
    def closeManageClassWindow():
        print(CRED+"CLose command recieved"+CEND)
        global closeAddClassScreen
        global CloseEditTree
        global CloseDeleteClassWindow
        try:
            closeAddClassScreen()
        except:
            pass
        try:
            CloseEditTree()
        except:
            pass
        try:
            CloseDeleteClassWindow()
        except:
            pass
        manageClassWindow.destroy()
    manageClassWindow.protocol("WM_DELETE_WINDOW",closeManageClassWindow)
    tkinter.Button(manageClassWindow,text="Exit..",fg='red',command=closeManageClassWindow,bd=0).grid(column=1,row=4)
    manageClassWindow.mainloop()
'''
Module Name:- AddUser
Module Purpose:- To create a form that allows the user to add a user to the system
Module Arguments:- user(the current user who logged in)
Module Inputs:- Current logged in user
Module Outputs:- a screen with a form that is capable of adding a user
'''
def AddUser(user):
    if CheckOpen("Add User"):
        return False
    AddUserScreen = tkinter.Toplevel(loginScreen)
    AddUserScreen.resizable(0,0)
    inter_temp = []
    AddUserScreen.title("Add User")
    tkinter.Label(AddUserScreen,text="Fill the user form").grid(column=1,row=0)
    tkinter.Label(AddUserScreen,text="User Name:").grid(column=0,row=1)
    NameEntry=tkinter.Entry(AddUserScreen,width=23)
    NameEntry.grid(column=1,row=1)
    
    tkinter.Label(AddUserScreen,text="Password:").grid(column=0,row=2)
    PassEntry = tkinter.Entry(AddUserScreen,show="*",width=23)
    PassEntry.grid(column=1,row=2)

    tkinter.Label(AddUserScreen,text="Role:").grid(column=0,row=3)
    RoleCombo = ttk.Combobox(AddUserScreen,state='readonly')
    RoleCombo.grid(column=1,row=3)
    print(CGREEN+"User add screen initialised"+CEND)
    k = 0
    file = open("roles.csv","r+")
    roleLines=file.readlines()
    file.close()
    comboArr = []
    while k<len(roleLines):
        if roleLines[k] == "" or roleLines[k]== "\n":
            pass
        else:
            comboArr.append(roleLines[k].split(',')[0])
        k+=1
    RoleCombo.config(values=comboArr)
    tkinter.Label(AddUserScreen,text="Email:").grid(column=0,row=4)
    EmailEntry = tkinter.Entry(AddUserScreen,width=23)
    EmailEntry.grid(column=1,row=4)
    
    '''
    Module Name:- EmailEntryCheck
    Module Purpose:- To toggle the 2FA entry box depending on the state of the 2FA enabled check button
    Module Args:- a,b,c(these arguments are passed by default when using .trace and is ignored)
    Module Inputs:- current check button state
    Module Outputs:- Changed entry box state to reflect the state of the check button
    '''
    def EmailEntryCheck(a,b,c):
        #toggle the entry box
        if twoFACheck.instate(['!selected']):
            print(CGREEN+"2FA Enabled"+CEND)
            EmailEntry.config(state='normal')
            EmailEntry.delete(0,tkinter.END)
        else:
            print(CRED+"2FA Disabled"+CEND)
            EmailEntry.delete(0,tkinter.END)
            EmailEntry.insert(tkinter.INSERT,"Enable 2FA")
            EmailEntry.config(state='disabled')
        EmailEntry.update_idletasks()

    tkinter.Label(AddUserScreen,text="2FA Enabled?").grid(column=0,row=5)
    tracerVar = tkinter.IntVar()
    twoFACheck = ttk.Checkbutton(AddUserScreen,variable=tracerVar)
    twoFACheck.state(['!alternate'])
    twoFACheck.state(['selected'])
    tracerVar.trace('w',EmailEntryCheck)
    twoFACheck.grid(column=1,row=5)
    
    tkinter.Label(AddUserScreen,text="Enrol to a Class").grid(column=0,row=6)
    '''
    Module Name:- Enrol_Sub
    Module Purpose:- To a enrol/waitlist the user into a subject. this is a sub screen
    Module Args:- None
    Module Inputs:-Subjects database information
    Module Outputs:- table of information about subjects that the user can enrol to
    '''
    def Enrol_Sub():
        global inter_temp
        global EnrolSubScreen
        inter_temp=[]
        # the initial plan for inter_temp was to use it as the standard default global variable to pass info between different subscreens but was later scrapped due to data conflicts.
        #Now the variable is only referenced in AddClass
        if CheckOpen("Pick Subjects to Enrol to"):return False
        EnrolSubScreen = tkinter.Toplevel(loginScreen)
        EnrolSubScreen.title("Pick Subjects to Enrol to")
        EnrolSubScreen.resizable(0,0)

        tkinter.Label(EnrolSubScreen,text="Double Click to Add/Remove Subjects to Enrol").grid(column=1,row=0)

        TreeFrame = tkinter.Frame(EnrolSubScreen)
        TreeFrame.grid(column=1,row=1)

        EnrolSubTreeview=ttk.Treeview(TreeFrame,columns=["Spots Left","Waitlisted","Teacher"])
        print(CGREEN+"Enrol SUb Screen Initialised"+CEND)
        EnrolSubTreeview.heading("#0",text="Subject/Class")
        EnrolSubTreeview.heading("Spots Left",text="Spots Left")
        EnrolSubTreeview.heading("Waitlisted",text="Waitlisted")
        EnrolSubTreeview.heading("Teacher",text="Teacher")
        '''
        Module Name:- refresh_EnrolSubTreeview
        Module Purpose:- to refresh the subjects that can be enrolled to
        Module Args:- None
        Module Inputs:- currently enrolled subjects , all subjects in the system
        Module Outputs:- Any subjects that the user can join to that has enough spaces will be plotted onto the table
        '''
        def refresh_EnrolSubTreeview(): 
            EnrolSubTreeview.delete(*EnrolSubTreeview.get_children())
            
            file = open("users.csv","r+")
            userLines=file.readlines()
            file.close()

            file = open("subjects.csv","r+")
            subjectLines=file.readlines()
            file.close()
            
            file = open("waitlist.csv","r+")
            waitlistLines=file.readlines()
            file.close()
            
            i = 0
            toAdd = []

            while i<len(subjectLines):
                count_enrol = 0
                count_wait = 0
                row = subjectLines[i].split(',')

                if len(row)!=subjectLEN:
                    i+=1
                    continue
                
                for t in range(0,len(row)):row[t]=row[t].strip()
                
                tempSubjectName = row[0]
                tempClassName = row[1]
                tempMax = row[2]
                tempTeacher = row[5]
                
                k = 0
                #this bit of code with the UserLines is used to calculate the amount of users who have enrolled to a certain subject
                while k<len(userLines):
                    row2 = userLines[k].split(',')
                
                    if len(row2)!=userLEN:
                        k+=1
                        continue
                
                    for t in range(0,len(row2)):row2[t]=row2[t].strip()
                
                    subjectList=row2[2].split('.')
                
                    r = 0
                    if row2[2] == "":
                        k+=1
                        continue
                    while r<len(subjectList):
                        if subjectList[r] == tempSubjectName and subjectList[r+1] == tempClassName:
                            #count_enrol is the temp variable used to track users who have already enrolled to this subject
                            count_enrol+=1
                        r+=2
                    k+=1
                k = 0
                #this bit of code is used to determine the amount of users who have already waitlisted to this subject
                while k<len(waitlistLines):
                    row2 = waitlistLines[k].split(',')
               
                    if len(row2) != 3:
                        k+=1
                        continue
               
                    for t in range(0,len(row2)):row2[t]=row2[t].strip()
               
                    if row2[1] == tempSubjectName and row2[2] == tempClassName:
                        count_wait+=1
                    k+=1
               #all the collected data is passed onto a matrix , which would later be accessed by the insertion algo
                toAdd.append((tempSubjectName,tempClassName,tempMax,tempTeacher,count_enrol,count_wait))
               
                i+=1
                #all variables deleted to optimize memory(this practice was stopped due to time constraints)
                del tempClassName,tempMax,tempSubjectName,tempTeacher,k,count_wait,count_enrol
            #data successfully collected, insertion begins from here
            del i
            #insertion \/
            i = 0
            #inserts all the classes under categories
            while i<len(toAdd):
                subject,class_,max_,teacher,intEnrolCount,intWaitCount=toAdd[i]
                print(CGREEN+f"Loaded {subject}:{class_} with {max_} spots."+CEND)
                k = 0
                parent_id = ""
                existingParents = list(EnrolSubTreeview.get_children())

                if len(existingParents) == 0:
                    parent_id = EnrolSubTreeview.insert("",tkinter.END,text=subject)
                    EnrolSubTreeview.insert(parent_id,tkinter.END,text=class_,values=[str(int(max_)-int(intEnrolCount)),intWaitCount,teacher])
            
                    i+=1
                    continue
            
                while k<len(existingParents):
            
                    try:
                        tempParent = EnrolSubTreeview.item(existingParents[k])["text"]
                    except:
                        tempParent=None
            
                    if tempParent == subject:
                        parent_id = existingParents[k]
                        break
                    else:
                        k+=1
            
                if parent_id != "":
                    EnrolSubTreeview.insert(parent_id,tkinter.END,text=class_,values=[str(int(max_)-int(intEnrolCount)),intWaitCount,teacher])
                else:
                    parent_id = EnrolSubTreeview.insert("",tkinter.END,text=subject)
                    EnrolSubTreeview.insert(parent_id,tkinter.END,text=class_,values=[str(int(max_)-int(intEnrolCount)),intWaitCount,teacher])
                i+=1
            #process over
        
        ScrollY = ttk.Scrollbar(TreeFrame,command=EnrolSubTreeview.yview,orient=tkinter.VERTICAL)
        ScrollY.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        
        ScrollX = ttk.Scrollbar(TreeFrame,command=EnrolSubTreeview.xview,orient=tkinter.HORIZONTAL)
        ScrollX.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        
        EnrolSubTreeview.configure(xscrollcommand=ScrollX.set)
        EnrolSubTreeview.configure(yscrollcommand=ScrollY.set)
        EnrolSubTreeview.pack(side=tkinter.TOP,expand='false')
        '''
        Module Name:- EnrolSubScreenEXIT
        Module Purpose:- To close child windows and confirm the user with a message
        Module args:- none
        Module Inputs:- None
        Module Outputs:- child windows closed
        '''
        def EnrolSubScreenEXIT():
            print(CRED+"Close command received"+CEND)
            global SearchEnrolSubScreen
            try:
                SearchEnrolSubScreen.destroy()
            except:
                pass
            if messagebox.askyesno("Confirm","Closing this window would save the changes. You cannot reopen this window due to technical limitations.Continue?"):
                EnrolButton.config(text="Saved")
                EnrolButton.config(state='disabled')
                EnrolSubScreen.destroy()
        tkinter.Button(EnrolSubScreen,text="Save Changes",fg="green",command=EnrolSubScreenEXIT,bd=0).grid(column=1,row=2)
        '''
        Module Name:- SearchEnrolSub
        Module Purpose:- a screen with a search form for the Enrolments table
        Module args:- none
        Module Inputs:- None
        Module Outputs:- A screen with a search form
        '''
        def SearchEnrolSub():
            global SearchEnrolSubScreen
            if CheckOpen("Search (EnrolSubTreeview)"):
                return False
            SearchEnrolSubScreen = tkinter.Toplevel(loginScreen)
            SearchEnrolSubScreen.title("Search (EnrolSubTreeview)")
            SearchEnrolSubScreen.resizable(0,0)
        
            tkinter.Label(SearchEnrolSubScreen,text="Search..",fg='purple').grid(column=1,row=0)
        
            SubjectEntry = tkinter.Entry(SearchEnrolSubScreen,width=23)
            SubjectEntry.grid(column=1,row=1)
        
            tkinter.Label(SearchEnrolSubScreen,text="Subject:").grid(column=0,row=1)
            print(CGREEN+"Search enrol screen initialised"+CEND)
            ClassEntry = tkinter.Entry(SearchEnrolSubScreen,width=23)
            ClassEntry.grid(column=1,row=2)
        
            tkinter.Label(SearchEnrolSubScreen,text="Class:").grid(column=0,row=2)
            ModeCombo = ttk.Combobox(SearchEnrolSubScreen,values=['Linear','Binary'],state='readonly')
            ModeCombo.grid(column=1,row=3)
            ModeCombo.set("Linear")
        
            tkinter.Label(SearchEnrolSubScreen,text="Mode:").grid(column=0,row=3)
            '''
            Module name:- SearchConfirmEnrol
            Module Purpose:- To search the table using the provided information in the form
            Module Args:- none
            Module Inputs:- classname,subjectname and mode , all the rows in the table
            Module Outputs:- Highlighted class on the table that the user is searching for
            '''
            def SearchConfirmEnrol():
                givenSubject = SubjectEntry.get()
                givenClass = ClassEntry.get()
                givenMode = ModeCombo.get()
                #checks whether the input exists
                if givenSubject == "" or givenClass=="" or givenMode == "":
                    print(CRED+"Missing data"+CEND)
                    messagebox.showerror("Error","Fill all the boxes")
                    return False
                
                #applies the correct algo
                if givenMode == "Linear":
                    existingSubjects = EnrolSubTreeview.get_children()
                    i = 0
                    while i<len(existingSubjects):
                        if EnrolSubTreeview.item(existingSubjects[i])['text'] == givenSubject:
                            print(CGREEN+"Subject found"+CEND)
                            existingClasses=EnrolSubTreeview.get_children(existingSubjects[i])
                            k = 0
                            while k<len(existingClasses):
                                if EnrolSubTreeview.item(existingClasses[k])['text'] == givenClass:
                                    print(CGREEN+"Class found"+CEND)
                                    #highlights item in table after linear search
                                    EnrolSubTreeview.item(existingSubjects[i],open=True)
                                    EnrolSubTreeview.focus(existingClasses[k])
                                    EnrolSubTreeview.selection_set(existingClasses[k])
                
                                    messagebox.showinfo("Success","Item has been highlighted for you in the list")
                
                                    ClassEntry.delete(0,tkinter.END)
                                    SubjectEntry.delete(0,tkinter.END)
                
                                    return False
                                k+=1
                            print(CRED+"Class missing"+CEND)
                            messagebox.showerror("Error","Class Not Found")
                            ClassEntry.delete(0,tkinter.END)
                
                            return False
                        i+=1
                    print(CRED+"Subject/Class missing"+CEND)
                    messagebox.showerror("Error","Subject/Class Not Found")
                    SubjectEntry.delete(0,tkinter.END)
                
                    return False
                elif givenMode == "Binary":
                    existingSubjects = EnrolSubTreeview.get_children()
                    NEWexistingSubjects = []
                    
                    for item in existingSubjects:
                        NEWexistingSubjects.append(EnrolSubTreeview.item(item)['text'])
                    
                    NEWexistingSubjects=QuickieSort(NEWexistingSubjects)
                    #the subjects are now sorted
                    if binarySearchAppr(NEWexistingSubjects,0,len(NEWexistingSubjects)-1,givenSubject):
                        for t in existingSubjects:
                            if EnrolSubTreeview.item(t)['text'] == givenSubject:
                                existingClasses = EnrolSubTreeview.get_children(t)
                                #gets the children for that subject
                        print(CGREEN+"Subject Found"+CEND)
                        NEWexistingClasses = []
                        for item in existingClasses:
                            NEWexistingClasses.append(EnrolSubTreeview.item(item)['text'])
                        
                        #sort the children
                        NEWexistingClasses = QuickieSort(NEWexistingClasses)
                        
                        if binarySearchAppr(NEWexistingClasses,0,len(NEWexistingClasses)-1,givenClass):
                            print(CGREEN+"Class Found"+CEND)
                            for item in existingSubjects:
                                if givenSubject == EnrolSubTreeview.item(item)['text']:
                                    for t in existingClasses:
                                        if givenClass == EnrolSubTreeview.item(t)['text']:
                                            #checks whether subject and user is what we are looking for
                                            EnrolSubTreeview.item(item,open=True)
                                            EnrolSubTreeview.focus(t)
                                            EnrolSubTreeview.selection_set(t)

                                            messagebox.showinfo("Success","Item has been highlighted for you in the table")
                                            
                                            ClassEntry.delete(0,tkinter.END)
                                            SubjectEntry.delete(0,tkinter.END)
                                            
                                            return False
                        else:
                            print(CRED+"Class not found"+CEND)
                            messagebox.showerror("Error","Class not found")
                            ClassEntry.delete(0,tkinter.END)
                            
                            return False
                    else:
                        print(CRED+"Subject not found"+CEND)
                        messagebox.showerror("Error","Subject not found")
                        SubjectEntry.delete(0,tkinter.END)

                        return False
                else:
                    messagebox.showerror("Error","Incorrect Mode")
            tkinter.Button(SearchEnrolSubScreen,text="Search",fg='green',command=SearchConfirmEnrol).grid(column=1,row=4)
        
        tkinter.Button(EnrolSubScreen,text="Search...",fg="blue",command=SearchEnrolSub,bd=0).grid(column=0,row=2)
        '''
        Module Name:- SortEnrolSub
        Module Purpose:- A algorithm that sorts the table using quicksort
        Module Args:- None
        Module Inputs:- all the rows on the table
        Module Outputs:- sorted table
        '''
        def SortEnrolSub():
            existingSubjects = EnrolSubTreeview.get_children()
            i = 0 
            newExistingSubjects=[]

            for i in existingSubjects:
                newExistingSubjects.append(EnrolSubTreeview.item(i)['text'])
            
            newExistingSubjects = QuickieSort(newExistingSubjects)
            finalInsert= []

            for i in newExistingSubjects:
                for t in existingSubjects:
                    if EnrolSubTreeview.item(t)['text'] == i:
                        ExistingClasses=EnrolSubTreeview.get_children(t)
                        newExistingClasses = []
                        
                        for k in ExistingClasses:newExistingClasses.append(EnrolSubTreeview.item(k)['text'])
                        newExistingClasses = QuickieSort(newExistingClasses)
                        newInsertClasses = []
                        
                        for k in newExistingClasses:
                            for p in ExistingClasses:
                                if EnrolSubTreeview.item(p)['text'] == k:
                                    valueTEMP = EnrolSubTreeview.item(p)['values']
                                    newInsertClasses.append((EnrolSubTreeview.item(p)['text'],valueTEMP[0],valueTEMP[1],valueTEMP[2]))
                        
                        finalInsert.append((EnrolSubTreeview.item(t)['text'],newInsertClasses))
            i = 0
            EnrolSubTreeview.delete(*EnrolSubTreeview.get_children())
            
            while i<len(finalInsert):
                subject,classes = finalInsert[i]
                existingSubjects = EnrolSubTreeview.get_children()
            
                if len(existingSubjects) == 0:
                    tempID=EnrolSubTreeview.insert("",tkinter.END,text=subject)
            
                    k = 0
                    while k<len(classes):
                        EnrolSubTreeview.insert(tempID,tkinter.END,text=classes[k][0],values=[classes[k][1],classes[k][2],classes[k][3]])
                        k+=1
                    i+=1
                    continue
            
                k = 0
                while k<len(existingSubjects):
                    if EnrolSubTreeview.item(existingSubjects[k])['text'] == subject:
                        r = 0
                        while r<len(classes):
                            EnrolSubTreeview.insert(existingSubjects[k],tkinter.END,text=classes[k][0],values=[classes[k][1],classes[k][2],classes[k][3]])
                            r+=1
                        i+=1
                        continue
                    k+=1
                tempID=EnrolSubTreeview.insert("",tkinter.END,text=subject)
            
                k = 0
                while k<len(classes):
                    EnrolSubTreeview.insert(tempID,tkinter.END,text=classes[k][0],values=[classes[k][1],classes[k][2],classes[k][3]])
                    k+=1
                i+=1
            print(CGREEN+"Sorted"+CEND)
        tkinter.Button(EnrolSubScreen,text="Sort...",fg='blue',command=SortEnrolSub,bd=0).grid(column=2,row=2)
        '''
        Module Name:- AddRemoveSubjects
        Module Purpose:- To add or remove the selected enrolement from the new user
        Module Args:- event(passed by default on python, ignored)
        Module Inputs:- The selected class
        Module Outputs:- changes to the inter_temp global(removal or adding enrolement)
        '''
        def AddRemoveSubjects(event):
            global inter_temp
            item2 = EnrolSubTreeview.focus()

            parent = EnrolSubTreeview.parent(item2)

            row = EnrolSubTreeview.item(EnrolSubTreeview.focus())

            try:
                #figure out whether user clicked on class or subject
                className = row['text']
                if EnrolSubTreeview.item(parent)['text'] == "":
                    print(CRED+"No parent.. Cannot modify subjects"+CEND)
                    return False
                classSpots = row['values'][0]
                classWaitlisted = row['values'][1]
                classTeacher = row['values'][2]
                del classWaitlisted,classTeacher
            except:
                return False
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
            subjectName = EnrolSubTreeview.item(parent)['text']
            #checks for whether the user is already enrolled/waitlisted to this subject , if he is , triggers the unenrolement algo
            if re.search("^ENROLLED:",className) or re.search("^WAITLISTED:",className):
                #confirms action
                print(CGREEN+"Waitlisted/Enrolled class detected"+CEND)
                if messagebox.askyesno("Confirm","Do you want to unenrol/unwaitlist from this subject?"):
                    classNameF = ""
                    i = 0
                    #removes the enrolement from inter_temp
                    while i<len(inter_temp):
                        tempMode,tempSub,tempClass=inter_temp[i]
                        if tempMode=="enrol":
                            classNameF=re.sub("ENROLLED:","",className)
                            if tempSub == subjectName and tempClass==classNameF:
                                print(CGREEN+"Class removed from enrolemnt list"+CEND)
                                del inter_temp[i]
                        else:
                            classNameF=re.sub("WAITLISTED:","",className)
                            if tempSub==subjectName and tempClass==classNameF:
                                print(CGREEN+"Class removed from the waitlist list"+CEND)
                                del inter_temp[i]                        
                        i+=1
                    #itirates the items then changes the name of the enrolement back to normal
                    for item in list(EnrolSubTreeview.get_children()):
                        if EnrolSubTreeview.item(item)['text'] == subjectName:
                            for item2 in list(EnrolSubTreeview.get_children(item)):
                                if EnrolSubTreeview.item(item2)['text'] == className:
                                    row = EnrolSubTreeview.item(item2)['values']
                                    valueArray = [row[0],row[1],row[2]]
                                    EnrolSubTreeview.item(item2,text=classNameF,values=valueArray)
        
                return False
            #if the class isnt already enrolled or waitlisted , the enrolement algo executes
            i = 0
            timeArr = []
            #the following algo checks for clashes in the existing enrolements , it does this by itirating the inter_temp and obtaining time data of all the currently enrolled classes
            while i<len(inter_temp):
                mode,tempSubI,tempClassI = inter_temp[i]
                del mode
                k = 0
                while k<len(subjectLines):
                    row2 = subjectLines[k].split(',')
                    if len(row2)!=subjectLEN:
                        k+=1
                        continue
                    for t in range(len(row2)):row2[t] = row2[t].strip()
                    if row2[0] == tempSubI and row2[1] == tempClassI:
                        #time data unpacking is time consuming
                        timeData = row2[3].split('.')
                        fromD,fromMo,fromY = timeData[0].split(':')
                        toD,toMo,toY = timeData[1].split(':')
                        fromH,fromMi = timeData[2].split(':')
                        toH,toMi = timeData[3].split(':')
                        monthswith31 = [1,3,5,7,8,10,12]
                        rState = timeData[4]
                        fromY=int(fromY)
                        fromMo = int(fromMo)
                        fromD = int(fromD)
                        toD = int(toD)
                        toMo = int(toMo)
                        toY = int(toY)
                        fromH = int(fromH)
                        fromMi = int(fromMi)
                        toH = int(toH)
                        toMi = int(toMi)
                        timeFrom = 0
                        timeTo = 0
                        n = 0
                        while n<fromY:
                            if n%4 == 0:
                                timeFrom+=366*24*60
                            else:
                                timeFrom+=365*24*60
                            n+=1
                        n = 1
                        while n<fromMo:
                            if n in monthswith31:
                                timeFrom+=31*24*60
                            elif n == 2:
                                if fromY%4 == 0:
                                    timeFrom+=29*24*60
                                else:
                                    timeFrom+=28*24*60
                            else:
                                timeFrom+=30*24*60
                            n+=1
                        timeFrom+=fromD*24*60
                        timeFrom+=fromH*60
                        timeFrom+=fromMi
                        n = 0
                        while n<toY:
                            if n%4 == 0:
                                timeTo+=366*24*60
                            else:
                                timeTo+=365*24*60
                            n+=1
                        n = 0
                        while n<toMo:
                            if n in monthswith31:
                                timeFrom+=31*24*60
                            elif n == 2:
                                if toY%4 == 0:
                                    timeFrom+=29*24*60
                                else:
                                    timeFrom+=28*24*60
                            else:
                                timeFrom+=30*24*60
                            n+=1
                        timeTo+=toD*24*60
                        timeTo+=toH*60
                        timeTo+=toMi
                        #once the times are obtained , they are appended to a array and passed on below
                        timeArr.append((row2[0],row2[1],timeFrom,timeTo,rState,fromH,fromMi,toH,toMi))
                        break
                    k+=1
                i+=1
            i = 0
            curr = []
            #the following algo checks for time data in the class that we are searching for , it does this by itirating the subject database for the selected class
            while i<len(subjectLines):
                row2 = subjectLines[i].split(',')
                if len(row2) != subjectLEN:
                    i+=1
                    continue
                for t in range(len(row2)):row2[t] = row2[t].strip()
                if row2[0] == subjectName and row2[1] == className:
                    timeData = row2[3].split('.')
                    fromD,fromMo,fromY = timeData[0].split(':')
                    toD,toMo,toY = timeData[1].split(':')
                    fromH,fromMi = timeData[2].split(':')
                    toH,toMi = timeData[3].split(':')
                    monthswith31 = [1,3,5,7,8,10,12]
                    rState = timeData[4]
                    fromY=int(fromY)
                    fromMo = int(fromMo)
                    fromD = int(fromD)
                    toD = int(toD)
                    toMo = int(toMo)
                    toY = int(toY)
                    fromH = int(fromH)
                    fromMi = int(fromMi)
                    toH = int(toH)
                    toMi = int(toMi)
                    timeFrom = 0
                    timeTo = 0
                    n = 0
                    while n<fromY:
                        if n%4 == 0:
                            timeFrom+=366*24*60
                        else:
                            timeFrom+=365*24*60
                        n+=1
                    n = 1
                    while n<fromMo:
                        if n in monthswith31:
                            timeFrom+=31*24*60
                        elif n == 2:
                            if fromY%4 == 0:
                                timeFrom+=29*24*60
                            else:
                                timeFrom+=28*24*60
                        else:
                            timeFrom+=30*24*60
                        n+=1
                    timeFrom+=fromD*24*60
                    timeFrom+=fromH*60
                    timeFrom+=fromMi
                    n = 0
                    while n<toY:
                        if n%4 == 0:
                            timeTo+=366*24*60
                        else:
                            timeTo+=365*24*60
                        n+=1
                    n = 0
                    while n<toMo:
                        if n in monthswith31:
                            timeFrom+=31*24*60
                        elif n == 2:
                            if toY%4 == 0:
                                timeFrom+=29*24*60
                            else:
                                timeFrom+=28*24*60
                        else:
                            timeFrom+=30*24*60
                        n+=1
                    timeTo+=toD*24*60
                    timeTo+=toH*60
                    timeTo+=toMi
                    #the time data is passed on below
                    curr.append((set(range(timeFrom,timeTo)),rState,fromH,fromMi,toH,toMi))
                    break
                i+=1
            i = 0
            tSet,rsS,fHs,fMiS,tHs,toMis = curr[0]
            fromTime = int(fHs)*60+int(fMiS)
            toTime = int(tHs)*60+int(toMis)
            currTime = set(range(fromTime,toTime))
            while i<len(timeArr):
                sub,clas,tF,tT,rS,fH,fMi,tH,tMi = timeArr[i]
                #sub is subject name
                #clas is class name
                #tF is timeFrom(total minutes from 0 till the from date)
                #tT is the timeTo(total minutes from 0 till the to date)
                #tH is the toHour
                #tMi is the toMinutes
                #fH is the fromHour
                #fMi is the fromMinutes
                #checks whether the class is in the same repeat date as the class that we are attempting to enrol to
                if rS == rsS and rS == "Everyday":
                    #checks for whether there is any intersection between the times given
                    if len(tSet.intersection(set(range(tF,tT))))>0:
                        fromTime = int(fH)*60+int(fMi)
                        toTime = int(tH)*60+int(tMi)
                        #checks whether the times in the day collide
                        if len(set(range(fromTime,toTime)).intersection(currTime))>0:
                            print(CRED+"Class found!"+CEND)
                            #asks whether the user wants to force the clash(some students are smart and the system must accomodate for that)
                            if not(messagebox.askyesno("Confirm","Class clash detected with "+sub+","+clas+". Do you want to force clash?")):
                                return False
                            break
                i+=1
            #once the clashes are over , checks for whether there is enough spaces in the class for the user to waitlist
            if int(classSpots)<=0:
                print(CRED+"Not enough spaces for enrolements"+CEND)
                #if there isnt , confirms user whether he wants to waitlist
                if messagebox.askyesno("Class Full!","This class is full. Do you want to waitlist to this class?"):
                    inter_temp.append(("waitlist",subjectName,className))
                    for item in list(EnrolSubTreeview.get_children()):
                        if EnrolSubTreeview.item(item)['text'] == subjectName:
                            for item2 in list(EnrolSubTreeview.get_children(item)):
                                if EnrolSubTreeview.item(item2)['text'] == className:
                                    row = EnrolSubTreeview.item(item2)['values']
                                    valueArray = [row[0],row[1],row[2]]
                                    #appends "WAITLISTED:" for the program to quickly detect that the user has already waitlisted
                                    EnrolSubTreeview.item(item2,text="WAITLISTED:"+className,values=valueArray)
                    print(CGREEN+"Waitlisted"+CEND)
                    messagebox.showinfo("Confirm","Successfully waitlisted. Finalise the account to save changes")    
                else:
                    messagebox.showerror("Error","Task Cancelled.")
                    return False
            else:
                #if there are enough spoaces , appends enrolment to intertemp
                inter_temp.append(("enrol",subjectName,className))
              
                for item in list(EnrolSubTreeview.get_children()):
              
                    if EnrolSubTreeview.item(item)['text'] == subjectName:
              
                        for item2 in list(EnrolSubTreeview.get_children(item)):
              
                            if EnrolSubTreeview.item(item2)['text']==className:
              
                                row2 = EnrolSubTreeview.item(item2)['values']
                                valueArray = [row2[0],row2[1],row2[2]]
                                #appends ENROLLED: for the program to quickly detect that the user has enrolled
                                EnrolSubTreeview.item(item2,text="ENROLLED:"+className,values=valueArray)
                print(CGREEN+"Enrolled"+CEND)
                messagebox.showinfo("Success","Successfully Added to Enrolement List. Finalise the account or pick more subjects!")
        
        EnrolSubTreeview.bind("<Double-1>",AddRemoveSubjects)
       
        refresh_EnrolSubTreeview()
       
        global WarningMessage
        #closes the children windows
        '''
        Module Name:- WarningMessage
        Module Purpose:- Closes child subscreens
        Module Args:- none
        Module Inputs:- None
        Module outputs:- Close commands for sub screens
        '''
        def WarningMessage():
            print(CRED+"Close command receieved"+CEND)
            global SearchEnrolSubScreen
            try:
                SearchEnrolSubScreen.destroy()
            except:
                pass
            EnrolSubScreen.destroy()
        EnrolSubScreen.protocol("WM_DELETE_WINDOW",WarningMessage)
        EnrolSubScreen.mainloop()
    
    EnrolButton=tkinter.Button(AddUserScreen,text="Enrol",command=Enrol_Sub,fg="darkblue",bd=0)
    EnrolButton.grid(column=1,row=6)    
    
    tkinter.Label(AddUserScreen,text="Bind To A Class(Teacher)").grid(column=0,row=7)
    #this variable is used to pass the bound class to confirm func
    BoundSub=[]
    '''
    Module Name:- Bind_Sub
    Module Purpose:- To bind a user to a subject
    Module Args:- None
    Module Inputs:- Currently bound users and subject info
    Module Outputs:- table with subjects that the user can bind to
    '''
    def Bind_Sub():
        global BoundSub
        BoundSub = []
        global BindSubScreen
    
        if CheckOpen("Bind to a Class"):return False
    
        BindSubScreen = tkinter.Toplevel(loginScreen)
        BindSubScreen.title("Bind to a Class")
        tkinter.Label(BindSubScreen,text="Binding a user to a class, would override role perms for the user , within that class.",fg="red").grid(column=1,row=0)
        BindSubScreenTFrame = tkinter.Frame(BindSubScreen)
        BindSubScreenTFrame.grid(column=1,row=1)
        BindSubScreen.resizable(0,0)
    
        BindSubTree = ttk.Treeview(BindSubScreenTFrame)
        BindSubTree.heading("#0",text="Subject/Class")
    
        YScroll = ttk.Scrollbar(BindSubScreenTFrame,orient="vertical",command=BindSubTree.yview)
        XScroll = ttk.Scrollbar(BindSubScreenTFrame,orient="horizontal",command=BindSubTree.xview)
    
        BindSubTree.configure(yscrollcommand=YScroll.set)
        BindSubTree.configure(xscrollcommand=XScroll.set)
        print(CGREEN+"Bind sub screen initialised"+CEND)
        YScroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        XScroll.pack(side=tkinter.BOTTOM,fill=tkinter.X)
    
        BindSubTree.pack(side=tkinter.LEFT)
        '''
        Module Name:- refresh_BindSubTree
        Module Purpose:- Refresh the bind tree
        Module Args:- None
        Module Inputs:- Subject Database
        Module Outputs:- Bind tree filled with data
        '''
        def refresh_BindSubTree():
            BindSubTree.delete(*BindSubTree.get_children())
    
            file = open("subjects.csv","r+")
            subjectLines=file.readlines()
            file.close()
    
            i = 0
            toAdd = []
            #subjects are checked for whether they are already bound to a user
            while i<len(subjectLines):
                row = subjectLines[i].split(',')
    
                if len(row)!=subjectLEN:
                    i+=1
                    continue
    
                for t in range(0,len(row)):row[t]=row[t].strip()
    
                if row[5] == "":
                    print(CGREEN+f"loaded {row[0]}:{row[1]} as a bindable class"+CEND)
                    toAdd.append((row[0],row[1]))
                i+=1
    
            i = 0
            while i<len(toAdd):
                parent_id=""
    
                tempSub,tempClass = toAdd[i]
                existingParents = BindSubTree.get_children()
                existingParents=list(existingParents)
                p = False
                for t in existingParents:
                    if BindSubTree.item(t)['text'] == tempSub:
                        parent_id=t
                        BindSubTree.insert(parent_id,tkinter.END,text=tempClass)
                        p=True
                        i+=1
                        break
                if p:
                    continue
                parent_id=BindSubTree.insert("",tkinter.END,text=tempSub)
                BindSubTree.insert(parent_id,tkinter.END,text=tempClass)
    
                i+=1

        refresh_BindSubTree()
        '''
        Module Name:- BindUserToClass
        Module Purpose:- Bind the user to the class that is selected
        Module Args:- None
        Module Inputs:- Selected class
        Module Outputs:-table reflects changes
        '''
        def BindUserToClass(event):
            global BoundSub
            try:
                if len(list(BindSubTree.get_children(BindSubTree.focus())))==0:
                    givenClass = BindSubTree.item(BindSubTree.focus())['text']
                else:
                    print(CRED+"Subject cannot be selected"+CEND)
                    raise TypeError
                subjectName=BindSubTree.item(BindSubTree.parent(BindSubTree.focus()))['text']
            except:
                return False
            #checks whether the user has already bound
            if re.search("^BOUND:",givenClass):

                if messagebox.askyesno("Confirm","Unbind from this class?"):
                
                    i = 0
                    print(CRED+"Un bound"+CEND)
                    givenClass=re.sub("^BOUND:","",givenClass)
                
                    while i<len(BoundSub):
                        tempSub , tempClass = BoundSub[i]
                
                        if tempSub == subjectName and tempClass == givenClass:
                        
                            BindSubTree.item(BindSubTree.focus(),text=givenClass)
                            del BoundSub[i]
                            break
                
                        i+=1
                return False
            BindSubTree.item(BindSubTree.focus(),text="BOUND:"+givenClass)
            BoundSub.append((subjectName,givenClass))
            print(CGREEN+"Bound"+CEND)
            messagebox.showinfo("Success","User Bound to class")
        BindSubTree.bind("<Double-1>",BindUserToClass)
        '''
        Module Name:- SaveChangesBindSub
        Module Purpose:- Close the window
        Module args:- none
        Module Inputs:- Window currently open
        Module Outputs:- Close command
        '''
        def SaveChangesBindSub():
            if messagebox.askyesno("Confirm","Reopening this window would delete all previous binds. Continue?"):
                print(CRED+"Close command received"+CEND)
                try:
                    warningMessageBT()
                except:
                    pass
        tkinter.Button(BindSubScreen,command=SaveChangesBindSub,text="Save Changes",fg="green",bd=0).grid(column=1,row=2)
        '''
        Module Name:- SortBindSub
        Module Purpose:- Sort the BindSubTree
        Module args:- none
        Module Inputs:-  table data
        Module outputs:- sorted table data
        '''
        def SortBindSub():
            existingSubjects = BindSubTree.get_children()
            NEWexistingSubjects=[]

            for subjectID in range(len(existingSubjects)):
                NEWexistingSubjects.append(BindSubTree.item(existingSubjects[subjectID])['text'])

            SortedSubjects=QuickieSort(NEWexistingSubjects)
            
            i = 0

            toInsert = []

            while i<len(SortedSubjects):
                t = 0
                tempSubID = ""

                while t<len(existingSubjects):
                    if SortedSubjects[i] == BindSubTree.item(existingSubjects[t])['text']:
                        tempSubID = existingSubjects[t]
                    t+=1

                tempSubChildren = []
                for item in BindSubTree.get_children(tempSubID):
                    tempSubChildren.append(BindSubTree.item(item)['text'])

                tempSubChildren=QuickieSort(tempSubChildren)
                #children are sorted and inserted with the sorted parent
                toInsert.append((SortedSubjects[i],tempSubChildren))

                i+=1
            i = 0

            BindSubTree.delete(*BindSubTree.get_children())
            #table cleared and sorted data inserted
            while i<len(toInsert):
                subName,classes=toInsert[i]
                existingSubjects = BindSubTree.get_children()

                tempID = ""

                for item in existingSubjects:
                    if BindSubTree.item(item)['text'] == subName:
                        tempID = item

                if tempID == "":
                    tempID=BindSubTree.insert("",tkinter.END,text=subName)

                    for class_ in classes:
                        BindSubTree.insert(tempID,tkinter.END,text=class_)
                else:
                    for class_ in classes:
                        BindSubTree.insert(tempID,tkinter.END,text=class_)
                i+=1
            print(CGREEN+"Sorted"+CEND)
        tkinter.Button(BindSubScreen,text="Sort Table",fg="blue",command=SortBindSub,bd=0).grid(column=0,row=2)
        '''
        Module name:- SearchBindSub
        Module purpose:-a screen with a form to search the BindSubTree
        Module args:- none
        Module Inputs:- None
        Module outputs:- tkinter screen with a form capable of searching BindSubTree
        '''
        def SearchBindSub():
            global SearchBindSubScreen
            if CheckOpen("Search Treeview(SearchBindSubScreen)"):
                return False

            SearchBindSubScreen = tkinter.Toplevel(loginScreen)
            SearchBindSubScreen.title("Search Treeview(SearchBindSubScreen)")
            SearchBindSubScreen.resizable(0,0)

            tkinter.Label(SearchBindSubScreen,text="Mode").grid(column=1,row=0)
            tkinter.Label(SearchBindSubScreen,text="Search Subject:").grid(column=0,row=1)

            SearchEntrySub=tkinter.Entry(SearchBindSubScreen,width=23)
            SearchEntrySub.grid(column=1,row=1)

            tkinter.Label(SearchBindSubScreen,text="Search Class:").grid(column=0,row=2)

            SearchEntryClass = tkinter.Entry(SearchBindSubScreen,width=23)
            SearchEntryClass.grid(column=1,row=2)
            print(CGREEN+"Search Bind screen initialized"+CEND)
            tkinter.Label(SearchBindSubScreen,text="Search Mode:").grid(column=0,row=3)

            SearchCombo = ttk.Combobox(SearchBindSubScreen,values=["Linear","Binary"],state='readonly')
            SearchCombo.set("Linear")
            SearchCombo.grid(column=1,row=3)
            '''
            Module Name:- BindSubSearchConfirm
            Module Purpose:- searches the bind sub tree using the data provided in the form.
            Module args:- none
            Module inputs:- search what(what to look for) , search mode(Mode to use)
            Module Outputs:- error if the item cannot be found, item highlight if the item is found.
            '''
            def BindSubSearchConfirm():
                if SearchEntrySub.get() == "" or SearchEntryClass.get()=="" or SearchCombo.get() == "":
                    print(CRED+"Missing Data"+CEND)
                    messagebox.showerror("Error","Fill all text boxes.")
            
                if SearchCombo.get() == "Linear":
                    i = 0
            
                    existingSubjects = BindSubTree.get_children()
            
                    while i<len(existingSubjects):
            
                        if BindSubTree.item(existingSubjects[i])['text'] == SearchEntrySub.get():
                            k = 0
                            parent_id = existingSubjects[i]
                            existingClasses = BindSubTree.get_children(existingSubjects[i])
            
                            while k<len(existingClasses):
            
                                if BindSubTree.item(existingClasses[k])['text'] == SearchEntryClass.get():
                                    #linear search is run and the item is highlighted            
                                    print(CGREEN+"Class found"+CEND)                        
                                    BindSubTree.item(parent_id,open=True)
                                    BindSubTree.focus(existingClasses[k])
                                    BindSubTree.selection_set(existingClasses[k])
                                    messagebox.showinfo("Success","Item found! The item has been highlighted in the table")            
                                    return False
                                k+=1
                        i+=1
                    print(CRED+"Unable to find subject/class"+CEND)
                    messagebox.showerror("Error","Unable to find item")
                    return False
                else:
                    i = 0
            
                    existingSubjects = BindSubTree.get_children()
                    existingSubjects=list(existingSubjects)
            
                    for b in range(len(existingSubjects)):
                        existingSubjects[b]=BindSubTree.item(existingSubjects[b])['text']
            
                    existingSubjects = QuickieSort(existingSubjects)

                    if binarySearchAppr(existingSubjects,0,len(existingSubjects)-1,SearchEntrySub.get()):
                        print(CGREEN+"Subject Found"+CEND)
                        existingSubjects = BindSubTree.get_children()
                    
                        for t in range(len(existingSubjects)):
           
                            if BindSubTree.item(existingSubjects[t])['text'] == SearchEntrySub.get():
                                parent_id = existingSubjects[t]
           
                        existingClasses = BindSubTree.get_children(parent_id)
                        newexistingClasses = []
                        
                        for b in range(len(existingClasses)):newexistingClasses.append(BindSubTree.item(existingClasses[b])['text'])
                        existingClasses = newexistingClasses
                        existingClasses = QuickieSort(existingClasses)
                      
                        if binarySearchAppr(existingClasses,0,len(existingClasses)-1,SearchEntryClass.get()):
                            print(CGREEN+"Class found"+CEND)
                            existingClasses = BindSubTree.get_children(parent_id)
                            existingClasses = list(existingClasses)
                      
                            for b in range(len(existingClasses)):
                                #binary search is run and the item is highlighted
                                if BindSubTree.item(existingClasses[b])['text'] == SearchEntryClass.get():
                                    BindSubTree.item(parent_id,open=True)
                                    BindSubTree.focus(existingClasses[b])
                                    BindSubTree.selection_set(existingClasses[b])
                            messagebox.showinfo("Success","Item found! The item has been highlighted in the table")
                            return False
                        else:
                            print(CRED+"Class not found"+CEND)
                            messagebox.showerror("Error","Class not found")
                    else:
                        print(CRED+"Subject not found"+CEND)
                        messagebox.showerror("Error","Subject not found. Check your spelling and try again")
                            
            tkinter.Button(SearchBindSubScreen,text="Search",command=BindSubSearchConfirm,bd=0).grid(column=1,row=4)
            SearchBindSubScreen.mainloop()

        tkinter.Button(BindSubScreen,text="Search Table",fg="blue",command=SearchBindSub,bd=0).grid(column=2,row=2)
        
        tkinter.Label(BindSubScreen,text="Make sure you trust\nthis user",fg="darkred").grid(column=0,row=1)
        tkinter.Label(BindSubScreen,text="Double click to \n set as teacher").grid(column=2,row=1)
        
        global warningMessageBT
        '''
        Module name:- warningmessageBT
        Module purpose:- to close the sub windows and children
        Module args:- none
        Module inputs:- None
        Module outputs:- close command to all sub window children
        '''
        def warningMessageBT():
            global SearchBindSubScreen
            print(CRED+"Close command received"+CEND)
            try:
                SearchBindSubScreen.destroy()
            except:
                pass
            BindSubScreen.destroy()
        
        BindSubScreen.protocol("WM_DELETE_WINDOW",warningMessageBT)
        

    TeacherButton = tkinter.Button(AddUserScreen,text="Bind(Optional)",fg="purple",command=Bind_Sub,bd=0)
    TeacherButton.grid(column=1,row=7)
    '''
    Module name:- AddUser_confirm
    Module purpose:- Grabs form data and sub menu data then validates and adds those information the users.csv
    Module args:- none
    Module inputs:- Password, username,rolename,subjects enrolled/waitlisted to , subjects bound as teacher to
    Module Outputs:- changes reflected in user database
    '''
    def AddUser_confirm():
        global inter_temp
        global BoundSub
    
        givenUserName = NameEntry.get()
        givenPassWord = PassEntry.get()
        givenRole = RoleCombo.get()
        #verification begins
        if givenRole == "":
            print(CRED+"Role Not Found"+CEND)
            messagebox.showerror("Error","Role Not Selected")
            return False
    
        if EnrolButton['text'] != "Saved":
            print(CRED+"Subjects not detected"+CEND)
            messagebox.showerror("Error","Give this user some subjects first!")
            return False
    
        if givenUserName == "" or givenUserName=="admin" or not(set(givenUserName).issubset(approved_text)):
            print(CRED+"Forbidden characters in username"+CEND)
            messagebox.showerror("Error","Username contains forbidden characters. Use CamelCase instead of spaces in your name")
            NameEntry.delete(0,tkinter.END)
            return False
    
        elif not(set(givenUserName).issubset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")):
            print(CRED+"Forbidden characters in username"+CEND)
            messagebox.showerror("Error","Username should contain only Alphabetical Characters")
            NameEntry.delete(0,tkinter.END)
            return False
    
        if givenPassWord == "" or "," in givenPassWord or ";" in givenPassWord:
            print(CRED+"Forbidden characters in password!"+CEND)
            messagebox.showerror("Error","Password cannot contain , and ;. It cannot be null.")
            PassEntry.delete(0,tkinter.END)
            return False
    
        if not twoFACheck.instate(['selected']):
            #message sent to users who do not have 2fa enabled
            print(CRED+"2FA Disabled"+CEND)
            if messagebox.askyesno("Confirm","Binding a email to your account will help you recover it if the password is forgotten. This can be used to notify you about major changes to your account. Do you want to enable 2FA?"):
                messagebox.showinfo("Tick the Box","Tick the 2FA Check box and fill the email bar with your email")
                return False
            else:
                pass
    
        if len(inter_temp) == 0:
            print(CRED+"No enrolements/waitlists detected"+CEND)
            messagebox.showerror("Error","No enrolements detected. Signup Process Halted")
            if twoFACheck.instate(['selected']):
                EmailEntry.delete(0,tkinter.END)
            EnrolButton.config(text="Enrol",state='normal')        
            NameEntry.delete(0,tkinter.END)
            PassEntry.delete(0,tkinter.END)
            RoleCombo.set("")
            return False
        #verification ends
        file = open("roles.csv","r+")
        roleLines=file.readlines()
        file.close()

        file = open("users.csv","r+")
        userLines = file.readlines()
        file.close()

        file = open("subjects.csv","r+")
        subjectLines = file.readlines()
        file.close()

        file = open("waitlist.csv","r+")
        waitlistLines = file.readlines()
        file.close()
        k = 0
        #the following while loop , itirates the role file and looks for the role provided for this user. once found , the permissions to "Bind User to class" and "Enrol to restricted" are checked
        while k<len(roleLines):
            row = roleLines[k].split(',')
    
            if len(row)!=roleLEN:
                k+=1
                continue
    
            if row[0] == givenRole:
                tempPerms = row[2].split('.')
                
                if tempPerms[0] == "0":
                    #if the user cannot bind to classes , the bound classes will be ignored in setup
                    try:
                        t=BoundSub
                        if len(BoundSub) >0:
                            print(CRED+"Bound permissions missing for bound classes!"+CEND)
                            messagebox.showwarning("Warning!","The Role you have given to this user prevents it from binding to a class\nBound classes ignored")
                            del BoundSub
                    except:
                        pass
                if tempPerms[4] == "0":
                    i = 0
                    c = 0
                    #if the user cannot enrol to classes , the classes that are restricted are removed from enrolements and binds
                    while i<len(inter_temp):
                        try:
                            mode,subject,classT = inter_temp[i]
                        except:
                            i+=1
                            continue
                        n = 0
                        l = True
                        while n<len(subjectLines):
                            rowS = subjectLines[n].split(',')
                            if len(rowS)!=subjectLEN:
                                n+=1
                                continue
                            for t in range(len(rowS)):rowS[t] = rowS[t].strip()
                            if rowS[0] == subject and rowS[1] == classT:
                                if rowS[4] == "1":
                                    #if the subject is restricted , the enrolement/waitlist is removed
                                    del inter_temp[i]
                                    c+=1
                                    l = False
                                    break
                            n+=1
                        if l:
                            i+=1
                    i = 0
                    try:
                        while i<len(BoundSub):
                            subject,classT = BoundSub[i]
                            n = 0
                            l = True
                            while n<len(subjectLines):
                                rowS = subjectLines[n].split(',')
                                if len(rowS)!=subjectLEN:
                                    n+=1
                                    continue
                                
                                for t in range(len(rowS)):rowS[t] = rowS[t].strip()
                                if rowS[0] == subject and rowS[1] == classT:
                                    if rowS[4] == "1":
                                        #if the bind is restricted , the bind is removed
                                        del BoundSub[i]
                                        l = False
                                        c+=1
                                        break
                                n+=1
                            if l:
                                i+=1
                    except:
                        pass
                    if c>0:
                        print(CRED+"Restricted Classes has been detected. All restricted class associations have been removed!"+CEND)
                        #warning message for the user if a subject has changed/deleted
                        messagebox.showwarning("Warning","Some classes were restricted. Your rolelevel is not enough to join these classes. You have been automatically unwaitlisted/unbound/unenrolled")
                break
            k+=1
        if twoFACheck.instate(['selected']):
    
            givenEmail = EmailEntry.get()
            i = 0
            # the following while loop checks whether the user's email has been bound
            while i<len(userLines):
                row = userLines[i].split(',')
    
                if len(row)!=userLEN:
                    i+=1
                    continue
    
                for t in range(len(row)):row[t] = row[t].strip()
    
                if row[4] == givenEmail:
                    #throws error if email found
                    print(CRED+"Email taken by a different user!"+CEND)
                    messagebox.showerror("Error","Email is already bound to a user!")
                    EmailEntry.delete(0,tkinter.END)
                    return False
                i+=1

            #the only way to verify a email is to attempt to send a email 
            
            try:
                if connected_ssid == b"gwsc.vic.edu.au":
                    raise TypeError
                server = smtplib.SMTP('smtp.office365.com',587)
                server.starttls()
                server.login("proofofconcept69420@outlook.com","somerandompassword69420")
            except:
                print(CRED+"Network error"+CEND)
                messagebox.showerror("Error","Cannot access the internet. Please reconnect and retry the signup")
                return False
    
            msg = MIMEMultipart()
            msg['From'] = 'proofofconcept69420@outlook.com'
            msg['To']=givenEmail
            msg['Subject'] = 'Email successfully registered ALLOCATE++ '+givenUserName
            message = "There has been a attempt to use your email for a account in Allocate++. If the attempt succeeds , you will receive a email with the credentials"
            msg.attach(MIMEText(message,'plain'))
    
            try:
                server.send_message(msg)
                server.quit()
                time.sleep(15)
                server = poplib.POP3_SSL("outlook.office365.com",995)
                server.user('proofofconcept69420@outlook.com')
                server.pass_("somerandompassword69420")
                resp , mails , octets = server.list()
                del resp,octets
                index = len(mails)
                resp,lines,octets = server.retr(index)
                msg_content = b'\r\n'.join(lines).decode('utf-8')
                msg = Parser().parsestr(msg_content)
                EmailSubject=msg.get('Subject').strip()
                #this code checks whether the system has received a autoemail with the subject "Undeliverable: Email successfully registered ALLOCATE++ <user>"
                if 'Undeliverable: Email successfully registered ALLOCATE++ '+givenUserName == EmailSubject:
                    print(CRED+"Invalid email provided!"+CEND)
                    messagebox.showerror("Error","Invalid Email Provided")
                    server.dele(index)
                    server.quit()
                    return False
            except:
                print(CRED+"Invalid email provided!"+CEND)
                messagebox.showerror("Error","Provided Email is invalid")
                EmailEntry.delete(0,tkinter.END)
                return False
    
            server.quit()
        else:
            givenEmail=""

        toWriteInterTempEnrols = ""
        toWriteInterTempWaitlist = []
    
        i = 0
        cycle = 0

        #inter_temp is read and the relevant data is passed onto the relevant arrays
        while i<len(inter_temp):
    
            try:
                mode,tempSubjectName,tempClassName = inter_temp[i]
            except:
                i+=1
                continue
            
            if mode == "enrol":
                print(CGREEN+f"Enrolement detected at {tempSubjectName}:{tempClassName}"+CEND)
                toWriteInterTempEnrols = toWriteInterTempEnrols+tempSubjectName+"."+tempClassName+"."
                cycle+=1
            else:
                print(CGREEN+f"Waitlist detected at {tempSubjectName}:{tempClassName}"+CEND)
                toWriteInterTempWaitlist.append((tempSubjectName,tempClassName))
        
            i+=1

        if i == 0:
            #if the user has no enrolements and waitlists... then it throws a error
            messagebox.showerror("Error","No enrolements detected. Signup Process Halted")
            print(CRED+"No Enrolements Detected!!!"+CEND)
            if twoFACheck.instate(['selected']):
                EmailEntry.delete(0,tkinter.END)
            EnrolButton.config(text="Enrol",state='normal')        
            NameEntry.delete(0,tkinter.END)
            PassEntry.delete(0,tkinter.END)
            RoleCombo.set("")
            #the system has disabled the creation of empty users to prevent user flooding to the user system by a mal actor
            return False
        if cycle != 0:
            del i
    
            a=list(toWriteInterTempEnrols)
    
            del a[len(a)-1]
    
            toWriteInterTempEnrols="".join([x for x in a])
  
        else:
            toWriteInterTempEnrols=""
        #VERIFICATION
        i = 0
        while i<len(userLines):
            row = userLines[i].split(',')
    
            if len(row) != userLEN:
                i+=1
                continue
            #quick clean
            for t in range(0,len(row)):row[t]=row[t].strip()
    
            userName = row[0]
            emailTag = row[4]
            
            if emailTag == "" and givenEmail == "":
                emailTag=1 
                givenEmail=""
            
            if userName == givenUserName or givenEmail == emailTag:
                print(CRED+"Email taken!"+CEND)
                messagebox.showerror("Error","This username or email is already taken , please pick a different username&/email")
                return False
            i+=1          

        if user!="admin":
            file = open("roles.csv","r+")
            roleLines=file.readlines()
            file.close()
 
            file = open("users.csv","r+")
            userLines=file.readlines()
            file.close()
 
            i=0
            #perm check for role provisions. to prevent the user from exploiting the role system for infinite perms
 
            while i<len(userLines):
                row = userLines[i].split(",")
 
                if len(row)!=userLEN:
                    i+=1
                    continue
 
                for t in range(0,len(row)):row[t]=row[t].strip()
 
                if row[0] == user:
                    setRole = row[3]
                    k = 0
 
                    roleLevelSave=""
                    roleLevelSaveGiven = ""
 
                    while k<len(roleLines):
                        row2 = roleLines[k].split(',')
 
                        if len(row2)!=roleLEN:
                            k+=1
                            continue
 
                        for t in range(0,len(row2)):row2[t]=row2[t].strip()
 
                        if row2[0] == setRole:
                            roleLevelSave = row2[1]
 
                        if row2[0] == givenRole:
                            roleLevelSaveGiven=row2[1]
 
                        k+=1
                    #prevents the currently logged in user from creating a user at a higher role then log into that role(essentially give yourself maximum permissions)
                    if int(roleLevelSave)>=int(roleLevelSaveGiven):
                        messagebox.showerror("Error","You're role level is not high enough to provide this role")
                        RoleCombo.set("")
                        return False
                i+=1
        i = 0

        #waitlists written
        file = open("waitlist.csv","r+")
        waitlistLines=file.readlines()
        file.close()
        while i<len(toWriteInterTempWaitlist):
            tempSub,tempClass=toWriteInterTempWaitlist[i]
            #TODO

            waitlistLines.append(givenUserName+","+tempSub+","+tempClass+"\n")
            i+=1
        
        file = open("waitlist.csv","w+")
        file.writelines(waitlistLines)
        file.close()
        print(CGREEN+"Waitlist data written!"+CEND)
        #TODO
        #user data written
        userLines.append(givenUserName+","+givenPassWord+","+toWriteInterTempEnrols+","+givenRole+","+givenEmail+"\n")
        
        file = open("users.csv","w+")
        file.writelines(userLines)
        file.close()
        print(CGREEN+"User data written!"+CEND)
        file = open("subjects.csv","r+")
        subjectLines=file.readlines()
        file.close()
        
        try:
            t=BoundSub
        except:
            EnrolButton.config(text="Enrol",state='normal')
        
            NameEntry.delete(0,tkinter.END)
            PassEntry.delete(0,tkinter.END)
        
            RoleCombo.set("")
        
            if twoFACheck.instate(['selected']):
                #confirmation email sent to users who have 2FA enabled
                givenEmail = EmailEntry.get()
        
                try:
                    if connected_ssid == b"gwsc.vic.edu.au":
                        raise TypeError
                    server = smtplib.SMTP('smtp.office365.com',587)
                    server.starttls()
                    server.login("proofofconcept69420@outlook.com","somerandompassword69420")
                except:
                    messagebox.showerror("Error","Cannot access the internet. Please reconnect and retry the signup")
                    return False
        
                msg = MIMEMultipart()
                msg['From'] = 'proofofconcept69420@outlook.com'
                msg['To']=givenEmail
                msg['Subject'] = 'Credentials For Your Account'
                message = "Username:"+givenUserName+"\nPassword:"+givenPassWord+"\nThanks for using Allocate++"
                msg.attach(MIMEText(message,'plain'))
        
                try:
                    server.send_message(msg)
                except:
                    messagebox.showerror("Error","Unknown error")
                    return False
        
                server.quit()    
        
            if twoFACheck.instate(['selected']):
                EmailEntry.delete(0,tkinter.END)
        
            messagebox.showinfo("Info","Successfully Added User to System")
            return False
        
        newSubjectLines = []
        ids= []
        
        for t in range(len(BoundSub)):
            i = 0    
        
            while i<len(subjectLines):
        
                row = subjectLines[i].split(',')
        
                if len(row) !=subjectLEN:
                    i+=1
                    continue
        
                if row[0] == BoundSub[t][0] and row[1] == BoundSub[t][1]:
                    ids.append(i)
                    #TODO
                    newSubjectLines.append(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+","+givenUserName+"\n")
                i+=1
        p = 0
        for t in range(len(ids)):
            subjectLines[ids[t]] = newSubjectLines[p]
            p+=1
        del p
        
        file = open("subjects.csv","w+")
        file.writelines(subjectLines)
        file.close()          
        print(CGREEN+"Bound data written!"+CEND)
        EnrolButton.config(text="Enrol",state='normal')
        
        NameEntry.delete(0,tkinter.END)
        PassEntry.delete(0,tkinter.END)
        
        if twoFACheck.instate(['selected']):
            givenEmail = EmailEntry.get()
        
            try:
                if connected_ssid == b"gwsc.vic.edu.au":
                    raise TypeError
                server = smtplib.SMTP('smtp.office365.com',587)
                server.starttls()
                server.login("proofofconcept69420@outlook.com","somerandompassword69420")
            except:
                print(CRED+"Network error, email cancelled")
                messagebox.showerror("Error","Cannot access the internet. Please reconnect and retry the signup")
                return False
        
            msg = MIMEMultipart()
            msg['From'] = 'proofofconcept69420@outlook.com'
            msg['To']=givenEmail
            msg['Subject'] = 'Credentials For Your Account'
            message = "Username:"+givenUserName+"\nPassword:"+givenPassWord+"\nThanks for using Allocate++"
            msg.attach(MIMEText(message,'plain'))
        
            try:
                server.send_message(msg)
            except:
                messagebox.showerror("Error","Provided Email is invalid")
                return False
        
            server.quit()
        
        if twoFACheck.instate(['selected']):
            EmailEntry.delete(0,tkinter.END)
        
        RoleCombo.set("")
        print(CGREEN+"User successfully added onto the system!"+CEND)
        messagebox.showinfo("Info","Successfully Added User to System")
    
    tkinter.Button(AddUserScreen,text="Create a User",fg="green",command=AddUser_confirm,bd=0).grid(column=1,row=8)
    '''
    Module Name:- CheckChildren
    Module Purpose:- Check and kill all the sub children(bind scnreen , enrol screen)
    Module Args:- None
    Module Inputs:- None
    Module Outputs:- close commands to the relevant children 
    '''
    def CheckChildren():
        print(CRED+"Close command received"+CEND)
        global EnrolSubScreen
        global WarningMessage
        global warningMessageBT
    
        try:
            EnrolSubScreen.destroy()
        except:
            pass
    
        try:
            BindSubScreen.destroy()
        except:
            pass
    
        try:
            WarningMessage()
        except:
            pass
    
        try:
            warningMessageBT()
        except:
            pass
    
        AddUserScreen.destroy()
    AddUserScreen.protocol("WM_DELETE_WINDOW",CheckChildren)
    AddUserScreen.mainloop()
'''
Module Name:- AddUser
Module Purpose:- TO create a table that is capable of deleting users
Module Arguments:- user(the current user who is logged in)
Module Inputs:- Current logged in user , user data
Module Outputs:- A screen with a table capable of deleting a user
'''
def DeleteUser(user):
    if CheckOpen("Delete Users"):
        return False

    DeleteUserWindow = tkinter.Toplevel(loginScreen)
    DeleteUserWindow.title("Delete Users")
    DeleteUserWindow.resizable(0,0)

    tkinter.Label(DeleteUserWindow,text="Double click on the user to delete",fg='red').grid(column=1,row=0)

    userTreeviewFrame = tkinter.Frame(DeleteUserWindow)
    userTreeviewFrame.grid(column=1,row=1)
    userTreeview = ttk.Treeview(userTreeviewFrame)
    userTreeview.heading("#0",text="Username")

    ScrollY = ttk.Scrollbar(userTreeviewFrame,command=userTreeview.yview,orient=tkinter.VERTICAL)
    ScrollY.pack(side=tkinter.RIGHT,fill = tkinter.Y)

    ScrollX = ttk.Scrollbar(userTreeviewFrame,command=userTreeview.xview,orient=tkinter.HORIZONTAL)
    ScrollX.pack(side=tkinter.BOTTOM,fill=tkinter.X)

    userTreeview.configure(xscrollcommand=ScrollX.set)
    userTreeview.configure(yscrollcommand=ScrollY.set)
    userTreeview.pack(side=tkinter.TOP,expand='false')
    '''
    Module Name:- userTreeview_refresh
    Module Purpose:- Refresh the usertable that shows the users that can be deleted
    Module Args:- None
    Module Inputs:- User database , roles database
    Module Outputs:- Refreshed table with recent data
    '''
    def userTreeview_refresh():
        userTreeview.delete(*userTreeview.get_children())

        file = open("roles.csv","r+")
        roleLines = file.readlines()
        file.close()

        file = open("users.csv","r+")
        userLines= file.readlines()
        file.close()

        i = 0
        #oLevel is assumed at the highest level(admin)
        oLevel = 0
        while i<len(userLines):
            row = userLines[i].split(',')
            oRole = ""
            if len(row)!=userLEN:
                i+=1
                continue
            for t in range(len(row)):row[t] = row[t].strip()
            if row[0] == user:
                oRole = row[3]
                k = 0
                while k<len(roleLines):
                    row2 = roleLines[k].split(',')
                    if len(row2)!=roleLEN:
                        k+=1
                        continue
                    for t in range(len(row2)):row2[t] = row2[t].strip()
                    if row2[0] == oRole:
                        #if the user's role is found , its level is assigned to oLevel
                        oLevel = row2[1]
                        break
                    k+=1
                break
            i+=1
        i = 0
        toAddFinal = []
        #this while loop checks whether the over user can delete this user (whether the user has lower role rank)
        while i<len(roleLines):
            row = roleLines[i].split(',')

            if len(row) != roleLEN:
                i+=1
                continue

            for t in range(len(row)):row[t] = row[t].strip()

            roleName = row[0]
            roleLevel = row[1]
            if int(roleLevel)<=int(oLevel):
                print(CRED+"Users at higher role level skipped"+CEND)
                i+=1
                continue
            k = 0
            toAddUsers = []
            while k<len(userLines):
                row2 = userLines[k].split(',')

                if len(row2)!=userLEN:
                    k+=1
                    continue

                for t in range(len(row2)):row2[t] = row2[t].strip()

                if row2[3] == roleName:
                    print(CGREEN+f"User at higher role({roleName}) named {row2[0]} inserted to delete table"+CEND)
                    toAddUsers.append(row2[0])

                k+=1

            toAddFinal.append((roleName,toAddUsers))

            i+=1
        i = 0
        #adds the information to a table
        while i<len(toAddFinal):
            role,users = toAddFinal[i]

            existingRoles = userTreeview.get_children()

            if len(existingRoles) == 0:
                tempID = userTreeview.insert("",tkinter.END,text=role)
                j = 0
            
                while j<len(users):
                    userTreeview.insert(tempID,tkinter.END,text=users[j])
                    j+=1
            
                i+=1
                continue
            k = 0
            while k<len(existingRoles):
            
                if userTreeview.item(existingRoles[k])['text'] == role:
                    tempID = existingRoles[k]
                    j = 0
            
                    while j <len(users):
                        userTreeview.insert(tempID,tkinter.END,text=users[j])
                        j+=1
                    i+=1
                    continue
                k+=1
            tempID = userTreeview.insert("",tkinter.END,text=role)
            j = 0
            
            while j<len(users):
                userTreeview.insert(tempID,tkinter.END,text=users[j])
                j+=1
            i+=1
    
    userTreeview_refresh()
    '''
    Module Name:- DeleteUserConfirm
    Module Purpose:- Deletes the selected user
    Module Args:- event(ignored)
    Module Inputs:- selected username,waitlistDatabase , user database , subject database
    Module Outputs:- User deleted and reflected in database
    '''
    def DeleteUserConfirm(event):
        selectedID = userTreeview.focus()

        if userTreeview.parent(selectedID) == "":
            return False
    
        givenUser = userTreeview.item(selectedID)['text']
        if givenUser == user:
            #this normally should not happen as your rolelevel needs to be higher than your role level inorder to be shown in the table , however i inserted this bit of code incase of edge cases
            messagebox.showerror("Error","You cannot delete yourself")
            return False
        pastEmail = ""
        file = open("users.csv","r+")
        userLines = file.readlines()
        file.close()

        i = 0
        newWriteUser = []
        #itirates and appends every user other than the selected user
        while i<len(userLines):
            row = userLines[i].split(',')
    
            if len(row)!=userLEN:
                i+=1
                continue
    
            for t in range(len(row)):row[t]=row[t].strip()
    
            if row[0] != givenUser:
                newWriteUser.append(userLines[i])
            else:
                pastEmail = row[4]
            i+=1
        print(CRED+f"{givenUser} removed from the user database"+CEND)
        file = open("users.csv","w+")
        file.writelines(newWriteUser)
        file.close()
    
        file = open("waitlist.csv","r+")
        waitlistLines=file.readlines()
        file.close()
    
        i = 0
        newWriteWaitlist = []
        #every waitlist other than any waitlists made by the selected user is added
        while i<len(waitlistLines):
            row = waitlistLines[i].split(',')
    
            if len(row)!=waitlistLEN:
                i+=1
                continue
    
            for t in range(len(row)):row[t] = row[t].strip()
    
            if row[0] != givenUser:
                newWriteWaitlist.append(waitlistLines[i])
            i+=1
        print(CRED+f"waitlists made by {givenUser} (if any) has been wiped!"+CEND)
        file = open("waitlist.csv","w+")
        file.writelines(newWriteWaitlist)
        file.close()
    
        file = open("subjects.csv","r+")
        subjectLines=file.readlines()
        file.close()
    
        newWriteSubject = []
        i = 0
        #removes all subject binds 
        while i<len(subjectLines):
            row = subjectLines[i].split(',')
    
            if len(row)!=subjectLEN:
                i+=1
                continue
    
            for t in range(len(row)):row[t] = row[t].strip()
    
            if row[5] == givenUser:
                #TODO
                newWriteSubject.append(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+","+"\n")
                i+=1
                continue
            newWriteSubject.append(subjectLines[i])
            i+=1
        print(CRED+f"Binds made by {givenUser} has been deleted"+CEND)
        file = open("subjects.csv","w+")
        file.writelines(newWriteSubject)
        file.close()
        #sends email
        try:
            if pastEmail != "":
                if connected_ssid == b"gwsc.vic.edu.au":
                    raise TypeError
                server = smtplib.SMTP("smtp.office365.com",587)
                server.starttls()
                server.login("proofofconcept69420@outlook.com","somerandompassword69420")
                msg = MIMEMultipart()
                msg['From']='proofofconcept69420@outlook.com'
                msg['To'] = pastEmail
                msg['Subject'] = 'Your account on Allocate++ has been deleted'
                message = "Your account named "+givenUser+" has been deleted by administrators."
                msg.attach(MIMEText(message,'plain'))
                server.send_message(msg)
                server.quit()
                print(CGREEN+"Goodbye email sent"+CEND)
        except:
            print(CRED+"Network error"+CEND)
            pass
        messagebox.showinfo("Sucess","User wiped from system")
    
        userTreeview_refresh()
    
    userTreeview.bind("<Double-1>",DeleteUserConfirm)
    '''
    Module Name:- userTreeview_search
    Module Purpose:- Provides a form to search data in the user databse
    Module Args:- None
    Module Inputs:- table data
    Module Outputs:- highlighted data or error messages
    '''
    def userTreeview_search():
        global SearchUserScreen
    
        if CheckOpen("Search UserTreeview"):
            return False
    
        SearchUserScreen = tkinter.Toplevel(loginScreen)
        SearchUserScreen.title("Search UserTreeview")
        SearchUserScreen.resizable(0,0)
    
        tkinter.Label(SearchUserScreen,text="Search Table",fg='blue').grid(column=1,row=0)
        tkinter.Label(SearchUserScreen,text="Search Criteria:").grid(column=0,row=1)
    
        SearchEntry = tkinter.Entry(SearchUserScreen,width=23)
        SearchEntry.grid(column=1,row=1)
    
        tkinter.Label(SearchUserScreen,text="Search Where:").grid(column=0,row=2)
    
        WhereCombo = ttk.Combobox(SearchUserScreen,values=["Users","Roles"],state='readonly')
        WhereCombo.grid(column=1,row=2)
        WhereCombo.set("Users")
    
        tkinter.Label(SearchUserScreen,text="Mode:").grid(column=0,row=3)
    
        HowCombo = ttk.Combobox(SearchUserScreen,values=["Linear","Binary"],state='readonly')
        HowCombo.set("Linear")
        HowCombo.grid(column=1,row=3)
        print(CGREEN+"Search window loaded"+CEND)
        '''
        Module Name:- SearchConfirmuserTreeview
        Module Purpose:- uses the relevant algorithm and searches for the provided criteria
        Module Args:- None
        Module Inputs:- Search criteria , where to search(users or roles) , how to search(linear or binary) , table data
        Module Outputs:- User/Role is selected or error thrown
        '''
        def SearchConfirmUserTreeview():
            FindWhat = SearchEntry.get()
            FindWhere = WhereCombo.get()
            FindHow = HowCombo.get()
            #existence verifs
            if FindWhat == "" or FindWhere == "" or FindHow == "":
                print(CRED+"Missing data"+CEND)
                messagebox.showerror("Error","Fill all the boxes")
                return False
    
            if FindHow == "Linear":
                if FindWhere == "Roles":
                    existingRoles = userTreeview.get_children()
                    i = 0
    
                    while i<len(existingRoles):
                        if userTreeview.item(existingRoles[i])['text'] == FindWhat:
                            print(CGREEN+"Role found"+CEND)
                            userTreeview.focus(existingRoles[i])
                            userTreeview.selection_set(existingRoles[i])
                            messagebox.showinfo("Sucess","Item has been highlighted in the table")
                            return False
                        i+=1
                    print(CRED+"Role Not Found"+CEND)
                    messagebox.showerror("Error","Unable to find role. Check your criteria and try again")
                    SearchEntry.delete(0,tkinter.END)
                else:
                
                    existingRoles = userTreeview.get_children()
                    i = 0
                
                    while i<len(existingRoles):
                        tempUser = userTreeview.get_children(existingRoles[i])
                
                        k = 0
                        while k<len(tempUser):
                            if userTreeview.item(tempUser[k])['text'] == FindWhat:
                                print(CGREEN+"User found"+CEND)
                                userTreeview.item(existingRoles[i],open=True)
                                userTreeview.focus(tempUser[k])
                                userTreeview.selection_set(tempUser[k])
                                messagebox.showinfo("Sucess","Item has been highlighted in the table")         
                                return False
         
                            k+=1
         
                        i+=1
                    print(CRED+"User not found"+CEND)
                    messagebox.showerror("Error","Unable to find user. check your criteria and try again")
                    return False
            else:
         
                if FindWhere == "Roles":
         
                    existingRoles = userTreeview.get_children()
                    searchRoles = []
         
                    for t in existingRoles:searchRoles.append(userTreeview.item(t)['text'])
         
                    searchRoles = QuickieSort(searchRoles)
         
                    if binarySearchAppr(searchRoles,0,len(searchRoles)-1,FindWhat):
                        print(CGREEN+"Role Found"+CEND)
                        for t in existingRoles:
         
                            if userTreeview.item(t)['text'] == FindWhat:
         
                                userTreeview.focus(t)
                                userTreeview.selection_set(t)
                                messagebox.showinfo("Success","Item has been highlighted for you in the treeview")
         
                                return False
         
                    else:
                        print(CRED+"Role not found"+CEND)
                        messagebox.showerror("Error","Role not found. Check your criteria and try again")
         
                        return False
         
                else:
         
                    existingRoles = userTreeview.get_children()
         
                    i = 0
         
                    while i<len(existingRoles):
                        existingUsers = userTreeview.get_children(existingRoles[i])
         
                        searchUsers = []
         
                        for t in existingUsers:searchUsers.append(userTreeview.item(t)['text'])
         
                        searchUsers = QuickieSort(searchUsers)
         
                        if binarySearchAppr(searchUsers,0,len(searchUsers)-1,FindWhat):
                            print(CGREEN+"User found"+CEND)
                            for t in existingUsers:
                                if userTreeview.item(t)['text'] == FindWhat:
                                    userTreeview.item(existingRoles[i],open=True)
                                    userTreeview.focus(t)
                                    userTreeview.selection_set(t)
                                    messagebox.showinfo("Sucess","Item has been highlighted for you in the treeview")

                                    return False
                        i+=1
                    print(CRED+"User Not FOund")
                    messagebox.showerror("Error","User not found, check your criteria and try again")
                    return False
        tkinter.Button(SearchUserScreen,text="Search..",fg='green',command=SearchConfirmUserTreeview,bd=0).grid(column=1,row=4)
        SearchUserScreen.mainloop()
    
    tkinter.Button(DeleteUserWindow,text="Search..",fg='blue',command=userTreeview_search,bd=0).grid(column=0,row=2)
    '''
    Module Name:- userTreeview_sort
    Module Purpose:- Sorts the user table
    Module Args:- None
    Module Inputs:- table data
    Module Outputs:- sorted table data
    '''
    def userTreeview_sort():
        existingRoles = userTreeview.get_children()
        NEWexistingRoles = []
    
        for t in existingRoles:NEWexistingRoles.append(userTreeview.item(t)['text'])
        #quick sort is used
        NEWexistingRoles=QuickieSort(NEWexistingRoles)
        FinalInsert = []
    
        for j in NEWexistingRoles:
            for p in existingRoles:
                if userTreeview.item(p)['text'] == j:
                    existingUsers=userTreeview.get_children(p)
    
                    allChildren = []
    
                    for e in existingUsers:allChildren.append(userTreeview.item(e)['text'])
    
                    allChildren = QuickieSort(allChildren)
                    FinalInsert.append((j,allChildren))
    
        userTreeview.delete(*userTreeview.get_children())
        i = 0
        #sorted data and children is inserted
        while i <len(FinalInsert):
            role,users = FinalInsert[i]
            existingRoles = userTreeview.get_children()
    
            if len(existingRoles) == 0:
                tempID = userTreeview.insert("",tkinter.END,text=role)
                k = 0
    
                while k<len(users):
                    userTreeview.insert(tempID,tkinter.END,text=users[k])
                    k+=1
                i+=1
                continue
            k = 0
    
            while k<len(existingRoles):
    
                if userTreeview.item(existingRoles[k])['text'] == role:
                    f = 0
    
                    while f<len(users):
                        userTreeview.insert(existingRoles[k],tkinter.END,text=users[f])
                        f+=1
    
                    i+=1
                    continue
                k+=1
    
            tempID = userTreeview.insert("",tkinter.END,text=role)
            k =0
    
            while k<len(users):
                userTreeview.insert(tempID,tkinter.END,text=users[k])
                k+=1
    
            i+=1
    
        messagebox.showinfo("Sucess","Sorted using QuickSort")
        print(CGREEN+"Sorted"+CEND)
    
    tkinter.Button(DeleteUserWindow,text="Sort..",fg='blue',command=userTreeview_sort,bd=0).grid(column=2,row=2)
    '''
    Module Name:- warningMessag
    Module Purpose:- Imitate inheritance and close child windows
    Module args:- none
    Module inputs:- None
    Module Outputs:- close commands to the children
    '''
    def warningMessage():
        global SearchUserScreen
        print(CRED+"Close command received"+CEND)
        try:
            SearchUserScreen.destroy()
        except:
            pass
    
        DeleteUserWindow.destroy()
    
    DeleteUserWindow.protocol("WM_DELETE_WINDOW",warningMessage)
    DeleteUserWindow.mainloop()
'''
Module Name:- EditUser
Module Purpose:- To create a table displaying a list of users that can be edited by the user that has logged in currently
Module Args:- user(the current user who logged in)
Module Inputs:- user who is logged in , user data
Module Outputs:- Table with users capable of being edited
'''
def EditUser(user):
    global Refresh_Clicked
    global warningMessage4
    if CheckOpen("Edit User"):
        return False
    EditUserScreen = tkinter.Toplevel(loginScreen)
    EditUserScreen.title("Edit User")
    EditUserScreen.resizable(0,0)
    
    tkinter.Label(EditUserScreen,text="Edit User",fg="green").grid(column=1,row=0)
    
    EditUserTreeviewFrame=tkinter.Frame(EditUserScreen)
    EditUserTreeviewFrame.grid(column=1,row=1)
    
    EditUserTreeview = ttk.Treeview(EditUserTreeviewFrame)
    EditUserTreeview.heading("#0",text="Username/Role")
    
    YScroll = ttk.Scrollbar(EditUserTreeviewFrame,command=EditUserTreeview.yview,orient=tkinter.VERTICAL)
    YScroll.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    
    XScroll = ttk.Scrollbar(EditUserTreeviewFrame,command=EditUserTreeview.xview,orient=tkinter.HORIZONTAL)
    XScroll.pack(side=tkinter.BOTTOM,fill=tkinter.X)
    
    EditUserTreeview.configure(xscrollcommand=XScroll.set)
    EditUserTreeview.configure(yscrollcommand=YScroll.set)
    EditUserTreeview.pack(side=tkinter.TOP,expand='false')
    print(CGREEN+"Edit user initialized"+CEND)
    '''
    Module Name:- EditUser_refresh
    module Purpose:- Refresh the EditUserTreeview to reflect the data in the csv
    Module Args:- none
    Module Inputs:- User data and Role Data
    Module Outputs:- Categorically filled table
    '''
    def EditUser_refresh():
        EditUserTreeview.delete(*EditUserTreeview.get_children())
    
        file = open("users.csv","r+")
        userLines=file.readlines()
        file.close()
    
        file = open("roles.csv","r+")
        roleLines=file.readlines()
        file.close()
        i = 0
        oRank = 0
        oRole = ""
        while i<len(userLines):
            row = userLines[i].split(',')
            if len(row)!=userLEN:
                i+=1
                continue
            for t in range(len(row)):row[t] = row[t].strip()
            if row[0] == user:
                oRole = row[3]
                break
            i+=1
        i = 0
        #once oRole is obtained , oRank is determined
        while i<len(roleLines):
            row = roleLines[i].split(',')
            if len(row)!=roleLEN:
                i+=1
                continue
            for t in range(len(row)):row[t] = row[t].strip()
            if row[0] == oRole:
                oRank = int(row[1])
                break
            i+=1
        i = 0
        finalInsert = []
        #proceeds to append users under roles who have a role rank below the user who is currently logged in
        while i<len(roleLines):
            row = roleLines[i].split(',')
    
            if len(row)!=roleLEN:
                i+=1
                continue
    
            for t in range(len(row)):row[t] = row[t].strip()
    
            roleName = row[0]
            roleRank = row[1]
            k = 0
            tempUserList = []
            if int(roleRank)<=oRank:
                i+=1
                continue
            while k<len(userLines):
                row2 = userLines[k].split(',')
    
                if len(row2)!=userLEN:
                    k+=1
                    continue
    
                for t in range(len(row2)):row2[t] = row2[t].strip()
    
                tempRole = row2[3]
                tempUser = row2[0]

                if tempRole == roleName:
                    tempUserList.append(tempUser)
                k+=1
    
            finalInsert.append((roleName,tempUserList))
            i+=1

        #insert appended data categorically
        i = 0
        while i<len(finalInsert):
            role,users = finalInsert[i]
            existingRoles = EditUserTreeview.get_children()
            print(CGREEN+f"Role added named {role}"+CEND)
            if len(existingRoles)  == 0:
                tempID=EditUserTreeview.insert("",tkinter.END,text=role)
                k = 0
    
                while k<len(users):
                    EditUserTreeview.insert(tempID,tkinter.END,text=users[k])
                    k+=1
    
                i+=1
                continue
    
            k = 0
    
            while k<len(existingRoles):
    
                if EditUserTreeview.item(existingRoles[k])['text'] == role:
                    j = 0
    
                    while j<len(users):
                        EditUserTreeview.insert(existingRoles[k],tkinter.END,text=users[j])
                        j+=1
    
                    i+=1
                    continue
                k+=1
    
            tempID=EditUserTreeview.insert("",tkinter.END,text=role)
    
            k = 0
            while k<len(users):
                EditUserTreeview.insert(tempID,tkinter.END,text=users[k])
                k+=1
            
            i+=1
    
    EditUser_refresh()
    '''
    Module Name:- EditUser_Clicked
    Module Purpose:- Display a form with the data of the selected user
    Module args:- event(ignored)
    Module Inputs:- Subject data , user data and selected user
    Module Outputs:- a form prefilled data of the selected user
    '''
    def EditUser_Clicked(event):
        global EditUserScreenDlg
        global subjectTRUE
        global Refresh_Clicked
        global warningMessage2
        subjectTRUE = []
    
        if CheckOpen("Edit User Dialog"):
            return False
    
        if EditUserTreeview.parent(EditUserTreeview.focus()) == "":
            return False
    
        EditUserScreenDlg = tkinter.Toplevel(loginScreen)
        givenUser = EditUserTreeview.item(EditUserTreeview.focus())['text']
        EditUserScreenDlg.title("Edit User Dialog")
        EditUserScreenDlg.resizable(0,0)
    
        tkinter.Label(EditUserScreenDlg,text="Edit the information below",fg="purple").grid(column=1,row=0)
        tkinter.Label(EditUserScreenDlg,text="Username:").grid(column=0,row=1)
    
        NameEntry=tkinter.Entry(EditUserScreenDlg,width=23)
        NameEntry.grid(column=1,row=1)
    
        tkinter.Label(EditUserScreenDlg,text="Role:").grid(column=0,row=2)
    
        RoleCombo = ttk.Combobox(EditUserScreenDlg,state='readonly')
        RoleCombo.grid(column=1,row=2)
        print(CGREEN+"Focused Edit User intialized"+CEND)
        
        EmailLabel =tkinter.Label(EditUserScreenDlg,text="Email:")
        EmailEntry = tkinter.Entry(EditUserScreenDlg,width=23)
        '''
        Module Name:- Refresh_Clicked
        Module Purpose:- Refresh the form to reflect latest changes to user
        Module Args:- None
        Module Inputs:- user database , subject database , role database , waitlist database
        Module Outputs:- refreshed form and globals
        '''
        def Refresh_Clicked():
            #redefining subject would make it assume a local state which doesnt save the values
            subjectTRUE.clear()
   
            try:
                EmailEntry.grid_forget()
            except:
                pass
   
            try:
                EmailLabel.grid_forget()
            except:
                pass
            file = open("users.csv","r+")
            userLines= file.readlines()
            file.close()
   
            file = open("roles.csv","r+")
            roleLines = file.readlines()
            file.close()
   
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
   
            file = open("waitlist.csv","r+")
            waitlistLines= file.readlines()
            file.close()

            i = 0
            #obtain the username , subjects and role
            while i<len(userLines):
                row = userLines[i].split(',')
   
                if len(row)!=userLEN:
                    i+=1
                    continue
   
                for t in range(len(row)):row[t] = row[t].strip()
   
                if row[0] == givenUser:
                    print(CGREEN+f"Loading User {row[0]}"+CEND)
                    NameEntry.delete(0,tkinter.END)
                    NameEntry.insert(0,givenUser)
   
                    tempSubjectList = row[2]
                    tempSubjectList=tempSubjectList.split('.')
                    k = 0
                    t = 0
   
                    while t < len(tempSubjectList):
   
                        if tempSubjectList[t].strip() == "":
                            del tempSubjectList[t]
                            continue
                        t+=1
   
                    while k<len(tempSubjectList):
                        tempSubject = tempSubjectList[k]
                        tempClass = tempSubjectList[k+1]
                        print(CGREEN+f"Enrolled at {tempSubject}:{tempClass}"+CEND)
                        subjectTRUE.append(("ENROLLED",tempSubject,tempClass))
                        k+=2
   
                    tempRole=row[3]
                    RoleCombo.set(tempRole)
   
                    if row[4] !="":
                        print(CGREEN+"Email Detected"+CEND)
                        EmailEntry.grid(column=1,row=3)
                        EmailLabel.grid(column=0,row=3)
                        EmailEntry.delete(0,tkinter.END)
                        EmailEntry.insert(tkinter.INSERT,row[4])
                    break
   
                i+=1
            i= 0
            roleComboArray = []
            #refresh RoleCombo dynamic values
            while i<len(roleLines):
                row = roleLines[i].split(',')
   
                if len(row)!=roleLEN:
                    i+=1
                    continue
   
                for t in range(len(row)):row[t] = row[t].strip()
                print(CGREEN+f"Role loaded {row[0]}"+CEND)
                roleComboArray.append(row[0])
                i+=1
   
            RoleCombo.config(values=roleComboArray)
            i = 0
            #fetch all the waitlists
            while i<len(waitlistLines):
                row = waitlistLines[i].split(',')
   
                if len(row)!=waitlistLEN:
                    i+=1
                    continue
   
                for t in range(len(row)):row[t] = row[t].strip()
   
                if row[0] == givenUser:
                    print(CGREEN+f"Waitlisted at {row[1]}:{row[2]}")
                    subjectTRUE.append(("WAITLISTED",row[1],row[2]))
                i+=1
            i = 0
            #fetch all the binds
            while i<len(subjectLines):
                row = subjectLines[i].split(',')
   
                if len(row)!=subjectLEN:
                    i+=1
                    continue
   
                for t in range(len(row)):row[t] = row[t].strip()
   
                if row[5] == givenUser:
                    print(CGREEN+f"Bound detected at {row[0]} : {row[1]}"+ CEND)
                    subjectTRUE.append(("BOUND",row[0],row[1]))
                i+=1
        '''
        Module Name:- Edit_ChangeSubjects
        Module Purpose:- Shows a table that shows current enrolements and options to add/remove enrolements/waitlists/binds
        Module Args:- None
        Module Inputs:- Subject info from global , subject database , user database , waitlist database , role info
        Module Outputs:- Table with current enrolement and waitlists and binds , with options to add/remove waitlists/binds/enrolements
        '''
        def Edit_ChangeSubjects():
            global ChangeAssociationsScreen
            global Refresh_Clicked
            global Refresh_ChangeAscTreeview
            global warningMessage4
            if CheckOpen("Change Subjects EditUserScreenDlg"):
                return False
    
            ChangeAssociationsScreen = tkinter.Toplevel(loginScreen)
            ChangeAssociationsScreen.title("Change Subjects EditUserScreenDlg")
            ChangeAssociationsScreen.resizable(0,0)
    
            tkinter.Label(ChangeAssociationsScreen,text="Double Click to Unbind/Denrol/Unwaitlist",fg='red').grid(column=1,row=0)
    
            ChangeAscTreeviewFrame = tkinter.Frame(ChangeAssociationsScreen)
            print(CGREEN+"Loaded Change Asc Screen"+CEND)
            ChangeAscTreeview = ttk.Treeview(ChangeAscTreeviewFrame,columns=["Class","Type"])
            ChangeAscTreeview.heading("#0",text="Subject")
            ChangeAscTreeview.heading("Class",text="Class")
            ChangeAscTreeview.heading("Type",text="Type")
    
            ScrollY2 = ttk.Scrollbar(ChangeAscTreeviewFrame,command=ChangeAscTreeview.yview,orient=tkinter.VERTICAL)
            ScrollY2.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    
            ChangeAscTreeview.configure(yscrollcommand=ScrollY2.set)
            ChangeAscTreeview.pack(side=tkinter.TOP,expand='false')
            ChangeAscTreeviewFrame.grid(column=1,row=1)
            '''
            Module Name:- Refresh_ChangeAscTreeview
            Module Purpose:- Refreshes the ChangeAscTreeview to reflect recent data from globals
            Module Args:- none
            Module Inputs:- global data
            Module Outputs:- refreshed table
            '''
            def Refresh_ChangeAscTreeview():
                global subjectTRUE
    
                ChangeAscTreeview.delete(*ChangeAscTreeview.get_children())
    
                i = 0
                while i<len(subjectTRUE):
                    state,subject,class_ = subjectTRUE[i]
                    print(CGREEN+f"Loaded {state} for {subject}:{class_}"+CEND)
                    ChangeAscTreeview.insert("",tkinter.END,text=subject,values=[class_,state])
                    i+=1
    
            Refresh_ChangeAscTreeview()
            '''
            Module Name:- EnrolToSubCHANGEASC
            Module Purpose:- enrols/waitlists user
            Module Args:- None
            Module Inputs:- user databse , subject databse , AuthMod
            Module Outputs:- Table with subjects that the user can enrol to
            '''
            def EnrolToSubCHANGEASC():
                global EnrolToSubChangeAscScreen
                global Refresh_EnrolToSubTree
                global warningMessage3
                if CheckOpen("Enrol To Subject CHANGEASCSCREEN"):
                    return False
    
                EnrolToSubChangeAscScreen = tkinter.Toplevel(loginScreen)
                EnrolToSubChangeAscScreen.title("Enrol To Subject CHANGEASCSCREEN")
                EnrolToSubChangeAscScreen.resizable(0,0)
    
                tkinter.Label(EnrolToSubChangeAscScreen,text="Enrol by double clicking on record",fg='purple').grid(column=1,row=0)
                print(CGREEN+"Loaded Enrol To Sub Change Asc Screen"+CEND)
                TreeFrame = tkinter.Frame(EnrolToSubChangeAscScreen)
                Tree=ttk.Treeview(TreeFrame,columns=["Spots Left","Waitlisted","Teacher"])
                Tree.heading("#0",text="Subject/Class")
                Tree.heading("Spots Left",text="Spots Left")
                Tree.heading("Waitlisted",text="Waitlisted")
                Tree.heading("Teacher",text="Teacher")
    
                YScroll3 = ttk.Scrollbar(TreeFrame,command=Tree.yview,orient=tkinter.VERTICAL)
                YScroll3.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    
                XScroll3 = ttk.Scrollbar(TreeFrame,command=Tree.xview,orient=tkinter.HORIZONTAL)
                XScroll3.pack(side=tkinter.BOTTOM,fill=tkinter.X)
    
                Tree.configure(xscrollcommand=XScroll3.set)
                Tree.configure(yscrollcommand=YScroll3.set)
    
                Tree.pack(side=tkinter.TOP,expand='false')

                '''
                Module Name:- Refresh_EnrolToSubTree
                Module Purpose:- Refresh the enrolement sub tree
                Module Args:- None
                module Inputs:- User database , waitlist database , subject database
                Module Outputs:- Refreshed Table
                '''
                def Refresh_EnrolToSubTree():
                    Tree.delete(*Tree.get_children())
    
                    file = open("users.csv","r+")
                    userLines = file.readlines()
                    file.close()
    
                    file = open("waitlist.csv","r+")
                    waitlistLines= file.readlines()
                    file.close()
    
                    file = open("subjects.csv","r+")
                    subjectLines = file.readlines()
                    file.close()

                    file = open("roles.csv","r+")
                    roleLines = file.readlines()
                    file.close()

                    i = 0
                    canJoinRestricted = ""
                    URole = ""
                    while i<len(userLines):
                        row=userLines[i].split(',')
    
                        if len(row)!=userLEN:
                            i+=1
                            continue
    
                        for t in range(len(row)):row[t] = row[t].strip()
    
                        if row[0] == givenUser:
                            tempsubsENROL = row[2].split('.')
                            URole = row[3]
                            break
                        else:
                            i+=1
    
                    i = 0
                    while i<len(roleLines):
                        row = roleLines[i].split(',')
                        if len(row)!=roleLEN:
                            i+=1
                            continue
                        for t in range(len(row)):row[t] = row[t].strip()
                        if row[0] == URole:
                            tempPerms = row[2].split('.')
                            for t in range(len(tempPerms)):tempPerms[t] = tempPerms[t].strip()
                            canJoinRestricted = bool(int(tempPerms[4]))
                            break
                        i+=1
                    i = 0
                    tempsubsWAITLIST = []
                    while i<len(waitlistLines):
                        row=waitlistLines[i].split(',')
    
                        if len(row)!=waitlistLEN:
                            i+=1
                            continue
    
                        for t in range(len(row)):row[t] = row[t].strip()
    
                        if row[0] == givenUser:
                            tempsubsWAITLIST.append(row[1])
                            tempsubsWAITLIST.append(row[2])
                        i+=1
    
                    i = 0
                    finalInsert = []
                    while i<len(subjectLines):
                        row = subjectLines[i].split(',')
    
                        if len(row)!=subjectLEN:
                            i+=1
                            continue
    
                        for t in range(len(row)):row[t] = row[t].strip()
    
                        classTrue = row[1]
                        subjectTrue = row[0]
                        max_ = row[2]
                        teacher = row[5]
                        RestrictState = row[4]
                        k = 0
                        count_enrol = 0
                        b = 0
                        t = False
                        #checks whether the user can join restricted and also whether the class is restricted
                        if canJoinRestricted == False and bool(int(RestrictState)) == True:
                            print(CRED+"Restricted class ignored"+CEND)
                            i+=1
                            continue
                        #checks whether the subject is already in enrolements list
                        while b<len(tempsubsENROL):
                            try:
    
                                if [tempsubsENROL[b],tempsubsENROL[b+1]] in [[subjectTrue,classTrue]]:
                                    print(CRED+"Enrolled class ignored"+CEND)
                                    i+=1
                                    t = True
                                    break
    
                            except:
                                break
                            b+=2
    
                        if t:
                            continue
    
                        b = 0
                        t = False
                        #checks whether the subject is already in waitlist
                        while b<len(tempsubsWAITLIST):
                            try:
    
                                if [tempsubsWAITLIST[b],tempsubsWAITLIST[b+1]] in [[subjectTrue,classTrue]]:
                                    print(CRED+"Waitlisted class ignored"+CEND)
                                    t = True
                                    i+=1
                                    break
    
                            except:
                                break
    
                            b+=2
    
                        if t:
                            continue                        
                        #gets the amount of user who are enrolled
                        while k<len(userLines):
                            row2 = userLines[k].split(',')
    
                            if len(row2)!=userLEN:
                                k+=1
                                continue
    
                            for t in range(len(row2)):row[t] = row2[t].strip()
    
                            tempSubjects = row[2].split('.')
    
                            t = 0
                            while t<len(tempSubjects):
    
                                if tempSubjects[t] == subjectTrue and tempSubjects[t+1] == classTrue:
                                    count_enrol+=1
    
                                t+=2
    
                            k+=1
    
                        k = 0
                        count_wait = 0
                        #gets the amount of waitlisted users
                        while k<len(waitlistLines):
                            row2 = waitlistLines[k].split(',')
    
                            if len(row2)!=waitlistLEN:
                                k+=1
                                continue
    
                            for t in range(len(row2)):row2[t] = row2[t].strip()
    
                            if row2[1] == subjectTrue and row2[2] == classTrue:
                                count_wait+=1
                            k+=1
    
                        finalInsert.append((subjectTrue,classTrue,teacher,max_,count_enrol,count_wait))
    
                        i+=1
    
                    i = 0
                    #insert data categorically
                    while i<len(finalInsert):
                        existingRows = Tree.get_children()
                        sub,clas,teac,max_,enrol,wait =finalInsert[i]
                        print(CGREEN+f"Loaded {sub}:{clas} taught by {teac} with {max_} spaces and {enrol} enrolements and {wait} waitlists"+CEND)
                        if len(existingRows) == 0:
                            tempID=Tree.insert("",tkinter.END,text=sub)
                            Tree.insert(tempID,tkinter.END,text=clas,values=[str(int(max_)-int(enrol)),wait,teac])
                            i+=1
                            continue
    
                        k = 0
                        t = False
    
                        while k<len(existingRows):
                            if Tree.item(existingRows[k])['text'] == sub:
                                Tree.insert(existingRows[k],tkinter.END,text=clas,values=[str(int(max_)-int(enrol)),wait,teac])
                                t = True
                                break
                            k+=1
    
                        if t == True:
                            i+=1
                            continue
    
                        tempID=Tree.insert("",tkinter.END,text=sub)
                        Tree.insert(tempID,tkinter.END,text=clas,values=[str(int(max_)-int(enrol)),wait,teac])
                        i+=1
    
                TreeFrame.grid(column=1,row=1)
    
                Refresh_EnrolToSubTree()

                '''
                Module Name:- EnrolToSubConfirm
                Module Purpose:-  Adds the selected class to enrolenments
                Module Args:- Event(ignored)
                Module Inputs:- selected class
                Module Outputs:- Changes reflected in csv or error message
                '''
                def EnrolToSubConfirm(event):
    
                    try:
                        #checks whether the item selected is a class and not a subject
                        className = Tree.item(Tree.focus())['text']
    
                        if Tree.parent(Tree.focus()) == "":
                            return False
                        subjectName = Tree.item(Tree.parent(Tree.focus()))['text']
                        spotsLeft = Tree.item(Tree.focus())['values'][0]
    
                    except:
                        return False
    
                    file = open("subjects.csv","r+")
                    subjectLines = file.readlines()
                    file.close()

                    file = open("users.csv","r+")
                    userLines = file.readlines()
                    file.close()
                    i = 0
                    #the following algo checks for class clashes with the selected class
                    while i<len(userLines):
                        row = userLines[i].split(',')
                        if len(row)!=userLEN:
                            i+=1
                            continue
                        for t in range(len(row)):row[t] = row[t].strip()
                        if row[0] == givenUser:
                            #gets the currently enrolled subjects
                            tempSubs = row[2].split('.')
                            if row[2] == "":
                                del tempSubs[0]
                            j = 0
                            timeArr = []
                            current = []
                            #itirates the subjects and appends the time information to a array
                            while j<len(tempSubs):
                                k = 0
                                while k<len(subjectLines):
                                    row2 = subjectLines[k].split(',')
                                    if len(row2)!=subjectLEN:
                                        k+=1
                                        continue
                                    for t in range(len(row2)):row2[t] = row2[t].strip()
                                    if row2[0] == tempSubs[j] and row2[1] == tempSubs[j+1]:
                                        timeData = row2[3].split('.')
                                        fromD,fromMo,fromY = timeData[0].split(':')
                                        toD,toMo,toY = timeData[1].split(':')
                                        fromH,fromMi = timeData[2].split(':')
                                        toH,toMi = timeData[3].split(':')
                                        monthswith31 = [1,3,5,7,8,10,12]
                                        rState = timeData[4]
                                        fromY=int(fromY)
                                        fromMo = int(fromMo)
                                        fromD = int(fromD)
                                        toD = int(toD)
                                        toMo = int(toMo)
                                        toY = int(toY)
                                        fromH = int(fromH)
                                        fromMi = int(fromMi)
                                        toH = int(toH)
                                        toMi = int(toMi)
                                        timeFrom = 0
                                        timeTo = 0
                                        n = 0
                                        while n<fromY:
                                            if n%4 == 0:
                                                timeFrom+=366*24*60
                                            else:
                                                timeFrom+=365*24*60
                                            n+=1
                                        n = 1
                                        while n<fromMo:
                                            if n in monthswith31:
                                                timeFrom+=31*24*60
                                            elif n == 2:
                                                if fromY%4 == 0:
                                                    timeFrom+=29*24*60
                                                else:
                                                    timeFrom+=28*24*60
                                            else:
                                                timeFrom+=30*24*60
                                            n+=1
                                        timeFrom+=fromD*24*60
                                        timeFrom+=fromH*60
                                        timeFrom+=fromMi
                                        n = 0
                                        while n<toY:
                                            if n%4 == 0:
                                                timeTo+=366*24*60
                                            else:
                                                timeTo+=365*24*60
                                            n+=1
                                        n = 0
                                        while n<toMo:
                                            if n in monthswith31:
                                                timeFrom+=31*24*60
                                            elif n == 2:
                                                if toY%4 == 0:
                                                    timeFrom+=29*24*60
                                                else:
                                                    timeFrom+=28*24*60
                                            else:
                                                timeFrom+=30*24*60
                                            n+=1
                                        timeTo+=toD*24*60
                                        timeTo+=toH*60
                                        timeTo+=toMi
                                        timeArr.append((row2[0],row2[1],timeFrom,timeTo,rState,fromH,fromMi,toH,toMi))
                                        break
                                    k+=1
                                j+=2
                            k = 0
                            #itirates the subjectlines database and if the class is found , sets the time data
                            while k<len(subjectLines):
                                row2 = subjectLines[k].split(',')
                                if len(row2)!=subjectLEN:
                                    k+=1
                                    continue
                                for t in range(len(row2)):row2[t] = row2[t].strip()
                                if row2[0] == subjectName and row2[1] == className:
                                    timeData = row2[3].split('.')
                                    fromD,fromMo,fromY = timeData[0].split(':')
                                    toD,toMo,toY = timeData[1].split(':')
                                    fromH,fromMi = timeData[2].split(':')
                                    toH,toMi = timeData[3].split(':')
                                    monthswith31 = [1,3,5,7,8,10,12]
                                    rState = timeData[4]
                                    fromY=int(fromY)
                                    fromMo = int(fromMo)
                                    fromD = int(fromD)
                                    toD = int(toD)
                                    toMo = int(toMo)
                                    toY = int(toY)
                                    fromH = int(fromH)
                                    fromMi = int(fromMi)
                                    toH = int(toH)
                                    toMi = int(toMi)
                                    timeFrom = 0
                                    timeTo = 0
                                    n = 0
                                    while n<fromY:
                                        if n%4 == 0:
                                            timeFrom+=366*24*60
                                        else:
                                            timeFrom+=365*24*60
                                        n+=1
                                    n = 1
                                    while n<fromMo:
                                        if n in monthswith31:
                                            timeFrom+=31*24*60
                                        elif n == 2:
                                            if fromY%4 == 0:
                                                timeFrom+=29*24*60
                                            else:
                                                timeFrom+=28*24*60
                                        else:
                                            timeFrom+=30*24*60
                                        n+=1
                                    timeFrom+=fromD*24*60
                                    timeFrom+=fromH*60
                                    timeFrom+=fromMi
                                    n = 0
                                    while n<toY:
                                        if n%4 == 0:
                                            timeTo+=366*24*60
                                        else:
                                            timeTo+=365*24*60
                                        n+=1
                                    n = 0
                                    while n<toMo:
                                        if n in monthswith31:
                                            timeFrom+=31*24*60
                                        elif n == 2:
                                            if toY%4 == 0:
                                                timeFrom+=29*24*60
                                            else:
                                                timeFrom+=28*24*60
                                        else:
                                            timeFrom+=30*24*60
                                        n+=1
                                    timeTo+=toD*24*60
                                    timeTo+=toH*60
                                    timeTo+=toMi
                                    current.append((timeFrom,timeTo,rState,fromH,fromMi,toH,toMi))
                                    break
                                k+=1
                            j = 0
                            try:
                                tFs,tTs,rSs,fHs,fMis,toHs,toMis = current[0]
                            except:
                                break
                            rangeForCurrent = set(range(tFs,tTs))
                            #itirates the time array containing all the currently enrolled classes
                            while j<len(timeArr):
                                tempSub,tempClass,tF,tT,rS,fH,fMi,toH,toMi = timeArr[j]
                                rangeForPast = set(range(tF,tT))
                                n = 0
                                z = False
                                #checks whether the class occurs on the same day
                                if rS == rSs or rS == "Everyday":
                                    #checks whether the class has inter lapping time range
                                    if len(rangeForPast.intersection(rangeForCurrent)) > 0:
                                        toTime = 0
                                        fromTime = 0
                                        toTime = int(toH)*60+int(toMi)
                                        fromTime = int(fH)*60+int(fMi)
                                        toTimeS = int(toHs)*60+int(toMis)
                                        fromTimeS = int(fHs)*60+int(fMis)
                                        #checks whether the class has interlapping times in a hours minutes sense
                                        if len(set(range(fromTime,toTime)).intersection(set(range(fromTimeS,toTimeS))))>0:
                                            if not messagebox.askyesno("Error","Clash detected with "+tempSub+","+tempClass+". Do you want to force clash?"):
                                                return False
                                            z = True
                                if z:
                                    break
                                j+=1
                            break
                        i+=1
                    #run waitlist function if there isnt enough spots
                    if int(spotsLeft)-1 < 0:
                        print(CRED+"Not enough spaces"+CEND)
                        if messagebox.askyesno("Confirm","There arent any spaces left to enrol. do you wish to waitlist instead?"):
                            file = open("waitlist.csv","r+")
                            waitlistLines = file.readlines()
                            file.close()
                            waitlistLines.append(givenUser+","+subjectName+","+className+"\n")
    
                            file = open("waitlist.csv","w+")
                            file.writelines(waitlistLines)
                            file.close()
                            print(CGREEN+"Waitlist complete"+CEND)
                            messagebox.showinfo("Success","Waitlisted!")
                            FileVerifs()
                            Refresh_Clicked()
                            Refresh_ChangeAscTreeview()
                            Refresh_EnrolToSubTree()
                            
                            return False
                        else:
                            return False
    
                    toWLines = []
                    i = 0
                    #itirates the user files and writes the new subject data
                    while i<len(userLines):
                        row = userLines[i].split(',')
    
                        if len(row)!=userLEN:
                            i+=1
                            continue
    
                        for t in range(len(row)):row[t] = row[t].strip()
    
                        if row[0] == givenUser:
                            #TODO
                            if row[2] == "":
                                row[2] = subjectName+"."+className
                            else:
                                row[2] = row[2]+"."+subjectName+"."+className
    
                        #TODO
                        toWLines.append(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+"\n")
                        i+=1
    
                    file = open("users.csv","w+")
                    file.writelines(toWLines)
                    file.close()
                    print(CGREEN+"Enrolement complete"+CEND)
                    messagebox.showinfo("Success","Successfully enrolled to the subject")
    
                    FileVerifs()
                    Refresh_Clicked()
                    Refresh_ChangeAscTreeview()
                    Refresh_EnrolToSubTree()
                    
                Tree.bind("<Double-1>",EnrolToSubConfirm)
                '''
                Module Name:- Sort_EnrolToSubTree
                Module Purpose:- Sorts the enrol to sub tree
                Module Args:- None
                Module Inputs:- table data
                Module outputs:- sorted table data
                '''
                def Sort_EnrolToSubTree():
                    existingRows = Tree.get_children()
    
                    newExistingRows = []
    
                    for t in existingRows:
                        newExistingRows.append(Tree.item(t)['text'])
    
                    newExistingRows = QuickieSort(newExistingRows)
                    finalInsert = []
    
                    for newSub in newExistingRows:
    
                        for t in existingRows:
    
                            if Tree.item(t)['text'] == newSub:
                                children = Tree.get_children(t)
                                newChildren = []
    
                                for t in children:newChildren.append(Tree.item(t)['text'])
    
                                newChildren = QuickieSort(newChildren)
    
                                for b in newChildren:
    
                                    for t in children:
    
                                        if Tree.item(t)['text'] == b:
    
                                            tempR = Tree.item(t)['values']
                                            finalInsert.append((newSub,b,tempR[0],tempR[1],tempR[2]))
    
                    i = 0
                    Tree.delete(*Tree.get_children())
    
                    while i<len(finalInsert):
                        tempSub,tempClass,tempSpot,tempWait,tempTeach=finalInsert[i]
                        existingRows = Tree.get_children()
    
                        if len(existingRows) == 0:
                            tempID = Tree.insert("",tkinter.END,text=tempSub)
                            Tree.insert(tempID,tkinter.END,text=tempClass,values=[tempSpot,tempWait,tempTeach])
                            i+=1
                            continue
    
                        k = 0
                        p = False
    
                        while k<len(existingRows):
                            if Tree.item(existingRows[k])['text'] == tempSub:
                                Tree.insert(existingRows[k],tkinter.END,text=tempClass,values=[tempSub,tempWait,tempTeach])
                                p = True
                                break
                            k+=1
    
                        if p:
                            i+=1
                            continue
    
                        tempID=Tree.insert("",tkinter.END,text=tempSub)
                        Tree.insert(tempID,tkinter.END,text=tempClass,values=[tempSpot,tempWait,tempTeach])
                        i+=1
                    print(CGREEN+"Sorted"+CEND)
                tkinter.Button(EnrolToSubChangeAscScreen,text="Sort",fg='blue',command=Sort_EnrolToSubTree,bd=0).grid(column=2,row=2)
                '''
                Module Name:- Search_EnrolToSubTree
                Module PUrpose:- shows a form capable of searching the enrol to sub tree
                Module Args:- None
                Module Inputs:- None
                Module Outputs:- Form capable of searching table
                '''
                def Search_EnrolToSubTree():
                    global Search_EnrolToSubTreeScreen
    
                    if CheckOpen("Search ENROLTOSUBTREE"):
                        return False
    
                    Search_EnrolToSubTreeScreen = tkinter.Toplevel(loginScreen)
                    Search_EnrolToSubTreeScreen.title("Search ENROLTOSUBTREE")
                    Search_EnrolToSubTreeScreen.resizable(0,0)
    
                    tkinter.Label(Search_EnrolToSubTreeScreen,text="Fill the form",fg='purple').grid(column=1,row=0)
    
                    SubjectEntry = tkinter.Entry(Search_EnrolToSubTreeScreen,width=23)
                    SubjectEntry.grid(column=1,row=1)
    
                    tkinter.Label(Search_EnrolToSubTreeScreen,text="Subject Name:").grid(column=0,row=1)
                    print(CGREEN+"Search screen loaded"+CEND)
                    ClassEntry = tkinter.Entry(Search_EnrolToSubTreeScreen,width=23)
                    ClassEntry.grid(column=1,row=2)
    
                    tkinter.Label(Search_EnrolToSubTreeScreen,text="Class Name:").grid(column=0,row=2)
    
                    ModeCombo = ttk.Combobox(Search_EnrolToSubTreeScreen,values=["Linear","Binary"],state='readonly')
                    ModeCombo.grid(column=1,row=3)
                    ModeCombo.set("Linear")
    
                    tkinter.Label(Search_EnrolToSubTreeScreen,text="Mode:").grid(column=0,row=3)
                    '''
                    Module Name:- ConfirmSearchEnrolToSubTree
                    Module Purpose:- Runs a search function for the given criteria using the correct mode
                    Module args:- none
                    Module inputs:- subject name , class name and search mode
                    Module Outputs:- if the item is found , highlighted in table or else messagebox with error
                    '''
                    def confirmSearchEnrolToSubTree():
    
                        if SubjectEntry.get() == "" or ClassEntry.get() == "":
                            print(CRED+"Missing data"+CEND)
                            messagebox.showerror("Error","Fill the form first")
                            return False
    
                        subName = SubjectEntry.get()
                        clasName = ClassEntry.get()
                        
                        if ModeCombo.get() == "Linear":
                            existingParents = Tree.get_children()
                            i = 0
                            #searches parents
                            while i<len(existingParents):
                                #parent found
                                if Tree.item(existingParents[i])['text'] == subName:
    
                                    existingChildren = Tree.get_children(existingParents[i])
                                    k = 0

                                    while k<len(existingChildren):
                                        #searches children
                                        if Tree.item(existingChildren[k])['text'] == clasName:
                                            #child found
                                            print(CGREEN+"Found"+CEND)
                                            Tree.item(existingParents[i],open=True)
                                            Tree.focus(existingChildren[k])
                                            Tree.selection_set(existingChildren[k])
                                            messagebox.showinfo("Success","Item Found. The item has been highlighted in the treeview")
                                            return False
    
                                        k+=1
                                i+=1
                            print(CRED+"Not found"+CEND)
                            messagebox.showerror("Error","Unable to find class. Check your form and try again")
    
                            SubjectEntry.delete(0,tkinter.END)
                            ClassEntry.delete(0,tkinter.END)
                            return False
                        else:
                            existingParents = Tree.get_children()
                            i = 0
                            newExistingParents = []
    
                            for t in existingParents:newExistingParents.append(Tree.item(t)['text'])
                            #sorts and searches parents
                            newExistingParents = QuickieSort(newExistingParents)
    
                            if binarySearchAppr(newExistingParents,0,len(newExistingParents)-1,subName):
    
                                for p in existingParents:
                                    #if parent found
                                    if Tree.item(p)['text'] == subName:
    
                                        tempC = Tree.get_children(p)
                                        newC = []
    
                                        for m in tempC:newC.append(Tree.item(m)['text'])
    
                                        newC = QuickieSort(newC)
                                        #if child found
                                        if binarySearchAppr(newC,0,len(newC)-1,clasName):
    
                                            for g in tempC:
    
                                                if Tree.item(g)['text'] == clasName:
                                                    #highlight child
                                                    print(CGREEN+"Found"+CEND)
                                                    Tree.item(p,open=True)
                                                    Tree.focus(g)
                                                    Tree.selection_set(g)
                                                    messagebox.showinfo("Success","Item Found.")
                                                    return False
                                        else:
                                            #highlight parent then throw error
                                            print(CRED+"Not Found"+CEND)
                                            Tree.focus(p)
                                            Tree.selection_set(p)
                                            ClassEntry.delete(0,tkinter.END)
                                            messagebox.showerror("Error","Class doesnot exist")
                                            return False
                            else: 
                                #throw error
                                print(CRED+"Not found"+CEND)
                                SubjectEntry.delete(0,tkinter.END)
                                messagebox.showerror("Error","Subject doesnot exist")
                                return False
                        
                    tkinter.Button(Search_EnrolToSubTreeScreen,text="Search..",fg='blue',command=confirmSearchEnrolToSubTree,bd=0).grid(column=1,row=4)
                tkinter.Button(EnrolToSubChangeAscScreen,text="Search",fg='blue',command=Search_EnrolToSubTree,bd=0).grid(column=0,row=2)
                '''
                Module Name:-warningMessage3
                Module Purpose:- Closes child windows
                Module args:- None
                Inputs:- none
                Outputs:- close commands for all child windows
                '''
                def warningMessage3():
                    global Search_EnrolToSubTreeScreen
                    global EnrolToSubChangeAscScreen        
                    print(CRED+"Close command receieved"+CEND)
                    try:
                        Search_EnrolToSubTreeScreen.destroy()
                    except:
                        pass
    
                    EnrolToSubChangeAscScreen.destroy()
                tkinter.Button(EnrolToSubChangeAscScreen,text="Finish",fg='green',command=warningMessage3,bd=0).grid(column=1,row=2)

                EnrolToSubChangeAscScreen.protocol("WM_DELETE_WINDOW",warningMessage3)
    
            tkinter.Button(ChangeAssociationsScreen,text="Enrol to Subjects",command=EnrolToSubCHANGEASC,fg='green',bd=0).grid(column=0,row=2)
            '''
            Module Name:- BindToSubCHANGEASC
            Module Purpose:- Binds the user
            Module Args:- None
            Module Inputs:- User database , subject database , auth mod
            Module Outputs:- Table with subjects the user can bind to
            '''
            def BindToSubCHANGEASC():
                global BindToSubScreen
                global BindTree_Refresh
                global Refresh_Clicked
                global Refresh_ChangeAscTreeview
                global BindTree_Refresh
                global SearchBindTreeScreen
                if CheckOpen("Bind To Sub"):
                    return False
                BindToSubScreen = tkinter.Toplevel(loginScreen)
                BindToSubScreen.title("Bind To Sub")
                BindToSubScreen.resizable(0,0)
                if not AuthMod(givenUser,1):
                    return False
                tkinter.Label(BindToSubScreen,text="Bind To Subjects by Double Clicking on a Record",fg='purple').grid(column=1,row=0)
                print(CGREEN+"Bind screen loaded"+CEND)
                BindTreeFrame = tkinter.Frame(BindToSubScreen)
                BindTree = ttk.Treeview(BindTreeFrame)
    
                '''
                Module Name:- SortBindTree
                Module Purpose:- Sorts the bindTree
                Module args:- none
                Module Inputs:- Table data
                Module Outputs:- sorted table data
                '''
                def SortBindTree():
                    existingParents = BindTree.get_children()
                    newParents = []

                    for k in existingParents:
                        newParents.append(BindTree.item(k)['text'])

                    newParents = QuickieSort(newParents)
                    finalInsert = []

                    for t in newParents:

                        for k in existingParents:

                            if BindTree.item(k)['text'] == t:

                                existingChildren = BindTree.get_children(k)
                                newChildren = []

                                for n in existingChildren:

                                    newChildren.append(BindTree.item(n)['text'])

                                finalInsert.append((t,newChildren))
                    i = 0
                    BindTree.delete(*BindTree.get_children())
                    print(CGREEN+"Sorted"+CEND)
                    while i<len(finalInsert):
                        existingParents = BindTree.get_children() 
                        subject,classes = finalInsert[i]                           

                        if len(existingParents) == 0:
                            tempID = BindTree.insert("",tkinter.END,text=subject)

                            k = 0

                            while k<len(classes):
                                BindTree.insert(tempID,tkinter.END,text=classes[k])
                                k+=1

                            i+=1
                            continue

                        k = 0
                        t = False

                        while k<len(existingParents):

                            if BindTree.item(existingParents[k])['text'] == subject:

                                j = 0

                                while j<len(classes):

                                    BindTree.insert(existingParents[k],tkinter.END,text=classes[j])
                                    j+=1
                                t = True
                            k+=1

                        if t:
                            i+=1
                            continue

                        tempID = BindTree.insert("",tkinter.END,text=subject)
                        k = 0

                        while k<len(classes):
                            BindTree.insert(tempID,tkinter.END,text=classes[k])
                            k+=1

                        i+=1
                BindTree.heading("#0",text="Subject/Class",command=SortBindTree)
    
                ScrollYBindTree = tkinter.Scrollbar(BindTreeFrame,command=BindTree.yview,orient=tkinter.VERTICAL)
                ScrollYBindTree.pack(side=tkinter.RIGHT,fill=tkinter.Y)
                ScrollXBindTree = tkinter.Scrollbar(BindTreeFrame,command=BindTree.xview,orient=tkinter.HORIZONTAL)
                '''
                Module Name:- BindTree_Refresh
                Module Purpose:- refreshs the BindTree
                Module Args:- None
                Module Inputs:- Subject databse , user database , role database
                Module Outputs:- refreshed table
                '''
                def BindTree_Refresh():
                    BindTree.delete(*BindTree.get_children())
                    file = open("subjects.csv","r+")
                    subjectLines = file.readlines()
                    file.close()

                    file = open("users.csv","r+")
                    userLines = file.readlines()
                    file.close()

                    file = open("roles.csv","r+")
                    roleLines = file.readlines()
                    file.close()
                    canJoinRestricted = ""
                    uRole = ""
                    i = 0
                    #finds the role of the selected user
                    while i<len(userLines):
                        row = userLines[i].split(',')
                        if len(row)!=userLEN:
                            i+=1
                            continue
                        for t in range(len(row)):row[t] = row[t].strip()
                        if row[0] == givenUser:
                            uRole = row[3]
                            break
                        i+=1
                    i = 0
                    #finds the permission of the user (whether he can join restricted)
                    while i<len(roleLines):
                        row = roleLines[i].split(',')
                        if len(row)!=roleLEN:
                            i+=1
                            continue
                        for t in range(len(row)):row[t] = row[t].strip()
                        if row[0] == uRole:
                            tempPerms = row[2].split('.')
                            for t in range(len(tempPerms)):tempPerms[t] = tempPerms[t].strip()
                            canJoinRestricted = bool(int(tempPerms[4]))
                            break
                        i+=1
                    i = 0
                    finalInsert = []
                    #adds the class for binding , if the user does not have permissions, then bind would fail
                    while i<len(subjectLines):
                        row = subjectLines[i].split(',')
    
                        if len(row)!=subjectLEN:
                            i+=1
                            continue
    
                        for t in range(len(row)):row[t] = row[t].strip()
    
                        subjectName = row[0]
                        bound = row[5]
                        restrictedState = row[4]
                        if not(bool(int(restrictedState))) == canJoinRestricted:
                            print(CRED+"Permission missing, class skipped"+CEND)
                            i+=1
                            continue
                        if bound != "":
                            print(CRED+"Already bound class, skipped"+CEND)
                            i+=1
                            continue
                        finalInsert.append((subjectName,row[1]))
                        i+=1
                    i = 0
                    #inserts categorically
                    while i<len(finalInsert):
                        existingParents =BindTree.get_children()
                        sub,clas = finalInsert[i]
                        print(CGREEN+f"Inserting {sub}:{clas}"+CEND)
                        if len(existingParents) == 0:
                            tempID = BindTree.insert("",tkinter.END,text=sub)
                            BindTree.insert(tempID,tkinter.END,text=clas)
                            i+=1
                            continue
    
                        k = 0
                        t = False
                        while k<len(existingParents):
    
                            if BindTree.item(existingParents[k])['text'] == sub:
    
                                BindTree.insert(existingParents[k],tkinter.END,text=clas)
                                t = True
                                break
    
                            k+=1
    
                        if t:
                            i+=1
                            continue
    
                        tempID = BindTree.insert("",tkinter.END,text=sub)
                        BindTree.insert(tempID,tkinter.END,text=clas)
    
                        i+=1
    
                BindTree_Refresh()
    
                ScrollXBindTree.pack(side=tkinter.BOTTOM,fill=tkinter.X)
   
                BindTree.configure(xscrollcommand=ScrollXBindTree.set)
                BindTree.configure(yscrollcommand=ScrollYBindTree.set)
                BindTree.pack(side=tkinter.TOP,expand='false')
                '''
                Module Name:- ConfirmBind
                Module Purpose:- Bind a user to a selected subject
                Module Args:- None
                Module Inputs:-selectedSubject , subject database , role data
                Module Outputs:- user bound or error thrown
                '''
                def ConfirmBind(event):
                    global Refresh_Clicked
                    global Refresh_ChangeAscTreeview

                    try:
                        #checks whether a class has been clicked and not a subject
                        className = BindTree.item(BindTree.focus())['text']
                        subjectName = BindTree.item(BindTree.parent(BindTree.focus()))['text']
   
                        if className == "":
                            raise TypeError
   
                        if subjectName == "":
                            raise TypeError
   
                    except:
                        return
   
                    subjectTRUE.append(("BOUND",subjectName,className))
                    #checks whether the roles are sufficient to bind to a class(this is 3rd layer role protection)
                    if not AuthMod(givenUser,1):
                        print(CRED+"Insufficient permissions"+CEND)
                        messagebox.showerror("Error","User cannot bind to any classes because his role is insufficient. change the role and reopen this window!")
                        try:
                            warningMessage5()
                        except:
                            pass
                        return False
                    file = open("subjects.csv","r+")
                    subjectLines=file.readlines()
                    file.close()
                    newLines = []
                    i = 0
                    #Binds the user to class
                    while i<len(subjectLines):
                        row = subjectLines[i].split(',')
   
                        if len(row)!=subjectLEN:
                            i+=1
                            continue
   
                        for t in range(len(row)):row[t] = row[t].strip()
   
                        if row[0] == subjectName and row[1] == className:
                            newLines.append((subjectName+","+className+","+row[2]+","+row[3]+","+row[4]+","+givenUser+"\n"))
                            i+=1
                            continue
                        newLines.append((row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+"\n"))
                        i+=1
                    file = open("subjects.csv","w+")
                    file.writelines(newLines)
                    file.close()
                    print(CGREEN+"Saved Changes"+CEND)
                    messagebox.showinfo("Success","User bound to class")
                    Refresh_Clicked()
                    try:
                        Refresh_ChangeAscTreeview()
                    except:
                        pass
                    BindTree_Refresh()

                BindTree.bind("<Double-1>",ConfirmBind)
                BindTreeFrame.grid(column=1,row=1)
                
                tkinter.Button(BindToSubScreen,text="Sort..",fg='blue',command=SortBindTree,bd=0).grid(column=0,row=2)
                '''
                Module Name:- SearchBindTree
                Module Purpose:- Search the BindTree using a form
                Module Args:- None
                Module Inputs:- none
                Module Outputs:- Provides a form to search the bind tree'''
                def SearchBindTree():
                    global SearchBindTreeScreen
                    if CheckOpen("Search Bind Treeview BindTree"):
                        return False
                    SearchBindTreeScreen = tkinter.Toplevel(loginScreen)
                    SearchBindTreeScreen.title("Search Bind Treeview BindTree")
                    SearchBindTreeScreen.resizable(0,0)

                    tkinter.Label(SearchBindTreeScreen,text="Search...",fg='purple').grid(column=1,row=0)

                    tkinter.Label(SearchBindTreeScreen,text="Search For:").grid(column=0,row=1)
                    SearchWhatEntry = tkinter.Entry(SearchBindTreeScreen,width=23)
                    SearchWhatEntry.grid(column=1,row=1)
                    
                    tkinter.Label(SearchBindTreeScreen,text="Search Where:").grid(column=0,row=2)
                    SearchWhereCombo = ttk.Combobox(SearchBindTreeScreen,values=["Subjects","Classes"],state='readonly')
                    SearchWhereCombo.set("Subjects")
                    SearchWhereCombo.grid(column=1,row=2)
                    print(CGREEN+"Search screen loaded"+CEND)

                    tkinter.Label(SearchBindTreeScreen,text="Search Mode:").grid(column=0,row=3)
                    SearchModeCombo = ttk.Combobox(SearchBindTreeScreen,values=["Linear","Binary"],state='readonly')
                    SearchModeCombo.set("Linear")
                    SearchModeCombo.grid(column=1,row=3)
                    '''
                    Module Name:- SearchBindTree_Confirm
                    Module Purpose:- Search the bind tree using the data provided in the form
                    Module Args:- None
                    Module Inputs:- SearchWhat(what to look for) , SearchWhere(where to look for(subjects/classes)) , SearchMode(what mode to use(linear/binary))'''
                    def SearchBindTree_Confirm():
                        SearchWhat = SearchWhatEntry.get()
                        SearchWhere = SearchWhereCombo.get()
                        SearchMode = SearchModeCombo.get()
                        if SearchWhat == "" or SearchWhere == "" or SearchMode == "":
                            print(CRED+"Missing data"+CEND)
                            messagebox.showerror("Error","Fill all the fields")
                            return False
                        if SearchMode == "Linear":
                            if SearchWhere == "Subjects":
                                existingSubjects = BindTree.get_children()

                                i = 0
                                while i<len(existingSubjects):
                                    if BindTree.item(existingSubjects[i])['text'] == SearchWhat:
                                        print(CGREEN+"Found"+CEND)
                                        messagebox.showinfo("Success","Item highlighted in the treeview")
                                        BindTree.focus(existingSubjects[i])
                                        BindTree.selection_set(existingSubjects[i])
                                        return False
                                    i+=1
                                
                                messagebox.showerror("Error","Unable to find the item")
                                return False
                            else:
                                existingSubjects = BindTree.get_children()
                                i = 0
                                toHighlightSub = []
                                toHighlightClas = []
                                while i<len(existingSubjects):
                                    existingClasses = BindTree.get_children(existingSubjects[i])
                                    k = 0
                                    while k<len(existingClasses):
                                        if BindTree.item(existingClasses[k])['text'] == SearchWhat:
                                            toHighlightSub.append(existingSubjects[i])
                                            toHighlightClas.append(existingClasses[k])
                                        k+=1
                                    i+=1
                                if len(toHighlightSub)==0:
                                    print(CRED+"Missing sub"+CEND)
                                    messagebox.showerror("Error","Unable to find class")
                                    SearchWhatEntry.delete(0,tkinter.END)    
                                    return False
                                i = 0
                                while i<len(toHighlightSub):
                                    parent = toHighlightSub[i]
                                    BindTree.item(parent,open=True)
                                    i+=1
                                BindTree.selection_set(toHighlightClas)
                                print(CGREEN+"Item/s found"+CEND)
                                messagebox.showinfo("Success","All instances highlighted")
                                return False
                        else:
                            if SearchWhere == "Subjects":
                                existingSubjects = BindTree.get_children()
                                newExistingSubjects = []
                                for t in existingSubjects:newExistingSubjects.append(BindTree.item(t)['text'])
                                newExistingSubjects = QuickieSort(newExistingSubjects)
                                if binarySearchAppr(newExistingSubjects,0,len(newExistingSubjects)-1,SearchWhat):
                                    for t in existingSubjects:
                                        if BindTree.item(t)['text'] == SearchWhat:
                                            print(CGREEN+"Item found BSearch"+CEND)
                                            BindTree.focus(t)
                                            BindTree.selection_set(t)
                                            messagebox.showinfo("Success","Subject highlighted in the treeview")
                                            SearchWhatEntry.delete(0,tkinter.END)
                                            return False
                                else:
                                    print(CRED+"Item not found BSearch"+CEND)
                                    messagebox.showerror("Error","Unable to find subject.")
                                    SearchWhatEntry.delete(0,tkinter.END)
                                    return False
                            else:
                                existingSubjects = BindTree.get_children()
                                for t in existingSubjects:
                                    existingChildren = BindTree.get_children(t)
                                    newExistingChildren = []
                                    for k in existingChildren:newExistingChildren.append(BindTree.item(k)['text'])
                                    newExistingChildren = QuickieSort(newExistingChildren)
                                    if binarySearchAppr(newExistingChildren,0,len(newExistingChildren)-1,SearchWhat):
                                        for n in existingChildren:
                                            if BindTree.item(n)['text'] == SearchWhat:
                                                print(CGREEN+"Item Found"+CEND)
                                                BindTree.focus(n)
                                                BindTree.selection_set(n)
                                                messagebox.showinfo("Success","Class highlighted in the treeview")
                                                SearchWhatEntry.delete(0,tkinter.END)
                                                return False
                                print(CRED+"Item not found"+CEND)
                                messagebox.showerror("Error","Unable to find Class.")
                                SearchWhatEntry.delete(0,tkinter.END)
                                return False
                            
                    tkinter.Button(SearchBindTreeScreen,text="Search..",fg='green',command=SearchBindTree_Confirm,bd=0).grid(column=1,row=4)
                tkinter.Button(BindToSubScreen,text="Search..",fg='blue',command=SearchBindTree,bd=0).grid(column=2,row=2)
                global warningMessage5
                '''
                Module name:- warningmessage5
                Module purpose:- close child windows
                module args:- none
                Module inps:- none
                module outs:- close commands for child windows
                '''
                def warningMessage5():
                    print(CRED+"Close command received"+CEND)
                    global SearchBindTreeScreen
                    try:
                        SearchBindTreeScreen.destroy()
                    except:
                        pass
                    BindToSubScreen.destroy()
                BindToSubScreen.protocol("WM_DELETE_WINDOW",warningMessage5)
            if AuthMod(givenUser,1):
                tkinter.Button(ChangeAssociationsScreen,text="Bind to Classes",command=BindToSubCHANGEASC,fg='green',bd=0).grid(column=2,row=2)
            else:
                print(CRED+"Permissions missing to bind to classes"+CEND)
                tkinter.Button(ChangeAssociationsScreen,text="Bind to Classes",command=BindToSubCHANGEASC,fg='red',state='disabled',bd=0).grid(column=2,row=2)
            '''
            Module Name:-  DeleteAssc
            Module Purpose:- Deletes a association between the user and a class(enrol/bind/waitlists)
            Module Args:- event(ignored)
            Module Inputs:- user databse , selected association data, waitlist database,subject database
            outputs:- Changes reflected in the respective database or error thrown
            '''
            def DeleteAssc(event):
                global subjectTRUE
                global Refresh_EnrolToSubTree
                global BindTree_Refresh
                global BindTree_Refresh
                try:
                    #to check whether a class association has been selected
                    subject = ChangeAscTreeview.item(ChangeAscTreeview.focus())['text']
                    class_ = ChangeAscTreeview.item(ChangeAscTreeview.focus())['values'][0]
                    type_ = ChangeAscTreeview.item(ChangeAscTreeview.focus())['values'][1]
                except:
                    return False
   
                if type_ == "ENROLLED":
                    #runs unenrolement algo
                    file= open("users.csv","r+")
                    userLines = file.readlines()
                    file.close()
   
                    i = 0
                    newUserLines = []
                    #modifies the enrolements of the user
                    while i<len(userLines):
                        row = userLines[i].split(',')
   
                        if len(row)!= userLEN:
                            i+=1
                            continue
   
                        for t in range(len(row)):row[t] = row[t].strip()
   
                        if row[0] == givenUser:
                            enrolledSubs = row[2].split('.')
                            k = 0
                            newSubs = []
   
                            while k<len(enrolledSubs):
   
                                if enrolledSubs[k] != subject or enrolledSubs[k+1] != class_:
                                    newSubs.append(enrolledSubs[k])
                                    newSubs.append(enrolledSubs[k+1])
                                k+=2
                            newSubsW = ""
                            k = 0
   
                            while k<len(newSubs):
   
                                if k == len(newSubs)-1:
                                    newSubsW=newSubsW+newSubs[k]
                                else:
                                    newSubsW=newSubsW+newSubs[k]+"."
                                k+=1
                            #TODO
                            newUserLines.append(row[0]+','+row[1]+','+newSubsW+','+row[3]+','+row[4]+"\n")
                            i+=1
                            continue
                        #TODO
                        newUserLines.append(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+"\n")
                        i+=1
   
                    file = open("users.csv","w+")
                    file.writelines(newUserLines)
                    file.close()
   
                    i = 0
                    #once enrolled , delete the enrolement from array
                    while i<len(subjectTRUE):
                        state,subject2,class_2 = subjectTRUE[i]
   
                        if state == "ENROLLED" and subject2 == subject and class_ == class_2:
                            del subjectTRUE[i]
                            break
                        i+=1
                    print(CRED+"Enrolement removed"+CEND)
                    messagebox.showinfo("Success","Enrolement Removed")
                    try:
                        FileVerifs()
                    except:
                        pass
                    Refresh_Clicked()
                    Refresh_ChangeAscTreeview()
   
                    try:
                        Refresh_EnrolToSubTree()
                    except:
                        pass                        
                    
                    return False
   
                elif type_ == "WAITLISTED":
   
                    file = open("waitlist.csv","r+")
                    waitlistLines=file.readlines()
                    file.close()
   
                    i = 0
                    newWaitlistLines = []
                    #deletes the waitlists of the user
                    while i<len(waitlistLines):
                        row = waitlistLines[i].split(',')
   
                        if len(row)!=waitlistLEN:
                            i+=1
                            continue
   
                        for t in range(len(row)):row[t] = row[t].strip()
   
                        if not(row[0] == givenUser and row[1] == subject and row[2] == class_):
                            newWaitlistLines.append(waitlistLines[i])

                        i+=1
   
                    file = open("waitlist.csv","w+")
                    file.writelines(newWaitlistLines)
                    file.close()
   
                    i = 0
                    #removes waitlist from the subject array
                    while i<len(subjectTRUE):
                        state,subject2,class_2 = subjectTRUE[i]
                        if state=="WAITLISTED" and subject2==subject and class_2==class_:
                            del subjectTRUE[i]
                            break
                        i+=1
                    print(CRED+"Waitlist removed"+CEND)
                    messagebox.showinfo("Success","Unwaitlisted successfully")
                    FileVerifs()
                    Refresh_Clicked()
                    Refresh_ChangeAscTreeview()
   
                    try:
                        Refresh_EnrolToSubTree()
                    except:
                        pass   
   
                    return False
                else:
                    file = open("subjects.csv","r+")
                    subjectLines=file.readlines()
                    file.close()
   
                    i = 0
                    newSubjectLines = []
                    #removes binds made by the user
                    while i<len(subjectLines):
                        row = subjectLines[i].split(',')
   
                        if len(row) != subjectLEN:
                            i+=1
                            continue
   
                        for t in range(len(row)):row[t]=row[t].strip()
   
                        if row[5] == givenUser and row[0] == subject and row[1] == class_:
                            newSubjectLines.append(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+",\n")
                            i+=1
                            continue
   
                        newSubjectLines.append(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+","+row[5]+"\n")
                        i+=1
   
                    file = open("subjects.csv","w+")
                    file.writelines(newSubjectLines)
                    file.close()
   
                    i = 0
   
                    while i<len(subjectTRUE):
                        state,subject2,class_2 = subjectTRUE[i]
   
                        if state=="BOUND" and subject2 == subject and class_2 == class_:
                            del subjectTRUE[i]
                            break
                        i+=1
                    print(CRED+"Bind removed"+CEND)
                    messagebox.showinfo("Success","Un bound from subject")
                    FileVerifs()
                    Refresh_Clicked()
                    Refresh_ChangeAscTreeview()
                    try:
                        BindTree_Refresh()
                    except:
                        pass
                    try:
                        Refresh_EnrolToSubTree()
                    except:
                        pass   
   
            ChangeAscTreeview.bind("<Double-1>",DeleteAssc) 
            '''
            Module Name:warningMessage4
            Purpose: Close childwindows
            Args:- none
            Input:- None
            Outputs:- Close commands for all child windows
            '''
            def warningMessage4():
                global EnrolToSubChangeAscScreen
                global ChangeAssociationsScreen
                global BindToSubScreen
                global warningMessage5
                print(CRED+"Close commands received"+CEND)
                try:
                    warningMessage3()
                except:
                    pass
   
                try:
                    EnrolToSubChangeAscScreen.destroy()
                except:
                    pass
                
                try:
                    warningMessage5()
                except:
                    pass
            
                try:
                    BindToSubScreen.destroy()
                except:
                    pass
                ChangeAssociationsScreen.destroy()
            tkinter.Label(ChangeAssociationsScreen,text="All enrolements and binds are realtime. Leaving the program would still save changes. This doesnot apply to username and role.",fg='purple').grid(column=1,row=2)
            ChangeAssociationsScreen.protocol("WM_DELETE_WINDOW",warningMessage4)
   
        tkinter.Button(EditUserScreenDlg,text="Manage Subjects",fg='blue',command=Edit_ChangeSubjects,bd=0).grid(column=0,row=4)
        Refresh_Clicked()
        tkinter.Button(EditUserScreenDlg,text="Refresh Form",fg='blue',command=Refresh_Clicked,bd=0).grid(column=0,row=5)
        '''
        Name:- Reset_Pass
        Args:- none
        inputs:- User database
        Outputs:- email sent to user whose password is resetted
        '''
        def Reset_Pass():
            file = open("users.csv","r+")
            userLines = file.readlines()
            file.close()
   
            i = 0
            newUserLines = []
            while i<len(userLines):
                row = userLines[i].split(',')
   
                if len(row)!=userLEN:
                    i+=1
                    continue
   
                for t in range(len(row)):row[t] = row[t].strip()
   
                if row[0] == givenUser:
                    randomPass = random.randint(0,10000)
                    randomPass = str(randomPass)
                    #TODO
                    email = row[4]
                    if email != "":
                        #email sent to user containing info that provides resetted password and username
                        try:
                            if connected_ssid == b"gwsc.vic.edu.au":
                                raise TypeError
                            server = smtplib.SMTP("smtp.office365.com",587)
                            server.starttls()
                            server.login("proofofconcept69420@outlook.com","somerandompassword69420")
                        except:
                            if messagebox.askyesno("Error","There is no network connection present to send a reset password message. Continue?"):
                                #TODO
                                newUserLines.append(row[0]+","+randomPass+","+row[2]+","+row[3]+"\n")
                                i+=1
                                continue
                            else:
                                return False
   
                        msg = MIMEMultipart()
                        msg['To'] = email
                        msg['From'] = 'proofofconcept69420@outlook.com'
                        msg['Subject']='Password Resetted'
                        msg2="Your password has been resetted for your account:"+givenUser+"\nYour new password is:"+randomPass
                        msg.attach(MIMEText(msg2,'plain'))
            
                        try:
                            server.send_message(msg,"proofofconcept69420@outlook.com",email)
                        except:
                            if messagebox.askyesno("Error","Email error occurred.\nNon Critical Error\nThis could be due to a invalid email. Do you want to remove the email bound to "+givenUser+"?"):
                                row[3]=""        
            
                        server.quit()
                        #TODO
                    newUserLines.append(row[0]+","+randomPass+","+row[2]+","+row[3]+","+row[4]+"\n")
                    i+=1
                    continue
            
                toW = ""
                k =0 
                while k<len(row):
            
                    if k == len(row)-1:
                        toW=toW+row[k]+"\n"
                    else:
                        toW=toW+row[k]+","
                    k+=1
            
                newUserLines.append(toW)
                i+=1
            
            file = open("users.csv","w+")
            file.writelines(newUserLines)
            file.close()
            print(CGREEN+"Password resetted"+CEND)
            messagebox.showinfo("Sucess","Password resetted to:"+randomPass)
            EditUser_refresh()
            warningMessage2()
       
        tkinter.Button(EditUserScreenDlg,text="Reset Pass",fg='blue',command=Reset_Pass,bd=0).grid(column=1,row=5)
        '''
        Name:- Edit_SaveChanges
        Args:- none
        Inputs:- username, rolename and email and user database and role database
        Outputs:- Users data edited
        '''
        def Edit_SaveChanges():
            global warningMessage2
            newUser = NameEntry.get()
            newEmail = EmailEntry.get()
            newRole = RoleCombo.get()
            if newEmail == "":
                i = 0
                slaves = EditUserScreenDlg.grid_slaves()
                while i<len(slaves):
                    #checks whether the email entry has been gridded , if it has been , asks the user on whether he wants to disable 2FA
                    if str(slaves[i]).split('.')[2]=="!entry2":
                        print(CRED+"2FA missing????"+CEND)
                        if messagebox.askyesno("Confirm","Disable 2FA?"):
                            break
                        else:
                            messagebox.showerror("Error","Operation Cancelled")
                            Refresh_Clicked()
                            return False
                    i+=1                
            #input filter
            if newUser == "" or newUser=="admin" or not(set(newUser).issubset(approved_text)):
                print(CRED+"Forbidden characters detected in name"+CEND)
                messagebox.showerror("Error","Username contains forbidden characters. Use CamelCase instead of spaces in your name")
                NameEntry.delete(0,tkinter.END)
                return False
    
            elif not(set(newUser).issubset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")):
                print(CRED+"Username contains Specials and illegals!"+CEND)
                messagebox.showerror("Error","Username should contain only Alphabetical Characters")
                NameEntry.delete(0,tkinter.END)
                return False
            if newRole == "":
                RoleCombo.current(1)
                newRole = RoleCombo.get()
            file = open("roles.csv","r+")
            roleLines=file.readlines()
            file.close()
            file = open("users.csv","r+")
            userLines = file.readlines()
            file.close()
            i = 0
            overUserRoleLevel = 0
            overUserRole = ""
            newRoleLevel = 0
            canBind = ""
            canEnrol = ""
            #2nd Layer protection to prevent manipulation of users on a higher role level
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == user:
                    overUserRole = row[3]
                    if overUserRole == newRole:
                        print(CRED+"Manipulation of user at a higher role detected!"+CEND)
                        messagebox.showerror("Error","You cannot modify users in the same role level you are in.")
                        return False
                    i = 0
                    while i<len(roleLines):
                        row = roleLines[i].split(',')
                        if len(row)!=roleLEN:
                            i+=1
                            continue
                        for t in range(len(row)):row[t] = row[t].strip()
                        if row[0] == overUserRole:
                            overUserRoleLevel = int(row[1])
                        if row[0] == newRole:
                            newRoleLevel = int(row[1])
                            canBind = row[2].split('.')[0]
                            canEnrol = row[2].split('.')[4]
                        i+=1
                    if newRoleLevel<=overUserRoleLevel:
                        print(CRED+"Promotion of user to a higher role level detected!"+CEND)
                        #prevents promoting users to a role higher than you
                        messagebox.showerror("Error","The role you are giving this user is at a higher role level than yours.")
                        RoleCombo.current(1)
                        return False
                    elif user == givenUser:
                        #Checks whether the user is the same user who is logged in and displays this message
                        if messagebox.askyesno("Confirm","Do you want to demote yourself?"):
                            print(CRED+"Demoted"+CEND)
                            messagebox.showinfo("Reboot","Restart program to view changes")
                            break
                        else:
                            RoleCombo.set(overUserRole)
                            return False
                    else:
                        break
                i+=1
            newUs = []
            i = 0
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == newUser and newUser != givenUser:
                    #prevents editing the user and overwriting other users
                    print(CRED+"Overwrite of other users prevented"+CEND)
                    messagebox.showerror("Confirm","This user that you are attempting to edit to, already exists. Edit/Delete that user and try again")
                    return False
                newUs.append(userLines[i])
                i+=1
            file = open("users.csv","w+")
            file.writelines(newUs)
            file.close()
            file = open("users.csv","r+")
            userLines=file.readlines()
            file.close()
            i = 0
            newULines = []
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == givenUser:
                    if canBind == "0":
                        #if the user cannot bind , removes all binds
                        file = open("subjects.csv","r+")
                        subjectLines = file.readlines()
                        file.close()
                        newSLines = []
                        p = 0
                        c = 0
                        while p<len(subjectLines):
                            row2 = subjectLines[p].split(',')
                            if len(row2)!=subjectLEN:
                                p+=1
                                continue
                            for t in range(len(row2)):row2[t] = row2[t].strip()
                            if row2[5] == givenUser:
                                #TODO
                                print(CRED+f"Bind removed for {row2[0]}:{row2[1]} due to permission revoke"+CEND)
                                newSLines.append(row2[0]+","+row2[1]+","+row2[2]+","+row2[3]+","+row2[4]+","+"\n")
                                c+=1
                            else:
                                #TODO
                                newSLines.append(subjectLines[p])
                            p+=1
                        file = open("subjects.csv","w+")
                        file.writelines(newSLines)
                        file.close()
                        if c>0:
                            messagebox.showwarning("Warning","You have bound to some subjects but have set a role that cannot be bound to classes.\nAll bound classes have been unbound!")
                    tempSubs = row[2].split('.')
                    c= 0
                    if canEnrol == "0":
                        #if the user cannot enrol restricted , removes all enrolements to restricted
                        file = open("subjects.csv","r+")
                        subjectLines = file.readlines()
                        file.close()
                        k= 0
                        tempSubs = row[2].split('.')
                        while k<len(subjectLines):
                            row2= subjectLines[k].split(',')
                            if len(row2)!=subjectLEN:
                                k+=1
                                continue
                            for t in range(len(row2)):row2[t] = row2[t].strip()
                            if row2[4] == "1":
                                p = 0
                                while p<len(tempSubs):
                                    if tempSubs[p] == row2[0] and tempSubs[p+1]==row2[1]:
                                        print(CRED+f"Removed enrolement {row2[0]}:{row2[1]} due to perm revoked"+CEND)
                                        del tempSubs[p]
                                        del tempSubs[p]
                                        c+=1
                                        break
                                    else:
                                        p+=2
                            k+=1
                        toWSubs = ""
                        p = 0
                        while p<len(tempSubs):
                            if p == 0:
                                toWSubs = tempSubs[p]+"."
                            elif p == len(tempSubs)-1:
                                toWSubs = toWSubs+tempSubs[p]
                            else:
                                toWSubs=toWSubs+tempSubs[p]+"."
                            p+=1                       
                    else:
                        toWSubs = row[2]
                    file = open("subjects.csv","r+")
                    subjectLines = file.readlines()
                    file.close()
                    newSLines = []
                    p = 0
                    while p<len(subjectLines):
                        row2 = subjectLines[p].split(',')
                        if len(row2)!=subjectLEN:
                            p+=1
                            continue
                        for t in range(len(row2)):row2[t] = row2[t].strip()
                        if row2[5] == givenUser:
                            #TODO
                            if row2[4] == "1":
                                newSLines.append(row2[0]+","+row2[1]+","+row2[2]+","+row2[3]+","+row2[4]+","+"\n")
                                c+=1
                            else:
                                newSLines.append(subjectLines[p])
                        else:
                            #TODO
                            newSLines.append(subjectLines[p])
                        p+=1
                    file = open("subjects.csv","w+")
                    file.writelines(newSLines)
                    file.close()
                    if c>0:
                        messagebox.showwarning("Warning","Restricted classes have been detected. These have been automatically removed from enrolements")
                    #TODO
                    #SETUP EMAIL VERIF
                    if newEmail != row[4]:
                        try:
                            #verifies email by sending a email
                            if connected_ssid == b"gwsc.vic.edu.au":
                                raise TypeError
                            server = smtplib.SMTP("smtp.office365.com",587)
                            server.starttls()
                            server.login("proofofconcept69420@outlook.com","somerandompassword69420")
                            msg= MIMEMultipart()
                            msg['From'] = "proofofconcept69420@outlook.com"
                            msg['To'] = newEmail
                            msg['Subject'] = 'This Email has been used to link a account to Allocate++ '+newUser
                            msg2 = "New Email bound succesfully!\nYour account may have changed. Please review your account changes:-\nUsername:"+newUser+"\nPassword:"+row[1]
                            msg.attach(MIMEText(msg2,'plain'))
                        except:
                            print(CRED+"Network Error"+CEND)
                            messagebox.showerror("Info","Unable to connect to the internet. Email verification failed.")
                            return False
                        try:
                            server.send_message(msg,"proofofconcept69420@outlook.com",newEmail)
                            time.sleep(15)
                            server.quit()
                            server = poplib.POP3_SSL("outlook.office365.com",995)
                            server.user('proofofconcept69420@outlook.com')
                            server.pass_("somerandompassword69420")
                            resp , mails , octets = server.list()
                            del resp,octets
                            print(mails)
                            index = len(mails)
                            resp,lines,octets = server.retr(index)
                            msg_content = b'\r\n'.join(lines).decode('utf-8')
                            msg = Parser().parsestr(msg_content)
                            EmailSubject=msg.get('Subject').strip()
                            if 'Undeliverable: This Email has been used to link a account to\r\n Allocate++ '+newUser == EmailSubject:
                                print(CRED+"Invalid Email Detected"+CEND)
                                messagebox.showerror("Error","Invalid Email Provided")
                                server.dele(index)
                                server.quit()
                                return False
                        except:
                            print(CRED+"Invalid email detected. Assuming"+CEND)
                            messagebox.showerror("Error","Invalid email.")
                            newEmail = row[4]
                        server.quit()
                        print(CGREEN+"Registered"+CEND)
                        messagebox.showinfo("Info","This email is registered")
                    newULines.append(newUser+","+row[1]+","+toWSubs+","+newRole+","+newEmail+"\n")
                    i+=1
                    continue
                #TODO
                newULines.append(row[0]+","+row[1]+','+row[2]+','+row[3]+','+row[4]+"\n")
                i+=1
            file = open('users.csv',"w+")
            file.writelines(newULines)
            file.close()
            file = open("waitlist.csv","r+")
            waitlistLines = file.readlines()
            file.close()
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
            i = 0
            newWLines = []
            #removes waitlists to restricted classes
            while i<len(waitlistLines):
                row = waitlistLines[i].split(',')
                if len(row)!=waitlistLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t]=row[t].strip()
                n = False
                if row[0]==givenUser:
                    p = 0
                    while p<len(subjectLines):
                        row2 = subjectLines[p].split(',')
                        if len(row2)!=subjectLEN:
                            p+=1
                            continue
                        for t in range(len(row2)):row2[t]=row2[t].strip()
                        if row2[0] == row[1] and row2[1] == row[2]:
                            state = row2[4]
                            if bool(int(state)) == True and bool(int(canEnrol)) == False:
                                i+=1
                                n = True
                                break
                            else:
                                break
                        p+=1
                if n:
                    print(CRED+f"waitlist to {row[0]}:{row[1]} removed due to perm revoke"+CEND)
                    continue
                newWLines.append(row[0]+","+row[1]+","+row[2]+"\n")
                i+=1
            file = open("waitlist.csv","w+")
            file.writelines(newWLines)
            file.close()
            print(CGREEN+"All changes saved and forms refreshed"+CEND)
            EditUser_refresh()
            warningMessage2()
            FileVerifs()
        tkinter.Button(EditUserScreenDlg,text="Save Changes",fg="green",command=Edit_SaveChanges,bd=0).grid(column=1,row=4)
        '''
        Name:- warningMessage2
        args:- none
        Inputs:- None
        Outputs:- close commands to all child windows
        '''
        def warningMessage2():
            global ChangeAssociationsScreen
            global EnrolToSubChangeAscScreen
            print(CRED+"Close command received"+CEND)
            try:
                ChangeAssociationsScreen.destroy()
            except:
                pass
       
            try:
                EnrolToSubChangeAscScreen.destroy()
            except:
                pass
       
            try:
                warningMessage4()
            except:
                pass
       
            try:
                warningMessage3()
            except:
                pass
            
                            
            EditUserScreenDlg.destroy()  
       
        EditUserScreenDlg.protocol("WM_DELETE_WINDOW",warningMessage2)
    
    EditUserTreeview.bind("<Double-1>",EditUser_Clicked)
    '''
    Module Name:- EditUser_Search
    Purpose:- provides a form to search for users to edit
    Args:- none
    Inputs:- none
    Outputs:- form capable of searching edit users
    '''
    def EditUser_Search():
        global EditUserSearchScreen
        if CheckOpen("Search EditUserTreeview"):
            return False
    
        EditUserSearchScreen = tkinter.Toplevel(loginScreen)
        EditUserSearchScreen.title("Search EditUserTreeview")
        EditUserSearchScreen.resizable(0,0)
    
        tkinter.Label(EditUserSearchScreen,text="Search..",fg='blue').grid(column=1,row=0)
    
        SearchWhatEntry=tkinter.Entry(EditUserSearchScreen,width=23)
        SearchWhatEntry.grid(column=1,row=1)
    
        tkinter.Label(EditUserSearchScreen,text="Search Criteria").grid(column=0,row=1)
    
        SearchWhereCombo = ttk.Combobox(EditUserSearchScreen,values=["Roles","Users"],state='readonly')
        SearchWhereCombo.set("Roles")
        SearchWhereCombo.grid(column=1,row=2)
    
        tkinter.Label(EditUserSearchScreen,text="Search Where:").grid(column=0,row=2)
        SearchModeCombo = ttk.Combobox(EditUserSearchScreen,values=["Linear","Binary"],state='readonly')
        SearchModeCombo.grid(column=1,row=3)
        SearchModeCombo.set("Linear")
        print(CGREEN+"Search window initialized"+CEND)
        tkinter.Label(EditUserSearchScreen,text="Search Mode:").grid(column=0,row=3)
        '''
        Name:- SearchConfirmEdit
        Args:- none
        Inputs:- Search What(criteria) , Search Mode(binary or linear) , search where(roles,users) , rows in table
        Outputs:-Highlights item or throws error
        '''
        def SearchConfirmEdit():
            SearchWhat = SearchWhatEntry.get()
            SearchMode = SearchModeCombo.get()
            SearchWhere = SearchWhereCombo.get()
    
            if SearchWhat.strip() == "" or SearchMode == "" or SearchWhere == "": 
                print(CRED+"Missing data"+CEND)
                messagebox.showerror("Error","Fill all the boxes")
                return False
    
            if SearchWhere == "Roles":
                if SearchMode == "Linear":
                    existingRoles = EditUserTreeview.get_children()
                    i = 0
                    while i<len(existingRoles):
                        if EditUserTreeview.item(existingRoles[i])['text'] == SearchWhat:
                            #conducts linear search and highlights item
                            EditUserTreeview.focus(existingRoles[i])
                            EditUserTreeview.selection_set(existingRoles[i])
                            print(CGREEN+"Found role"+CEND)
                            messagebox.showinfo("Sucess","Item has been highlighted in the table")
                            return False
                        i+=1
                    print(CRED+"Unable to find role"+CEND)
                    messagebox.showerror("Error","Unable to find Role. Check your criteria and try again")
                    return False
                else:
                    existingRoles = EditUserTreeview.get_children()
                    i = 0
                    NEWexistingRoles = []
    
                    for k in existingRoles:NEWexistingRoles.append(EditUserTreeview.item(k)['text'])
    
                    NEWexistingRoles = QuickieSort(NEWexistingRoles)
    
                    if binarySearchAppr(NEWexistingRoles,0,len(NEWexistingRoles)-1,SearchWhat):
                        for i in existingRoles:
                            if EditUserTreeview.item(i)['text'] == SearchWhat:
                                #conducts binary search and highlights item
                                EditUserTreeview.focus(i)
                                print(CGREEN+"item found"+CEND)
                                EditUserTreeview.selection_set(i)
                                messagebox.showinfo("Success","Item has been highlighted in the table")
                                return False
                    else:
                        print(CRED+"Role not found"+CEND)
                        messagebox.showerror("Error","Unable to find role. Check your criteria and try again")
                        return False
            else:
                if SearchMode == "Linear":
                    existingRoles = EditUserTreeview.get_children()
                    t = 0
    
                    while t<len(existingRoles):
    
                        for i in EditUserTreeview.get_children(existingRoles[t]):
    
                            if EditUserTreeview.item(i)['text'] == SearchWhat:
                                #conducts linear search and highlights item
                                EditUserTreeview.item(EditUserTreeview.parent(i),open=True)
                                EditUserTreeview.selection_set(i)
                                EditUserTreeview.focus(i)
                                print(CGREEN+"item found"+CEND)
                                messagebox.showinfo("Sucess","User found and highlighted in the table")
                                return False
                        t+=1
                    print(CRED+"Item not found"+CEND)
                    messagebox.showerror("Error","User not found. Check your criteria and try again.")                    
                    return False
                else:
                    existingRoles = EditUserTreeview.get_children()
                    i = 0
    
                    while i<len(existingRoles):
                        tempChildren = []
                        t=0
    
                        for t in EditUserTreeview.get_children(existingRoles[i]):tempChildren.append(EditUserTreeview.item(t)['text'])
    
                        if binarySearchAppr(tempChildren,0,len(tempChildren)-1,SearchWhat):
    
                            for k in EditUserTreeview.get_children(existingRoles[i]):
    
                                if EditUserTreeview.item(k)['text'] == SearchWhat:
                                    #conducts binary search and highlights item
                                    print(CGREEN+"item found"+CEND)
                                    EditUserTreeview.item(EditUserTreeview.parent(k),open=True)
                                    EditUserTreeview.focus(k)
                                    EditUserTreeview.selection_set(k)
                                    messagebox.showinfo("Success","User has been highlighted in the table")
                                    return False
                        i+=1
                    print(CRED+"item not found"+CEND)
                    messagebox.showerror("Error","Unable to find user. check your criteria and try again")
                    return False
    
        tkinter.Button(EditUserSearchScreen,text="Search..",fg='green',command=SearchConfirmEdit,bd=0).grid(column=1,row=4)
  
    tkinter.Button(EditUserScreen,command=EditUser_Search,text="Search..",fg='blue',bd=0).grid(column=0,row=2)
    '''
    Name:- EditUser_Sort
    Purpose:- Sorts the table
    Args:- None
    Inputs:- Rows in the table
    Outputs:- Sorted rows
    '''
    def EditUser_Sort():
        ExistingRoles = EditUserTreeview.get_children()
        NEWexistingRoles = []
  
        for t in ExistingRoles:NEWexistingRoles.append(EditUserTreeview.item(t)['text'])

        NEWexistingRoles = QuickieSort(NEWexistingRoles)
        k = 0
        FinalInsert = []
  
        while k<len(ExistingRoles):
            #sorts the children and parents
            tempChildren = EditUserTreeview.get_children(ExistingRoles[k])
            j = 0
            NEWtempChildren = []
  
            for t in tempChildren:NEWtempChildren.append(EditUserTreeview.item(t)['text'])
  
            NEWtempChildren = QuickieSort(NEWtempChildren)
            FinalInsert.append((EditUserTreeview.item(ExistingRoles[k])['text'],NEWtempChildren))
            k+=1
  
        i = 0
        EditUserTreeview.delete(*EditUserTreeview.get_children())
        #inserts sorted item
        while i<len(FinalInsert):
            role,users = FinalInsert[i]
            ExistingRoles = EditUserTreeview.get_children()
  
            if len(ExistingRoles) == 0:
                tempID=EditUserTreeview.insert("",tkinter.END,text=role)
                k = 0
  
                while k<len(users):
                    EditUserTreeview.insert(tempID,tkinter.END,text=users[k])
                    k+=1
  
                i+=1
                continue
            k = 0
  
            while k<len(ExistingRoles):
                if EditUserTreeview.item(ExistingRoles[k])['text'] == role:
                    j = 0
  
                    while j<len(users):
                        EditUserTreeview.insert(ExistingRoles[k],tkinter.END,text=users[j])
                        j+=1
  
                    i+=1
                    continue
                k+=1
  
            tempID = EditUserTreeview.insert("",tkinter.END,text=role)
            k = 0
  
            while k<len(users):
                EditUserTreeview.insert(tempID,tkinter.END,text=users[k])
                k+=1
  
            i+=1
        print(CGREEN+"Sorted data"+CEND)
        messagebox.showinfo("Success","Sorted Using Quick Sort")
  
    tkinter.Button(EditUserScreen,text="Sort..",command=EditUser_Sort,fg='blue',bd=0).grid(column=2,row=2)
    '''
    Name:- warningMessage
    Purpose:- Closes children
    Args:- None
    Inputs:- None
    Outputs:- closes sub children'''
    def warningMessage():
        global EditUserSearchScreen
        global EditUserScreenDlg
        global warningMessage4
        print(CGREEN+"Close commmands received"+CEND)
        try:
            EditUserSearchScreen.destroy()
        except:
            pass
  
        try:
            EditUserScreenDlg.destroy()
        except:
            pass
  
        try:
            warningMessage4()
        except:
            pass
  
        try:
            warningMessage3()
        except:
            pass
  
        EditUserScreen.destroy()
    
    EditUserScreen.protocol("WM_DELETE_WINDOW",warningMessage)
    EditUserScreen.mainloop()
'''
Name:- ManageRoles
Purpose:- open sub window that provides options to add/edit/remove roles
Args:- user(current user who logged in)
Inputs:- user   
Outputs:- screen with options to add/edit/remove roles
'''
def ManageRoles(user):
    if CheckOpen("Manage Roles"):return False
    ManageRolesScreen = tkinter.Toplevel(loginScreen)
    ManageRolesScreen.title("Manage Roles")
    ManageRolesScreen.resizable(0,0)
    tkinter.Label(ManageRolesScreen,text="Click button to perform action").grid(column=1,row=0)
    print(CGREEN+"Manage roles screen initialized"+CEND)
    '''
    Name:- CreateRole
    Purpose:- Creates a screen with a form to create a role
    Args:- None
    Inputs:- None
    Outputs:- Screen with a form to create roles
    '''
    def CreateRole():
        global CreateRoleScreen
        if CheckOpen("Create Role"):return False
        CreateRoleScreen=tkinter.Toplevel(loginScreen)
        CreateRoleScreen.resizable(0,0)
        CreateRoleScreen.title("Create Role")
        tkinter.Label(CreateRoleScreen,text="Fill the form to create a role").grid(column=1,row=0)

        tkinter.Label(CreateRoleScreen,text="Role Name:").grid(column=0,row=1)
        RoleNameEntry = tkinter.Entry(CreateRoleScreen,width=23)
        RoleNameEntry.grid(column=1,row=1)
        tkinter.Button(CreateRoleScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Role name is the way the program will represent these permissions. For example:- Student Role")).grid(column=2,row=1)

        CanBindToClassLbl=tkinter.Label(CreateRoleScreen,text="Can Bind To Class?",fg='red')
        CanBindToClassLbl.grid(column=0,row=2)
        '''
        Name:-CanBindToClassFunc
        Purpose:- Toggles colour of the label near the checkbox
        Args:- a,b,c(ignored)
        Inputs:- Check button state
        Outputs:- Label colour change
        '''
        def CanBindToClassFunc(a,b,c):
            if CanBindToClassCheck.instate(['!selected']):
                print(CGREEN+"Can Bind Class Check , toggled true"+CEND)
                CanBindToClassLbl.config(fg='green')
            else:
                print(CRED+"Can Bind Class Check , toggled false"+CEND)
                CanBindToClassLbl.config(fg='red')
        tracerCanBindToClass = tkinter.IntVar()
        CanBindToClassCheck = ttk.Checkbutton(CreateRoleScreen,variable=tracerCanBindToClass)
        tracerCanBindToClass.trace('w',CanBindToClassFunc)
        CanBindToClassCheck.state(['!alternate'])
        CanBindToClassCheck.state(['!selected'])
        CanBindToClassCheck.grid(column=1,row=2)
        tkinter.Button(CreateRoleScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Determines whether the user can bind(become a teacher) and manage a class. Removing this permission is recommended for student roles and other non teachers\nUsers that are Bound to a class have certain permisions within that class that may or maynot have been granted for that role level.")).grid(column=2,row=2)
        
        CanManageRolesLbl=tkinter.Label(CreateRoleScreen,text="Can Manage Roles?",fg='red')
        CanManageRolesLbl.grid(column=0,row=3)
        '''
        Name:-CanManageRolesFunc
        Purpose:- Toggles colour of the label near the checkbox
        Args:- a,b,c(ignored)
        Inputs:- Check button state
        Outputs:- Label colour change
        '''
        def CanManageRolesFunc(a,b,c):
            if canManageRolesCheck.instate(['!selected']):
                print(CGREEN+"Can manage roles Check , toggled true"+CEND)
                CanManageRolesLbl.config(fg='green')
            else:
                print(CRED+"Can manage roles Check , toggled false"+CEND)
                CanManageRolesLbl.config(fg='red')
        tracerCanManageRoles = tkinter.IntVar()
        canManageRolesCheck = ttk.Checkbutton(CreateRoleScreen,variable=tracerCanManageRoles)
        tracerCanManageRoles.trace('w',CanManageRolesFunc)
        canManageRolesCheck.state(['!alternate'])
        canManageRolesCheck.state(['!selected'])
        canManageRolesCheck.grid(column=1,row=3)
        tkinter.Button(CreateRoleScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Determines whether the user can add/edit/delete roles. This setting is affected by role level.ie , they cannot create roles at a higher role level than them neither can they grant permissions that they do not have.(press help near role level for more info).")).grid(column=2,row=3)
        
        CanAddUsersLbl = tkinter.Label(CreateRoleScreen,text="Can Add Users?",fg='red')
        CanAddUsersLbl.grid(column=0,row=4)
        '''
        Name:-CanAddUsersFunc
        Purpose:- Toggles colour of the label near the checkbox
        Args:- a,b,c(ignored)
        Inputs:- Check button state
        Outputs:- Label colour change
        '''
        def CanAddUsersFunc(a,b,c):
            if canAddUsersCheck.instate(['!selected']):
                print(CGREEN+"Can Add Users Check , toggled true"+CEND)
                CanAddUsersLbl.config(fg='green')
            else:
                print(CRED+"Can Add Users Check , toggled false"+CEND)
                CanAddUsersLbl.config(fg='red')
        tracerCanAddUsers = tkinter.IntVar()
        canAddUsersCheck = ttk.Checkbutton(CreateRoleScreen,variable=tracerCanAddUsers)
        tracerCanAddUsers.trace('w',CanAddUsersFunc)
        canAddUsersCheck.state(['!alternate'])
        canAddUsersCheck.state(['!selected'])
        canAddUsersCheck.grid(column=1,row=4)
        tkinter.Button(CreateRoleScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Determines whether the user can add users. This setting is affected by role level. ie, they cannot give new users a role in a higher level than theirs. (press help near role level for more info)")).grid(column=2,row=4)

        CanDeleteUsersLbl = tkinter.Label(CreateRoleScreen,text="Can Delete Users?",fg='red')
        CanDeleteUsersLbl.grid(column=0,row=5)
        '''
        Name:-CanDeleteUsersFunc
        Purpose:- Toggles colour of the label near the checkbox
        Args:- a,b,c(ignored)
        Inputs:- Check button state
        Outputs:- Label colour change
        '''
        def CanDeleteUsersFunc(a,b,c):
            if CanDeleteUsersCheck.instate(['!selected']):
                print(CGREEN+"Can Delete Users Check , toggled true"+CEND)
                CanDeleteUsersLbl.config(fg='green')
            else:
                print(CRED+"Can Delete Users Check , toggled false"+CEND)
                CanDeleteUsersLbl.config(fg='red')
        tracerCanDeleteUsers = tkinter.IntVar()
        CanDeleteUsersCheck = ttk.Checkbutton(CreateRoleScreen,variable=tracerCanDeleteUsers)
        tracerCanDeleteUsers.trace('w',CanDeleteUsersFunc)
        CanDeleteUsersCheck.state(['!alternate'])
        CanDeleteUsersCheck.state(['!selected'])
        CanDeleteUsersCheck.grid(column=1,row=5)
        tkinter.Button(CreateRoleScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Determines whether the user can delete other users. this is affected by role level. They cannot delete users that are at a higher role level than them. (press help near role level for more info)")).grid(column=2,row=5)

        CanJoinRestrictedLbl = tkinter.Label(CreateRoleScreen,text="Can Join Restricted?",fg='red')
        CanJoinRestrictedLbl.grid(column=0,row=6)
        '''
        Name:-CanJoinRestrictedFunc
        Purpose:- Toggles colour of the label near the checkbox
        Args:- a,b,c(ignored)
        Inputs:- Check button state
        Outputs:- Label colour change
        '''
        def canJoinRestrictedFunc(a,b,c):
            if canJoinRestrictedCheck.instate(['!selected']):
                print(CGREEN+"Can Join Restricted Check , toggled true"+CEND)
                CanJoinRestrictedLbl.config(fg='green')
            else:
                print(CRED+"Can Join Restricted Check , toggled false"+CEND)
                CanJoinRestrictedLbl.config(fg='red')
        tracerCanJoinRestricted = tkinter.IntVar()
        canJoinRestrictedCheck = ttk.Checkbutton(CreateRoleScreen,variable=tracerCanJoinRestricted)
        tracerCanJoinRestricted.trace('w',canJoinRestrictedFunc)
        canJoinRestrictedCheck.state(['!alternate'])
        canJoinRestrictedCheck.state(['!selected'])
        canJoinRestrictedCheck.grid(column=1,row=6)
        tkinter.Button(CreateRoleScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Determines whether the user has the permission to join restricted classes. Eg:- Staff Meetings would be a restricted class and staff should have this permission to enrol to that class")).grid(column=2,row=6)

        CanManageClassLbl = tkinter.Label(CreateRoleScreen,text="Can Manage Class?",fg='red')
        CanManageClassLbl.grid(column=0,row=7)
        '''
        Name:-CanManageClassFunc
        Purpose:- Toggles colour of the label near the checkbox
        Args:- a,b,c(ignored)
        Inputs:- Check button state
        Outputs:- Label colour change
        '''
        def canManageClassFunc(a,b,c):
            if CanManageClassCheck.instate(['!selected']):
                print(CGREEN+"Can Manage Class Check , toggled true"+CEND)
                CanManageClassLbl.config(fg='green')
            else:
                print(CRED+"Can Manage Class Check , toggled false"+CEND)
                CanManageClassLbl.config(fg='red')
        tracerCanManageClass = tkinter.IntVar()
        CanManageClassCheck = ttk.Checkbutton(CreateRoleScreen,variable=tracerCanManageClass)
        tracerCanManageClass.trace('w',canManageClassFunc)
        CanManageClassCheck.state(['!alternate'])
        CanManageClassCheck.state(['!selected'])
        CanManageClassCheck.grid(column=1,row=7)
        tkinter.Button(CreateRoleScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Gives the ability to add , remove and edit classes. The user can make restricted classes even if the user doesnot have the capability to join the class")).grid(column=2,row=7)

        tkinter.Label(CreateRoleScreen,text="Role Rank:").grid(column=0,row=8)
        RoleRankEntry=tkinter.Entry(CreateRoleScreen,width=23)
        RoleRankEntry.grid(column=1,row=8)
        tkinter.Button(CreateRoleScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Role levels makes sure that important roles cannot be modified by lower roles. for example , the staff role level should be the highest to prevent low roles such as student from changing it. In this situation:- staff would have role level 1 and students would have role level 2. This would prevent any modifications to the staff roles and all the users registered to staff.\n In conclusion , Role level is used to tell the program which roles are more important than others(tip:- more than 1 role can be bound to the same rank.)")).grid(column=2,row=8)
        '''
        Name:- CreateRoleConfirm
        Purpose:- Creates a role using the data in the form
        Args:- none
        Inputs:- rolename , permissions,role rank
        Outputs:- added role in role database or throws error
        '''
        if not(AuthMod(user,1)):
            print(CRED+"Can Bind Class perm missing"+CEND)
            CanBindToClassCheck.state(['disabled'])
        if not(AuthMod(user,2)):
            print(CRED+"Can Manage Class perm missing"+CEND)
            CanManageClassCheck.state(['disabled'])
        if not(AuthMod(user,3)):
            print(CRED+"Can Add Users perm missing"+CEND)
            canAddUsersCheck.state(['disabled'])
        if not(AuthMod(user,4)):
            print(CRED+"Can Delte Users perm missing"+CEND)
            CanDeleteUsersCheck.state(['disabled'])
        if not(AuthMod(user,5)):
            print(CRED+"Can join restricted perm missing"+CEND)
            canJoinRestrictedCheck.state(['disabled'])
        if not(AuthMod(user,6)):
            print(CRED+"Can manage class perm missing"+CEND)
            CanManageClassCheck.state(['disabled'])
        def CreateRoleConfirm():
            #freeze data
            CanBindToClass = CanBindToClassCheck.instate(['selected'])
            CanManageClass = CanManageClassCheck.instate(['selected'])
            canAddUsers = canAddUsersCheck.instate(['selected'])
            canManageRoles = canManageRolesCheck.instate(['selected'])
            CanDeleteUsers = CanDeleteUsersCheck.instate(['selected'])
            canJoinRestricted = canJoinRestrictedCheck.instate(['selected'])
            roleName = RoleNameEntry.get()
            print(CGREEN+"Data frozen"+CEND)
            #verify data
            if roleName == "" or not(set(roleName).issubset(approved_text)):
                print(CRED+"Invalid role name"+CEND)
                messagebox.showerror("Error","Please provide a valid role name with no spaces. Use camel case instead.")
                RoleNameEntry.delete(0,tkinter.END)
                return False
            try:
                #type check
                roleLevel = int(RoleRankEntry.get())
            except:
                print(CRED+"Invalid Role Rank"+CEND)
                messagebox.showerror("Error","The role level needs to be a integer")
                RoleRankEntry.delete(0,tkinter.END)
                return False
            permClash = []
            #The user cannot give perms he doesnt have
            if AuthMod(user,1) == False and CanBindToClass == True:
                permClash.append("Can Bind To Class\n")
                CanBindToClass=False
            if AuthMod(user,2) == False and canManageRoles!=False:
                permClash.append("Can Manage Roles\n")
                canManageRoles=False
            if AuthMod(user,3) == False and canAddUsers!=False:
                permClash.append("Can Add Users\n")
                canAddUsers=False
            if AuthMod(user,4) == False and CanDeleteUsers!=False:
                permClash.append("Can Delete Users\n")
                CanDeleteUsers = False
            if AuthMod(user,5) == False and canJoinRestricted!=False:
                permClash.append("Can Join Restricted\n")
                canJoinRestricted=False
            if AuthMod(user,6) == False and CanManageClass!=False:
                permClash.append("Can Manage Class\n")
                CanManageClass = False
            file = open("users.csv","r+")
            userLines=file.readlines()
            file.close()
            file = open("roles.csv","r+")
            roleLines = file.readlines()
            file.close()
            i = 0
            oLevel = 0
            #obtains role rank of user
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == user:
                    k = 0
                    oRole = row[3]
                    p = False
                    while k<len(roleLines):
                        row2 = roleLines[k].split(',')
                        if len(row2)!=roleLEN:
                            k+=1
                            continue
                        for t in range(len(row2)):row2[t] = row2[t].strip()
                        if row2[0] == oRole:
                            oLevel = int(row2[1])
                            p = True
                            break
                        k+=1
                    if p:
                        break
                i+=1
            #prevents user from adding a role at a higher rank than themselves
            if int(oLevel)>=int(roleLevel):
                print(CRED+"Too low role level"+CEND)
                messagebox.showerror("Error","Your role rank is too low to create a role at that level. The role rank has been set to the highest rank you can provide automatically. Resubmit the form after you make your necessary changes")
                RoleRankEntry.delete(0,tkinter.END)
                RoleRankEntry.insert(0,str(oLevel+1))
                return False
            toWPerms = ""
            #Perm data compiled
            if CanBindToClass:
                toWPerms="1."
            else:
                toWPerms="0."
            if canManageRoles:
                toWPerms=toWPerms+"1."
            else:
                toWPerms=toWPerms+"0."
            if canAddUsers:
                toWPerms=toWPerms+"1."
            else:
                toWPerms=toWPerms+"0."
            if CanDeleteUsers:
                toWPerms = toWPerms+"1."
            else:
                toWPerms=toWPerms+"0."
            if canJoinRestricted:
                toWPerms=toWPerms+"1."
            else:
                toWPerms=toWPerms+"0."
            if CanManageClass:
                toWPerms=toWPerms+"1\n"
            else:
                toWPerms=toWPerms+"0\n"
            i = 0
            print(CGREEN+f"Role data {toWPerms}"+CEND)
            while i<len(roleLines):
                row = roleLines[i].split(',')
                if len(row)!=roleLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                #Checks for whether the role name is taken
                if row[0] == roleName:
                    print(CRED+"Role name taken"+CEND)
                    messagebox.showerror("Error","Role name is already taken!")
                    RoleNameEntry.delete(0,tkinter.END)
                    return False
                i+=1
            roleLines.append(roleName+","+str(roleLevel)+","+toWPerms)
            file = open("roles.csv","w+")
            file.writelines(roleLines)
            file.close()
            if len(permClash) > 0:
                print(CRED+"Some errors detected"+CEND)
                #displays perm clash message
                toWPermClash=""
                for item in permClash:toWPermClash=toWPermClash+item
                messagebox.showwarning("Success","The role was added successfully but some permissions cannot be granted because you do not have that permission.\n"+toWPermClash)
            else:
                print(CGREEN+"Role added!"+CEND)
                messagebox.showinfo("Success","The role is added successfully")
        tkinter.Button(CreateRoleScreen,text="Add Role",fg='green',bd=0,command=CreateRoleConfirm).grid(column=1,row=9)
        CreateRoleScreen.mainloop()
    tkinter.Button(ManageRolesScreen,text="Create Roles",fg='blue',bd=0,command=CreateRole).grid(column=1,row=1)
    '''
    Name:- EditRole
    Purpose:- Provides a table to edit a form
    Args:- none
    Inputs:- role database
    Outputs:- Edit Role Screen with a table to select roles
    '''
    def EditRole():
        global CloseEditRoleScreen
        if CheckOpen("Edit Roles"):return False
        EditRoleScreen = tkinter.Toplevel(loginScreen)
        EditRoleScreen.title("Edit Roles")
        EditRoleScreen.resizable(0,0)
        EditRoleScreen.geometry("720x300")
        print(CGREEN+"Edit Roles screen initialized"+CEND)
        tkinter.Label(EditRoleScreen,text="Edit A Role",fg='blue').grid(column=1,row=0)
        EditRoleFrame = tkinter.Frame(EditRoleScreen)
        EditTree = ttk.Treeview(EditRoleFrame,columns=["Rank","Can Bind To Class","Can Manage Roles","Can Add Users","Can Delete Users","Can Join Restricted","Can Manage Class"])
        EditTree.heading("Can Bind To Class",text="Can Bind To Class")
        EditTree.heading("Can Manage Roles",text="Can Manage Roles")
        EditTree.heading("Can Add Users",text='Can Add Users')
        EditTree.heading("Can Delete Users",text="Can Delete Users")
        EditTree.heading("Can Join Restricted",text="Can Join Restricted")
        EditTree.heading("Can Manage Class",text="Can Manage Class")
        EditTree.heading("#0",text="Role Name")
        EditTree.heading("Rank",text="Rank")
        XEdit = tkinter.Scrollbar(EditRoleFrame,orient=tkinter.HORIZONTAL,command=EditTree.xview)
        EditTree.configure(xscrollcommand=XEdit.set)
        YEdit = tkinter.Scrollbar(EditRoleFrame,orient=tkinter.VERTICAL,command=EditTree.yview)
        EditTree.configure(yscrollcommand=YEdit.set)
        YEdit.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        XEdit.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        EditTree.pack(side=tkinter.TOP,expand='false')
        EditTree.column("Rank",width=87,stretch=0,minwidth=87)
        EditTree.column("Can Bind To Class",width=87,stretch=0,minwidth=87)
        EditTree.column("Can Manage Roles",width=87,stretch=0,minwidth=87)
        EditTree.column("Can Add Users",width=87,stretch=0,minwidth=87)
        EditTree.column("Can Delete Users",width=87,stretch=0,minwidth=87)
        EditTree.column("Can Join Restricted",width=87,stretch=0,minwidth=87)
        EditTree.column("Can Manage Class",width=87,stretch=0,minwidth=87)
        EditTree.column("#0",width=87,stretch=0,minwidth=87)
        '''
        Name:- RefreshEditTree
        Purpose:- To Refresh the role tree(to reflect the latest data in database)
        Args:- none
        Inputs:- Role database , user database
        Outputs:- Role table refreshed
        '''
        def RefreshEditTree():
            EditTree.delete(*EditTree.get_children())
            file = open("roles.csv","r+")
            roleLines= file.readlines()
            file.close()
            oLevel = 0
            file = open("users.csv","r+")
            userLines = file.readlines()
            file.close()
            i = 0
            #grabs OLevel of the user
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == user:
                    oRole = row[3]
                    k = 0
                    while k<len(roleLines):
                        row2 = roleLines[k].split(',')
                        if len(row2)!=roleLEN:
                            k+=1
                            continue
                        for t in range(len(row2)):row2[t] = row2[t].strip()
                        if row2[0] == oRole:
                            oLevel=int(row2[1])
                            break
                        k+=1
                    break
                i+=1
            
            i = 0
            toIns= []
            #inserts all roles that are below the role rank of the user
            while i<len(roleLines):
                row = roleLines[i].split(',')
                if len(row)!=roleLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t]=row[t].strip()
                if oLevel>=int(row[1]):
                    i+=1
                    continue
                permList = row[2].split('.')
                CanBindToClass = bool(int(permList[0]))
                CanManageRoles = bool(int(permList[1]))
                CanAddUsers = bool(int(permList[2]))
                CanDeleteUsers=bool(int(permList[3]))
                CanJoinRestricted = bool(int(permList[4]))
                CanManageClass = bool(int(permList[5]))
                print(CGREEN+f"Role added with name {row[0]} and rank of {row[1]}"+CEND)
                toIns.append((row[0],[row[1],CanBindToClass,CanManageRoles,CanAddUsers,CanDeleteUsers,CanJoinRestricted,CanManageClass]))
                i+=1
            i = 0
            listOfRanks = []
            while i<len(toIns):
                listOfRanks.append(int(toIns[i][1][0]))
                i+=1
            listOfRanks = list(set(listOfRanks))
            listOfRanks = QuickieSort(listOfRanks)
            i = 0
            while i<len(listOfRanks):
                k = 0
                selectedID = listOfRanks[i]
                while k<len(toIns):
                    if toIns[k][1][0] == str(selectedID):
                        EditTree.insert("",tkinter.END,text=toIns[k][0],values=toIns[k][1])
                    k+=1
                i+=1
            
        RefreshEditTree()
        '''
        Name :- EditRoleConfirm
        Purpose:- To Open a form with modifiable settings for the selected role
        Args:- event(ignored)
        inputs:- rolename , permission data
        Outputs:- Screen with a form , with preset data of the role taken from the table
        '''
        def EditRoleConfirm(event):
            global EditRoleConfirmScreen
            try:
                #checks whether a role is clicked or not
                rolename = EditTree.item(EditTree.focus())['text']
                CanBindToClass = False
                CanManageRoles = False
                CanAddUsers = False
                CanDeleteUsers = False
                CanJoinRestricted =False
                CanManageClass = False
                EditTree.item(EditTree.focus())['values'][0]
            except:
                return False
            EditRoleConfirmScreen = tkinter.Toplevel(loginScreen)
            EditRoleConfirmScreen.resizable(0,0)
            EditRoleConfirmScreen.title("Edit Role")
            tkinter.Label(EditRoleConfirmScreen,text="Edit Role").grid(column=1,row=0)
            print(CGREEN+"Loaded edit role confirm screen"+CEND)
            tkinter.Label(EditRoleConfirmScreen,text="Role Name:").grid(column=0,row=1)
            RoleNameEntry = tkinter.Entry(EditRoleConfirmScreen,width=23)
            RoleNameEntry.insert(0,EditTree.item(EditTree.focus())['text'])
            RoleNameEntry.grid(column=1,row=1)
            tkinter.Button(EditRoleConfirmScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Role name is the way the program will represent these permissions. For example:- Student Role")).grid(column=2,row=1)

            tkinter.Label(EditRoleConfirmScreen,text="Role Rank:").grid(column=0,row=2)
            RoleRankEntry = tkinter.Entry(EditRoleConfirmScreen,width=23)
            RoleRankEntry.insert(0,EditTree.item(EditTree.focus())['values'][0])
            RoleRankEntry.grid(column=1,row=2)
            tkinter.Button(EditRoleConfirmScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Role levels makes sure that important roles cannot be modified by lower roles. for example , the staff role level should be the highest to prevent low roles such as student from changing it. In this situation:- staff would have role level 1 and students would have role level 2. This would prevent any modifications to the staff roles and all the users registered to staff.\n In conclusion , Role level is used to tell the program which roles are more important than others(tip:- more than 1 role can be bound to the same rank.)")).grid(column=2,row=2)

            tracerCanBindToClass = tkinter.IntVar()
            CanBindToClassLbl=tkinter.Label(EditRoleConfirmScreen,text="Can Bind To Class",fg='red')
            CanBindToClassLbl.grid(column=0,row=3)
            CanBindToClassCheck = ttk.Checkbutton(EditRoleConfirmScreen,variable=tracerCanBindToClass)
            CanBindToClassCheck.state(['!alternate'])
            if str(EditTree.item(EditTree.focus())['values'][1]) == "True":
                CanBindToClassCheck.state(['selected'])
                CanBindToClassLbl.config(fg='green')
                CanBindToClass = True
            CanBindToClassCheck.grid(column=1,row=3)
            '''
            Name:-CanBindToClassFunc
            Purpose:- Toggles colour of the label near the checkbox
            Args:- a,b,c(ignored)
            Inputs:- Check button state
            Outputs:- Label colour change
            '''
            def CanBindToClassFunc(a,b,c):
                if CanBindToClassCheck.instate(['!selected']):
                    print(CGREEN+"Can Bind Class Check , toggled true"+CEND)
                    CanBindToClassLbl.config(fg='green')
                else:
                    print(CRED+"Can Bind Class Check , toggled false"+CEND)
                    CanBindToClassLbl.config(fg='red')
            tracerCanBindToClass.trace('w',CanBindToClassFunc)
            tkinter.Button(EditRoleConfirmScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Determines whether the user can bind(become a teacher) and manage a class. Removing this permission is recommended for student roles and other non teachers\nUsers that are Bound to a class have certain permisions within that class that may or maynot have been granted for that role level.")).grid(column=2,row=3)

            tracerCanManageRoles = tkinter.IntVar()
            '''
            Name:-CanManageRolesFunc
            Purpose:- Toggles colour of the label near the checkbox
            Args:- a,b,c(ignored)
            Inputs:- Check button state
            Outputs:- Label colour change
            '''
            def CanManageRolesFunc(a,b,c):
                if CanManageRolesCheck.instate(['!selected']):
                    print(CGREEN+"Can Manage Roles Check , toggled true"+CEND)
                    CanManageRolesLbl.config(fg='green')
                else:
                    print(CRED+"Can Manage Roles Check , toggled false"+CEND)
                    CanManageRolesLbl.config(fg='red')
            CanManageRolesLbl = tkinter.Label(EditRoleConfirmScreen,text="Can Manage Roles",fg="red")
            CanManageRolesLbl.grid(column=0,row=4)
            CanManageRolesCheck = ttk.Checkbutton(EditRoleConfirmScreen,variable=tracerCanManageRoles)
            CanManageRolesCheck.state(['!alternate'])
            if str(EditTree.item(EditTree.focus())['values'][2]) == "True":
                CanManageRolesLbl.config(fg='green')
                CanManageRolesCheck.state(['selected'])
                CanManageRoles = True
            tracerCanManageRoles.trace('w',CanManageRolesFunc)
            CanManageRolesCheck.grid(column=1,row=4)
            tkinter.Button(EditRoleConfirmScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Determines whether the user can add/edit/delete roles. This setting is affected by role level.ie , they cannot create roles at a higher role level than them neither can they grant permissions that they do not have.(press help near role level for more info).")).grid(column=2,row=4)

            tracerCanAddUsers = tkinter.IntVar()
            '''
            Name:-CanAddUsersFunc
            Purpose:- Toggles colour of the label near the checkbox
            Args:- a,b,c(ignored)
            Inputs:- Check button state
            Outputs:- Label colour change
            '''
            def CanAddUsersFunc(a,b,c):
                if CanAddUsersCheck.instate(['!selected']):
                    print(CGREEN+"Can Add Users Check , toggled true"+CEND)
                    CanAddUsersLbl.config(fg='green')
                else:
                    print(CRED+"Can Add Users Check , toggled false"+CEND)
                    CanAddUsersLbl.config(fg='red')
            CanAddUsersLbl = tkinter.Label(EditRoleConfirmScreen,text="Can Add Users",fg='red')
            CanAddUsersLbl.grid(column=0,row=5)
            CanAddUsersCheck = ttk.Checkbutton(EditRoleConfirmScreen,variable=tracerCanAddUsers)
            CanAddUsersCheck.state(['!alternate'])
            if str(EditTree.item(EditTree.focus())['values'][3]) == "True":
                CanAddUsersLbl.config(fg='green')
                CanAddUsersCheck.state(['selected'])
                CanAddUsers = True
            tracerCanAddUsers.trace('w',CanAddUsersFunc)
            CanAddUsersCheck.grid(column=1,row=5)
            tkinter.Button(EditRoleConfirmScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Determines whether the user can add users. This setting is affected by role level. ie, they cannot give new users a role in a higher level than theirs. (press help near role level for more info)")).grid(column=2,row=5)

            tracerCanDeleteUsers = tkinter.IntVar()
            '''
            Name:-CanDeleteUsersFunc
            Purpose:- Toggles colour of the label near the checkbox
            Args:- a,b,c(ignored)
            Inputs:- Check button state
            Outputs:- Label colour change
            '''
            def CanDeleteUsersFunc(a,b,c):
                if CanDeleteUsersCheck.instate(['!selected']):
                    print(CGREEN+"Can Delete Users Check , toggled true"+CEND)
                    CanDeleteUsersLbl.config(fg='green')
                else:
                    print(CRED+"Can Delete Users Check , toggled false"+CEND)
                    CanDeleteUsersLbl.config(fg='red')
            CanDeleteUsersLbl = tkinter.Label(EditRoleConfirmScreen,text="Can Delete Users",fg='red')
            CanDeleteUsersLbl.grid(column=0,row=6)
            CanDeleteUsersCheck = ttk.Checkbutton(EditRoleConfirmScreen,variable=tracerCanDeleteUsers)
            CanDeleteUsersCheck.state(['!alternate'])
            if str(EditTree.item(EditTree.focus())['values'][4]) == "True":
                CanDeleteUsersLbl.config(fg='green')
                CanDeleteUsersCheck.state(['selected'])
                CanDeleteUsers = True
            CanDeleteUsersCheck.grid(column=1,row=6)
            tracerCanDeleteUsers.trace('w',CanDeleteUsersFunc)
            tkinter.Button(EditRoleConfirmScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Determines whether the user can delete other users. this is affected by role level. They cannot delete users that are at a higher role level than them. (press help near role level for more info)")).grid(column=2,row=6)

            tracerCanJoinRestricted = tkinter.IntVar()
            '''
            Name:-CanJoinRestrictedFunc
            Purpose:- Toggles colour of the label near the checkbox
            Args:- a,b,c(ignored)
            Inputs:- Check button state
            Outputs:- Label colour change
            '''
            def CanJoinRestrictedFunc(a,b,c):
                if CanJoinRestrictedCheck.instate(['!selected']):
                    print(CGREEN+"Can Join Restricted Check , toggled true"+CEND)
                    CanJoinRestrictedLbl.config(fg='green')
                else:
                    print(CRED+"Can Join Restricted Check , toggled false"+CEND)
                    CanJoinRestrictedLbl.config(fg='red')
            CanJoinRestrictedLbl = tkinter.Label(EditRoleConfirmScreen,text="Can Join Restricted",fg='red')
            CanJoinRestrictedLbl.grid(column=0,row=7)
            CanJoinRestrictedCheck = ttk.Checkbutton(EditRoleConfirmScreen,variable=tracerCanJoinRestricted)
            CanJoinRestrictedCheck.state(['!alternate'])
            if str(EditTree.item(EditTree.focus())['values'][5]) == "True":
                CanJoinRestrictedCheck.state(['selected'])
                CanJoinRestrictedLbl.config(fg='green')
                CanJoinRestricted = True
            CanJoinRestrictedCheck.grid(column=1,row=7)
            tracerCanJoinRestricted.trace('w',CanJoinRestrictedFunc)
            tkinter.Button(EditRoleConfirmScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Determines whether the user has the permission to join restricted classes. Eg:- Staff Meetings would be a restricted class and staff should have this permission to enrol to that class")).grid(column=2,row=7)
            tracerCanManageClass = tkinter.IntVar()
            '''
            Name:-CanManageClassFunc
            Purpose:- Toggles colour of the label near the checkbox
            Args:- a,b,c(ignored)
            Inputs:- Check button state
            Outputs:- Label colour change
            '''
            def CanManageClassFunc(a,b,c):
                if CanManageClassCheck.instate(['!selected']):
                    print(CGREEN+"Can Manage Class Check , toggled true"+CEND)
                    CanManageClassLbl.config(fg='green')
                else:
                    print(CRED+"Can Manage Class Check , toggled false"+CEND)
                    CanManageClassLbl.config(fg='red')
            CanManageClassLbl = tkinter.Label(EditRoleConfirmScreen,text="Can Manage Class",fg='red')
            CanManageClassLbl.grid(column=0,row=8)
            CanManageClassCheck = ttk.Checkbutton(EditRoleConfirmScreen,variable=tracerCanManageClass)
            CanManageClassCheck.state(['!alternate'])
            if str(EditTree.item(EditTree.focus())['values'][6]) == "True":
                CanManageClassCheck.state(['selected'])
                CanManageClassLbl.config(fg='green')
                CanManageClass = True
            CanManageClassCheck.grid(column=1,row=8)
            tracerCanManageClass.trace('w',CanManageClassFunc)
            tkinter.Button(EditRoleConfirmScreen,text="Help",fg='blue',bd=0,command=lambda:messagebox.showinfo("Info","Gives the ability to add , remove and edit classes. The user can make restricted classes even if the user doesnot have the capability to join the class")).grid(column=2,row=8)
            if not(AuthMod(user,1)):
                print(CRED+"Missing can bind to class check"+CEND)
                CanBindToClassCheck.state(['disabled'])
            if not(AuthMod(user,2)):
                print(CRED+"Missing can manage roles check"+CEND)
                CanManageRolesCheck.state(['disabled'])
            if not(AuthMod(user,3)):
                print(CRED+"Missing can add users check"+CEND)
                CanAddUsersCheck.state(['disabled'])
            if not(AuthMod(user,4)):
                print(CRED+"Missing can delete users check"+CEND)
                CanDeleteUsersCheck.state(['disabled'])
            if not(AuthMod(user,5)):
                print(CRED+"Missing can join restricted check"+CEND)
                CanJoinRestrictedCheck.state(['disabled'])
            if not(AuthMod(user,6)):
                print(CRED+"Missing can manage class check"+CEND)
                CanManageClassCheck.state(['disabled'])

            '''
            name:- EditRoleConfirmScreenSave
            Purpose:- save all changes made in the form
            Args:- none
            Inputs:- role name , permission data , role database
            Outputs:- Changes in role database or throws error
            '''
            def EditRoleConfirmScreenSave():
                newRoleName = RoleNameEntry.get()
                newRoleRank = RoleRankEntry.get()

                newCanAddUsers = CanAddUsersCheck.instate(['selected'])
                newCanDeleteUsers = CanDeleteUsersCheck.instate(['selected'])
                newCanJoinRestricted = CanJoinRestrictedCheck.instate(['selected'])
                newCanManageClass = CanManageClassCheck.instate(['selected'])
                newCanManageRoles = CanManageRolesCheck.instate(['selected'])
                newCanBindToClass = CanBindToClassCheck.instate(['selected'])
                if newRoleName == "" or not(set(newRoleName).issubset(approved_text)):
                    print(CRED+"Invalid Role Name"+CEND)
                    messagebox.showerror("Error","Invalid role name. Dont use spaces in name instead use CamelCase")
                    return False
                file = open("users.csv","r+")
                userLines = file.readlines()
                file.close()

                file = open("roles.csv","r+")
                roleLines = file.readlines()
                file.close()

                i = 0
                oLevel = 0
                #obtains OLevel
                while i<len(userLines):
                    row = userLines[i].split(',')
                    if len(row)!=userLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    if row[0] == user:
                        oRole = row[3]
                        k = 0
                        while k<len(roleLines):
                            row2= roleLines[k].split(',')
                            if len(row2)!=roleLEN:
                                k+=1
                                continue
                            for t in range(len(row2)):row2[t] = row2[t].strip()
                            if row2[0] == oRole:
                                oLevel = int(row2[1])
                                break
                            k+=1
                        break
                    i+=1
                #if oLevel is not high enough to provide role rank , throws error
                if oLevel>=int(newRoleRank):
                    print(CRED+"Role rank too low"+CEND)
                    messagebox.showerror("Error","You cannot provide this rank for this role. The program has automatically filled the form with the highest role rank you can provide.\nMake necessary changes and click 'Save Changes' again")
                    RoleRankEntry.delete(0,tkinter.END)
                    RoleRankEntry.insert(0,str(oLevel+1))
                    return False
                permClash = []
                permLoss = []
                #Perm loss checks for perms that are lost , ie , you cannot reprovide this permission if its removed
                #perm clash checks for perms that are given but is not present in your role. The user cannot provide these roles
                if AuthMod(user,1) == False and newCanBindToClass == False and CanBindToClass!=newCanBindToClass:
                    permLoss.append('Can Bind To Class')
                if AuthMod(user,1) == False and newCanBindToClass == True and CanBindToClass != newCanBindToClass:
                    newCanBindToClass = False
                    permClash.append("Can Bind To Class")

                if AuthMod(user,2) == False and CanManageRoles == False and CanManageRoles!=newCanBindToClass:
                    permLoss.append("Can Manage Roles")
                if AuthMod(user,2) == False and newCanManageRoles == True and CanManageRoles!=newCanManageRoles:
                    newCanManageRoles = False
                    permClash.append("Can Manage Roles")
                
                if AuthMod(user,3) == False and newCanAddUsers == False and CanAddUsers != newCanAddUsers:
                    permLoss.append("Can Add Users")
                if AuthMod(user,3) == False and newCanAddUsers == True and newCanAddUsers!=CanAddUsers:
                    newCanAddUsers = False
                    permClash.append("Can Add Users")
                
                if AuthMod(user,4) == False and newCanDeleteUsers == False and newCanDeleteUsers!=CanDeleteUsers:
                    permLoss.append("Can Delete Users")
                if AuthMod(user,4) == False and newCanDeleteUsers==True and newCanDeleteUsers!=CanDeleteUsers:
                    newCanDeleteUsers = False
                    permClash.append("Can Delete Users")
                
                if AuthMod(user,5) == False and newCanJoinRestricted == False and newCanJoinRestricted != CanJoinRestricted:
                    permLoss.append("Can Join Restricted")
                if AuthMod(user,5) == False and newCanJoinRestricted == True and newCanJoinRestricted != CanJoinRestricted:
                    newCanJoinRestricted = False
                    permClash.append("Can Join Restricted")
                
                if AuthMod(user,6) == False and newCanManageClass == False and newCanManageClass != CanManageClass:
                    permLoss.append("Can Manage Class")
                if AuthMod(user,6) == False and newCanManageClass == True and newCanManageClass != CanManageClass:
                    newCanManageClass = False
                    permClash.append("Can Manage Class")
                
                if len(permLoss)>0:
                    print(CRED+"Perm loss detected"+CEND)
                    toWPermLoss= ""
                    for item in permLoss:toWPermLoss=toWPermLoss+item+"\n"
                    if not messagebox.askyesno("Confirm","The following perms , once removed , cannot be granted by you again.\n"+toWPermLoss+"Are you sure you want to continue setup?"):
                        return False
                if len(permClash)>0:
                    print(CRED+"Perm clash detected"+CRED)
                    toWPermClash =""
                    for item in permClash:toWPermClash=toWPermClash+item+"\n"
                    if not messagebox.askyesno("Confirm","The following perms cannot be granted by you\n"+toWPermClash+"Do you still want to continue setup?"):
                        return False
                
                i = 0
                newRoleLines = []
                #Edits role
                while i<len(roleLines):
                    row = roleLines[i].split(',')
                    if len(row)!=roleLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    if row[0] == rolename:
                        toWPerms = ""
                        if newCanBindToClass:
                            toWPerms = "1."
                        else:
                            toWPerms = "0."
                        if newCanManageRoles:
                            toWPerms=toWPerms+"1."
                        else:
                            toWPerms = toWPerms+"0."
                        if newCanAddUsers:
                            toWPerms = toWPerms+"1."
                        else:
                            toWPerms = toWPerms+"0."
                        if newCanDeleteUsers:
                            toWPerms = toWPerms+"1."
                        else:
                            toWPerms = toWPerms+"0."
                        if newCanJoinRestricted:
                            toWPerms = toWPerms+"1."
                        else:
                            toWPerms = toWPerms+"0."
                        if newCanManageClass:
                            toWPerms = toWPerms+"1"
                        else:
                            toWPerms = toWPerms+"0"
                        newRoleLines.append(newRoleName+","+str(newRoleRank)+","+toWPerms+"\n")
                        i+=1
                        continue
                    if row[0] == newRoleName and newRoleName!=rolename:
                        print(CRED+"Role name already taken by a different role"+CEND)
                        messagebox.showerror("Error","The name that you are attempting to change to is already taken. Please pick a different name")
                        RoleNameEntry.delete(0,tkinter.END)
                        return False
                    newRoleLines.append(roleLines[i])
                    i+=1
                file = open("roles.csv","w+")
                file.writelines(newRoleLines)
                file.close()
                print(CGREEN+f"changes saved for role {newRoleName}"+CEND)
                messagebox.showinfo("Success","Role Updated")
                RefreshEditTree()
                EditRoleConfirmScreen.destroy()
            tkinter.Button(EditRoleConfirmScreen,text="Save Changes",fg='green',bd=0,command=EditRoleConfirmScreenSave).grid(column=1,row=9)
            EditRoleConfirmScreen.mainloop()
        EditTree.bind("<Double-1>",EditRoleConfirm)
        '''
        Name:- CloseEditRoleScreen
        Purpose:- Closes children of the screen
        Args:- None
        Inputs:- None
        Outputs:- close commands for sub children
        '''
        def CloseEditRoleScreen():
            print(CRED+"Close command detected"+CEND)
            global EditRoleConfirmScreen
            try:
                EditRoleConfirmScreen.destroy()
            except:
                pass
            EditRoleScreen.destroy()
        EditRoleScreen.protocol("WM_DELETE_WINDOW",CloseEditRoleScreen)
        EditRoleFrame.grid(column=1,row=1)
        tkinter.Button(EditRoleScreen,text="Exit..",command=EditRoleScreen.destroy,fg='red',bd=0).grid(column=1,row=2)
    tkinter.Button(ManageRolesScreen,text="Edit Roles",fg='blue',bd=0,command=EditRole).grid(column=1,row=2)
    '''
    Name:- DeleteRole
    Purpose:- Provides table with roles that can be deleted
    Args:- None
    Inputs:- Role database , user database
    Outputs:- Role Table with roles that can be deleted
    '''
    def DeleteRole():
        global CloseDeleteRoleScreen
        if CheckOpen("Delete Roles"):return False
        DeleteRoleScreen = tkinter.Toplevel(loginScreen)
        DeleteRoleScreen.title("Delete Roles")
        tkinter.Label(DeleteRoleScreen,text="Double Click to delete role",fg='red').grid(column=1,row=0)
        DeleteRoleFrame =tkinter.Frame(DeleteRoleScreen)
        DeleteRoleTable = ttk.Treeview(DeleteRoleFrame,columns=["Rank"])
        DeleteRoleTable.heading("Rank",text='Rank') 
        print(CGREEN+"Delete role screen initialized"+CEND)
        DeleteRoleTable.heading("#0",text="Role Name")
        XScrollDeleteRole = tkinter.Scrollbar(DeleteRoleFrame,orient=tkinter.HORIZONTAL,command=DeleteRoleTable.xview)
        DeleteRoleTable.configure(xscrollcommand=XScrollDeleteRole.set)
        YScrollDeleteRole = tkinter.Scrollbar(DeleteRoleFrame,orient=tkinter.VERTICAL,command=DeleteRoleTable.yview)
        DeleteRoleTable.configure(yscrollcommand=YScrollDeleteRole.set)
        YScrollDeleteRole.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        XScrollDeleteRole.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        DeleteRoleTable.pack(side=tkinter.TOP,expand='false')
        DeleteRoleFrame.grid(column=1,row=1)
        '''
        Name:- Refresh_DeleteRoleTable
        Purpose:- refresh the delete role table
        Args:- none
        Inputs:- Role database , user database
        Outputs:- Refreshed role table reflecting any changes on role database
        '''
        def Refresh_DeleteRoleTable():
            DeleteRoleTable.delete(*DeleteRoleTable.get_children())
            file = open("roles.csv","r+")
            roleLines = file.readlines()
            file.close()
            file = open("users.csv","r+")
            userLines = file.readlines()
            file.close()
            oRank = 0
            i = 0
            #obtains oRank
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == user:
                    oRole = row[3]
                    k = 0
                    while k<len(roleLines):
                        row2 = roleLines[k].split(',')
                        if len(row2)!=roleLEN:
                            k+=1
                            continue
                        for t in range(len(row2)):row2[t] = row2[t].strip()
                        if row2[0] == oRole:
                            oRank = int(row2[1])
                            break
                        k+=1
                    break
                i+=1
            i = 0
            toIns = []
            #append to table if the role can be modified and is below the role rank
            while i<len(roleLines):
                row = roleLines[i].split(',')
                if len(row)!=roleLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                k = 0
                tempRole = row[0]
                tempRank = row[1]
                if oRank>=int(tempRank):
                    i+=1
                    continue
                uCount = 0
                while k<len(userLines):
                    row2 = userLines[k].split(',')
                    if len(row2)!=userLEN:
                        k+=1
                        continue
                    for t in range(len(row2)):row2[t] = row2[t].strip()
                    if row2[3] == tempRole:
                        uCount+=1
                    k+=1
                if uCount > 0:
                    i+=1
                    continue
                print(CGREEN+f"Role detected that can be deleted! Name:{tempRole}"+CEND)
                toIns.append((tempRole,tempRank))
                i+=1
            i = 0
            listOfRanks = []
            while i<len(toIns):
                listOfRanks.append(int(toIns[i][1]))
                i+=1
            listOfRanks = list(set(listOfRanks))
            listOfRanks = QuickieSort(listOfRanks)
            i = 0
            while i<len(listOfRanks):
                selectedRank = str(listOfRanks[i])
                k = 0
                while k<len(toIns):
                    if toIns[k][1] == selectedRank:
                        DeleteRoleTable.insert("",tkinter.END,text=toIns[k][0],values=[toIns[k][1]])
                    k+=1
                i+=1
        Refresh_DeleteRoleTable()
        tkinter.Button(DeleteRoleScreen,text="Help I Cant Find A Role",bd=0,fg='purple',command=lambda:messagebox.showinfo("Info","The role must have no members under it in order for it to be shown here. Go to Edit User and change the role of those users to a different role. \nIf it still doesnot show up , your role rank may not be high enough to modify that role.")).grid(column=2,row=1)
        '''
        Name:-SearchDeleteRole
        Purpose:- Provides a form to search the delete roles table
        Args:- none
        Inputs:- None
        Outputs:- Screen with a form to search delete roles table
        '''
        def SearchDeleteRole():
            global SearchDeleteRoleScreen
            if CheckOpen("Search Delete Role Screen"):return False
            SearchDeleteRoleScreen = tkinter.Toplevel(loginScreen)
            SearchDeleteRoleScreen.title("Search Delete Role Screen")
            tkinter.Label(SearchDeleteRoleScreen,text="Fill the form",fg='blue').grid(column=1,row=0)
            tkinter.Label(SearchDeleteRoleScreen,text="Search What:").grid(column=0,row=1)
            SearchWhatEntry = tkinter.Entry(SearchDeleteRoleScreen,width=23)
            SearchWhatEntry.grid(column=1,row=1)
            tkinter.Label(SearchDeleteRoleScreen,text="Search How:").grid(column=0,row=2)
            SearchHowCombo = ttk.Combobox(SearchDeleteRoleScreen,values=["Linear","Binary"],state='readonly')
            SearchHowCombo.set("Linear")
            print(CGREEN+"Search screen initialized"+CEND)
            SearchHowCombo.grid(column=1,row=2)
            '''
            Name:- SearchDeleteRoleConfirm
            Purpose:- uses the correct algorithm and form data to search the delete roles table
            Args:- none
            Inputs:- Table data , search what(What to look for) , search how(binary/linear)
            '''
            def SearchDeleteRoleConfirm():
                SearchWhat = SearchWhatEntry.get()
                SearchHow = SearchHowCombo.get()
                if SearchWhat == "" or SearchHow == "":
                    print(CRED+"Missing data"+CEND)
                    messagebox.showerror("Error","Fill the form")
                    return False
                existingRows = DeleteRoleTable.get_children()
                if SearchHow == "Linear":
                    #executes linear search for role
                    i = 0
                    while i<len(existingRows):
                        if DeleteRoleTable.item(existingRows[i])['text'] == SearchWhat:
                            print(CGREEN+"Role found"+CEND)
                            DeleteRoleTable.selection_set(existingRows[i])
                            DeleteRoleTable.focus(existingRows[i])
                            messagebox.showinfo("Success","Item highlighted in the table")
                            return False
                        i+=1
                    print(CRED+"Missing item"+CEND)
                    messagebox.showerror("Error","Unable to find item")
                    return False
                else:
                    newExistingRows = []
                    for t in existingRows:newExistingRows.append(DeleteRoleTable.item(t)['text'])
                    newExistingRows = QuickieSort(newExistingRows)
                    if binarySearchAppr(newExistingRows,0,len(newExistingRows)-1,SearchWhat):
                        #executes binary search then , highlights item
                        i = 0
                        while i<len(existingRows):
                            if DeleteRoleTable.item(existingRows[i])['text'] == SearchWhat:
                                print(CGREEN+"Item found"+CEND)
                                DeleteRoleTable.selection_set(existingRows[i])
                                DeleteRoleTable.focus(existingRows[i])
                                messagebox.showinfo("Success","Item highlighted in the table")
                                return False
                            i+=1
                    else:
                        print(CRED+"Item not found"+CEND)
                        messagebox.showerror("Error","Unable to find item")
                        return False
            tkinter.Button(SearchDeleteRoleScreen,text="Search..",fg='green',command=SearchDeleteRoleConfirm,bd=0).grid(column=1,row=3)
        tkinter.Button(DeleteRoleScreen,text="Search..",fg='blue',command=SearchDeleteRole,bd=0).grid(column=0,row=2)
        '''
        Name:- SortDeleteRole
        Purpose:- Sort the delete role table using quick sort
        Args:- none
        Inputs:- table data
        Outputs:- Sorted table data'''
        def SortDeleteRole():
            existingRows = DeleteRoleTable.get_children()
            newExistingRows = []
            toIns = []
            for t in existingRows:newExistingRows.append(DeleteRoleTable.item(t)['text'])
            newExistingRows= QuickieSort(newExistingRows)
            #grabs the data
            for item in newExistingRows:
                for old in existingRows:
                    if DeleteRoleTable.item(old)['text'] == item:
                        toIns.append((item,DeleteRoleTable.item(old)['values']))
            i = 0
            DeleteRoleTable.delete(*DeleteRoleTable.get_children())
            #inserts the sorted data
            while i<len(toIns):
                text,values = toIns[i]
                DeleteRoleTable.insert("",tkinter.END,text=text,values=values)
                i+=1
            print(CGREEN+"Sorted"+CEND)
        tkinter.Button(DeleteRoleScreen,text="Sort..",fg='blue',command=SortDeleteRole,bd=0).grid(column=2,row=2)
        '''
        Name:- Confirm_DeleteRole
        Purpose:- Delete the selected role
        Args:- None
        Inputs:- selected role , role database
        Outputs:- deleted role or error
        '''
        def Confirm_DeleteRole(event):
            try:
                givenRoleName = DeleteRoleTable.item(DeleteRoleTable.focus())['text']
                DeleteRoleTable.item(DeleteRoleTable.focus())['values'][0]
            except:
                return False
            if not messagebox.askyesno("Confirm","Do you want to delete this role(this action cannot be revoked)"):
                return False
            file = open("roles.csv","r+")
            roleLines = file.readlines()
            file.close()
            i = 0
            newRLines = []
            while i<len(roleLines):
                row = roleLines[i].split(',')
                if len(row)!=roleLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == givenRoleName:
                    print(CGREEN+"Role wiped"+CEND)
                    i+=1
                    continue
                newRLines.append(roleLines[i])
                i+=1
            file = open("roles.csv","w+")
            file.writelines(newRLines)
            file.close()
            messagebox.showinfo("Success","Role Deleted")
            Refresh_DeleteRoleTable()
        DeleteRoleTable.bind("<Double-1>",Confirm_DeleteRole)
        '''
        Name:- CloseDeleteRoleScreen
        Purpose:- Close the children of delete role screen
        args:- none
        Inputs:- None
        Outputs:- close commands for the children
        '''
        def CloseDeleteRoleScreen():
            print(CRED+"Close command detected"+CEND)
            global SearchDeleteRoleScreen
            try:
                SearchDeleteRoleScreen.destroy()
            except:
                pass
            DeleteRoleScreen.destroy()
        DeleteRoleScreen.protocol("WM_DELETE_WINDOW",CloseDeleteRoleScreen)
        
        tkinter.Button(DeleteRoleScreen,text="Exit..",fg='red',command=CloseDeleteRoleScreen,bd=0).grid(column=1,row=2)
    tkinter.Button(ManageRolesScreen,text="Delete Roles",fg='blue',bd=0,command=DeleteRole).grid(column=1,row=3)
    tkinter.Button(ManageRolesScreen,text="Help",fg='purple',bd=0,command=lambda:messagebox.showinfo("Info","Roles are required to set up permissions and limit what certain users can do. When roles are setup , you can setup users for those roles")).grid(column=1,row=4)
    '''
    Name:- CloseManageRolesScreen
    Purpose:- Close the Manage Roles screen children
    Args:- None
    Inputs:- None
    Outputs:- close commands for all children
    '''
    def CloseManageRolesScreen():
        print(CRED+"Close command detected"+CEND)
        global CreateRoleScreen
        global CloseEditRoleScreen
        global CloseDeleteRoleScreen
        try:
            CreateRoleScreen.destroy()
        except:
            pass
        try:
            CloseEditRoleScreen()
        except:
            pass
        try:
            CloseDeleteRoleScreen()
        except:
            pass
        ManageRolesScreen.destroy()
    ManageRolesScreen.protocol("WM_DELETE_WINDOW",CloseManageRolesScreen)
    tkinter.Button(ManageRolesScreen,text="Exit",fg='red',bd=0,command=CloseManageRolesScreen).grid(column=1,row=5)
'''
Name:- Misc
Purpose:- open sub portal for more functions
Args:- user(current user who is logged in)
Inputs:- user
Outputs:- portal screen with more options
'''
def Misc(user):
    if CheckOpen("Misc Portal"):return False
    MiscPortal = tkinter.Toplevel(loginScreen)
    MiscPortal.title("Misc Portal")
    MiscPortal.resizable(0,0)
    tkinter.Label(MiscPortal,text="Misc Portal").grid(column=1,row=0)
    print(CGREEN+"Initialised Misc Portal"+CEND)
    '''
    Name:- Scheduler
    Purpose:- Display the daily schedule of classes
    Args:- None
    Inputs:- subject data , time data , current PC time
    Outputs:- screen with a scheduler window
    '''
    def Scheduler():
        global SchedulerScreen
        if CheckOpen("Scheduler Screen"):return False
        SchedulerScreen = tkinter.Toplevel(loginScreen)
        SchedulerScreen.title("Scheduler Screen")
        SchedulerScreen.resizable(0,0)
        print(CGREEN+"Initialised scheduler window"+CEND)
        global globalViewYear
        global globalViewMonth
        global globalViewDay
        global globalViewWeekday
        globalViewYear = time.strftime("%Y",localtime())
        globalViewMonth = time.strftime("%m",localtime())
        globalViewDay = time.strftime("%d",localtime())
        globalViewWeekday = time.strftime("%A",localtime())
        tkinter.Label(SchedulerScreen,text="Use the arrows to navigate days.").grid(column=1,row=0)
        SchedulerFrame = tkinter.Frame(SchedulerScreen)
        SchedulerFrame.grid(column=1,row=1)
        SchedulerTable = ttk.Treeview(SchedulerFrame,columns=["Class","Time From","Time To"])
        SchedulerTable.heading("#0",text="Subject")
        SchedulerTable.heading("Class",text="Class")
        SchedulerTable.heading("Time From",text="Time From")
        SchedulerTable.heading("Time To",text="Time To")
        XScrollScheduler = tkinter.Scrollbar(SchedulerFrame,command=SchedulerTable.xview,orient=tkinter.HORIZONTAL)
        SchedulerTable.configure(xscrollcommand=XScrollScheduler.set)
        YScrollScheduler = tkinter.Scrollbar(SchedulerFrame,command=SchedulerTable.yview,orient=tkinter.VERTICAL)
        SchedulerTable.configure(yscrollcommand=YScrollScheduler.set)
        YScrollScheduler.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        XScrollScheduler.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        SchedulerTable.pack(side=tkinter.TOP,expand='false')
        DateShownLbl=tkinter.Label(SchedulerScreen,text="Date Shown:",fg='purple')
        DateShownLbl.grid(column=1,row=2)
        '''
        Name : ShowDate
        Purpose: fill the scheduler table with scheduler data
        Args: year(year to view) , month(month to view) , day (day to view) , weekday(current weekday)
        Inputs: time data , subject data , user data
        Outputs: fill the SchedulerTable with the subjects that are scheduled for the passed date
        '''
        def ShowDate(year,month,day,weekday):
            print(CGREEN+f"Showing date for {year} , {month} , {day} , {weekday}"+CEND)
            SchedulerTable.delete(*SchedulerTable.get_children())
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
            file = open("users.csv","r+")
            userLines = file.readlines()
            file.close()
            toIns = []
            curTime =0
            year = int(year)
            month = int(month)
            day = int(day)
            monthsWith31 = [1,3,5,7,8,10,12]
            i = 0
            while i<year:
                if i%4==0:
                    curTime+=366*24*60
                else:
                    curTime+=365*24*60
                i+=1
            i = 1
            while i<month:
                if i in monthsWith31:
                    curTime+=31
                elif i == 2:
                    if year%4 == 0:
                        curTime+=29
                    else:
                        curTime+=28
                else:
                    curTime+=30
                i+=1
            curTime+=day
            i = 0
            selectedEnrolements = []
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == user:
                    selectedEnrolements = row[2].split('.')
                    break
                i+=1
            i = 0
            while i<len(subjectLines):
                row = subjectLines[i].split(',')
                if len(row)!=subjectLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                selectedSubject = row[0]
                selectedClass = row[1]
                k = 0
                n = True
                while k<len(selectedEnrolements):
                    if selectedEnrolements[k] == selectedSubject and selectedEnrolements[k+1] == selectedClass:
                        #looks for whether the user is enrolled to the subject or not
                        n=False
                        break
                    k+=1
                if n:
                    i+=1
                    continue
                timeData = row[3].split('.')
                fromD,fromM,fromY = timeData[0].split(':')
                toD,toM,toY = timeData[1].split(':')
                fromH,fromMi = timeData[2].split(':')
                toH,toMi = timeData[3].split(':')
                givenTime = 0
                RState = timeData[4]
                fromD = int(fromD)
                fromM = int(fromM)
                fromY = int(fromY)
                toD = int(toD)
                toM = int(toM)
                toY = int(toY)
                if not(RState == weekday or RState == "Everyday"):
                    i+=1
                    continue
                k = 0
                givenTime=0
                while k<toY:
                    if k%4 == 0:
                        givenTime+=366*24*60
                    else:
                        givenTime+=365*24*60
                    k+=1
                k = 1
                while k<toM:
                    if k in monthsWith31:
                        givenTime+=31
                    elif k == 2:
                        if toY%4==0:
                            givenTime+=29
                        else:
                            givenTime+=28
                    else:
                        givenTime+=30
                    k+=1
                givenTime+=toD
                givenTimeF = 0
                k = 0
                while k<fromY:
                    if k%4 == 0:
                        givenTimeF+=366*24*60
                    else:
                        givenTimeF+=365*24*60
                    k+=1
                k = 1
                while k<fromM:
                    if k in monthsWith31:
                        givenTimeF+=31
                    elif k == 2:
                        if fromY%4==0:
                            givenTimeF+=29
                        else:
                            givenTimeF+=28
                    else:
                        givenTimeF+=30
                    k+=1
                givenTimeF+=fromD
                #checks whether the current time is in range of the subject time and if so , insert to insertion array
                if curTime in range(givenTimeF,givenTime+1):
                    toIns.append((selectedSubject,selectedClass,fromH,fromMi,toH,toMi))
                i+=1
            i = 0
            #inserts the data
            while i<len(toIns):
                selectedSubject,selectedClass,fromH,fromMi,toH,toMi = toIns[i]
                #time sorting cannot be done due to time limitations
                toTime = str(toH)+":"+str(toMi)
                fromTime = str(fromH)+":"+str(fromMi)
                print(CGREEN+f"Detected class,{selectedSubject}:{selectedClass} from {fromTime} to {toTime}"+CEND)
                SchedulerTable.insert("",tkinter.END,text=selectedSubject,values=[selectedClass,fromTime,toTime])
                i+=1
            DateShownLbl.config(text="Date Shown:"+str(year)+"/"+str(month)+"/"+str(day))
        ShowDate(globalViewYear,globalViewMonth,globalViewDay,globalViewWeekday)
        '''
        Name:Go Back Day
        Purpose:Go back one day in the global dates
        Args: none
        Inputs: global date
        Outputs: show date table showing the date of the day before the current view date
        '''
        def GoBackDay():
            global globalViewDay
            global globalViewMonth
            global globalViewYear
            global globalViewWeekday
            globalViewDay=int(globalViewDay)
            globalViewMonth = int(globalViewMonth)
            globalViewYear = int(globalViewYear)
            weekDayList = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            monthsWith31 = [1,3,5,7,8,10,12]
            if globalViewDay-1 == 0:
                if globalViewMonth-1 == 0:
                    globalViewYear-=1
                    globalViewMonth=12
                    globalViewDay=31
                    try:
                        globalViewWeekday = weekDayList[weekDayList.index(globalViewWeekday)-1]
                    except:
                        globalViewWeekday = "Sunday"
                else:
                    globalViewMonth-=1
                    if globalViewMonth in monthsWith31:
                        globalViewDay=31
                    elif globalViewMonth == 2:
                        if globalViewYear%4==0:
                            globalViewDay=29
                        else:
                            globalViewDay=28
                    else:
                        globalViewDay=30
                    try:
                        globalViewWeekday = weekDayList[weekDayList.index(globalViewWeekday)-1]
                    except:
                        globalViewWeekday = "Sunday"
            else:
                globalViewDay-=1
                try:
                    globalViewWeekday = weekDayList[weekDayList.index(globalViewWeekday)-1]
                except:
                    globalViewWeekday = "Sunday"
            ShowDate(globalViewYear,globalViewMonth,globalViewDay,globalViewWeekday)
        '''
        Name: Go Forward Day
        Purpose: To go forward one more day
        Args: None
        Inputs: global date
        Outputs: show date table showing the date of the day after the current view date
        '''
        def GoForwardDay():
            global globalViewDay,globalViewMonth,globalViewYear,globalViewWeekday
            monthsWith31 = [1,3,5,7,8,10,12]
            globalViewDay = int(globalViewDay)
            globalViewMonth = int(globalViewMonth)
            globalViewYear = int(globalViewYear)
            dM = 0
            #dM is date Max
            weekDayList = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            if globalViewMonth in monthsWith31:
                dM = 31
            elif globalViewMonth == 2:
                if globalViewYear%4 == 0:
                    dM=29
                else:
                    dM=28
            else:
                dM = 30
            if globalViewDay+1>dM:
                if globalViewMonth+1>12:
                    globalViewYear+=1
                    globalViewMonth=1
                    globalViewDay=1
                    try:
                        globalViewWeekday = weekDayList[weekDayList.index(globalViewWeekday)+1]
                    except:
                        globalViewWeekday = "Monday"
                else:
                    globalViewMonth+=1
                    globalViewDay=1
                    try:
                        globalViewWeekday = weekDayList[weekDayList.index(globalViewWeekday)+1]
                    except:
                        globalViewWeekday = "Monday"
            else:
                globalViewDay+=1
                try:
                    globalViewWeekday = weekDayList[weekDayList.index(globalViewWeekday)+1]
                except:
                    globalViewWeekday = "Monday"
            ShowDate(globalViewYear,globalViewMonth,globalViewDay,globalViewWeekday)
        tkinter.Button(SchedulerScreen,text="⏪",command=GoBackDay,bd=0,fg='green').grid(column=0,row=2)
        tkinter.Button(SchedulerScreen,text="⏩",bd=0,command=GoForwardDay,fg='green').grid(column=2,row=2)
    tkinter.Button(MiscPortal,text="My Schedule",fg='green',bd=0,command=Scheduler).grid(column=0,row=1)
    '''
    Name:- Profiler
    Purpose:- View the current profile information of the user , change password and email eg
    Args:- None
    Inputs - current user who is logged in , user database
    Outputs:- Form with user data
    '''
    def Profiler():
        global ProfilerScreen
        if CheckOpen("My Profile"):return False
        ProfilerScreen = tkinter.Toplevel(loginScreen)
        ProfilerScreen.title("My Profile")
        ProfilerScreen.resizable(0,0)
        print(CGREEN+"Profiler screen loaded"+CEND)
        tkinter.Label(ProfilerScreen,text="Your Account",fg='blue').grid(column=1,row=0)
        tkinter.Label(ProfilerScreen,text="Username:").grid(column=0,row=1)
        UserNameLbl = tkinter.Label(ProfilerScreen)
        UserNameLbl.grid(column=1,row=1)
        tkinter.Label(ProfilerScreen,text="Password:").grid(column=0,row=2)
        PassEntry=tkinter.Entry(ProfilerScreen)
        PassEntry.grid(column=1,row=2)
        tkinter.Label(ProfilerScreen,text="Role:").grid(column=0,row=3)
        RoleLbl = tkinter.Label(ProfilerScreen)
        RoleLbl.grid(column=1,row=3)
        tkinter.Label(ProfilerScreen,text="Role Rank:").grid(column=0,row=4)
        RoleRank = tkinter.Label(ProfilerScreen)
        RoleRank.grid(column=1,row=4)
        tkinter.Label(ProfilerScreen,text="Email:").grid(column=0,row=5)
        EmailEntry = tkinter.Entry(ProfilerScreen)
        EmailEntry.grid(column=1,row=5)
        '''
        name : refreshProfiler
        purpose : To refresh the profiler page to reflect the most recent data of the logged in user
        args: none
        input: '''
        def refreshProfiler():
            print(CGREEN+"Profiler refreshed"+CEND)
            EmailEntry.delete(0,tkinter.END)
            PassEntry.delete(0,tkinter.END)
            if user == "admin":
                UserNameLbl.config(text="admin")
                PassEntry.config(state='disabled')
                RoleLbl.config(text="Maximum Permissions")
                RoleRank.config(text="0")
                return False
            file = open('users.csv',"r+")
            userLines=file.readlines()
            file.close()
            i = 0
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == user:
                    UserNameLbl.config(text=user)
                    PassEntry.insert(0,row[1])
                    RoleLbl.config(text=row[3])
                    EmailEntry.insert(0,row[4])
                    file = open("roles.csv","r+")
                    roleLines = file.readlines()
                    file.close()
                    k = 0
                    while k<len(roleLines):
                        row2 = roleLines[k].split(',')
                        if len(row2) != roleLEN:
                            k+=1
                            continue
                        for t in range(len(row2)):row2[t] = row2[t].strip()
                        if row2[0] == row[3]:
                            RoleRank.config(text=row2[1])
                            return False
                        k+=1
                    break
                i+=1
        refreshProfiler()
        '''
        name:- saveChanges
        purpose:- save any changes that have occured in the form to the userdatabase
        args:- none
        inputs:- User database , given password in form , given email in form
        Outputs:- new data reflected in database or error thrown
        '''
        def saveChanges():
            if user == 'admin':
                messagebox.showerror("Error","admin cannot change settings")
                return False
            try:
                givenpass = PassEntry.get()
                givenEmail = EmailEntry.get()
            except:
                return False
            if givenpass == "" or not(set(givenpass).issubset(approved_text)):
                messagebox.showerror("Error","Avoid spaces , use camel case in your password")
                return False
            file = open("users.csv","r+")
            userLines= file.readlines()
            file.close()
            i = 0
            newULines = []
            #sends email with new user configuration to a user with a email , other wise , saves changes to database
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == user:
                    try:
                        if givenEmail != "":
                            print(CGREEN+"Email detected"+CEND)
                            if connected_ssid == b"gwsc.vic.edu.au":
                                raise TypeError
                            server = smtplib.SMTP("smtp.office365.com",587)
                            server.starttls()
                            server.login("proofofconcept69420@outlook.com","somerandompassword69420")
                            msg = MIMEMultipart()
                            msg['From'] = "proofofconcept69420@outlook.com"
                            msg['To'] = givenEmail
                            msg['Subject'] = "New Email successfully bound to your new account "+row[0]
                            msg2 = "New Email bound succesfully. Your account mayhave changed, please review account changes.\nUsername "+row[0]+"\nPassword:"+givenpass
                            msg.attach(MIMEText(msg2,'plain'))
                            server.send_message(msg,"proofofconcept69420@outlook.com",givenEmail)
                            time.sleep(15)
                            server.quit()
                            server = poplib.POP3_SSL("outlook.office365.com",995)
                            server.user("proofofconcept69420@outlook.com")
                            server.pass_("somerandompassword69420")
                            resp,mails,octets = server.list()
                            del resp,octets
                            index = len(mails)
                            resp,lines,octets = server.retr(index)
                            msg_content = b'\r\n'.join(lines).decode('utf-8')
                            msg = Parser().parsestr(msg_content)
                            EmailSubject = msg.get('Subject').strip()
                            if "Undeliverable: New Email successfully bound to your new account "+row[0] == EmailSubject:
                                print(CRED+"Invalid Email"+CEND)
                                messagebox.showerror("Error","The email is invalid")
                                server.dele(index)
                                server.quit()
                                return False
                            server.quit()
                            print(CGREEN+"Sent email to new bind"+CEND)
                            if row[4]!="":
                                if connected_ssid == b"gwsc.vic.edu.au":
                                    raise TypeError
                                server = smtplib.SMTP("smtp.office365.com",587)
                                server.starttls()
                                server.login("proofofconcept69420@outlook.com","somerandompassword69420")
                                msg = MIMEMultipart()
                                msg['From'] = "proofofconcept69420@outlook.com"
                                msg['To'] = row[4]
                                msg['Subject'] = "Email Unbound "+row[0]
                                msg2 = "This Email has been unbound from your account. Your account mayhave changed, please review account changes.\nUsername "+row[0]+"\nPassword:"+givenpass+"\nNew Email:"+givenEmail
                                msg.attach(MIMEText(msg2,'plain'))
                                server.send_message(msg,"proofofconcept69420@outlook.com",row[4])
                                server.quit()
                                print(CGREEN+"Sent email for old email unbind"+CEND)
                    except:
                        print(CRED+"Network Error"+CEND)
                        messagebox.showerror("Error","Cannot Access the internet. Unable to verify emails. Assuming old email")
                        givenEmail = row[4]
                    newULines.append(row[0]+","+givenpass+","+row[2]+","+row[3]+","+givenEmail+"\n")
                else:
                    newULines.append(userLines[i])
                i+=1
            file = open('users.csv',"w+")
            file.writelines(newULines)
            file.close()
            messagebox.showinfo("Success","Changes saved")
            print(CGREEN+"Changes saved"+CEND)
            refreshProfiler()
        tkinter.Button(ProfilerScreen,text="Save Changes",command=saveChanges,bd=0,fg='green').grid(column=1,row=6)
        tkinter.Button(ProfilerScreen,text="Close",fg='red',command=ProfilerScreen.destroy,bd=0).grid(column=1,row=7)
    ProfilerButton = tkinter.Button(MiscPortal,text="My Profile",fg='green',bd=0,command=Profiler)
    if user == "admin":
        print(CRED+"Admin user detected, profiler disabled"+CEND)
        ProfilerButton['state'] = 'disabled'
    ProfilerButton.grid(column=1,row=1)
    '''
    name:- Exporter
    purpose:- export data in a human readable format for data and statistical purposes, also provides option to create a encrypted backup
    args:- none
    inputs:- user database , waitlist database , role database , subject database
    outputs:- encrypted and/or human readable versions of the databases
    '''
    def Exporter():
        if not messagebox.askyesno("Confirm","Do you want to Export data? Any data theft is not a responsibility of the developer"):return False
        FileVerifs()
        file = open("users.csv","r+")
        userLines = file.readlines()
        file.close()
        #writes headers
        newUserLines = ["Username,Role,Contact Info\n"]
        i = 0
        #encrypts user data using ord key manipulation
        while i<len(userLines):
            row = userLines[i].split(',')
            if len(row)!=userLEN:
                i+=1
                continue
            for t in range(len(row)):row[t] = row[t].strip()
            #inserts relevant data and omits sensitive info
            newUserLines.append(row[0]+","+row[3]+","+row[4]+"\n")
            i+=1
        file = open("users[HUMAN READABLE].csv","w+")
        file.writelines(newUserLines)
        file.close()
        print(CGREEN+f"{i} records have been processed for UData"+CEND)
        file = open("roles.csv","r+")
        roleLines = file.readlines()
        file.close()
        i = 0
        #initialize headers
        newRoleLines = ["Role Name,Role Ranking,Can Bind To Class?,Can Manage Roles?,Can Add Users,Can Delete Users,Can Join Restricted,Can Manage Class\n"]
        #encrypts role data using ord key manipulation
        while i<len(roleLines):
            row = roleLines[i].split(',')
            if len(row)!=roleLEN:
                i+=1
                continue
            for t in range(len(row)):row[t] = row[t].strip()
            roleName = row[0]
            roleRank = row[1]
            subP = ""
            tempP = row[2].split('.')
            k = 0
            while k<len(tempP):
                if tempP[k] == "1":
                    subP=subP+"True"+","
                elif tempP[k] == "0":
                    subP = subP+"False"+","
                else:
                    pass
                k+=1
            idZ = len(subP)-1
            subP = ''.join([subP[i] for i in range(len(subP)) if i!=idZ])
            subP = str(subP)
            #appends relevant data to file
            newRoleLines.append(roleName+","+roleRank+","+subP+'\n')
            i+=1
        file = open("roles[HUMAN READABLE].csv","w+")
        file.writelines(newRoleLines)
        file.close()
        print(CGREEN+f"{i} records have been processed for RData"+CEND)
        file = open("waitlist.csv","r+")
        waitlistLines = file.readlines()
        file.close()
        #initialize headers
        newWaitlistLines = ["Username,Subject,Class\n"]
        i = 0
        #encrypts waitlist data using ord key manipulation
        while i<len(waitlistLines):
            row = waitlistLines[i].split(',')
            if len(row)!=waitlistLEN:
                i+=1
                continue
            for t in range(len(row)):row[t] = row[t].strip()
            #appends relevant data for the columns
            newWaitlistLines.append(row[0]+","+row[1]+","+row[2]+"\n")
            i+=1
        file = open("waitlist[HUMAN READABLE].csv","w+")
        file.writelines(newWaitlistLines)
        file.close()
        print(CGREEN+f"{i} records have been processed for WData"+CEND)
        file = open("subjects.csv","r+")
        subjectLines=file.readlines()
        file.close()
        i = 0
        newSubjectLines = ["Subject Name,Class Name,Maximum Capacity,From DD/MM/YYYY,To DD/MM/YYYY,From Hour:Minutes,To Hour:Minutes,Repeat Day,Restricted?,Bound User\n"]
        #encrypts subject data using ord key manipulation
        while i<len(subjectLines):
            row = subjectLines[i].split(',')
            if len(row)!=subjectLEN:
                i+=1
                continue
            for t in range(len(row)):row[t] = row[t].strip()
            timeData = row[3].split('.')
            fromY = timeData[0].split(':')
            fromYS = ""
            k = 0
            while k<len(fromY):
                if k == len(fromY)-1:
                    fromYS = fromYS+fromY[k]
                else:
                    fromYS = fromYS+fromY[k]+"/"
                k+=1
            toY = timeData[1].split(':')
            toYS = ""
            k = 0
            while k<len(toY):
                if k == len(toY)-1:
                    toYS = toYS+toY[k]
                else:
                    toYS = toYS+toY[k]+"/"
                k+=1
            fromHM = timeData[2]
            toHM = timeData[3]
            RDay = timeData[4]
            if row[4] == "0":
                RMode = "False"
            else:
                RMode = "True"
            BUser = row[5]
            #writes subject data relevant to the headers
            newSubjectLines.append(row[0]+","+row[1]+","+row[2]+","+fromYS+","+toYS+","+fromHM+","+toHM+","+RDay+","+RMode+","+BUser+"\n")
            i+=1
        file = open("subjects[HUMAN READABLE].csv","w+")
        file.writelines(newSubjectLines)
        file.close()
        print(CGREEN+f"{i} records have been processed for SData"+CEND)
        #asks user whether they want to create a encrypted back up of the machine readable data(contains sensitive info)
        if messagebox.askyesno("Confirm","Do you want to encrypt a copy of machine readable data for backup as well?"):
            file = open("users.csv","r+")
            userLines = file.readlines()
            file.close()
            newULines = []
            i = 0
            while i<len(userLines):
                try:
                    p=0
                    encryptedtxt=""
                    key=1
                    plaintext=userLines[i]
                    temp=""
                    plaintext=str(plaintext)
                    for p in range (0,len(plaintext)):
                        temp = ord(plaintext[p])-key
                        temp=chr(temp)
                        encryptedtxt=encryptedtxt+temp
                    newULines.append(encryptedtxt)
                    i+=1
                except:
                    print(CRED+"Encryption failed for UData. Unicode Error?"+CEND)
                    messagebox.showerror("Error","Encryption Error. Exited to prevent data loss")
                    return False
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
            print(CGREEN+f"{i} records have been processed for UData"+CEND)
            i = 0
            newSLines = []
            while i<len(subjectLines):
                try:
                    p=0
                    encryptedtxt=""
                    key=1
                    plaintext=subjectLines[i]
                    temp=""
                    plaintext=str(plaintext)
                    for p in range (0,len(plaintext)):
                        temp = ord(plaintext[p])-key
                        temp=chr(temp)
                        encryptedtxt=encryptedtxt+temp
                    newSLines.append(encryptedtxt)
                    i+=1
                except:
                    print(CRED+"Encryption failed for SData. Unicode Error?"+CEND)
                    messagebox.showerror("Error","Encryption Error. Exited to prevent data loss")
                    return False
            file = open("waitlist.csv","r+")
            waitlistLines = file.readlines()
            file.close()
            print(CGREEN+f"{i} records have been processed for SData"+CEND)
            i = 0
            newWLines = []
            while i<len(waitlistLines):
                try:
                    p=0
                    encryptedtxt=""
                    key=1
                    plaintext=waitlistLines[i]
                    temp=""
                    plaintext=str(plaintext)
                    for p in range (0,len(plaintext)):
                        temp = ord(plaintext[p])-key
                        temp=chr(temp)
                        encryptedtxt=encryptedtxt+temp
                    newWLines.append(encryptedtxt)
                    i+=1                
                except:
                    print(CRED+"Encryption failed for WData. Unicode Error?"+CEND)
                    messagebox.showerror("Error","Encryption Error. Exited to prevent data loss")
                    return False
            file = open("roles.csv","r+")
            roleLines = file.readlines()
            file.close()
            print(CGREEN+f"{i} records have been processed for WData"+CEND)
            i = 0
            newRLines = []
            while i<len(roleLines):
                try:
                    p=0
                    encryptedtxt=""
                    key=1
                    plaintext=roleLines[i]
                    temp=""
                    plaintext=str(plaintext)
                    for p in range (0,len(plaintext)):
                        temp = ord(plaintext[p])-key
                        temp=chr(temp)
                        encryptedtxt=encryptedtxt+temp
                    newRLines.append(encryptedtxt)
                    i+=1
                except:
                    print(CRED+"Encryption failed for RData. Unicode Error?"+CEND)
                    messagebox.showerror("Error","Encryption Error. Exited to prevent data loss")
                    return False
            print(CGREEN+f"{i} records have been processed for RData"+CEND)
            file = open("users[ENCRYPTED].csv","w+")
            file.writelines(newULines)
            file.close()
            file = open("roles[ENCRYPTED].csv","w+")
            file.writelines(newRLines)
            file.close()
            file = open("waitlist[ENCRYPTED].csv","w+")
            file.writelines(newWLines)
            file.close()
            file = open("subjects[ENCRYPTED].csv","w+")
            file.writelines(newSLines)
            file.close()
        messagebox.showwarning("Data Exported","It is recommended that you dispose of these files after use.")
        os.system('start .')
        print(CGREEN+"Successfully exported"+CEND)
    ExportDataB=tkinter.Button(MiscPortal,text="Export Data",fg='green',bd=0,command=Exporter)
    ExportDataB.grid(column=2,row=1)
    #the user should have every single permission to export data , as it is a massive secuirity risk
    if not(AuthMod(user,1) and AuthMod(user,2) and AuthMod(user,3) and AuthMod(user,4) and AuthMod(user,5) and AuthMod(user,6)):
        print(CRED+"Insufficient permissions for exporting"+CEND)
        ExportDataB.config(state='disabled')
    '''
    name:-MyClasses
    purpose:- Displays a table with information about classes that a user is enrolled to
    args:- none
    inputs:-subject data , current logged in user , waitlist data
    Outputs:- A table with classes that users are enrolled/waitlisted to
    '''
    def MyClasses():
        global CloseMyEnrolements
        global Refresh_JoinClassTree
        if CheckOpen("My Classes"):return False
        MyClassesScreen = tkinter.Toplevel(loginScreen)
        MyClassesScreen.title("My Classes")
        MyClassesScreen.resizable(0,0)
        print(CGREEN+"My classes initialised"+CEND)
        tkinter.Label(MyClassesScreen,text="My Enrolements(Double click to deenrol)").grid(column=1,row=0)
        MyEFrame = tkinter.Frame(MyClassesScreen)
        MyEFrame.grid(column=1,row=1)
        MyEnrolementsTable = ttk.Treeview(MyEFrame,columns=["Classes","Type"])
        MyEnrolementsTable.heading("Classes",text="Classes")
        MyEnrolementsTable.heading("Type",text="Type")
        MyEnrolementsTable.heading("#0",text="Subjects")
        YScrollMyE = tkinter.Scrollbar(MyEFrame,command=MyEnrolementsTable.yview,orient=tkinter.VERTICAL)
        MyEnrolementsTable.configure(yscrollcommand=YScrollMyE.set)
        XScrollMyE = tkinter.Scrollbar(MyEFrame,command=MyEnrolementsTable.xview,orient=tkinter.HORIZONTAL)
        MyEnrolementsTable.configure(xscrollcommand=XScrollMyE.set)

        YScrollMyE.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        XScrollMyE.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        MyEnrolementsTable.pack(side=tkinter.TOP,expand='false')
        '''
        name:- Refresh_EnrolementsTable
        purpose:-refresh the enrolements table
        args:- none
        inputs:- user data , waitlist data , current logged in user
        outputs:- table refreshed to reflect new data from database
        '''
        def Refresh_EnrolementsTable():
            MyEnrolementsTable.delete(*MyEnrolementsTable.get_children())
            file = open("users.csv","r+")
            userLines = file.readlines()
            file.close()
            file = open("waitlist.csv","r+")
            waitlistLines = file.readlines()
            file.close()
            i = 0
            enrolements = []
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == user:
                    enrolements = row[2].split('.')
                    break
                i+=1
            i = 0
            while i<len(enrolements):
                try:
                    MyEnrolementsTable.insert("",tkinter.END,text=enrolements[i],values=[enrolements[i+1],"ENROLLED"])
                    print(CGREEN+f"Enrollment detected {enrolements[i]},{enrolements[i+1]}"+CEND)
                except:
                    break
                i+=2
            i=0
            while i<len(waitlistLines):
                row = waitlistLines[i].split(',')
                if len(row)!=waitlistLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == user:
                    print(CGREEN+f"Waitlist detected {row[1]},{row[2]}"+CEND)
                    MyEnrolementsTable.insert("",tkinter.END,text=row[1],values=[row[2],"WAITLISTED"])
                i+=1
        Refresh_EnrolementsTable()
        '''
        name:-JoinClass
        purpose:- shows a sub window with a table that has the capabilities of enrolling/waitlisting a user to a class
        args:- none
        inputs:- none
        outputs:- table with classes that the user can enrol/waitlist to
        '''
        def JoinClass():
            global JoinClassScreen
            global Refresh_JoinClassTree
            if CheckOpen("Join Class Screen"):return False
            JoinClassScreen = tkinter.Toplevel(loginScreen)
            JoinClassScreen.title("Join Class Screen")
            JoinClassScreen.resizable(0,0)
            print(CGREEN+"Join class initialised"+CEND)
            tkinter.Label(JoinClassScreen,text="Double Click to Enrol/Waitlist to a class").grid(column=1,row=0)
            JoinClassFrame = tkinter.Frame(JoinClassScreen)
            JoinClassFrame.grid(column=1,row=1)
            JoinClassTree = ttk.Treeview(JoinClassFrame,columns=["Class","Teacher","Spots Left","Waitlisted"])
            JoinClassTree.heading("#0",text="Subject")
            JoinClassTree.heading("Class",text="Class")
            JoinClassTree.heading("Teacher",text='Teacher')
            JoinClassTree.heading("Spots Left",text="Spots Left")
            JoinClassTree.heading("Waitlisted",text="Waitlisted")
            
            XJoinTree = tkinter.Scrollbar(JoinClassFrame,command=JoinClassTree.xview,orient=tkinter.HORIZONTAL)
            JoinClassTree.configure(xscrollcommand=XJoinTree.set)
            YJoinTree = tkinter.Scrollbar(JoinClassFrame,command=JoinClassTree.yview,orient=tkinter.VERTICAL)
            JoinClassTree.configure(yscrollcommand=YJoinTree.set)

            YJoinTree.pack(side=tkinter.RIGHT,fill=tkinter.Y)
            XJoinTree.pack(side=tkinter.BOTTOM,fill=tkinter.X)
            JoinClassTree.pack(side=tkinter.TOP,expand='false')
            '''
            name:- Refresh_JoinClassTree
            purpose:- refresh the join class table which shows the possible enrolements
            args:- none
            Inputs:- subject data , user data , waitlist data
            Outputs:- JoinClassTree refreshed
            '''
            def Refresh_JoinClassTree():
                Refresh_EnrolementsTable()
                JoinClassTree.delete(*JoinClassTree.get_children())
                canJoinRestricted= AuthMod(user,5)
                existingEnrolements=MyEnrolementsTable.get_children()
                newExistingEnrolements = []
                for a in range(len(existingEnrolements)):
                    newExistingEnrolements.append((MyEnrolementsTable.item(existingEnrolements[a])['text'],MyEnrolementsTable.item(existingEnrolements[a])['values'][0]))
                existingEnrolements = newExistingEnrolements
                del newExistingEnrolements
                i = 0
                file = open("subjects.csv","r+")
                subjectLines = file.readlines()
                file.close()
                file = open("users.csv","r+")
                userLines = file.readlines()
                file.close()
                file = open("waitlist.csv","r+")
                waitlistLines = file.readlines()
                file.close()
                #inserts the subject if the user is not enrolled/waitlisted to it 
                while i<len(subjectLines):
                    row = subjectLines[i].split(',')
                    if len(row)!=subjectLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    a=False
                    k = 0
                    if row[4] == "1" and canJoinRestricted == False:
                        print(CRED+"Restricted permission missing , class skipped"+CEND)
                        i+=1
                        continue
                    while k<len(existingEnrolements):
                        subject,class_ = existingEnrolements[k]
                        if subject == row[0] and class_ == row[1]:
                            a=True
                        k+=1
                    if a:
                        print(CRED+"Already enrolled class detected, class skipped"+CEND)
                        i+=1
                        continue
                    k = 0
                    countEnrols = 0
                    while k<len(userLines):
                        row2 = userLines[k].split(',')
                        if len(row2)!=userLEN:
                            k+=1
                            continue
                        for t in range(len(row2)):row2[t] = row2[t].strip()
                        tempEnrols = row2[2].split('.')
                        j = 0
                        while j<len(tempEnrols):
                            try:
                                if tempEnrols[j] == row[0] and tempEnrols[j+1] == row[1]:
                                    countEnrols+=1
                                j+=2
                            except:
                                break
                        k+=1
                    k = 0
                    countWaitlists = 0
                    while k<len(waitlistLines):
                        row2 = waitlistLines[k].split(',')
                        if len(row2)!=waitlistLEN:
                            k+=1
                            continue
                        for t in range(len(row2)):row2[t] = row2[t].strip()
                        if row2[1] == row[0] and row2[2] == row[1]:
                            countWaitlists+=1
                        k+=1
                    spotsLeft = str(int(row[2])-countEnrols)
                    JoinClassTree.insert("",tkinter.END,text=row[0],values=[row[1],row[5],spotsLeft,countWaitlists])
                    i+=1
            Refresh_JoinClassTree()
            '''
            name:- Search_JoinClassTree
            purpose:- provides a form to search the join class tree
            args:- none
            inputs:- None
            outputs:- form to search join class tree
            '''
            def Search_JoinClassTree():
                if CheckOpen("Search Screen Join Class"):return False
                SearchScreenJoinClass = tkinter.Toplevel(loginScreen)
                SearchScreenJoinClass.title("Search Screen Join Class")
                SearchScreenJoinClass.resizable(0,0)
                print(CGREEN+"Search screen loaded"+CEND)
                tkinter.Label(SearchScreenJoinClass,text="Enrol").grid(column=1,row=0)
                tkinter.Label(SearchScreenJoinClass,text="Class Name:").grid(column=0,row=1)
                ClassNameEntry = tkinter.Entry(SearchScreenJoinClass,width=23)
                ClassNameEntry.grid(column=1,row=1)
                tkinter.Label(SearchScreenJoinClass,text="Subject Name:").grid(column=0,row=2)
                SubjectNameEntry = tkinter.Entry(SearchScreenJoinClass,width=23)
                SubjectNameEntry.grid(column=1,row=2)
                #only linear search has been implemented due to time constraints
                '''
                name:- SearchConfirm_JoinClassTree
                purpose:- Search the join class tree using linear search and provided criteria
                args:- none
                inputs:- subject,class , table data
                outputs:- class highlighted or error thrown
                '''
                def SearchConfirm_JoinClassTree():
                    ClassName = ClassNameEntry.get()
                    SubjectName = SubjectNameEntry.get()
                    existingRows = JoinClassTree.get_children()
                    if ClassName == "" or SubjectName == "":
                        print(CRED+"Incorrect input"+CEND)
                        messagebox.showerror("Error","Fill the form")
                        return False
                    i = 0
                    while i<len(existingRows):
                        if JoinClassTree.item(existingRows[i])['text'] == SubjectName and JoinClassTree.item(existingRows[i])['values'][0] == ClassName:
                            JoinClassTree.focus(existingRows[i])
                            JoinClassTree.selection_set(existingRows[i])
                            print(CGREEN+"Item found!"+CEND)
                            messagebox.showinfo("Success","Item highlighted in table")
                            return False
                        i+=1
                    print(CRED+"Item missing!"+CEND)
                    messagebox.showerror("Error","Item unable to be found")
                tkinter.Button(SearchScreenJoinClass,text="Search..",fg='green',bd=0,command=SearchConfirm_JoinClassTree).grid(column=1,row=3)
            tkinter.Button(JoinClassScreen,text="Search.",fg='blue',bd=0,command=Search_JoinClassTree).grid(column=0,row=2)
            '''
            name:- Sort_JoinClassTree
            purpose:- sorts the join class tree using subject
            args:- none
            inputs:- Table data
            Outputs:- sorted table data
            '''
            def Sort_JoinClassTree():
                existingRows = JoinClassTree.get_children()
                newExistingRows = []
                for t in existingRows:
                    k = True
                    for l in newExistingRows:
                        #prevents the same subject being inserted multiple times(because subject isnt a unique peice of information)
                        if l == JoinClassTree.item(t)['text']:
                            k=False
                    if k:
                        newExistingRows.append(JoinClassTree.item(t)['text'])
                newExistingRows = QuickieSort(newExistingRows)
                toIns = []
                for t in newExistingRows:
                    k = 0
                    while k<len(existingRows):
                        #inserts all the classes under the subject
                        if JoinClassTree.item(existingRows[k])['text'] == t:
                            toIns.append((JoinClassTree.item(existingRows[k])['text'],JoinClassTree.item(existingRows[k])['values']))
                        k+=1
                JoinClassTree.delete(*JoinClassTree.get_children())
                i = 0
                while i<len(toIns):
                    text,values = toIns[i]
                    JoinClassTree.insert("",tkinter.END,text=text,values=values)
                    i+=1
            tkinter.Button(JoinClassScreen,text="Sort..",fg='blue',bd=0,command=Sort_JoinClassTree).grid(column=2,row=2)
            '''
            name:- confirm_JoinClassTree
            purpose:- Joins/waitlists the user to class
            args:- event(ignored)
            inputs:- selected subject,class , user data , waitlist data , subject data
            outputs:- enrolled/waitlisted or error thrown
            '''
            def confirm_JoinClassTree(event):
                try:
                    selectedSubject = JoinClassTree.item(JoinClassTree.focus())['text']
                    selectedClass = JoinClassTree.item(JoinClassTree.focus())['values'][0]
                    selectedSpotsLeft = int(JoinClassTree.item(JoinClassTree.focus())['values'][2])
                except:
                    return False
                file = open("users.csv","r+")
                userLines = file.readlines()
                file.close()
                file = open("waitlist.csv","r+")
                waitlistLines = file.readlines()
                file.close()
                file = open("subjects.csv","r+")
                subjectLines = file.readlines()
                file.close()
                i = 0
                #checks for clashes with any existing classes of the user
                while i<len(userLines):
                    row = userLines[i].split(',')
                    if len(row)!=userLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] =row[t].strip()
                    if row[0] == user:
                        subs = row[2].split('.')
                        k = 0
                        if len(subs)%2 != 0:
                            del subs[0]
                        timeArr = []
                        #gets time data of all the subjects the user is currently enrolled in
                        while k<len(subs):
                            j = 0
                            while j<len(subjectLines):
                                row2 = subjectLines[j].split(',')
                                if len(row2)!=subjectLEN:
                                    j+=1
                                    continue
                                for t in range(len(row2)):row2[t] = row2[t].strip()
                                if row2[0] == subs[k] and row2[1] == subs[k+1]:
                                    timeData = row2[3].split('.')
                                    fromD,fromMo,fromY = timeData[0].split(':')
                                    toD,toMo,toY = timeData[1].split(':')
                                    fromH,fromMi = timeData[2].split(':')
                                    toH,toMi = timeData[3].split(':')
                                    monthswith31 = [1,3,5,7,8,10,12]
                                    rState = timeData[4]
                                    fromY=int(fromY)
                                    fromMo = int(fromMo)
                                    fromD = int(fromD)
                                    toD = int(toD)
                                    toMo = int(toMo)
                                    toY = int(toY)
                                    fromH = int(fromH)
                                    fromMi = int(fromMi)
                                    toH = int(toH)
                                    toMi = int(toMi)
                                    timeFrom = 0
                                    timeTo = 0
                                    n = 0
                                    while n<fromY:
                                        if n%4 == 0:
                                            timeFrom+=366*24*60
                                        else:
                                            timeFrom+=365*24*60
                                        n+=1
                                    n = 1
                                    while n<fromMo:
                                        if n in monthswith31:
                                            timeFrom+=31*24*60
                                        elif n == 2:
                                            if fromY%4 == 0:
                                                timeFrom+=29*24*60
                                            else:
                                                timeFrom+=28*24*60
                                        else:
                                            timeFrom+=30*24*60
                                        n+=1
                                    timeFrom+=fromD*24*60
                                    timeFrom+=fromH*60
                                    timeFrom+=fromMi
                                    n = 0
                                    while n<toY:
                                        if n%4 == 0:
                                            timeTo+=366*24*60
                                        else:
                                            timeTo+=365*24*60
                                        n+=1
                                    n = 0
                                    while n<toMo:
                                        if n in monthswith31:
                                            timeFrom+=31*24*60
                                        elif n == 2:
                                            if toY%4 == 0:
                                                timeFrom+=29*24*60
                                            else:
                                                timeFrom+=28*24*60
                                        else:
                                            timeFrom+=30*24*60
                                        n+=1
                                    timeTo+=toD*24*60
                                    timeTo+=toH*60
                                    timeTo+=toMi
                                    timeArr.append((row2[0],row2[1],timeFrom,timeTo,rState,fromH,fromMi,toH,toMi))
                                    break
                                j+=1
                            k+=1
                        k = 0
                        selectedTime = []
                        #gets the time data of the selected class
                        while k<len(subjectLines):
                            row2 = subjectLines[k].split(',')
                            if len(row2) != subjectLEN:
                                k+=1
                                continue
                            if row2[0] == selectedSubject and row2[1] == selectedClass:
                                timeData = row2[3].split('.')
                                fromD,fromMo,fromY = timeData[0].split(':')
                                toD,toMo,toY = timeData[1].split(':')
                                fromH,fromMi = timeData[2].split(':')
                                toH,toMi = timeData[3].split(':')
                                monthswith31 = [1,3,5,7,8,10,12]
                                rState = timeData[4]
                                fromY=int(fromY)
                                fromMo = int(fromMo)
                                fromD = int(fromD)
                                toD = int(toD)
                                toMo = int(toMo)
                                toY = int(toY)
                                fromH = int(fromH)
                                fromMi = int(fromMi)
                                toH = int(toH)
                                toMi = int(toMi)
                                timeFrom = 0
                                timeTo = 0
                                n = 0
                                while n<fromY:
                                    if n%4 == 0:
                                        timeFrom+=366*24*60
                                    else:
                                        timeFrom+=365*24*60
                                    n+=1
                                n = 1
                                while n<fromMo:
                                    if n in monthswith31:
                                        timeFrom+=31*24*60
                                    elif n == 2:
                                        if fromY%4 == 0:
                                            timeFrom+=29*24*60
                                        else:
                                            timeFrom+=28*24*60
                                    else:
                                        timeFrom+=30*24*60
                                    n+=1
                                timeFrom+=fromD*24*60
                                timeFrom+=fromH*60
                                timeFrom+=fromMi
                                n = 0
                                while n<toY:
                                    if n%4 == 0:
                                        timeTo+=366*24*60
                                    else:
                                        timeTo+=365*24*60
                                    n+=1
                                n = 0
                                while n<toMo:
                                    if n in monthswith31:
                                        timeFrom+=31*24*60
                                    elif n == 2:
                                        if toY%4 == 0:
                                            timeFrom+=29*24*60
                                        else:
                                            timeFrom+=28*24*60
                                    else:
                                        timeFrom+=30*24*60
                                    n+=1
                                timeTo+=toD*24*60
                                timeTo+=toH*60
                                timeTo+=toMi
                                selectedTime.append((timeFrom,timeTo,rState,fromH,fromMi,toH,toMi))
                                break
                            k+=1
                        j = 0
                        try:
                            timefromS,timetoS,rStateS,fHs,fMs,tHs,tMs =selectedTime[0]
                            tRange = set(range(timefromS,timetoS))
                            currTime = set(range(int(fHs)*60+int(fMs),int(tHs)*60+int(tMs)))
                        except:
                            break
                        while j<len(timeArr):
                            sub,class_,timefrom,timeto,rState,fH,fM,tH,tM = timeArr[j]
                            #checks whether the classes happen on the same day
                            if rState == rStateS or rState == "Everyday":
                                check = set(range(timefrom,timeto))
                                #checks whether the time ranges collide
                                if len(tRange.intersection(check))>0:
                                    check = set(range(int(fH)*60+int(fM),int(tH)*60+int(tM)))
                                    #checks whether the time in Hours and Minutes collide
                                    if len(currTime.intersection(check))>0:
                                        if not messagebox.askyesno("Error","Clash detected with "+sub+","+class_+". Do you want to force clash?"):
                                            return False
                                        break
                            j+=1
                        break
                    i+=1
                if selectedSpotsLeft-1<0:
                    #executes waitlist func
                    if not messagebox.askyesno("Confirm","There isnt enough spaces in this class. Do you want to waitlist instead?"):
                        return False
                    i = 0
                    waitlistLines.append(user+","+selectedSubject+","+selectedClass+"\n")
                    file = open('waitlist.csv','w+')
                    file.writelines(waitlistLines)
                    file.close()
                    messagebox.showinfo("Success","Successfully waitlisted.")
                    Refresh_JoinClassTree()
                    Refresh_EnrolementsTable()
                    return False
                i= 0
                newULines = []
                while i<len(userLines):
                    row = userLines[i].split(',')
                    for t in range(len(row)):row[t] = row[t].strip()
                    if len(row)!=userLEN:
                        i+=1
                        continue
                    if row[0] == user:
                        #appends enrolement
                        if not(row[2] == ""):
                            row[2] = row[2]+"."+selectedSubject+"."+selectedClass
                        else:
                            row[2] = selectedSubject+"."+selectedClass
                    newULines.append(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+"\n")
                    i+=1
                file = open("users.csv","w+")
                file.writelines(newULines)
                file.close()
                messagebox.showinfo("Success","Enrolled")
                Refresh_JoinClassTree()
                Refresh_EnrolementsTable()
            JoinClassTree.bind("<Double-1>",confirm_JoinClassTree)
        tkinter.Button(MyClassesScreen,text="Join A Class",fg='green',bd=0,command=JoinClass).grid(column=1,row=2)
        '''
        name:- LeaveClass
        purpose:- unenrols/unwaitlists the selected class
        args:- event(ignored)
        inputs:- selected subject , class and mode(mode is data about whether its a enrolement or waitilist) , user database , waitlist database
        outputs:- changes reflected in databases
        '''
        def LeaveClass(event):
            global Refresh_JoinClassTree
            try:
                #checks whether a class has been selected
                selectedSubject = MyEnrolementsTable.item(MyEnrolementsTable.focus())['text']
                selectedClass = MyEnrolementsTable.item(MyEnrolementsTable.focus())['values'][0]
                selectedMode = MyEnrolementsTable.item(MyEnrolementsTable.focus())['values'][1]
            except:
                return False
            if selectedMode == "ENROLLED":
                file = open("users.csv","r+")
                userLines = file.readlines()
                file.close()
                newUserLines = []
                i = 0
                #removes the enrolement
                while i<len(userLines):
                    row = userLines[i].split(',')
                    if len(row)!=userLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    if row[0] == user:
                        tempSub = row[2].split('.')
                        k = 0
                        newSub = []
                        while k<len(tempSub):
                            try:
                                if not(tempSub[k] == selectedSubject and tempSub[k+1] == selectedClass):
                                    newSub.append(tempSub[k])
                                    newSub.append(tempSub[k+1])
                                k+=2
                            except:
                                break
                        k = 0
                        tempSubW = ""
                        while k<len(newSub):
                            if k == len(newSub)-1:
                                tempSubW = tempSubW+newSub[k]
                            else:
                                tempSubW = tempSubW+newSub[k]+"."
                            k+=1
                        #TODO
                        newUserLines.append(row[0]+","+row[1]+","+tempSubW+","+row[3]+","+row[4]+"\n")
                    else:
                        newUserLines.append(userLines[i])
                    i+=1
                print(CGREEN+"New enrolement data written!"+CEND)
                file = open("users.csv","w+")
                file.writelines(newUserLines)
                file.close()
                print(CGREEN+"Unenrolled successfully"+CEND)
                messagebox.showinfo("Success","Successfully unenrolled from "+selectedSubject+","+selectedClass)
                Refresh_EnrolementsTable()
                try:
                    Refresh_JoinClassTree()
                except:
                    print("window refresh ignored")
                    pass
                return False
            else:
                #unwaitlists
                file = open("waitlist.csv","r+")
                waitlistLines = file.readlines()
                file.close()
                i = 0
                newWaitlistLines = []
                while i<len(waitlistLines):
                    row = waitlistLines[i].split(',')
                    if len(row)!=waitlistLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    if row[0] == user:
                        if row[1] == selectedSubject and row[2] == selectedClass:
                            i+=1
                            continue
                    newWaitlistLines.append(waitlistLines[i])
                    i+=1
                file = open("waitlist.csv","w+")
                file.writelines(newWaitlistLines)
                file.close()
                print(CGREEN+"Unwaitlisted successfully"+CEND)
                messagebox.showinfo("Success","You have been unwaitlisted from "+selectedSubject+","+selectedClass+".")
                Refresh_EnrolementsTable()
                try:
                    Refresh_JoinClassTree()
                except:
                    pass
                return False
        MyEnrolementsTable.bind("<Double-1>",LeaveClass)
        '''
        name:- CloseMyEnrolements
        purpose:- Close My Classes Screen and children
        args:- none
        inputs:- none
        outputs:- close commands for all children
        '''
        def CloseMyEnrolements():
            global JoinClassScreen
            try:
                JoinClassScreen.destroy()
            except:
                pass
            MyClassesScreen.destroy()
        MyClassesScreen.protocol("WM_DELETE_WINDOW",CloseMyEnrolements)
    MC=tkinter.Button(MiscPortal,text="My Classes",fg='green',bd=0,command=MyClasses)
    MC.grid(column=0,row=2)
    if user == "admin":
        MC.config(state='disabled')
    '''
    name:- ManageMyClass
    purpose:- Opens a screen in which the user can pick a class to manage from list of classes that the user is bound to
    args:- none
    inputs:- none
    outputs:- table that displays bound classes of the user
    '''
    def ManageMyClass():
        global CloseMMC
        if CheckOpen("Manage My Classes(BINDS)"):return False
        ManageMyClassScreen = tkinter.Toplevel(loginScreen)
        ManageMyClassScreen.resizable(0,0)
        ManageMyClassScreen.title("Manage My Classes(BINDS)")
        print(CGREEN+"Manage my class loaded"+CEND)
        tkinter.Label(ManageMyClassScreen,text="Pick A Class To Manage").grid(column=1,row=0)
        MMCFrame = tkinter.Frame(ManageMyClassScreen)
        MMCFrame.grid(column=1,row=1)
        MMCTable = ttk.Treeview(MMCFrame)
        YScrollMMCTable = tkinter.Scrollbar(MMCFrame,orient=tkinter.VERTICAL,command=MMCTable.yview)
        YScrollMMCTable.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        MMCTable.configure(yscrollcommand=YScrollMMCTable.set)
        XScrollMMCTable = tkinter.Scrollbar(MMCFrame,orient=tkinter.HORIZONTAL,command=MMCTable.xview)
        XScrollMMCTable.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        MMCTable.configure(xscrollcommand=XScrollMMCTable.set)
        MMCTable.pack(side=tkinter.TOP)
        MMCTable.heading("#0",text="Subject/Class")
        '''
        name:-RefreshMMCTable
        purpose:Refresh the table that displays all bound classes of the user
        inputs:subject database,current logged in user
        outputs:refreshed MMC Table
        '''
        def RefreshMMCTable():
            MMCTable.delete(*MMCTable.get_children())
            file = open("subjects.csv","r+")
            subjectLines = file.readlines()
            file.close()
            i = 0
            toIns = []
            #itirate table and look for subjects that has the user bound to it
            while i<len(subjectLines):
                row = subjectLines[i].split(',')
                if len(row)!=subjectLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[5] == user or user == "admin":
                    toIns.append((row[0],row[1]))
                i+=1
            i = 0
            #inserts the subjects and classes categorically
            while i<len(toIns):
                subject,class_ = toIns[i]
                print(CGREEN+f"Successfuly inserted {subject} : {class_} to bind table"+CEND)
                existingRows = MMCTable.get_children()
                k = 0
                n = False
                while k<len(existingRows):
                    if MMCTable.item(existingRows[k])['text'] == subject:
                        MMCTable.insert(existingRows[k],tkinter.END,text=class_)
                        n=True
                        break
                    k+=1
                if n:
                    i+=1
                    continue

                pID=MMCTable.insert("",tkinter.END,text=subject)
                MMCTable.insert(pID,tkinter.END,text=class_)
                i+=1
        RefreshMMCTable()
        '''
        name:- ManageClassFocused
        purpose:- display sub menu showing list of users joined to that class , with the capability to kick a user off the class
        args:event(ignored)
        inputs: selected class
        outputs: table with class users and info
        '''
        def ManageClassFocused(event):
            global SearchScreenMST
            global MCScreenClose
            if CheckOpen("MC Screen Focused"):return False
            try:
                #checks whether a class is selected or not
                selectedClass = MMCTable.item(MMCTable.focus())['text']
                selectedSubject = MMCTable.item(MMCTable.parent(MMCTable.focus()))['text']
                if selectedSubject == "":
                    return False
            except:
                return False
            MCScreen = tkinter.Toplevel(loginScreen)
            MCScreen.title("MC Screen Focused")
            print(CGREEN+"Initialized Manage Class Focused screen"+CEND)
            MCScreen.resizable(0,0)
            MCf1 = tkinter.Frame(MCScreen)
            MCf1.grid(column=1,row=0)
            MCf2 = tkinter.Frame(MCScreen)
            MCf2.grid(column=1,row=1)
            MCf3 = tkinter.Frame(MCf2)
            MCf3.grid(column=1,row=1)
            tkinter.Label(MCf2,text="Unenrol students by double clicking.",fg='purple').grid(column=1,row=0)
            ManageStudentsTree = ttk.Treeview(MCf3)
            ManageStudentsTree.heading("#0",text="Username")
            YScrollMST = tkinter.Scrollbar(MCf3,orient=tkinter.VERTICAL,command=ManageStudentsTree.yview)
            ManageStudentsTree.configure(yscrollcommand=YScrollMST.set)
            XScrollMST = tkinter.Scrollbar(MCf3,orient=tkinter.HORIZONTAL,command=ManageStudentsTree.xview)
            ManageStudentsTree.configure(xscrollcommand=XScrollMST.set)
            YScrollMST.pack(side=tkinter.RIGHT,fill=tkinter.Y)
            XScrollMST.pack(side=tkinter.BOTTOM,fill=tkinter.X)
            ManageStudentsTree.pack(side=tkinter.TOP,expand='false')
            '''
            name:RefreshManageStudentsTree
            purpose:fill the table with data relating to users who have joined this class
            args:- none
            inputs:user database , selected class
            outputs: ManageStudentsTree filled with users who have enrolled to this class
            '''
            def RefreshManageStudentsTree():
                file = open("users.csv","r+")
                userLines = file.readlines()
                file.close()
                i = 0
                toIns = []
                #scans each users enrolements for whether they are enrolled or not , if they are insert to table
                while i<len(userLines):
                    row = userLines[i].split(',')
                    if len(row)!=userLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    tempSubs = row[2].split('.')
                    k = 0
                    if row[2] == "":
                        i+=1
                        continue
                    while k<len(tempSubs):
                        if tempSubs[k] ==selectedSubject and tempSubs[k+1] == selectedClass:
                            toIns.append(row[0])
                            break
                        k+=1
                    i+=1
                toIns = QuickieSort(toIns)
                i = 0 
                ManageStudentsTree.delete(*ManageStudentsTree.get_children())
                while i<len(toIns):
                    print(CGREEN+f"User detected {toIns[i]}"+CEND)
                    ManageStudentsTree.insert("",tkinter.END,text=toIns[i])
                    i+=1
            RefreshManageStudentsTree()
            '''
            name:UnEnrolManageStudentsTree
            purpose: run unenrolement command when the tree is pressed , where the selected user gets unenrolled. this is a "kick" from the class
            args: event(ignored)
            inputs: user database , selected user
            outputs: user unenrolled
            '''
            def UnEnrolManageStudentsTree(event):
                try:
                    username = ManageStudentsTree.item(ManageStudentsTree.focus())['text']
                    if username == "":
                        return False
                except:
                    return False
                if not(messagebox.askyesno("Confirm","Do you want to unenrol this user? \nYou might need special permissions(Edit User) to reenrol a user to this class again.")):
                    return False
                file = open("users.csv","r+")
                userLines = file.readlines()
                file.close()
                newUserLines = []
                i = 0
                #itirate the users and remove the enrolement from the list
                while i<len(userLines):
                    row = userLines[i].split(',')
                    if len(row)!=userLEN:
                        i+=1
                        continue
                    for t in range(len(row)):row[t] = row[t].strip()
                    if row[0] == username:
                        enrolements = row[2].split('.')
                        k = 0
                        toWEnrolements = ""
                        while k<len(enrolements):
                            if not(enrolements[k] == selectedSubject and enrolements[k+1] == selectedClass):
                                if k == len(enrolements) - 2:
                                    toWEnrolements = toWEnrolements+enrolements[k]+"."+enrolements[k+1]
                                else:
                                    toWEnrolements = toWEnrolements+enrolements[k]+"."+enrolements[k+1]+"."
                            k+=2
                        row[2] = toWEnrolements
                    newUserLines.append(row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]+"\n")
                    i+=1
                file = open("users.csv","w+")
                file.writelines(newUserLines)
                file.close()
                FileVerifs()
                print(CGREEN+"User unenrolled/kicked"+CEND)
                messagebox.showinfo("Confirmed","User unenrolled")
                RefreshManageStudentsTree()
            ManageStudentsTree.bind("<Double-1>",UnEnrolManageStudentsTree)
            tkinter.Label(MCf1,text="Subject Name:"+selectedSubject).grid(column=1,row=0)
            tkinter.Label(MCf1,text="Class Name:"+selectedClass).grid(column=1,row=1)
            '''
            name:SearchManageStudentsTree
            purpose: a window that allows the user to search the tree using a form
            args:none
            inputs:none
            outputs: window with a form to search the user tree
            '''
            def SearchManageStudentsTree():
                global SearchScreenMST
                if CheckOpen("Search MST"):return False
                SearchScreenMST = tkinter.Toplevel(loginScreen)
                SearchScreenMST.title("Search MST")
                SearchScreenMST.resizable(0,0)
                print(CGREEN+"Search students screen initialised"+CEND)
                tkinter.Label(SearchScreenMST,text="Fill the form").grid(column=1,row=0)
                tkinter.Label(SearchScreenMST,text="Username:").grid(column=0,row=1)
                UsernameEntry = tkinter.Entry(SearchScreenMST,width=23)
                UsernameEntry.grid(column=1,row=1)
                tkinter.Label(SearchScreenMST,text="Mode:").grid(column=0,row=2)
                ModeCombo = ttk.Combobox(SearchScreenMST,values=["Linear","Binary"],state='readonly')
                ModeCombo.set("Linear")
                ModeCombo.grid(column=1,row=2)
                #searches are getting less feature rich due to time restraints
                '''
                name: SearchConfirmMST
                purpose: search the manage students table using the data provided in the form
                args:none
                inputs: user to look for and how to look for that user(binary/linear)'''
                def SearchConfirmMST():
                    existingUsers = ManageStudentsTree.get_children()
                    mode = ModeCombo.get()
                    username = UsernameEntry.get()
                    if mode == "" or username == "":
                        print(CRED+"Invalid data provided"+CEND)
                        messagebox.showerror("Error","Fill the form")
                        return False
                    if mode == "Linear":
                        i = 0
                        while i<len(existingUsers):
                            if ManageStudentsTree.item(existingUsers[i])['text'] == username:
                                ManageStudentsTree.focus(existingUsers[i])
                                ManageStudentsTree.selection_set(existingUsers[i])
                                print(CGREEN+"user found"+CEND)
                                messagebox.showinfo("Info","User has been found and highlighted in the table")
                                return False
                            i+=1
                        print(CRED+"User not found!"+CEND)
                        messagebox.showerror("Error","Unable to find user")
                    else:
                        newExistingUsers = []
                        for t in existingUsers:newExistingUsers.append(ManageStudentsTree.item(t)['text'])
                        newExistingUsers = QuickieSort(newExistingUsers)
                        if binarySearchAppr(newExistingUsers,0,len(newExistingUsers)-1,username):
                            for a in existingUsers:
                                if ManageStudentsTree.item(a)['text'] == username:
                                    ManageStudentsTree.focus(a)
                                    ManageStudentsTree.selection_set(a)
                                    print(CGREEN+"User found"+CEND)
                                    messagebox.showinfo("Info","User has been found and highlighted in the table")
                                    return False
                        else:
                            print(CRED+"User not found!"+CEND)
                            messagebox.showerror("Error","Unable to find user")
                tkinter.Button(SearchScreenMST,command=SearchConfirmMST,text="Confirm Search",fg='green',bd=0).grid(column=1,row=3)
            tkinter.Button(MCf2,text="Search..",fg='blue',bd=0,command=SearchManageStudentsTree).grid(column=1,row=2)
            '''
            name:MCScreenCLose
            Purpose:Close all the child window
            args: none
            inputs:none
            outputs:close commands for child windows
            '''
            def MCScreenClose():
                print(CRED+"Close command sent"+CEND)
                global SearchScreenMST
                try:
                    SearchScreenMST.destroy()
                except:
                    pass
                MCScreen.destroy()
            MCScreen.protocol("WM_DELETE_WINDOW",MCScreenClose)
            tkinter.Button(MCScreen,text="Exit",command=MCScreenClose,bd=0,fg='red').grid(column=1,row=2)
        MMCTable.bind("<Double-1>",ManageClassFocused)
        '''
        name:closeMMC
        purpose: close all child windows
        args: none
        inputs: none
        outputs: close commands for the children
        '''
        def CloseMMC():
            global MCScreenClose
            try:
                MCScreenClose()
            except:
                pass
            ManageMyClassScreen.destroy()
        ManageMyClassScreen.protocol("WM_DELETE_WINDOW",CloseMMC)
        tkinter.Button(ManageMyClassScreen,text="Exit",command=CloseMMC,fg='red',bd=0).grid(column=1,row=2)
    MMCButton = tkinter.Button(MiscPortal,text="Teacher Portal",fg='green',bd=0,command=ManageMyClass)
    MMCButton.grid(column=1,row=2)
    if not(AuthMod(user,1)):
        print(CRED+"Missing can bind to classes perm"+CEND)
        MMCButton.config(state='disabled')
    file = open("subjects.csv","r+")
    subjectLines = file.readlines()
    file.close()
    i = 0
    n = False
    while i<len(subjectLines):
        row = subjectLines[i].split(',')
        if len(row)!=subjectLEN:
            i+=1
            continue
        for t in range(len(row)):row[t] = row[t].strip()
        if row[5] == user:
            n = True
            break
        i+=1
    if not(n):
        if user!="admin":
            print(CRED+"No bound classes detected"+CEND)
            MMCButton.config(state='disabled')
    '''
    name:Decrypter
    purpose:Import encrypted data previously exported by Exporter, serves as backup system
    args: none
    inputs: encrypted waitlists, users , subject , roles
    outputs: unencrypted waitlists , users,subject,roles
    '''
    #the user should have every single permission to import data , as false and modified data can be imported which can result in vulnerabilites in the system
    def Decrypter():
        try:
            file = open("users[ENCRYPTED].csv","r+")
            userLines = file.readlines()
            file.close()
            file = open("waitlist[ENCRYPTED].csv","r+")
            waitlistLines = file.readlines()
            file.close()
            file = open("subjects[ENCRYPTED].csv","r+")
            subjectLines = file.readlines()
            file.close()
            file = open("roles[ENCRYPTED].csv","r+")
            roleLines = file.readlines()
            file.close()
        except:
            print(CRED+"Not enough files to perform file recovery"+CEND)
            messagebox.showerror("Error","Files missing for decryption and import. Makes sure all the files are available")
            return False
        newULines = []
        i = 0
        #decrypts User data using ord key manipulation
        while i<len(userLines):
            try:
                p=0
                encryptedtxt=""
                key=1
                plaintext=userLines[i]
                temp=""
                plaintext=str(plaintext)
                for p in range (0,len(plaintext)):
                    temp = ord(plaintext[p])+key
                    temp=chr(temp)
                    encryptedtxt=encryptedtxt+temp
                newULines.append(encryptedtxt)
                i+=1
            except:
                print(CRED+"Decryption error for uData"+CEND)
                messagebox.showerror("Error","Decryption Error. Exited to prevent data loss")
                return False
        file = open("users.csv","w+")
        file.writelines(newULines)
        file.close()
        newWLines = []
        i = 0
        #decrypts waitlist data using ord key manipulation
        while i<len(waitlistLines):
            try:
                p=0
                encryptedtxt=""
                key=1
                plaintext=waitlistLines[i]
                temp=""
                plaintext=str(plaintext)
                for p in range (0,len(plaintext)):
                    temp = ord(plaintext[p])+key
                    temp=chr(temp)
                    encryptedtxt=encryptedtxt+temp
                newWLines.append(encryptedtxt)
                i+=1
            except:
                print(CRED+"Decryption error for wData"+CEND)
                messagebox.showerror("Error","Decryption Error. Exited to prevent data loss")
                return False
        file = open("waitlist.csv","w+")
        file.writelines(newWLines)
        file.close()
        newRLines = []
        i = 0
        #decrypts role data using ord key manipulation
        while i<len(roleLines):
            try:
                p=0
                encryptedtxt=""
                key=1
                plaintext=roleLines[i]
                temp=""
                plaintext=str(plaintext)
                for p in range (0,len(plaintext)):
                    temp = ord(plaintext[p])+key
                    temp=chr(temp)
                    encryptedtxt=encryptedtxt+temp
                newRLines.append(encryptedtxt)
                i+=1
            except:
                print(CRED+"Decryption error for rData"+CEND)
                messagebox.showerror("Error","Decryption Error. Exited to prevent data loss")
                return False
        file = open("roles.csv","w+")
        file.writelines(newRLines)
        file.close()
        newSLines = []
        i = 0
        #decrypts subject data using ord key manipulation
        while i<len(subjectLines):
            try:
                p=0
                encryptedtxt=""
                key=1
                plaintext=subjectLines[i]
                temp=""
                plaintext=str(plaintext)
                for p in range (0,len(plaintext)):
                    temp = ord(plaintext[p])+key
                    temp=chr(temp)
                    encryptedtxt=encryptedtxt+temp
                newSLines.append(encryptedtxt)
                i+=1
            except:
                print(CRED+"Decryption error for SData"+CEND)
                messagebox.showerror("Error","Decryption Error. Exited to prevent data loss")
                return False
        file = open("subjects.csv","w+")
        file.writelines(newSLines)
        file.close()
        messagebox.showinfo("Data Imported","Data has been successfully imported")
        if messagebox.askyesno("Dispose files..","Do you want to dispose of the encrypted copies of the files?"):
            try:
                os.remove("waitlist[ENCRYPTED].csv")
            except:
                pass
            try:
                os.remove("users[ENCRYPTED].csv")
            except:
                pass
            try:
                os.remove("subjects[ENCRYPTED].csv")
            except:
                pass
            try:
                os.remove("roles[ENCRYPTED].csv")
            except:
                pass
            messagebox.showinfo("Success","Copies deleted")
        FileVerifs()
    tkinter.Button(MiscPortal,text="Decrypt and Import",bd=0,fg='green',command=Decrypter,state=ExportDataB['state']).grid(column=2,row=2)
    tkinter.Button(MiscPortal,text="About",bd=0,fg='purple',command=lambda:messagebox.showinfo("Info","Program built by walter-the-dog. MIT license")).grid(column=1,row=3)
    def CloseMiscPortal():
        print(CRED+"Close command received"+CEND)
        global SchedulerScreen
        global CloseMyEnrolements
        global ProfilerScreen
        global CloseMMC
        try:
            SchedulerScreen.destroy()
        except:
            pass
        try:
            CloseMyEnrolements()
        except:
            pass
        try:
            ProfilerScreen.destroy()
        except:
            pass
        try:
            CloseMMC()
        except:
            pass
        MiscPortal.destroy()
    MiscPortal.protocol("WM_DELETE_WINDOW",CloseMiscPortal)
'''
Name:firstRun
Purpose: act as a portal for all the other windows
Args: state(whether to show the tutorial messagebox) , user(current user who is logged in)
Inputs: current user and application state , permission info
outputs:portals with buttons to their respective actions
'''
def firstRun(state,user):
    try:
        file = open("users.csv","r+")
        file.close()
    except:
        file = open("users.csv","w+")
        file.close()
    
    try:
        file = open("roles.csv","r+")
        file.close()
    except:
        file = open("roles.csv","w+")
        file.close()
    
    try:
        file = open("subjects.csv","r+")
        file.close()
    except:
        file = open("subjects.csv","w+")
        file.close()

    try:
        file = open("waitlist.csv","r+")
        file.close()
    except:
        file = open("waitlist.csv","w+")
        file.close()
    
    if CheckOpen("Portal"):return False
    print(CGREEN+"Portal initialised"+CEND)
    firstRunScreen = tkinter.Toplevel(loginScreen)
    firstRunScreen.withdraw()
    
    state = bool(int(state))
    if state:
        
        if messagebox.askyesno("Confirm","Do you want to refer to the setup tutorial?"):
            try:
                file = open("README.docx")
                file.close()
                os.system("start README.docx")
            except:
                print(CRED+"Missing Tutorial Doc"+CEND)
                if connected_ssid == b"gwsc.vic.edu.au":
                    print(CRED+"Network Failure"+CEND)
                    messagebox.showerror("Error","Tutorial file cannot be fetched in this network. Change access point and try again")
                else:
                    try:
                        urllib.request.urlretrieve("https://onedrive.live.com/download?cid=462F43BFC225E6DA&resid=462F43BFC225E6DA%213633&authkey=ABulzsu8nLZCWcE&em=2","README.docx")
                        print(CGREEN+"Tutorial Doc fetched"+CEND)
                        os.system("start README.docx")
                    except:
                        print(CRED+"Network Failure"+CEND)
                        messagebox.showerror("Error","Cannot access the network. Check network connectivity and try again")
            
    
    firstRunScreen.deiconify()
    
    firstRunScreen.title("Portal")
    firstRunScreen.resizable(0,0)
    '''
    name:warningMessage
    purpose:shuts down program
    args:none
    inputs:none
    outputs: all winodws closes
    '''
    def warningMessage():
        if messagebox.askyesno("Warning","Closing this window will close all windows. Continue?"):
            print(CRED+"Closed Program"+CEND)
            loginScreen.destroy()
        else:
            firstRunScreen.deiconify()
            firstRunScreen.update()
            return False
    
    firstRunScreen.protocol("WM_DELETE_WINDOW",warningMessage)
    
    tkinter.Label(firstRunScreen,text="Portal to where you want to go!").grid(column=1,row=0)
    #Buttons \/
    
    loadButtons = [tkinter.Button(firstRunScreen,text="Manage a Class",fg='green',command=lambda:manageClass(user),bd=0),
        tkinter.Button(firstRunScreen,text="Add a User",fg='green',command=lambda:AddUser(user),bd=0),
        tkinter.Button(firstRunScreen,text="Delete a User",fg='green',command=lambda:DeleteUser(user),bd=0),
        tkinter.Button(firstRunScreen,text="Edit a User",fg='green',command=lambda:EditUser(user),bd=0),
        tkinter.Button(firstRunScreen,text="Manage Roles",fg='green',command=lambda:ManageRoles(user),bd=0),
        tkinter.Button(firstRunScreen,text="Misc",fg='green',command=lambda:Misc(user),bd=0)]
    
    if user != "admin":
        #if the user cannot manage roles , disable button
        if not AuthMod(user,2):
            print(CRED+"Missing Manage Roles Permission"+CEND)
            loadButtons[4]['state'] = 'disabled'
        #if the user cannot add users, disable button
        if not AuthMod(user,3):
            print(CRED+"Missing Add User permission"+CEND)
            loadButtons[1]['state']='disabled'
        #if the user cannot delete users , disable button
        if not AuthMod(user,4):
            print(CRED+"Missing Delete user permission"+CEND)
            loadButtons[2]['state']='disabled'
        #if the user cannot add and delete users , disable button
        if not(AuthMod(user,3) and AuthMod(user,4)):
            print(CRED+"Insufficient permissions for editing users"+CEND)
            loadButtons[3]['state']='disabled'
        #if the user cannot manage classes , disable button
        if not AuthMod(user,6):
            print(CRED+"Missing manage classes permissions"+CEND)
            loadButtons[0]['state']='disabled'
    
    i = 0
    k = 0
    
    while i<len(loadButtons):
    
        if i<3:
            loadButtons[i].grid(column=0,row=i+1)
        else:
            loadButtons[i].grid(column=2,row=k+1)
            k+=1
        i+=1
    
#init
#base level Login Screen
#purpose :- Used as a base window for Toplevels. All toplevels are built on this
print("Logging "+CGREEN+"all"+CEND+" events.. Ignore these if you are not a developer")
loginScreen = tkinter.Tk()
loginScreen.title("Login")
loginScreen.withdraw()
#gets the current network connection dns
subWarnList = []
connected_ssid = subprocess.check_output("powershell.exe (get-netconnectionProfile).Name", shell=True).strip()
if connected_ssid == b"gwsc.vic.edu.au":
    print(CRED+"Network Script access blocked"+CEND)
    subWarnList.append("This network has blocked script access. Email functions have been disabled.(Please Connect to a different access point)\n")
availableram=subprocess.check_output("powershell.exe systeminfo |find \"Available Physical Memory\"",shell=True).strip()
availableram=availableram.decode("utf-8")
availableram = availableram.strip("Available Physical Memory: ")
past = availableram
availableram = availableram.strip("MB")
availableram = availableram.split(',')
if len(availableram) == 1:
    print(CRED+"Not Enough RAM"+CEND)
    subWarnList.append(f"Your system is below the recommended amount of free RAM. Current Value({past}). Minimum recommended is 2GB\n")
elif availableram[0] in ["0","1"]:
    print(CRED+"Not enough RAM"+CEND)
    subWarnList.append(f"Your system is below the recommended amount of free RAM. Current Value({past}). Minimum recommended is 2GB\n")
if len(subWarnList)!=0:
    print(CRED+"Non crit errors detected."+CEND)
    toWSubWS = "".join([i for i in subWarnList])
    messagebox.showwarning("Warning","Non Critical Problems that might lead to suboptimal performance:\n "+toWSubWS)
loginScreen.deiconify()
init = False
'''
name:FileVerifs
Purpose: Run file verifications and ensure that GIGO doesnot happen
args: none
inputs: waitlist data , user data , role data , subject data
outputs: cleaned databases (this function will also return a list of errors if encountered any)
'''
def FileVerifs():
    errorList = []
    try:
        file = open("roles.csv","r+")
        roleLines = file.readlines()
        file.close()
        i = 0
        newRLines = []
        while i<len(roleLines):
            row = roleLines[i].split(',')
            if len(row)!=roleLEN:
                i+=1
                continue
            newRLines.append(roleLines[i])
            i+=1
        file = open("roles.csv","w+")
        file.writelines(newRLines)
        file.close()
        file = open("roles.csv","r+")
        if file.readlines()[0].strip() == [""]:
            raise TypeError
        file.close()
        print(CGREEN+f"Records of {i} has been processed"+CEND)
    except:
        file = open("roles.csv","w+")
        file.close()
        print(CRED+"Roles wiped!"+CEND)
        errorList.append("roles.csv is missing/corrupted\n")
    try:
        file = open("subjects.csv","r+")
        subjectLines = file.readlines()
        file.close()
        i = 0
        trueSubjectLines = []
        while i<len(subjectLines):
            row = subjectLines[i].split(',')
            if len(row)!=subjectLEN:
                i+=1
                continue
            trueSubjectLines.append(subjectLines[i])
            i+=1
        file = open("subjects.csv","w+")
        file.writelines(trueSubjectLines)
        file.close()
        file = open("subjects.csv","r+")
        subjectLines = file.readlines()
        file.close()
        newSubLines = []
        i = 0
        while i<len(subjectLines):
            row = subjectLines[i].split(',')
            if len(row)!=subjectLEN:
                i+=1
                continue
            if int(row[2])<=0:
                i+=1
                continue
            elif len(row[3].split('.'))!=5:
                i+=1
                continue
            elif not(row[3].split('.')[4] in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","Everyday"]):
                i+=1
                continue
            newSubLines.append(subjectLines[i])
            i+=1
        file = open("subjects.csv","w+")
        file.writelines(newSubLines)
        file.close()
        file = open("subjects.csv","r+")
        if file.readlines()[0].strip() == [""]:
            raise TypeError
        file.close()
        print(CGREEN+f"Records of {i} has been processed"+CEND)
    except:
        file = open("subjects.csv","w+")
        file.close()
        print(CRED+"Subjects wiped!"+CEND)
        errorList.append("subjects.csv is missing/corrupted\n")
    try:
        file = open("users.csv","r+")
        userLines=file.readlines()
        file.close()
        i = 0
        newULines = []
        while i<len(userLines):
            row = userLines[i].split(',')
            if len(row)==userLEN:
                newULines.append(userLines[i])
            i+=1
        file = open('users.csv','w+')
        file.writelines(newULines)
        file.close()
        file = open("users.csv","r+")
        userLines = file.readlines()
        file.close()
        file = open("subjects.csv","r+")
        subjectLines = file.readlines()
        file.close()
        file = open("roles.csv","r+")
        roleLines = file.readlines()
        file.close()
        i = 0
        newULines = []
        while i<len(userLines):
            row = userLines[i].split(',')
            if len(row)!=userLEN:
                i+=1
                continue
            for t in range(len(row)):row[t] = row[t].strip()
            userName = row[0]
            passW = row[1]
            subjects = row[2]
            if userName == "" and passW == "":
                i+=1
                continue
            subjects = list(subjects)
            k =0
            while k<len(subjects):
                try:
                    if subjects[k] == "." and subjects[k+1] == ".":
                        del subjects[k]
                    else:
                        k+=1
                except:
                    break
            try:
                if subjects[0] == ".":
                    del subjects[0]
                if subjects[len(subjects)-1] == ".":
                    del subjects[len(subjects)-1]
            except:
                pass
            subjectsT = ""
            for t in subjects:
                subjectsT = subjectsT+t
            subjects = subjectsT
            del subjectsT
            subjects = subjects.split('.')
            n = 0
            while n<len(subjects):
                k = 0
                found = False
                while k<len(subjectLines):
                    row2 = subjectLines[k].split(',')
                    if len(row2)!=subjectLEN:
                        k+=1
                        continue
                    for t in range(len(row2)):row2[t] = row2[t].strip()
                    try:
                        if row2[0] == subjects[n] and row2[1] == subjects[n+1]:
                            found=True
                            break
                    except:
                        pass
                    k+=1
                if found!=True:
                    try:
                        del subjects[n]
                        del subjects[n+1]
                    except:
                        pass
                else:
                    n+=2
            toWSubjects = ""
            k = 0
            while k<len(subjects):
                if k == len(subjects)-1:
                    toWSubjects = toWSubjects+subjects[k]
                else:
                    toWSubjects = toWSubjects + subjects[k]+"."
                k+=1
            k = 0
            found = False
            while k<len(roleLines):
                row2 = roleLines[k].split(',')
                if len(row2)!=roleLEN:
                    k+=1
                    continue
                if row2[0] == row[3]:
                    found = True
                    break
                k+=1
            if found == False:
                i+=1
                continue
            newULines.append(row[0]+","+row[1]+","+toWSubjects+","+row[3]+","+row[4]+"\n")
            i+=1
        file = open('users.csv',"w+")
        file.writelines(newULines)
        file.close()
        file = open("users.csv","r+")
        if file.readlines()[0].strip() == [""]:
            raise TypeError
        file.close()
        print(CGREEN+f"Records of {i} has been processed"+CEND)
    except:
        file= open("users.csv",'w+')
        file.close()
        print(CRED+"User database wiped!"+CEND)
        errorList.append("users.csv missing/corrupted\n")
    try:
        file = open('waitlist.csv',"r+")
        waitlistLines = file.readlines()
        file.close()
        file = open("users.csv","r+")
        userLines = file.readlines()
        file.close()
        file = open("subjects.csv","r+")
        subjectLines = file.readlines()
        file.close()
        i = 0
        newWaitlistLines = []
        while i<len(waitlistLines):
            row = waitlistLines[i].split(',')
            for t in range(len(row)):row[t] = row[t].strip()
            k = 0
            found = False
            while k<len(userLines):
                row2 = userLines[k].split(',')
                if len(row2)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row2)):row2[t] = row2[t].strip()
                if row2[0] == row[0]:
                    found = True
                    break
                k+=1
            if found != True:
                i+=1
                continue
            found = False
            k = 0
            while k<len(subjectLines):
                row2 = subjectLines[k].split(',')
                if len(row2)!=subjectLEN:
                    k+=1
                    continue
                for t in range(len(row2)):row2[t] = row2[t].strip()
                if row2[0] == row[1] and row2[1] == row[2]:
                    found=True
                    #begin space verifs
                    maxSpace = row2[2]
                    cEnrol = 0
                    j = 0
                    file = open("users.csv","r+")
                    userLines = file.readlines()
                    file.close()
                    while j<len(userLines):
                        row3 = userLines[j].split(',')
                        if len(row3)!=userLEN:
                            j+=1
                            continue
                        for t in range(len(row3)):row3[t] = row3[t].strip()
                        tempEnrols = row3[2].split('.')
                        n = 0
                        while n<len(tempEnrols):
                            try:
                                if tempEnrols[n] == row[1] and tempEnrols[n+1] == row[2]:
                                    cEnrol+=1
                            except:
                                break
                            n+=1
                        j+=1
                    if int(maxSpace)-cEnrol>0:
                        newULines = []
                        j = 0
                        while j<len(userLines):
                            row3 = userLines[j].split(',')
                            if len(row3)!=userLEN:
                                j+=1
                                continue
                            for t in range(len(row3)):row3[t] = row3[t].strip()
                            if row3[0] == row[0]:
                                if row3[2] == "":
                                    row3[2] = row[1]+"."+row[2]
                                else:
                                    row3[2] = row3[2]+"."+row[1]+"."+row[2]
                            newULines.append(row3[0]+","+row3[1]+","+row3[2]+","+row3[3]+","+row3[4]+"\n")
                            j+=1
                        file =open("users.csv","w+")
                        file.writelines(newULines)
                        file.close()
                        found = False
                k+=1
            if found != True:
                i+=1
                continue
            newWaitlistLines.append(waitlistLines[i])                
            i+=1
        file = open("waitlist.csv","w+")
        file.writelines(newWaitlistLines)
        file.close()
        print(CGREEN+f"Records of {i} has been processed"+CEND)
    except:
        file = open("waitlist.csv","w+")
        file.close()
        print(CRED+"Waitlist wiped!"+CEND)
        errorList.append("waitlist.csv missing\n")
    return errorList
errorList = FileVerifs()
i = 0
errorString = "\n"
while i<len(errorList):
    errorString = errorString+errorList[i]
    i+=1
if len(errorList) > 0:
    loginScreen.withdraw()
    print(CRED+"Errors caught"+CEND)
    messagebox.showerror("Info","List of errors that happened during intilization:"+errorString+"\n You will be logged in as administrator to fix any issues that could have occurred. Reboot when fixes are complete")
    firstRun(1,"admin")
else:
    print(CGREEN+"Login screen loaded"+CEND)
    tkinter.Label(loginScreen,text="Login").grid(column=1,row=0)
    tkinter.Label(loginScreen,text="Username:").grid(column=0,row=1)
    UsernameEntry = tkinter.Entry(loginScreen)
    UsernameEntry.grid(column=1,row=1)
    tkinter.Label(loginScreen,text="Password:").grid(column=0,row=2)
    PasswordEntry = tkinter.Entry(loginScreen,show="*")
    PasswordEntry.grid(column=1,row=2)
    tkinter.Label(loginScreen,text="OTP(Optional):").grid(column=0,row=3)
    OTPEntry = tkinter.Entry(loginScreen,state='disabled')
    OTPEntry.grid(column=1,row=3)
    modeLogin = "Init"
    otpCode = 0
    '''
    name:ConfirmLogin 
    purpose:login the user or process the 2 Factor code(depending on the mode)
    args:none
    inputs:mode , user database
    outputs: emails(2FA exclusive), logjn or failure message
    '''
    def ConfirmLogin():
        global modeLogin
        global otpCode
        selectedUser = UsernameEntry.get()
        selectedPassword = PasswordEntry.get()
        selectedOTP = OTPEntry.get()
        if modeLogin == "OTP":
            print(CGREEN+"Checking OTP"+CEND)
            try:
                if otpCode == int(selectedOTP):
                    firstRun(0,selectedUser)
                    InitializeForm()
                    loginScreen.withdraw()
                else:
                    print(CRED+"Incorrect OTP detected"+CEND)
                    messagebox.showerror("Error","Incorrect OTP")
                    InitializeForm()
            except:
                print(CRED+"Incorrect OTP detected"+CEND)
                messagebox.showerror("Error","Incorrect OTP")
                InitializeForm()
        else:
            if selectedUser == "admin":
                if selectedPassword == "admin":
                    print(CGREEN+"Loaded as admin"+CEND)
                    firstRun(0,"admin")
                    InitializeForm()
                    loginScreen.withdraw()
                    return False
            file = open("users.csv","r+")
            userLines = file.readlines()
            file.close()
            i = 0
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == selectedUser:
                    if row[1] == selectedPassword:
                        if row[4] != "":

                            try:
                                if connected_ssid == b"gwsc.vic.edu.au":
                                    raise TypeError
                                server = smtplib.SMTP('smtp.office365.com',587)
                                server.starttls()
                                server.login("proofofconcept69420@outlook.com","somerandompassword69420")
                            except:
                                print(CRED+"Network Fail"+CEND)
                                messagebox.showerror("Error","Cannot access the internet. Please reconnect and retry login")
                                InitializeForm()                    
                                return False
                            msg = MIMEMultipart()
                            msg['From'] = 'proofofconcept69420@outlook.com'
                            msg['To']=row[4]
                            msg['Subject'] = 'OTP ALLOCATE++'
                            otpCode = random.randint(0,1000000)
                            message = "Account: "+selectedUser+"\nOTP:"+str(otpCode)
                            msg.attach(MIMEText(message,'plain'))
                            server.send_message(msg)
                            server.quit()
                            print(CGREEN+"OTP sent successfully sent"+CEND)
                            messagebox.showinfo("2 Factor Module","An One Time Password has been sent to your mailbox registered to this email")
                            modeLogin = "OTP"
                            UsernameEntry.config(state='disabled')
                            PasswordEntry.config(state='disabled')
                            OTPEntry.config(state='normal')
                            return False
                        firstRun(0,selectedUser)
                        InitializeForm()
                        print(CGREEN+"Loaded regular user"+CEND)
                        loginScreen.withdraw()
                        return False
                    else:
                        print(CRED+"Auth Fail"+CEND)
                        messagebox.showerror("Error","Incorrect Password provided")
                        InitializeForm()
                        return False
                i+=1
            print(CRED+"Auth missing"+CEND)
            messagebox.showerror("Error","Incorrect user")
            InitializeForm()
    ConfirmButton = tkinter.Button(loginScreen,text="Confirm",fg='green',bd=0,command=ConfirmLogin)
    ConfirmButton.focus_set()
    ConfirmButton.grid(column=1,row=4)
    '''
    name:InitializeForm
    purpose:Clears and initializes the login form
    args: none
    inputs:none
    Outputs: mode changed , form cleared and resetted to default
    '''
    def InitializeForm():
        global modeLogin
        global otpCode
        print(CGREEN+"Form inited"+CEND)
        modeLogin = "Init"
        otpCode = 0
        UsernameEntry.config(state='normal')
        UsernameEntry.delete(0,tkinter.END)
        PasswordEntry.config(state='normal')
        PasswordEntry.delete(0,tkinter.END)
        OTPEntry.config(state='normal')
        OTPEntry.delete(0,tkinter.END)
        OTPEntry.config(state='disabled')
        ConfirmButton.config(text="Confirm",fg='green')
    '''
    name:ConfirmRecovery
    purpose:window to recover a lost account(forgotten password)
    args: none
    inputs: none
    outputs: Window with the capabilities to recover any lost accounts(2FA enabled accounts Only)
    '''
    def ConfirmRecovery():
        if CheckOpen("Recover your account"):return False
        print(CGREEN+"Loaded Recovery screen"+CEND)
        RecoveryScreen = tkinter.Toplevel(loginScreen)
        RecoveryScreen.resizable(0,0)
        RecoveryScreen.title("Recover your account")
        tkinter.Label(RecoveryScreen,text="Enter your username below , a recovery email will be sent if the user has 2FA").grid(column=1,row=0)
        UEntry = tkinter.Entry(RecoveryScreen,width=23)
        UEntry.grid(column=1,row=1)
        '''
        name:FinishRecovery
        purpose:sends message to the email bound to the given user with login info
        args:none
        inputs:user database,provided username to recover
        outputs:email sent or error thrown if use cannot be found
        '''
        def FinishRecovery():
            file = open("users.csv","r+")
            userLines = file.readlines()
            file.close()
            i = 0
            givenU = UEntry.get()
            if givenU == "":
                messagebox.showerror("Error","Fill a valid user")
                return False
            while i<len(userLines):
                row = userLines[i].split(',')
                if len(row)!=userLEN:
                    i+=1
                    continue
                for t in range(len(row)):row[t] = row[t].strip()
                if row[0] == givenU:
                    if row[4] == "":
                        #doesnt throw error to prevent any malactors from knowing that 2FA is disabled
                        break
                    try:
                        if connected_ssid == b"gwsc.vic.edu.au":
                            raise TypeError
                        server = smtplib.SMTP('smtp.office365.com',587)
                        server.starttls()
                        server.login("proofofconcept69420@outlook.com","somerandompassword69420")
                    except:
                        messagebox.showerror("Error","Cannot access the internet. Please reconnect and retry recovery")
                        return False                    
                    msg = MIMEMultipart()
                    msg['From'] = 'proofofconcept69420@outlook.com'
                    msg['To']=row[4]
                    msg['Subject'] = 'Account Recovery ALLOCATE++'
                    message = "Account Recovery has been initiated for your account\nAccount: "+row[0]+"\nPassword:"+row[1]
                    msg.attach(MIMEText(message,'plain'))
                    server.send_message(msg)
                    server.quit()
                i+=1
            messagebox.showinfo("Success","If a user has been found, a email has been sent with the login details")

        tkinter.Button(RecoveryScreen,text="Perform Recovery",command=FinishRecovery,bd=0,fg='blue').grid(column=1,row=2)
    tkinter.Button(loginScreen,text="Recover Acc",bd=0,fg='blue',command=ConfirmRecovery).grid(column=0,row=4)
loginScreen.mainloop()