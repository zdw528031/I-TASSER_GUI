#!/usr/bin/python
import subprocess
import os
import threading
import queue
import inspect
import shutil

class Protein_modoling_task(threading.Thread):
    def __init__(self, queue, file_name, name, sequence_id, LIGHT, LBS,ITASSER_DIR,LIBRARY_DIR,OUTPUT_DIR,task_id=0):
        super(Protein_modoling_task, self).__init__()
        self._stop_event = threading.Event()
        self.queue = queue
        self.file_name = file_name
        self.sequence_id = sequence_id
        self.name = name
        self.LIGHT_MODE = LIGHT
        self.LBS_MODE = LBS
        self.task_id = task_id
        self.ITASSER_DIR = ITASSER_DIR
        self.LIBRARY_DIR = LIBRARY_DIR
        self.OUTPUT_DIR = OUTPUT_DIR
        self.base_directory= os.path.join(os.path.join(OUTPUT_DIR,name),sequence_id)
        self.target_folder = os.path.join(os.path.dirname(__file__),self.name)

        self.generate_output_directory()


    def generate_output_directory(self):
        if not os.path.exists(self.target_folder):
            os.mkdir(self.target_folder)
        self.target_folder = os.path.join(self.target_folder,self.sequence_id)
        if not os.path.exists(self.target_folder):
            os.mkdir(self.target_folder)
        if self.LBS_MODE is "true" and not os.path.exists(os.path.join(self.target_folder,"coach")):
            os.mkdir(os.path.join(self.target_folder,"coach"))

    def stop(self):
        self._stop_event.set()

    def get_LBS(self):
        return self.LBS_MODE

    def get_name(self):
        return self.nam

    def get_sequence_id(self):
        return self.sequence_id

    def run(self):
        print(self.file_name)
        cmd = subprocess.Popen(["perl", os.path.join(self.ITASSER_DIR,"I-TASSERmod/runI-TASSER.pl"), "-pkgdir",
                                self.ITASSER_DIR, "-libdir",self.LIBRARY_DIR,
                                "-seqname",
                                "M", "seq.fasta", "-datadir", self.file_name, "-runstyle", "gnuparallel", "-java_home",
                                "/usr",
                                "-light", self.LIGHT_MODE, "-LBS", self.LBS_MODE], stdout=subprocess.PIPE)

        self.queue.put("create" + "#" + str(self.task_id) + "#" + self.name + ":" + self.sequence_id + "#" + "init...")

        for line in cmd.stdout:
            print(line)
            if self.stopped():
                break
            if line.decode("utf-8")[0].isdigit():
                self.queue.put(
                    "modifiy" + "#" + str(self.task_id) + "#" + self.name + ":" + self.sequence_id + "#" + "state:" +
                    line.decode("utf-8")[0]+" /8 ")
                self.queue.put("add_child" + "#" + str(
                    self.task_id) + "#" + self.name + ":" + self.sequence_id + "#" + "state:" + line.decode("utf-8"))
        self.queue.put("modifiy" + "#" + str(self.task_id) + "#" + self.name + ":" + self.sequence_id + "#" + "state:Done")

        cmd.wait()

    def copy_all_file(self):
        self.copy_protein_file()
        self.copy_cscore_file()
        self.copy_LBS_protein_file()

    def copy_protein_file(self):
        for i in range(5):
            protein_file = os.path.join(self.base_directory,"model"+str(i+1)+".pdb")
            if os.path.exists(protein_file) and not os.path.exists(os.path.join(self.target_folder,"model"+str(i+1)+".pdb")):
                shutil.copy2(protein_file, self.target_folder)

    def copy_cscore_file(self):
        cscore_file = os.path.join(self.base_directory,"cscore")
        if os.path.exists(cscore_file) and not os.path.exists(os.path.join(os.path.join(self.target_folder,"coach"),"cscore")):
            shutil.copy2(cscore_file, self.target_folder)

    def copy_LBS_protein_file(self):
        if self.LBS_MODE is "true":
            LBS_Directory = os.path.join(self.base_directory, "model1")
            LBS_Directory = os.path.join(LBS_Directory, "coach")
            for file in os.listdir(LBS_Directory):
                if file.endswith(".pdb") and ("complex" in file):
                    if not os.path.exists(os.path.join(self.target_folder,file)):
                        shutil.copy2(os.path.join(LBS_Directory,file), os.path.join(self.target_folder,"coach"))

    def stopped(self):
        return self._stop_event.is_set()