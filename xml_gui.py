
#region imports
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pyautogui
from datetime import datetime
import uuid
from TkTreectrl import *
import TkTreectrl as treectrl
import os
from lxml import etree
from io import StringIO, BytesIO
import elementpath
import xml.etree.ElementTree as ET
#endregion

getRes = pyautogui.size()
resolution = str(getRes[0]) + "x" + str(getRes[1])
main_window = Tk()
main_window.geometry(resolution) ###########################################resolution
main_window.title("XML GUI")
main_window.configure()
main_window.state("zoomed")
#main_window.attributes('-fullscreen', True)
none="none" # προσωρινο για μεταβαση σε frames
previous_frame="previous_frame"
frame_counter=0
init_pass=0
mydir=os.getcwd()
daylist=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]


#region Frames For Main Window
frame_temp=Frame()#Frame to get as temp to successfull change between frames
school_Frame=Frame(main_window, bg="white")
school_menu_Frame=Frame(school_Frame, bg="gray26")
school_intro_Frame = Frame(school_Frame, bg="floral white")
add_data_Frame = Frame(school_Frame, bg="floral white")
show_results_Frame= Frame(school_Frame, bg="floral white")
#endregion


def ExitApp():
    MsgBox = messagebox.askquestion('Έξοδος Εφαρμογής!', 'Είστε σίγουροι ότι θέλετε να αποσυνδεθείτε από την Εφαρμογή ;', icon='warning')
    if MsgBox == 'yes':
        main_window.destroy()
    else:
        messagebox.showinfo('Επιστροφή', 'Θα επιστραφείτε στην προηγούμενη σας οθόνη !')

def raiseNdrop_frame(frameUp,frameDown):
    global frame_counter
    global init_pass #flag to see if menu frame has appeared (0 is  no, 1 is yes)
    global frame_temp #απλα οριζω οτι το frame temp εινια τυπου frame γιατι αλλιως προβλημα στο forget γτ το διαβάζει ως string

    #print(frameDown)
    if(frameDown!="none"):
        if(frameDown=="previous_frame"):#forget previous frame
            frame_counter=0
            #print("going to delete frame: ",frame_temp)
            frame_temp.pack_forget()    
        else:
            frameDown.pack_forget()
    
    if(frame_counter==0 and init_pass==1 ):   #frame to close (memory)
        temp2=0
        frame_counter=1
        frame_temp=frameUp
        #print("memory",frame_temp)
    

    if(frameUp==school_menu_Frame):
        frameUp.tkraise()
        frameUp.pack(side=LEFT, fill=Y)
        init_pass=1
    else:
        frameUp.tkraise()
        frameUp.pack(expand=1,fill=BOTH)


##### METABLHTES GIA DIRECTORY ARXEIWN 
xml_file_tk = StringVar()#(label_AddData_all_mt8l_left)
xsd_file_tk = StringVar()#(label_AddData_all_mt9l_left)
xml_file_tk.set("")
xsd_file_tk.set("")

##### METABLHTES GIA ONOMA ARXEIWN
xml_filename=""
xsd_filename=""
##### METABLHTES GIA PATH ARXEIWN
xml_path=""
xsd_path=""


def browse_xml():  #filedialog documentation  για λεπτομερειες 
    # Allow user to select a file and store it in global variable xml_file_tk  και ασφάλεια από λάθος αρχείο
    global xml_file_tk
    global xml_filename
    global xml_path
    file_path_xml = filedialog.askopenfilename()
    file_type=file_path_xml.split(".")
    if(file_type[-1]=="xml"): #αν το τελευταιο στοιχειο της λιστας είναι το string xml
        xml_path=file_path_xml#path
        file_split=file_path_xml.split("/")
        xml_filename=file_split[-1]
        xml_file_tk.set(xml_filename)
        print(xml_filename)
    else:
        msg_error_form = messagebox.showerror('Πρόβλημα Αρχείου!', 'Παρακαλώ επιλέξτε ένα αρχείο τύπου xml!', icon='warning')
        file_path_xml=""
        xml_filename=""
        xml_path=""
        xml_file_tk.set("")



def browse_xsd():  #filedialog documentation  για λεπτομερειες 
    # Allow user to select a file and store it in global variable xsd_file_tk  και ασφάλεια από λάθος αρχείο
    global xsd_file_tk
    global xsd_filename
    global xsd_path
    file_path_xsd = filedialog.askopenfilename()
    file_type2=file_path_xsd.split(".")
    if(file_type2[-1]=="xsd"): #αν το τελευταιο στοιχειο της λιστας είναι το string xsd
        xsd_path=file_path_xsd#path
        file_split2=file_path_xsd.split("/")
        xsd_filename=file_split2[-1]
        xsd_file_tk.set(xsd_filename)
        print(xsd_filename)
    else:
        msg_error_form = messagebox.showerror('Πρόβλημα Αρχείου!', 'Παρακαλώ επιλέξτε ένα αρχείο τύπου xsd!', icon='warning')
        file_path_xsd=""
        xsd_filename=""
        xsd_path=""
        xsd_file_tk.set("")

def confirm_files():
    global xml_path
    global xsd_path
    global tree
    #SCHEMA VALIDATOR WITH LXML
    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    
    xml_doc = etree.parse(xml_path)
    result = xmlschema.validate(xml_doc)

    if(result): #AN EPITYXIA
        MsgBox = messagebox.showerror('Schema Validation!', 'Επιτυχής επικύρωση αρχείων! Τώρα μπορείτε να περιηγηθείτε στο υπόλοιπο πρόγραμμα!', icon='warning')
        tree = etree.parse(xml_path)#για χρηση στην ADD ELEMENT
    else:
        messagebox.showerror('Schema Validation!', 'Σφάλμα επικύρωσης αρχείων! \nΠαρακαλώ διορθώστε τα αρχεία και προσπαθήστε ξανά!')

def main():
    global exams_dates#list containing data from memory exams school

    school_menu = Label(school_menu_Frame, bg="gray26",font=("Calibri", 24, "bold"))  # aristero menu
    smenu_l_up = Label(school_menu, borderwidth=1, highlightthickness=0, bg="gray26")  # photo parmenidi
    smenu_l_down = Label(school_menu, borderwidth=1, highlightthickness=0,bg="gray26")  # button gia menu kai alla frames

    initialPage_all = Label(school_intro_Frame, borderwidth=1, highlightthickness=0, bg="floral white")  # dexia arxikh selida
    initialPage_all_top = Label(initialPage_all, text='Καλώς ορίσατε στο XML GUI!',borderwidth=1, highlightthickness=0, bg="floral white",font=("Times New Roman (Times)", 36, "bold"))
    initialPage_all_bot = Label(initialPage_all, borderwidth=1, highlightthickness=0, bg="floral white")
    initialPage_ab_top = Label(initialPage_all_bot, text='Παρακαλώ επιλέξτε τα XML ΚΑΙ XML Schema αρχεία πριν προχωρείσετε!',borderwidth=1, highlightthickness=0, bg="floral white",font=("Times New Roman (Times)", 25, "bold"))
    initialPage_ab_bot = Label(initialPage_all_bot, borderwidth=1, highlightthickness=0, bg="floral white")

    initialPage_abb_top = Label(initialPage_ab_bot, borderwidth=1, highlightthickness=0, bg="floral white")
    initialPage_abbt_left = Label(initialPage_abb_top, text='Αρχείο XML:',borderwidth=1, highlightthickness=0, bg="floral white",font=("Times New Roman (Times)", 25, "bold"))
    initialPage_abbt_mid =  Label(initialPage_abb_top, bg="gray",font=("Times New Roman (Times)", 18, "bold"),fg="blue",textvariable=xml_file_tk)# η μεταβλητη εχει οριστει πανω απο την συναρτηση που καλειται browse_form

    initialPage_abb_mid = Label(initialPage_ab_bot, borderwidth=1, highlightthickness=0, bg="floral white")
    initialPage_abbm_left = Label(initialPage_abb_mid, text='Αρχείο XSD:',borderwidth=1, highlightthickness=0, bg="floral white",font=("Times New Roman (Times)", 25, "bold"))
    initialPage_abbm_mid =  Label(initialPage_abb_mid, bg="gray",font=("Times New Roman (Times)", 18, "bold"),fg="blue",textvariable=xsd_file_tk)# η μεταβλητη εχει οριστει πανω απο την συναρτηση που καλειται browse_form

    initialPage_abb_bot = Label(initialPage_ab_bot, borderwidth=1, highlightthickness=0, bg="floral white")

    #orismos buttons
    btn_next0 = Button(smenu_l_down, text="Αρχική Σελίδα", command=lambda: raiseNdrop_frame(school_intro_Frame,previous_frame), bg="gray26",height = 2, width = 35,font=("Calibri", 14, "bold"))
    btn_next1 = Button(smenu_l_down, text="Προσθήκη Δεδομένων", command=lambda: raiseNdrop_frame(add_data_Frame,previous_frame), bg="gray26",height = 2, width = 35,font=("Calibri", 14, "bold"))
    btn_next2 = Button(smenu_l_down, text="Αποτελέσματα", command=lambda: raiseNdrop_frame(show_results_Frame,previous_frame), bg="gray26",height = 2, width = 35,font=("Calibri", 14, "bold")) 
    btn_next3 = Button(smenu_l_down, text="Έξοδος", command=lambda: ExitApp(), bg="gray26",height = 2, width = 35,font=("Calibri", 14, "bold"))

    #browse_buttons
    buttton_browse_xml = Button(initialPage_abb_top, text="Αναζήτηση", command=lambda:browse_xml(), bg="floral white",font=("Times New Roman (Times)", 14, "bold"),height=1 ,width=15)
    buttton_browse_xsd = Button(initialPage_abb_mid, text="Αναζήτηση", command=lambda:browse_xsd(), bg="floral white",font=("Times New Roman (Times)", 14, "bold"),height=1 ,width=15)

    #confirm btn
    buttton_confirm_files = Button(initialPage_abb_bot, text="Επιβεβαίωση", command=lambda: confirm_files(),bg="green4",font=("Times New Roman (Times)", 14, "bold"),height=1 ,width=15)

    #packs εμφάνιση στοιχείων
    school_menu.pack(side=LEFT,expand=1,fill=Y)
    smenu_l_up.pack(side=TOP,pady=50)#PARMENIDIS LOGO
    smenu_l_down.pack(side=TOP)#CONTAINS BUTTONS
    initialPage_all.pack(side=TOP,fill=BOTH,expand=1)#δεξιο μενου-αρχικη σελίδα
    initialPage_all_top.pack(side=TOP,fill=X)
    initialPage_all_bot.pack(side=LEFT, expand=1, fill=BOTH)
    initialPage_ab_top.pack(side=TOP, fill=X, pady=60)


    #κατω πλευρα μαμα με btns 
    initialPage_ab_bot.pack(side=TOP, expand=1, fill=BOTH)
    #browse xml
    initialPage_abb_top.pack(side=TOP,pady=2,expand=1,fill=X, padx=30)
    initialPage_abbt_left.pack(side=LEFT,padx=10)
    initialPage_abbt_mid.pack(side=LEFT,padx=5,expand=1,fill=X)
    #browse xsd
    initialPage_abb_mid.pack(side=TOP,pady=2,expand=1,fill=X, padx=30)
    initialPage_abbm_left.pack(side=LEFT,padx=10)
    initialPage_abbm_mid.pack(side=LEFT,padx=5,expand=1,fill=X)
    #confirm
    initialPage_abb_bot.pack(side=TOP,expand=1, fill=BOTH)

    #buttons MENU
    btn_next0.pack(side=TOP,pady=2,ipady=5)
    btn_next1.pack(side=TOP,pady=2,ipady=5)
    btn_next2.pack(side=TOP,pady=2,ipady=5)
    btn_next3.pack(side=TOP,pady=2,ipady=5)
    #search and confirm btns
    buttton_browse_xml.pack(side=LEFT)
    buttton_browse_xsd.pack(side=LEFT)
    buttton_confirm_files.pack(side=RIGHT,padx=50)

        #ΑΡΧΙΚΑ FRAMES ΕΜΦΑΝΙΣΗ
    raiseNdrop_frame(school_Frame,none)
    raiseNdrop_frame(school_menu_Frame,none)
    raiseNdrop_frame(school_intro_Frame,none)  


    #---------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------

    #statement_Frame1 δηλωση Συμμετοχής
    label_AddData_all = Label(add_data_Frame, bg="floral white")
    label_AddData_all_top = Label(label_AddData_all, text="Προσθήκη Νέων Δεδομένων(Lectures)",  bg="floral white",font=("Times New Roman (Times)", 36, "bold"),fg="dodger blue")
    label_AddData_all_mid_top = Label(label_AddData_all, relief="groove", borderwidth=2, highlightthickness=2,  bg="floral white")
    label_AddData_all_down = Label(label_AddData_all_mid_top, bg="floral white")

    label_AddData_all_m_t1 = Label(label_AddData_all_mid_top, bg="floral white")
    label_AddData_all_mt1_left = Label(label_AddData_all_m_t1, text="Title:          ",  bg="floral white",font=("Times New Roman (Times)", 20, "bold"),fg="black")
    info_text_Title = Text(label_AddData_all_m_t1, bg="WHITE", height=1, width=20, fg="black", borderwidth=2, highlightthickness=2,font=("Times New Roman (Times)", 20))

    label_AddData_all_m_t2 = Label(label_AddData_all_mid_top, bg="floral white")
    label_AddData_all_mt2_left = Label(label_AddData_all_m_t2, text="Professor: ",  bg="floral white",font=("Times New Roman (Times)", 20, "bold"),fg="black")
    info_text_Professor = Text(label_AddData_all_m_t2, bg="WHITE", height=1, width=20, fg="black", borderwidth=1, highlightthickness=2,font=("Times New Roman (Times)", 20))
    
    label_AddData_all_m_t4 = Label(label_AddData_all_mid_top, bg="floral white")
    label_AddData_all_mt4_left = Label(label_AddData_all_m_t4, text="Day:           ",  bg="floral white",font=("Times New Roman (Times)", 20, "bold"),fg="black")
    info_text_Day = Text(label_AddData_all_m_t4, bg="WHITE", height=1, width=20, fg="black", borderwidth=1, highlightthickness=2,font=("Times New Roman (Times)", 20))
    
    #BUTTON CONFIRMATION
    buttton_confirm = Button(label_AddData_all_down, text="Επιβεβαίωση", command=lambda: confirm_choice(),bg="green4",font=("Times New Roman (Times)", 14, "bold"),height=1 ,width=12)
    
    
    #ΠΡΟΧΕΙΡΗ ΤΟΠΟΘΕΤΗΣΗ ΣΥΝΑΡΤΗΣΗΣ----------------------------------------------------------
    def confirm_choice():
        global daylist
        global xml_path
        global tree
        day_ok_check=0
        errorT=0
        errorP=0
        errorD1=0
        errorD2=0
        data_title = info_text_Title.get('1.0', 'end-1c')
        data_professor = info_text_Professor.get('1.0', 'end-1c')
        data_day = info_text_Day.get('1.0', 'end-1c')
        for elem_day in daylist:
            if(data_day==elem_day):
                day_ok_check=1

        if (data_title==""):#if empty
            errorT=1
        if (data_professor==""):#if empty
            errorP=1
        if (data_day==""):#if empty
            errorD1=1
        if (day_ok_check==0):#if not correct day writing
            errorD2=1

        if(errorT==1|errorP==1|errorD1|errorD2==1):
            #clear τα text!!!!
            messagebox.showinfo('Αποτυχία', 'Παρακαλώ ελέγξτε πως δεν έχετε αφήσει κενό κάποιο input είτε δεν έχετε γράψει σωστά την ημέρα(Σωστός τύπος μέρας πχ MondayTuesday)!')
        else:
            msg_confirmation = messagebox.askquestion('Επιβεβαίωση!', 'Είστε σίγουροι ότι θέλετε να κάνετε εισαγωγή αυτών των στοιχείων;',icon='warning')
            if msg_confirmation == 'yes':
                #get value from user
                data_title_final = info_text_Title.get('1.0', 'end-1c')
                data_professor_final = info_text_Professor.get('1.0', 'end-1c')
                data_day_final = info_text_Day.get('1.0', 'end-1c')
                #clear ta text
                #info_text_Title.config(state=DISABLED)#to be un editable
                #info_text_Professor.config(state=DISABLED)#to be un editable
                #info_text_Day.config(state=DISABLED)#to be un editable

                ##PARSE XML
                
                root = tree.getroot()
                lesson = etree.Element("Lesson")
                title = etree.SubElement(lesson,"Title")
                title.text = data_title_final
                lecture = etree.SubElement(lesson,"Lecture")
                day = etree.SubElement(lecture,"Day")
                day.text = data_day_final
                professor = etree.SubElement(lesson,"Professor")
                professor.text = data_professor_final
                #etree.dump(lesson)
                root.append(lesson)#ADD Lesson
                etree.dump(root)
                tree.write('XMLoutput.xml')



                messagebox.showinfo('Oλοκλήρωση', 'Η εισαγωγή δεδομένων έγινε με επιτυχία!\nΜπορείτε να ελέγξετε το XMLoutput.xml αρχείο στο directory για να δείτε την επιτυχή εισαγωγή τν στοιχείων.')

            else:
                messagebox.showinfo('Αποτυχία', 'Αποτυχία εισαγωγής δεδομένων!')



    ###EMFANISH LABELS BUTTONS MENU KLP
    label_AddData_all.pack(side=TOP, expand=1, fill=BOTH)
    label_AddData_all_top.pack(side=TOP)
    label_AddData_all_mid_top.pack(side=TOP, expand=1, fill=BOTH, pady=100)
    label_AddData_all_down.pack(side=BOTTOM, expand=1, fill=X)

    label_AddData_all_m_t1.pack(side=TOP,expand=1,fill=X, padx=100)
    label_AddData_all_mt1_left.pack(side=LEFT,ipadx=10)
    info_text_Title.pack(side=RIGHT,expand=1, fill=X)

    label_AddData_all_m_t2.pack(side=TOP,expand=1,fill=X, padx=100)
    label_AddData_all_mt2_left.pack(side=LEFT,ipadx=10)
    info_text_Professor.pack(side=RIGHT,expand=1, fill=X)


    label_AddData_all_m_t4.pack(side=TOP,expand=1,fill=X, padx=100)
    label_AddData_all_mt4_left.pack(side=LEFT,ipadx=10)
    info_text_Day.pack(side=RIGHT,expand=1, fill=X)

    buttton_confirm.pack(side=RIGHT,padx=50)



    # ---------------------------ΑΝΑΚΟΙΝΩΣΕΙΣ END, Start of PAGE ΑΝΑΚΟΙΝΩΣΕΙΣ---------------------------
    #---------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    
    #statement_Frame2 δηλωση μαθημάτων
    label_results_all = Label(show_results_Frame, bg="floral white")
    label_results_all_top = Label(label_results_all, text="Περιεχόμενα XML Αρχείου",  bg="floral white",font=("Times New Roman (Times)", 36, "bold"),fg="dodger blue")
    label_results_all_mid = Label(label_results_all, relief="groove", borderwidth=2, highlightthickness=2,  bg="floral white")
    label_results_m_mid = Label(label_results_all_mid, bg="floral white")
    label_results_m_bottom = Label(label_results_all_mid, bg="floral white")


    # sos sos sos sos sos sos προσθήκη textvariable ώστε να ανανεώνεται από δεδομένα ΄βασης δεδομένων 



    ### MIDDLE LABELS LESSONS
    label_results_mm_top = Label(label_results_m_mid, bg="floral white") #panw meros middle kateyuynsh : 8etikh klp
    label_results_mmt_left = Label(label_results_mm_top, text="Φιλτράρισμά: ",  bg="floral white",font=("Times New Roman (Times)", 18, "bold"),fg="black")
    label_results_mmt_right = Label(label_results_mm_top, bg="floral white",fg="black") #option menu για κατευθυνσεις και κουμπι για επιβεβαιωση-συναρτηση αλλαγης textvariables kai pack labels
    #epishs isws na xreiazetai synarthsh poy me bash ta stoixeia tou root na allazei ta posa label exoume me textvariables me bash to ka8e systhma 

    label_results_mm_mid = Label(label_results_m_mid, bg="floral white") #ma8hmata kai ma8hmata eidikhw kathgorias

    #ΑΡΙΣΤΕΡΑ ΜΑΘΗΜΑΤΑ
    label_results_mmm_left = Label(label_results_mm_mid, bg="floral white",relief='groove')
    label_results_mmml_top = Label(label_results_mmm_left, text="Μάθημα(Lesson)",  bg="floral white",font=("Times New Roman (Times)", 18, "bold"),fg="black")
    label_results_mmml_top1 = Label(label_results_mmm_left, bg="floral white")
    
    #Καθηγητές
    label_results_mmm_right = Label(label_results_mm_mid, bg="floral white",relief='groove')
    label_results_mmmr_top = Label(label_results_mmm_right, text="Μέρα(Day)Καθηγητής(Professor)",  bg="floral white",font=("Times New Roman (Times)", 20, "bold"),fg="black")
    label_results_mmmr_top1 = Label(label_results_mmm_right, bg="floral white")

    #Ημερομηνία
    label_results_mmm_right2 = Label(label_results_mm_mid, bg="floral white",relief='groove')
    label_results_mmmr2_top = Label(label_results_mmm_right2, text="Καθηγητής(Professor)",  bg="floral white",font=("Times New Roman (Times)", 20, "bold"),fg="black")
    label_results_mmmr2_top1 = Label(label_results_mmm_right2, bg="floral white")

    #Option Menu  για τα Μαθήματα  ΚΑΘΗΓΗΤΕΣ ΚΑΙ ΜΕΡΑ
    lessons_list  = Listbox (label_results_mmml_top1, bg="floral white", borderwidth=2, highlightthickness=0, selectmode='multiple', export=FALSE, activestyle=none, width = 35, height=20)
    professors_list  = Listbox (label_results_mmmr2_top1, bg="floral white", borderwidth=2, highlightthickness=0, selectmode='multiple', export=FALSE, activestyle=none, width = 35, height=20)
    day_list  = Listbox (label_results_mmmr_top1, bg="floral white", borderwidth=2, highlightthickness=0, selectmode='multiple', export=FALSE, activestyle=none, width = 35, height=20)


    def yview_me():
        lessons_list.yview
        professors_list.yview
        day_list.yview
    
    def χview_me():
       lessons_list.yview
       professors_list.yview
       day_list.yview

    #ORISMOS SCROLL BAR
    scrollbarh2 = Scrollbar(label_results_mm_mid, orient="horizontal", command=χview_me())
    scrollbarv2= Scrollbar(label_results_mm_mid, orient="vertical", command=yview_me())

    #SCROLL BINDING TO LISTBOXES
    #Lesson
    label_results_mm_mid.bind("<Configure>",lambda e: lessons_list.configure(scrollregion=lessons_list.bbox("all")))
    lessons_list.configure(yscrollcommand=scrollbarv2.set, xscrollcommand=scrollbarh2.set, font=("Times New Roman (Times)", 18,"bold"))
    label_results_mm_mid.bind("<MouseWheel>", scrollbarv2)#ΚΑΘΕΤΟ SCROLL ΜΕ ΡΟΔΑ ΠΟΝΤΙΚΙΟΥ
    #Professor
    label_results_mmmr_top1.bind("<Configure>",lambda e: professors_list.configure(scrollregion=professors_list.bbox("all")))
    professors_list.configure(yscrollcommand=scrollbarv2.set, xscrollcommand=scrollbarh2.set, font=("Times New Roman (Times)", 18,"bold"))
    #DAY
    label_results_mmmr_top1.bind("<Configure>",lambda e: day_list.configure(scrollregion=day_list.bbox("all")))
    day_list.configure(yscrollcommand=scrollbarv2.set, xscrollcommand=scrollbarh2.set, font=("Times New Roman (Times)", 18,"bold"))


    day_names = ['All_Days','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day_value = StringVar(label_results_mmt_right)
    day_value.set(day_names[0])#ΑΡΧΙΚΗ ΤΙΜΗ Κατέυθυνσης
    day_choice = OptionMenu(label_results_mmt_right, day_value, *day_names)
    day_choice.config(bg="snow", width=20)

    btn_conf_direction = Button(label_results_mm_top, text="Επιβεβαίωση", command=lambda: show_xml_results(), bg="green4",font=("Times New Roman (Times)", 14, "bold"),height=1 ,width=15)

    def show_xml_results(): #sos sos proxeira topo8ethsh
        lessons_list.insert(1,"Artificial Intelligence")
        lessons_list.insert(2,"Artificial Intelligence")
        lessons_list.insert(3,"Artificial Intelligence")
        lessons_list.insert(4,"Constraint Satisfaction Problems")
        lessons_list.insert(5,"Knowledge Representation in Web")
        lessons_list.insert(6,"TestTitle")
        
        day_list.insert(1,"Wednesday")
        day_list.insert(2,"Thursday")
        day_list.insert(3,"Friday")
        day_list.insert(4,"Monday")
        day_list.insert(5,"Friday")
        day_list.insert(6,"Saturday")
        professors_list.insert(1,"Hatzilygeroudis")
        professors_list.insert(2,"Hatzilygeroudis")
        professors_list.insert(3,"")
        professors_list.insert(4,"")
        professors_list.insert(5,"Hatzilygeroudis")
        professors_list.insert(2,"Stelios Vazaios")


        global tree
        root2 = tree.getroot()
        lessons_list.delete(0,'end')
        professors_list.delete(0,'end')
        day_list.delete(0,'end')
        ###StringVar  για να πάρει το τρεχον σύστημα και με  βαση αυτό και την κατεύθυνση να πάρει τα elements απο το dictionary
        day_save= day_value.get()#τρέχουσα επιλεγμενη κατεύθυνση
        row_count=1
        if (day_save== "All_Days"):
            #initialization of array
            lessons_list.delete(0,'end')
            professors_list.delete(0,'end')
            day_list.delete(0,'end')

            for Lesson in root2.findall('Lesson'):#search for all Lesson elements
                #etree.dump(root)
                title_name = lesson_elem.find('Title').text #get title
                professor_name = lesson_elem.find('Professor').text #get professor
                for Lecture in lesson_elem.findall('Lecture'): #for each lecture-Day add to listbox
                    lecture_day = lecture_elem.find('Day').text
                    #insert data to lists
                    lessons_list.insert(row_count,"title_name")
                    professors_list.insert(row_count,professor_name)
                    day_list.insert(row_count,lecture_day)
                    row_count+=1

        elif(day_save== "Monday"):
            #initialization of array
            lessons_list.delete(0,'end')
            professors_list.delete(0,'end')
            day_list.delete(0,'end')

        elif(day_save== "Tuesday"):
            #initialization of array
            lessons_list.delete(0,'end')
            professors_list.delete(0,'end')
            day_list.delete(0,'end')

        elif(day_save== "Wednesday"):
            #initialization of array
            lessons_list.delete(0,'end')
            professors_list.delete(0,'end')
            day_list.delete(0,'end')

        elif(day_save== "Thursday"):
            #initialization of array
            lessons_list.delete(0,'end')
            professors_list.delete(0,'end')
            day_list.delete(0,'end')

        elif(day_save== "Friday"):
            #initialization of array
            lessons_list.delete(0,'end')
            professors_list.delete(0,'end')
            day_list.delete(0,'end')

        elif(day_save== "Saturday"):
            #initialization of array
            lessons_list.delete(0,'end')
            professors_list.delete(0,'end')
            day_list.delete(0,'end')

        elif(day_save== "Sunday"):
            #initialization of array
            lessons_list.delete(0,'end')
            professors_list.delete(0,'end')
            day_list.delete(0,'end')
        




    #pack -emfanish stoixeiwn selidas-frame

    #MIDDLE KATEYUYNSH- MAUHMATA SYNOLIKA
    label_results_mm_top.pack(side=TOP, expand=1, fill=BOTH,padx=10)
    label_results_mmt_left.pack(side=LEFT)
    label_results_mmt_right.pack(side=LEFT, padx=5)
    day_choice.pack()

    label_results_mm_mid.pack(side=TOP, expand=1, fill=BOTH,padx=20)
    
    
    #Εμφάνιση SCROLL
    scrollbarv2.pack(side=RIGHT, fill=Y)
    scrollbarh2.pack(side=BOTTOM, fill=X)
    #MIDDLE MA8HAMATA ARISTERA
    label_results_mmm_left.pack(side=LEFT)
    label_results_mmml_top.pack(side=TOP)
    label_results_mmml_top1.pack(side=TOP)
    


    #MIDDLE  DEXIA
    label_results_mmm_right.pack(side=LEFT)
    label_results_mmmr_top.pack(side=TOP)
    label_results_mmmr_top1.pack(side=TOP)
    #Εμφάνιση ListBox
    lessons_list.pack(side=LEFT, fill=BOTH, expand=1)
    professors_list.pack(side=LEFT, fill=BOTH, expand=1)
    day_list.pack(side=LEFT, fill=BOTH, expand=1)
    

    

    label_results_mmm_right2.pack(side=LEFT)
    label_results_mmmr2_top.pack(side=TOP)
    label_results_mmmr2_top1.pack(side=TOP)


    #EXWTERIKA LABELS SYNOLIKA FATHER LABELS OF FRAME
    label_results_all.pack(side=TOP, expand=1, fill=BOTH)
    label_results_all_top.pack(side=TOP)
    label_results_all_mid.pack(side=LEFT, expand=1, fill=BOTH, pady=50)
    label_results_m_mid.pack(side=TOP, expand=1, fill=BOTH)
    label_results_m_bottom.pack(side=BOTTOM, expand=1, fill=BOTH,padx=20)

    btn_conf_direction.pack(side=LEFT, padx=50)



    main_window.mainloop()  # ------------------------------Put always to end of frames


main()