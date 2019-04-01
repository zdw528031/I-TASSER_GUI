#!/usr/bin/python
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from config_loader import xml_loader
from protein_task_loader import Protein_modoling_task
import subprocess
import os
import threading
import queue
from functools import partial
import inspect
import shutil


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.queue = queue.Queue()
        self.config = xml_loader()
        self.ITASSER_DIR = self.config.get_ITASSER_DIR()
        self.LIBRARY_DIR = self.config.get_LIBRARY_DIR()
        self.OUTPUT_DIR = self.config.get_OUTPUT_DIR()
        self.task_pool = dict()

    def upate_task_thread(self):
        while True:
            msg = self.queue.get()
            msgs = msg.split("#")
            if msgs[0] == "create":
                self.tree.insert("", int(msgs[1]), values=(msgs[2], msgs[3]))
            if msgs[0] == "modifiy":
                child = self.tree.get_children()
                self.tree.item(child[int(msgs[1])], values=(msgs[2], msgs[3]))
            if msgs[0] == "add_child":
                child = self.tree.get_children()
                self.tree.insert(child[int(msgs[1])], "end", values=(msgs[2], msgs[3]))

    def init_window(self):
        self.master.title("GUI_test")
        self.master.geometry('1100x450')
        self.sequence_input = Text(self.master, height=20, width=45)
        self.sequence_input.place(x=40, y=10)

        self.choose_file_buttom = Button(self.master, text="choose file", command=self.OpenFile)
        self.choose_file_buttom.place(x=40, y=280)

        self.choose_file_buttom = Button(self.master, text="top", command=self.open_top)
        self.choose_file_buttom.place(x=160, y=280)

        self.Stop_buttom = Button(self.master, text="Stop the task", command=self.stop_task)
        self.Stop_buttom.place(x=890, y=10)

        self.Restart_buttom = Button(self.master, text="restart the task")
        self.Restart_buttom.place(x=890, y=50)

        self.open_txt_file = Button(self.master, text="open  txt  file ", command=self.open_cscore_txt)
        self.open_txt_file.place(x=890, y=90)

        self.open_protein_file = Button(self.master, text="Open protein file",command = self.open_new_protein_windows)
        self.open_protein_file.place(x=890, y=130)

        self.light_var = IntVar()
        self.light_mode = Checkbutton(self.master, text="light", variable=self.light_var)
        self.light_mode.place(x=210, y=285)

        self.LBS_var = IntVar()
        self.LBS_MODE = Checkbutton(self.master, text="LBS", variable=self.LBS_var)
        self.LBS_MODE.place(x=260, y=285)

        self.run_buttom = Button(self.master, text="run", command=self.run_start)
        self.run_buttom.place(x=310, y=280)

        self.name_label = Label(self.master, text="*  Name")
        self.name_label.place(x=35, y=320)

        self.name_input = Entry(self.master, width=35)
        self.name_input.place(x=100, y=320)

        self.email_label = Label(self.master, text="    Email")
        self.email_label.place(x=35, y=360)

        self.email_input = Entry(self.master, width=35)
        self.email_input.place(x=100, y=360)

        self.sequence_id_lable = Label(self.master, text="*sequence")
        self.sequence_id_lable.place(x=35, y=400)

        self.sequence_id_input = Entry(self.master, width=35)
        self.sequence_id_input.place(x=100, y=400)

        self.tree = ttk.Treeview(self.master, show="headings", height=20, columns=("sequnce", "status",))

        self.tree.column("sequnce", width=230, anchor="center")
        self.tree.column("status", width=230, anchor="center")

        self.tree.heading("sequnce", text="sequence")
        self.tree.heading("status", text="status")

        self.tree.place(x=400, y=10)

    def open_new_protein_file(self,file_directory,index):
        pdb_file = os.path.join(file_directory,"model"+str(index)+".pdb")
        if not os.path.exists(pdb_file):
            return
        subprocess.Popen([os.path.join(self.config.get_CHIMERA_DIR,"chimera"), pdb_file])

    def open_new_lbs_protein_file(self,file_path):
        if not os.path.exists(file_path):
            return
        subprocess.Popen([os.path.join(self.config.get_CHIMERA_DIR,"chimera"), file_path])

    def open_new_protein_windows(self):
        self.protein_Window = Toplevel(self.master)
        self.protein_Window.geometry('500x500')

        self.protein_lable = Label(self.protein_Window, text="3D protein file")
        self.protein_lable.place(x=10, y=10)
        self.cscore_lable = Label(self.protein_Window, text="C - score value")
        self.cscore_lable.place(x=140, y=10)

        selected_item = self.tree.selection()[0]
        child_set = self.tree.get_children()
        task_id = 0
        for child in child_set:
            if child == selected_item:
                self.task_pool[str(task_id)].stop()
                break
            task_id += 1
        name = self.task_pool[str(task_id)].get_name()
        LBS_mode = self.task_pool[str(task_id)].get_LBS()
        sequence_id = self.task_pool[str(task_id)].get_sequence_id()
        self.protein_Window.title("3D protein file for:" + name + " // " + sequence_id)
        name_directory = os.path.join(self.OUTPUT_DIR, name)
        file_directory = os.path.join(name_directory, sequence_id)
        txt_file = os.path.join(file_directory, "cscore")
        cscore_arrray = []
        if not os.path.exists(txt_file):
            print("cscore file haven't generated yet")
        else:
            with open(txt_file) as fp:
                for line in fp:
                    if "model1" in line:
                        cscore_arrray.append(line.split("   ")[1])
                        continue
                    if "model2" in line:
                        cscore_arrray.append(line.split("   ")[1])
                        continue
                    if "model3" in line:
                        cscore_arrray.append(line.split("   ")[1])
                        continue
                    if "model4" in line:
                        cscore_arrray.append(line.split("   ")[1])
                        continue
                    if "model5" in line:
                        cscore_arrray.append(line.split("   ")[1])
                        break
        print("finish read")
        print(cscore_arrray)
        open_model1 = partial(self.open_new_protein_file, file_directory,1)
        self.model_1_buttom = Button(self.protein_Window, text="model_1",command = open_model1)
        self.model_1_buttom.place(x=20, y=50)
        open_model2 = partial(self.open_new_protein_file, file_directory,2)
        self.model_2_buttom = Button(self.protein_Window, text="model_2",command = open_model2)
        self.model_2_buttom.place(x=20, y=90)
        open_model3 = partial(self.open_new_protein_file, file_directory,3)
        self.model_3_buttom = Button(self.protein_Window, text="model_3",command = open_model3)
        self.model_3_buttom.place(x=20, y=130)
        open_model4 = partial(self.open_new_protein_file, file_directory,4)
        self.model_4_buttom = Button(self.protein_Window, text="model_4",command = open_model4)
        self.model_4_buttom.place(x=20, y=170)
        open_model5 = partial(self.open_new_protein_file, file_directory,5)
        self.model_5_buttom = Button(self.protein_Window, text="model_5",command = open_model5)
        self.model_5_buttom.place(x=20, y=210)

        self.model_1_cscore_label = Label(self.protein_Window, text=cscore_arrray[0])
        self.model_1_cscore_label.place(x=140, y=50)

        self.model_2_cscore_label = Label(self.protein_Window, text=cscore_arrray[1])
        self.model_2_cscore_label.place(x=140, y=90)

        self.model_3_cscore_label = Label(self.protein_Window, text=cscore_arrray[2])
        self.model_3_cscore_label.place(x=140, y=130)

        self.model_4_cscore_label = Label(self.protein_Window, text=cscore_arrray[3])
        self.model_4_cscore_label.place(x=140, y=170)

        self.model_5_cscore_label = Label(self.protein_Window, text=cscore_arrray[4])
        self.model_5_cscore_label.place(x=140, y=210)

        if LBS_mode is "true":
            self.LBS_file_label = Label(self.protein_Window, text="LBS protein file")
            self.LBS_file_label.place(x=270, y=10)
            LBS_Directory = os.path.join(file_directory,"model1")
            LBS_Directory = os.path.join(LBS_Directory, "coach")
            LBS_Protein_file_array = []
            for file in os.listdir(LBS_Directory):
                if file.endswith(".pdb") and ("complex" in file):
                    LBS_Protein_file_array.append(file)
                    print(file)
            self.LBS_button_array = []
            self.LBS_command_array = []
            low_bounce = 50
            for LBS_Protein_file in LBS_Protein_file_array:
                open_LBS_file = partial(self.open_new_lbs_protein_file,os.path.join(LBS_Directory,LBS_Protein_file))
                button = Button(self.protein_Window, text=LBS_Protein_file,command = open_LBS_file)
                button.place(x=270, y=low_bounce)
                low_bounce += 40
                self.LBS_button_array.append(button)

    def client_exit(self):
        exit()

    def stop_task(self):
        selected_item = self.tree.selection()[0]
        child_set = self.tree.get_children()
        task_id = 0
        for child in child_set:
            if child == selected_item:
                self.task_pool[str(task_id)].stop()
                break
            task_id += 1
        self.tree.delete(selected_item)

    def open_cscore_txt(self):
        selected_item = self.tree.selection()[0]
        child_set = self.tree.get_children()
        task_id = 0
        for child in child_set:
            if child == selected_item:
                self.task_pool[str(task_id)].stop()
                break
            task_id += 1
        name = self.task_pool[str(task_id)].get_name()
        sequence_id = self.task_pool[str(task_id)].get_sequence_id()
        name_directory = os.path.join(self.OUTPUT_DIR, name)
        file_directory = os.path.join(name_directory, sequence_id)
        txt_file = os.path.join(file_directory, "cscore")
        if not os.path.exists(txt_file):
            print("file haven't generated yet")
        else:
            subprocess.Popen(["gedit", txt_file])

    def open_top(self):
        subprocess.call(["gnome-terminal", "--command= top"])

    def run_start(self):
        sequence = self.sequence_input.get("1.0", "end-1c")
        print("sequence: " + sequence)

        name = self.name_input.get()
        print("name: " + name)

        email = self.email_input.get()
        print("email: " + email)

        sequence_id = self.sequence_id_input.get()
        print("sequence_id: " + sequence_id)

        file_name = self.create_enviornment(sequence, name, sequence_id)

        task_id = len(self.tree.get_children())
        p = Protein_modoling_task(self.queue, file_name, name, sequence_id, self.get_light_mode(), self.get_LBS_mode(),self.ITASSER_DIR,self.LIBRARY_DIR,self.OUTPUT_DIR,task_id)
        p.start()
        self.task_pool[str(task_id)] = p

    def create_enviornment(self, sequence_input, name, sequence_id,file_name="seq.fasta"):
        # todo: add config xml here instead of hard code here
        name_directory = os.path.join(self.OUTPUT_DIR, name)
        if not os.path.exists(name_directory):
            os.makedirs(name_directory)
        print(name)

        sequence_input_directory = os.path.join(name_directory, sequence_id)
        if not os.path.exists(sequence_input_directory):
            os.makedirs(sequence_input_directory)

        file_name = os.path.join(sequence_input_directory, file_name)
        f = open(file_name, "w+")  # create a new file
        f.write(">seq1\n")
        f.write(sequence_input)
        f.close()
        return file_name

    def get_light_mode(self):
        LIGHT_MODE = "true"
        if self.light_var.get() == 0:
            LIGHT_MODE = "false"
        return LIGHT_MODE

    def get_LBS_mode(self):
        LBS_MODE = "true"
        if self.LBS_var.get() == 0:
            LBS_MODE = "false"
        return LBS_MODE

    def OpenFile(self):
        name = askopenfilename(initialdir=self.OUTPUT_DIR,
                               filetypes=(
                                   ("protein sequence file", "*.fasta"), ("Text File", "*.txt"), ("All Files", "*.*")),
                               title="please choose a input file")
        print("file name: " + name)
        # Using try in case user types in unknown file or closes without choosing a file.
        try:
            with open(name, 'r') as UseFile:
                self.sequence_input.delete('1.0', END)
                self.sequence_input.insert(chars=UseFile.read().replace(">seq1\n",""), index=END)
        except:
            print("No file exists")


root = Tk()
app = Window(root)
thread1 = threading.Thread(target=app.upate_task_thread, args=())
thread1.start()
root.mainloop()

