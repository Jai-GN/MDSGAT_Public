#################################################################################
# Program: MDS Generator & Analysis Tool (MDSGAT)                               #
# Author: Jai Geddes Nelson                                                     #
# Affiliations: School of Biomedical Engineering (University of Sydney) &       #
#               Nanobiophotonics Lab Research Group (University of Sydney)      #
# Last Updated Date: 25/05/2024                                                 #
#                                                                               #
# Description:                                                                  #
# Used for the automatic generation of MDS scripts for use with the GROMACS     #
# MDS package on a HPC system (ideally with PBS job queues).                    #
# The program aims to drastically lower the barrier of entry to run             #
# Molecular Dynamics Simulations alongside reduce the complexity of analysing   #
# them by automating much of the process and implementing easy-to-understand    #
# GUI elements for the remainder of processes required.                         #
#################################################################################

# Import Packages
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
from tkinter import messagebox
from tktooltip import ToolTip
import customtkinter
import os
import pprint
import time
import subprocess
import threading

from Instructions import (Introduction_Instructions, Generator_Instructions, Analysis_Instructions)
import ScriptGenerator as SG
from MDSAnalysis import ExecuteAnalysis
from CheckScriptInputs import CheckScriptInputs







'''
# Setup
ScriptWindowOpen = False
AnalysisWindowOpen = False

def StartScriptGen():
    MainApp.PrintOutputs("button presssed")
    ScriptGen = customtkinter.CTk()
    WorkingOnScript=True

    while WorkingOnScript == True:
        ScriptGen.mainloop()
'''
AnalysisFolderFilepath = ""



##### GUI #####        
class ScriptTabs(customtkinter.CTkTabview):
                def __init__(self, master):
                    super().__init__(master)

                    self.add("Script Settings")
                    self.add("MDS Options")
                    self.add("Hardware Options")
                    self.add("Advanced Options")

                    #-----------------------------------------------------### SCRIPT SETTINGS ###----------------------------------------------------------------------------#
                    self.ScriptSettingsFrame = customtkinter.CTkFrame(self.tab("Script Settings"))
                    self.ScriptSettingsFrame.grid(row=0,column=0,sticky='nsew')
                    self.ScriptSettingsFrame.grid_columnconfigure((0,1), weight=1)
                    self.ScriptSettingsFrame.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)

                    #ScriptName
                    self.ScriptNameText = customtkinter.CTkLabel(self.ScriptSettingsFrame,text="Name of Job:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.ScriptNameText.grid(row=0,column=0,padx=20,pady=10,sticky='w')
                    self.ScriptName = customtkinter.CTkEntry(self.ScriptSettingsFrame, placeholder_text="e.g. Hsp17_300K_100ns")
                    self.ScriptName.grid(row=0,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.ScriptName, msg="Determines the name of the pbs file alongside the job queue name. Cannot contain spaces or illegal filename characters.", delay=1.0)
                    
                    #PathOption
                    self.PathOptionText = customtkinter.CTkLabel(self.ScriptSettingsFrame,text="Automatic Filepath:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PathOptionText.grid(row=1,column=0,padx=20,pady=10,sticky='w')
                    PathOption = customtkinter.StringVar(value='Automatic')
                    self.PathSwitch = customtkinter.CTkSwitch(self.ScriptSettingsFrame,variable=PathOption, text='', onvalue='Automatic', offvalue='Manual', command=self.ToggleFilepath)
                    self.PathSwitch.grid(row=1,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.PathSwitch, msg="Enables for the generated script to automatically detect the filepath it is used within and setup accordingly. Highly recomended due to filepath differences between operating systems.", delay=1.0)

                    #Path
                    self.PathText = customtkinter.CTkLabel(self.ScriptSettingsFrame,text="Manual Filepath:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PathText.grid(row=2,column=0,padx=20,pady=10,sticky='w')
                    self.PathName = customtkinter.CTkEntry(self.ScriptSettingsFrame, placeholder_text="Set to Automatic")
                    self.PathName.grid(row=2,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.PathName, msg="Manual Entry for where the Script will be used from. Automatic filepath is highly recomended but if manual is required please copy and paste the filepath directly.", delay=1.0)

                    #Protein
                    self.PDBFilenameText = customtkinter.CTkLabel(self.ScriptSettingsFrame,text="Protein File:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PDBFilenameText.grid(row=3,column=0,padx=20,pady=10,sticky='w')
                    #self.Filename = customtkinter.CTkEntry(self.ScriptSettingsFrame, placeholder_text="e.g. Hsp17.pbd")
                    self.Filename = customtkinter.CTkButton(self.ScriptSettingsFrame, text="Select File", command=self.SelectProteinName)
                    self.Filename.grid(row=3,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.Filename, msg="The complete filename of the protein of interest. PDB file format.", delay=1.0)

                    #AlphaFold Check
                    self.GeneratedStructureText = customtkinter.CTkLabel(self.ScriptSettingsFrame,text="AlphaFold File:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.GeneratedStructureText.grid(row=4,column=0,padx=20,pady=10,sticky="w")
                    self.GeneratedStructure = customtkinter.CTkCheckBox(self.ScriptSettingsFrame,text="")
                    self.GeneratedStructure.grid(row=4,column=1,padx=(0,20),pady=10,sticky='e')
                    ToolTip(self.GeneratedStructure, msg="Select this if you are using an AlphaFold generated pdb file.")

                    #SimType
                    self.SimTypeText = customtkinter.CTkLabel(self.ScriptSettingsFrame,text="Simulation Type:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.SimTypeText.grid(row=5,column=0,padx=20,pady=10,sticky='w')
                    self.SimType = customtkinter.CTkComboBox(self.ScriptSettingsFrame, values=["Single Protein", "Multi-Protein"],command=self.SimTypeSelection)
                    self.SimType.grid(row=5,column=1,sticky='ew')
                    ToolTip(self.SimType, msg='Single Protein: Singular protein within a cube of solvent.\nMulti-Protein: Multiple proteins dispered within a cube of solvent (quantity is specified below).\nVerification: For use on AI generated or understudied protein structures.',delay=1)

                    #Protein Count
                    self.QuantityText = customtkinter.CTkLabel(self.ScriptSettingsFrame,text="Protein Quantity:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.QuantityText.grid(row=6,column=0,padx=20,pady=10,sticky='w')
                    self.CountFrame = customtkinter.CTkFrame(self.ScriptSettingsFrame)
                    self.CountFrame.grid(row=6,column=1,sticky='ew')
                    self.ProteinQuantity = customtkinter.CTkSlider(self.CountFrame, from_=0, to=20, command=self.ProteinCountUpdate, number_of_steps=20, width=150, state='disabled', button_color='grey')
                    self.ProteinQuantity.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.QuantityText = customtkinter.CTkLabel(self.CountFrame,text='01' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.QuantityText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.ProteinQuantity.set(1)
                    ToolTip(self.ProteinQuantity, msg="The number of proteins to be generated when using the 'Multi-Protein' Simulation Type", delay=1.0)

                    #Email
                    self.EmailText = customtkinter.CTkLabel(self.ScriptSettingsFrame,text="Email for Notification:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.EmailText.grid(row=7,column=0,padx=20,pady=10,sticky='w')
                    self.Email = customtkinter.CTkEntry(self.ScriptSettingsFrame, placeholder_text="e.g. JohnDoe@outlook.com")
                    self.Email.grid(row=7,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.Email, msg="The Email address that job updates are sent to when using PBS queue systems. Leave blank to disable", delay=1.0)
                


                    #-----------------------------------------------------### MDS OPTIONS ###----------------------------------------------------------------------------#
                    self.MDSOptionsFrame = customtkinter.CTkFrame(self.tab("MDS Options"))
                    self.MDSOptionsFrame.grid(row=0,column=0,sticky='nsew')
                    self.MDSOptionsFrame.grid_columnconfigure((0,1), weight=1)
                    self.MDSOptionsFrame.grid_rowconfigure((0,0), weight=1)

                    #Temp
                    self.TemperatureText = customtkinter.CTkLabel(self.MDSOptionsFrame,text="System Temperature (K):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.TemperatureText.grid(row=0,column=0,padx=20,pady=10,sticky='w')
                    self.Temperature = customtkinter.CTkEntry(self.MDSOptionsFrame, placeholder_text="e.g. 300")
                    self.Temperature.grid(row=0,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.Temperature, msg="Determines the complete system temperature for both the protein and solvent", delay=1.0)

                    #Pressure
                    self.PressureText = customtkinter.CTkLabel(self.MDSOptionsFrame,text="Refereence Pressure (bar):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PressureText.grid(row=1,column=0,padx=20,pady=10,sticky='w')
                    self.Pressure = customtkinter.CTkEntry(self.MDSOptionsFrame, placeholder_text="e.g. 1.0")
                    self.Pressure.grid(row=1,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.Pressure, msg="Determines the reference pressure of the system. Recommended value is 1.00 bar", delay=1.0)

                    #Solvent
                    self.SolventText = customtkinter.CTkLabel(self.MDSOptionsFrame,text="Solvent Type:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.SolventText.grid(row=2,column=0,padx=20,pady=10,sticky='w')
                    self.SolventType = customtkinter.CTkComboBox(self.MDSOptionsFrame, values=["Water"])
                    self.SolventType.grid(row=2,column=1,sticky='ew')
                    ToolTip(self.SolventType, msg='Specifies what solvent the protein will be surrounded by. Currently WIP & limited to water',delay=1)

                    #Force Field Type
                    self.ForceFieldText = customtkinter.CTkLabel(self.MDSOptionsFrame,text="Force Field:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.ForceFieldText.grid(row=3,column=0,padx=20,pady=10,sticky='w')
                    self.ForceFieldSelection = customtkinter.CTkComboBox(self.MDSOptionsFrame, values=["amber99sb-ildn", "amber03", "amber94", "amber96", "amber99", "amber99sb", "ambergs", "charmm27", "gromos96", "opls-aa/l"])
                    self.ForceFieldSelection.grid(row=3,column=1,sticky='ew')
                    ToolTip(self.SolventType, msg='Specifies what Force Field will be used for Newtonian calculations. Currently WIP & limited to AMBER',delay=1)

                    #MinimisationTime
                    self.MinimisationTimeText = customtkinter.CTkLabel(self.MDSOptionsFrame,text="Energy Minimisation Time (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MinimisationTimeText.grid(row=4,column=0,padx=20,pady=10,sticky='w')
                    self.MinimisationTime = customtkinter.CTkEntry(self.MDSOptionsFrame, placeholder_text="e.g. 100")
                    self.MinimisationTime.grid(row=4,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.MinimisationTime, msg="Determines how much time the program will dedicate to minimising the system potential energy before production simulation. Largely irrelevant as most systems will reach energy minima before any significant time as passed.", delay=1.0)

                    #NVT Time
                    self.NVTTimeText = customtkinter.CTkLabel(self.MDSOptionsFrame,text="NVT Time (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTTimeText.grid(row=5,column=0,padx=20,pady=10,sticky='w')
                    self.NVTTime = customtkinter.CTkEntry(self.MDSOptionsFrame, placeholder_text="e.g. 500")
                    self.NVTTime.grid(row=5,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.NVTTime, msg="Determines how much time the program will dedicate to Canonical enemble calculations. This allows for pressure differences to stabalise whilst keeping the protein structure fixed.", delay=1.0)

                    #NPT Time
                    self.NPTTimeText = customtkinter.CTkLabel(self.MDSOptionsFrame,text="NPT Time (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTTimeText.grid(row=6,column=0,padx=20,pady=10,sticky='w')
                    self.NPTTime = customtkinter.CTkEntry(self.MDSOptionsFrame, placeholder_text="e.g. 500")
                    self.NPTTime.grid(row=6,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.NPTTime, msg="Determines how much time the program will dedicate to Isothermal-isobaric ensemble calculations. This allows for volume to stabalise whilst keeping the protein structure fixed.", delay=1.0)

                    #Production Time
                    self.ProductionTimeText = customtkinter.CTkLabel(self.MDSOptionsFrame,text="Production Time (ns):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.ProductionTimeText.grid(row=7,column=0,padx=20,pady=10,sticky='w')
                    self.ProductionTime = customtkinter.CTkEntry(self.MDSOptionsFrame, placeholder_text="e.g. 10")
                    self.ProductionTime.grid(row=7,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.ProductionTime, msg="Determines how much time the program will simulate protein changes for. This is the primary simulation stage of MDS where the protein structure is no longer fixed.", delay=1.0)



                    #-----------------------------------------------------### HARDWARE OPTIONS ###----------------------------------------------------------------------------#
                    self.HardwareOptionsFrame = customtkinter.CTkFrame(self.tab("Hardware Options"))
                    self.HardwareOptionsFrame.grid(row=0,column=0,sticky='nsew')
                    self.HardwareOptionsFrame.grid_columnconfigure((0,1), weight=1)
                    self.HardwareOptionsFrame.grid_rowconfigure((0,1,2,3,4), weight=1)

                    #Parallel?
                    self.ParallelOptionText = customtkinter.CTkLabel(self.HardwareOptionsFrame,text="Enable Parallelisation:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.ParallelOptionText.grid(row=0,column=0,padx=20,pady=10,sticky='w')
                    ParallelOption = customtkinter.StringVar(value='Single')
                    self.ParallelSwitch = customtkinter.CTkSwitch(self.HardwareOptionsFrame,variable=ParallelOption, text='', onvalue='Parallel', offvalue='Single',command=self.ParallelOptionToggle)
                    self.ParallelSwitch.grid(row=0,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.ParallelSwitch, msg="Enables parallelisation for more computing by using multiple nodes. If using a shared queue based system, this can significantly increase job queue times.\nNOTE: With this option enabled all below hardware counts are for EACH NODE.", delay=1.0)

                    #NodeCount
                    self.NodeCountText = customtkinter.CTkLabel(self.HardwareOptionsFrame,text="Number of Nodes:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NodeCountText.grid(row=1,column=0,padx=20,pady=10,sticky='w')
                    self.NodeCountFrame = customtkinter.CTkFrame(self.HardwareOptionsFrame)
                    self.NodeCountFrame.grid(row=1,column=1,sticky='ew')
                    self.NodeCount = customtkinter.CTkSlider(self.NodeCountFrame, from_=1, to=20, command=self.NodeCountUpdate, number_of_steps=19, width=150,state='disabled')
                    self.NodeCount.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NodeCountText = customtkinter.CTkLabel(self.NodeCountFrame,text='01' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NodeCountText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NodeCount.set(1)
                    ToolTip(self.NodeCount, msg="The number of Node Cores to allocate to this job.\nPlease check your HPC system specifications for the maximum cores per node.", delay=1.0)

                    #CPUCount
                    self.CPUCountText = customtkinter.CTkLabel(self.HardwareOptionsFrame,text="CPU Count:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.CPUCountText.grid(row=2,column=0,padx=20,pady=10,sticky='w')
                    self.CPUCountFrame = customtkinter.CTkFrame(self.HardwareOptionsFrame)
                    self.CPUCountFrame.grid(row=2,column=1,sticky='ew')
                    self.CPUCount = customtkinter.CTkSlider(self.CPUCountFrame, from_=0, to=48, command=self.CPUCountUpdate, number_of_steps=12, width=150)
                    self.CPUCount.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.CPUCountText = customtkinter.CTkLabel(self.CPUCountFrame,text='24' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.CPUCountText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.CPUCount.set(24)
                    ToolTip(self.CPUCount, msg="The number of CPU Cores to allocate to this job.\nPlease check your HPC system specifications for the maximum cores per node.", delay=1.0)

                    #GPUCount
                    self.GPUCountText = customtkinter.CTkLabel(self.HardwareOptionsFrame,text="GPU Count:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.GPUCountText.grid(row=3,column=0,padx=20,pady=10,sticky='w')
                    self.GPUCountFrame = customtkinter.CTkFrame(self.HardwareOptionsFrame)
                    self.GPUCountFrame.grid(row=3,column=1,sticky='ew')
                    self.GPUCount = customtkinter.CTkSlider(self.GPUCountFrame, from_=0, to=20, command=self.GPUCountUpdate, number_of_steps=20, width=150)
                    self.GPUCount.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.GPUCountText = customtkinter.CTkLabel(self.GPUCountFrame,text='01' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.GPUCountText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.GPUCount.set(1)
                    ToolTip(self.GPUCount, msg="The number of compute nodes to allocate to this job. If using a shared queue based system, this can significantly increase job queue times.\nPlease check your HPC system specifications for the number of nodes available.", delay=1.0)

                    #MemoryAllocation
                    self.MemoryAllocationText = customtkinter.CTkLabel(self.HardwareOptionsFrame,text="Memory Allocated:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MemoryAllocationText.grid(row=4,column=0,padx=20,pady=10,sticky='w')
                    self.MemoryAllocationFrame = customtkinter.CTkFrame(self.HardwareOptionsFrame)
                    self.MemoryAllocationFrame.grid(row=4,column=1,sticky='ew')
                    self.MemoryAllocation = customtkinter.CTkSlider(self.MemoryAllocationFrame, from_=0, to=64, command=self.MemoryAllocationUpdate, number_of_steps=16, width=150)
                    self.MemoryAllocation.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.MemoryAllocationText = customtkinter.CTkLabel(self.MemoryAllocationFrame,text='32' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.MemoryAllocationText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.MemoryAllocation.set(32)
                    ToolTip(self.CPUCount, msg="The number of gigabytes of RAM to allocate to this job.\nPlease check your HPC system specifications for the maximum RAM installed per node.", delay=1.0)


                    #Walltime
                    self.WalltimeText = customtkinter.CTkLabel(self.HardwareOptionsFrame,text="Walltime:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.WalltimeText.grid(row=5,column=0,padx=20,pady=10,sticky='w')

                    self.WalltimeFrame = customtkinter.CTkFrame(self.HardwareOptionsFrame)
                    self.WalltimeFrame.grid(row=5,column=1,sticky='ew')
                    self.WalltimeHours = customtkinter.CTkEntry(self.WalltimeFrame, placeholder_text="HH",width=50)
                    self.WalltimeHours.grid(row=0,column=0,padx=10,pady=10,sticky='ew')
                    ToolTip(self.WalltimeHours, msg="The Total time to pre-allocate hardware for the job.\nFormat is HH : MM : SS", delay=1.0)
                    self.WalltimeSpacer1 = customtkinter.CTkLabel(self.WalltimeFrame,text=":",fg_color="transparent",font=('arial',16),anchor='center')
                    self.WalltimeSpacer1.grid(row=0,column=1,padx=0,pady=10,sticky='w')
                    self.WalltimeMinutes = customtkinter.CTkEntry(self.WalltimeFrame, placeholder_text="MM",width=50)
                    self.WalltimeMinutes.grid(row=0,column=2,padx=10,pady=10,sticky='ew')
                    ToolTip(self.WalltimeMinutes, msg="The Total time to pre-allocate hardware for the job.\nFormat is HH : MM : SS", delay=1.0)
                    self.WalltimeSpacer2 = customtkinter.CTkLabel(self.WalltimeFrame,text=":",fg_color="transparent",font=('arial',16),anchor='center')
                    self.WalltimeSpacer2.grid(row=0,column=3,padx=0,pady=10,sticky='w')
                    self.WalltimeSeconds = customtkinter.CTkEntry(self.WalltimeFrame, placeholder_text="SS",width=50)
                    self.WalltimeSeconds.grid(row=0,column=4,padx=10,pady=10,sticky='ew')
                    ToolTip(self.WalltimeSeconds, msg="The Total time to pre-allocate hardware for the job.\nFormat is HH : MM : SS", delay=1.0)
                    ToolTip(self.WalltimeFrame, msg="The Total time to pre-allocate hardware for the job.\nFormat is HH : MM : SS", delay=1.0)



                    #-----------------------------------------------------### ADVNACED OPTIONS ###----------------------------------------------------------------------------#
                    self.AdvancedOptionsFrame = customtkinter.CTkScrollableFrame(self.tab("Advanced Options"), width = 400, height = 570)
                    self.AdvancedOptionsFrame.grid(row=0,column=0,sticky='nsew')
                    self.AdvancedOptionsFrame.grid_columnconfigure((0,1), weight=1)
                    self.AdvancedOptionsFrame.grid_rowconfigure((0,1,2,3,4), weight=1)

                    # Advanced Options Header
                    self.AdvancedHeader = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="Advanced Options", fg_color = "transparent", font=('arial',30),anchor=("center"))
                    self.AdvancedHeader.grid(row=0, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")
                    # Advanced Options Description
                    self.AdvancedDescription = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="WARNING: Improper use of Advanced\nSettings could result in misleading results!\nPlease use the standard settings if unsure.", fg_color = "transparent", font=('arial',14),anchor=("center"))
                    self.AdvancedDescription.grid(row=1, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    # Gromacs Build
                    self.GromacsTitle = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="Module Selection", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.GromacsTitle.grid(row=2, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    self.GromacsModuleText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Gromacs Build:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.GromacsModuleText.grid(row=3,column=0,padx=20,pady=10,sticky='w')
                    self.GromacsModuleSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Recomended", "2021.4"])
                    self.GromacsModuleSelection.grid(row=3,column=1,sticky='ew')
                    ToolTip(self.GromacsModuleSelection, msg='Specifies the GROMACS build to use for the simulation. Please ensure GROMACS builds are consistent with the desired run options!',delay=1)

                    # Water Model
                    self.RemoveExistingWater = True # Choice to remove HOH molecules that may be in the structure, typically good practive for experimentally derived molecules but could cause innacuracies with very specific proteins.

                    self.WaterModelTitle = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="Water Options", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.WaterModelTitle.grid(row=4, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    self.RemoveWaterOptionText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Remove Water:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.RemoveWaterOptionText.grid(row=5,column=0,padx=20,pady=10,sticky='w')
                    RemoveWaterOption = customtkinter.StringVar(value="True")
                    self.RemoveWaterSwitch = customtkinter.CTkSwitch(self.AdvancedOptionsFrame,variable=RemoveWaterOption, text='', onvalue="True", offvalue="False")
                    self.RemoveWaterSwitch.grid(row=5,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.RemoveWaterSwitch, msg="Removes existing water molecules from the input structure file (pdb). Usually removes excess captured water from structural analysis however can effect protein function for some water-dependand proteins.", delay=1.0)

                    self.WaterModelText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Water Model:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.WaterModelText.grid(row=6,column=0,padx=20,pady=10,sticky='w')
                    self.WaterModelSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["spce"])
                    self.WaterModelSelection.grid(row=6,column=1,sticky='ew')
                    ToolTip(self.WaterModelSelection, msg='Specifies the water model to use for the simulation. Please ensure the selected option is consistent with the desired run options!',delay=1)

                    # Charge Molecules
                    self.ChargeTitle = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="Charged Atom Selection", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.ChargeTitle.grid(row=7, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    self.SystemChargeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="System Charge:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.SystemChargeText.grid(row=8,column=0,padx=20,pady=10,sticky='w')
                    self.SystemChargeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Neutral"])
                    self.SystemChargeSelection.grid(row=8,column=1,sticky='ew')
                    ToolTip(self.SystemChargeSelection, msg='Specifies the starting charge of the simulated system',delay=1)

                    self.PositiveChargeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Positive Atom:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PositiveChargeText.grid(row=9,column=0,padx=20,pady=10,sticky='w')
                    self.PositiveChargeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["[+1] Na"])
                    self.PositiveChargeSelection.grid(row=9,column=1,sticky='ew')
                    ToolTip(self.PositiveChargeSelection, msg='Specifies what positively charged atom will be added for charge balancing.',delay=1)

                    self.NegativeChargeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Negative Atom:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NegativeChargeText.grid(row=10,column=0,padx=20,pady=10,sticky='w')
                    self.NegativeChargeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["[-1] Cl"])
                    self.NegativeChargeSelection.grid(row=10,column=1,sticky='ew')
                    ToolTip(self.NegativeChargeSelection, msg='Specifies what negatively charged atom will be added for charge balancing.',delay=1)

                    # Boundry Options
                    self.BoundryTitle = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="Boundry Options", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.BoundryTitle.grid(row=11, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    self.BoundryTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Boundry Shape:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.BoundryTypeText.grid(row=12,column=0,padx=20,pady=10,sticky='w')
                    self.BoundryTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["cubic"])
                    self.BoundryTypeSelection.grid(row=12,column=1,sticky='ew')
                    ToolTip(self.BoundryTypeSelection, msg='Specifies the boundry limit shape of the system.',delay=1)

                    self.BoundryGapText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Boundry Gap:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.BoundryGapText.grid(row=13,column=0,padx=20,pady=10,sticky='w')
                    self.BoundryGapFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.BoundryGapFrame.grid(row=13,column=1,sticky='ew')
                    self.BoundryGap = customtkinter.CTkSlider(self.BoundryGapFrame, from_=0, to=10, command=self.BoundryGapUpdate, number_of_steps=20, width=130)
                    self.BoundryGap.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.BoundryGapText = customtkinter.CTkLabel(self.BoundryGapFrame,text='1.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.BoundryGapText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.BoundryGap.set(1.0)
                    ToolTip(self.BoundryGap, msg="The distance between the outermost structural atom and the edge of the system boundry.", delay=1.0)

                    self.AdvancedOptionSpacer = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text=" ", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.AdvancedOptionSpacer.grid(row=14, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")


                    # MDP Options
                    self.MDPOptionsTitle = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="MDP File Options", fg_color = "transparent", font=('arial',30),anchor=("center"))
                    self.MDPOptionsTitle.grid(row=15, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    ### ION ###
                    self.IONMDPTitle = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="ION MDP Options", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.IONMDPTitle.grid(row=16, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    self.IONIntegratorText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Integration Method:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONIntegratorText.grid(row=17,column=0,padx=20,pady=10,sticky='w')
                    self.IONIntegratorSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Steep", "md", "md-vv", "md-vv-avek", "sd", "bd", "cg", "l-bfgs", "nm", "tpi", "tpic", "mimic"])
                    self.IONIntegratorSelection.grid(row=17,column=1,sticky='ew')
                    ToolTip(self.IONIntegratorSelection, msg='Specifies the integration method used by the charge balancing system.',delay=1)

                    self.IONLimitText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Lower Limit:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONLimitText.grid(row=18,column=0,padx=20,pady=10,sticky='w')
                    self.IONLimitFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.IONLimitFrame.grid(row=18,column=1,sticky='ew')
                    self.IONLimit = customtkinter.CTkSlider(self.IONLimitFrame, from_=0, to=10000, command=self.IONLimitUpdate, number_of_steps=100, width=130)
                    self.IONLimit.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.IONLimitText = customtkinter.CTkLabel(self.IONLimitFrame,text='1000_' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.IONLimitText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.IONLimit.set(1000)
                    ToolTip(self.IONLimit, msg="The lower limit for when Ion Minimisation ends early. Measured in kJ/mol/nm.", delay=1.0)

                    self.IONTimeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Time (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONTimeText.grid(row=19,column=0,padx=20,pady=10,sticky='w')
                    self.IONTime = customtkinter.CTkEntry(self.AdvancedOptionsFrame, placeholder_text="e.g. 100")
                    self.IONTime.configure(textvariable="100")
                    self.IONTime.grid(row=19,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.IONTime, msg="Determines the maximum amount of time spend on minimisaing system charge.", delay=1.0)

                    self.IONGranularityText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Granularity (fs):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONGranularityText.grid(row=20,column=0,padx=20,pady=10,sticky='w')
                    self.IONGranularityFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.IONGranularityFrame.grid(row=20,column=1,sticky='ew')
                    self.IONGranularity = customtkinter.CTkSlider(self.IONGranularityFrame, from_=0, to=10, command=self.IONGranularityUpdate, number_of_steps=20, width=130)
                    self.IONGranularity.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.IONGranularityText = customtkinter.CTkLabel(self.IONGranularityFrame,text='1.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.IONGranularityText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.IONGranularity.set(1)
                    ToolTip(self.IONGranularity, msg="The step size for newtonian equations when performing charge minimisation.", delay=1.0)

                    self.IONForceUpdateLabel = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Update Rate (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONForceUpdateLabel.grid(row=21,column=0,padx=20,pady=10,sticky='w')
                    self.IONForceUpdateFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.IONForceUpdateFrame.grid(row=21,column=1,sticky='ew')
                    self.IONForceUpdate = customtkinter.CTkSlider(self.IONForceUpdateFrame, from_=0, to=25, command=self.IONForceUpdateUpdate, number_of_steps=50, width=130)
                    self.IONForceUpdate.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.IONForceUpdateText = customtkinter.CTkLabel(self.IONForceUpdateFrame,text='10.0' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.IONForceUpdateText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.IONForceUpdate.set(10)
                    ToolTip(self.IONForceUpdate, msg="The rate at which an update will be written to the log file. (e.g. 2 = every 2 picoseconds).", delay=1.0)

                    self.IONNeighbourSchemeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Neighbour Detection:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONNeighbourSchemeText.grid(row=22,column=0,padx=20,pady=10,sticky='w')
                    self.IONNeighbourSchemeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Verlet", "group"])
                    self.IONNeighbourSchemeSelection.grid(row=22,column=1,sticky='ew')
                    ToolTip(self.IONNeighbourSchemeSelection, msg='Specifies the neighbour detection method used by the charge minimisation system.',delay=1)

                    self.IONNeighbourListText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Neighbour Search:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONNeighbourListText.grid(row=23,column=0,padx=20,pady=10,sticky='w')
                    self.IONNeighbourListSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Grid"])
                    self.IONNeighbourListSelection.grid(row=23,column=1,sticky='ew')
                    ToolTip(self.IONNeighbourListSelection, msg='Specifies the neighbour searching method used by the charge minimisation system.',delay=1)

                    self.IONColoumbTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Model:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONColoumbTypeText.grid(row=24,column=0,padx=20,pady=10,sticky='w')
                    self.IONColoumbTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["PME", "Cut-off", "Ewald", "P3M-AD", "Reaction-Field"])
                    self.IONColoumbTypeSelection.grid(row=24,column=1,sticky='ew')
                    ToolTip(self.IONColoumbTypeSelection, msg='Specifies the type of model used for long range electrostatic calculations.',delay=1)

                    self.IONColoumbCutoffText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Range:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONColoumbCutoffText.grid(row=25,column=0,padx=20,pady=10,sticky='w')
                    self.IONColoumbCutoffFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.IONColoumbCutoffFrame.grid(row=25,column=1,sticky='ew')
                    self.IONColoumbCutoff = customtkinter.CTkSlider(self.IONColoumbCutoffFrame, from_=0, to=5, command=self.IONColoumbCutoffUpdate, number_of_steps=25, width=130)
                    self.IONColoumbCutoff.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.IONColoumbCutoffText = customtkinter.CTkLabel(self.IONColoumbCutoffFrame,text='1.2' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.IONColoumbCutoffText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.IONColoumbCutoff.set(1.2)
                    ToolTip(self.IONColoumbCutoff, msg="The interaction cutoff range for electrostatic interactions. Measured in nm.", delay=1.0)

                    self.IONVanderwaalCutoffText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Vanderwaal Range:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONVanderwaalCutoffText.grid(row=26,column=0,padx=20,pady=10,sticky='w')
                    self.IONVanderwaalCutoffFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.IONVanderwaalCutoffFrame.grid(row=26,column=1,sticky='ew')
                    self.IONVanderwaalCutoff = customtkinter.CTkSlider(self.IONVanderwaalCutoffFrame, from_=0, to=5, command=self.IONVanderwaalCutoffUpdate, number_of_steps=25, width=130)
                    self.IONVanderwaalCutoff.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.IONVanderwaalCutoffText = customtkinter.CTkLabel(self.IONVanderwaalCutoffFrame,text='1.2' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.IONVanderwaalCutoffText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.IONVanderwaalCutoff.set(1.2)
                    ToolTip(self.IONVanderwaalCutoff, msg="The interaction cutoff range for van der Waals interactions. Measured in nm.", delay=1.0)

                    self.IONBoundryTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Boundry Type:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.IONBoundryTypeText.grid(row=27,column=0,padx=20,pady=10,sticky='w')
                    self.IONBoundryTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["xyz", "xy", "no"])
                    self.IONBoundryTypeSelection.grid(row=27,column=1,sticky='ew')
                    ToolTip(self.IONBoundryTypeSelection, msg='Specifies the dimensions periodic boundry conditions will be calculated in.',delay=1)

                    self.IONMDPSpacer = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text=" ", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.IONMDPSpacer.grid(row=28, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")


                    ### Minimisation ###
                    self.MINMDPTitle = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="Minimisation MDP Options", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.MINMDPTitle.grid(row=29, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    self.MINIntegratorText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Integration Method:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MINIntegratorText.grid(row=30,column=0,padx=20,pady=10,sticky='w')
                    self.MINIntegratorSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Steep", "md", "md-vv", "md-vv-avek", "sd", "bd", "cg", "l-bfgs", "nm", "tpi", "tpic", "mimic"])
                    self.MINIntegratorSelection.grid(row=30,column=1,sticky='ew')
                    ToolTip(self.MINIntegratorSelection, msg='Specifies the integration method used by the energy minimisation system.',delay=1)

                    self.MINLimitText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Lower Limit:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MINLimitText.grid(row=31,column=0,padx=20,pady=10,sticky='w')
                    self.MINLimitFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.MINLimitFrame.grid(row=31,column=1,sticky='ew')
                    self.MINLimit = customtkinter.CTkSlider(self.MINLimitFrame, from_=0, to=10000, command=self.MINLimitUpdate, number_of_steps=100, width=130)
                    self.MINLimit.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.MINLimitText = customtkinter.CTkLabel(self.MINLimitFrame,text='500__' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.MINLimitText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.MINLimit.set(500)
                    ToolTip(self.MINLimit, msg="The lower limit for when Energy Minimisation ends early. Measured in kJ/mol/nm.", delay=1.0)

                    self.MINGranularityText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Granularity (fs):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MINGranularityText.grid(row=33,column=0,padx=20,pady=10,sticky='w')
                    self.MINGranularityFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.MINGranularityFrame.grid(row=33,column=1,sticky='ew')
                    self.MINGranularity = customtkinter.CTkSlider(self.MINGranularityFrame, from_=0, to=10, command=self.MINGranularityUpdate, number_of_steps=20, width=130)
                    self.MINGranularity.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.MINGranularityText = customtkinter.CTkLabel(self.MINGranularityFrame,text='1.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.MINGranularityText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.MINGranularity.set(1)
                    ToolTip(self.MINGranularity, msg="The step size for newtonian equations when performing energy minimisation.", delay=1.0)

                    self.MINForceUpdateLabel = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Update Rate (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MINForceUpdateLabel.grid(row=34,column=0,padx=20,pady=10,sticky='w')
                    self.MINForceUpdateFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.MINForceUpdateFrame.grid(row=34,column=1,sticky='ew')
                    self.MINForceUpdate = customtkinter.CTkSlider(self.MINForceUpdateFrame, from_=0, to=25, command=self.MINForceUpdateUpdate, number_of_steps=50, width=130)
                    self.MINForceUpdate.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.MINForceUpdateText = customtkinter.CTkLabel(self.MINForceUpdateFrame,text='10.0' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.MINForceUpdateText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.MINForceUpdate.set(10)
                    ToolTip(self.MINForceUpdate, msg="The rate at which an update will be written to the log file. (e.g. 2 = every 2 picoseconds).", delay=1.0)

                    self.MINNeighbourSchemeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Neighbour Detection:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MINNeighbourSchemeText.grid(row=35,column=0,padx=20,pady=10,sticky='w')
                    self.MINNeighbourSchemeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Verlet", "group"])
                    self.MINNeighbourSchemeSelection.grid(row=35,column=1,sticky='ew')
                    ToolTip(self.MINNeighbourSchemeSelection, msg='Specifies the neighbour detection method used by the energy minimisation system.',delay=1)

                    self.MINNeighbourListText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Neighbour Search:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MINNeighbourListText.grid(row=36,column=0,padx=20,pady=10,sticky='w')
                    self.MINNeighbourListSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Grid"])
                    self.MINNeighbourListSelection.grid(row=36,column=1,sticky='ew')
                    ToolTip(self.MINNeighbourListSelection, msg='Specifies the neighbour searching method used by the energy minimisation system.',delay=1)

                    self.MINColoumbTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Model:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MINColoumbTypeText.grid(row=37,column=0,padx=20,pady=10,sticky='w')
                    self.MINColoumbTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["PME", "Cut-off", "Ewald", "P3M-AD", "Reaction-Field"])
                    self.MINColoumbTypeSelection.grid(row=37,column=1,sticky='ew')
                    ToolTip(self.MINColoumbTypeSelection, msg='Specifies the type of model used for long range electrostatic calculations.',delay=1)

                    self.MINColoumbCutoffText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Range:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MINColoumbCutoffText.grid(row=38,column=0,padx=20,pady=10,sticky='w')
                    self.MINColoumbCutoffFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.MINColoumbCutoffFrame.grid(row=38,column=1,sticky='ew')
                    self.MINColoumbCutoff = customtkinter.CTkSlider(self.MINColoumbCutoffFrame, from_=0, to=5, command=self.MINColoumbCutoffUpdate, number_of_steps=25, width=130)
                    self.MINColoumbCutoff.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.MINColoumbCutoffText = customtkinter.CTkLabel(self.MINColoumbCutoffFrame,text='1.4' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.MINColoumbCutoffText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.MINColoumbCutoff.set(1.4)
                    ToolTip(self.MINColoumbCutoff, msg="The interaction cutoff range for electrostatic interactions. Measured in nm.", delay=1.0)

                    self.MINVanderwaalCutoffText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Vanderwaal Range:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MINVanderwaalCutoffText.grid(row=39,column=0,padx=20,pady=10,sticky='w')
                    self.MINVanderwaalCutoffFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.MINVanderwaalCutoffFrame.grid(row=39,column=1,sticky='ew')
                    self.MINVanderwaalCutoff = customtkinter.CTkSlider(self.MINVanderwaalCutoffFrame, from_=0, to=5, command=self.MINVanderwaalCutoffUpdate, number_of_steps=25, width=130)
                    self.MINVanderwaalCutoff.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.MINVanderwaalCutoffText = customtkinter.CTkLabel(self.MINVanderwaalCutoffFrame,text='1.4' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.MINVanderwaalCutoffText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.MINVanderwaalCutoff.set(1.4)
                    ToolTip(self.MINVanderwaalCutoff, msg="The interaction cutoff range for van der Waals interactions. Measured in nm.", delay=1.0)

                    self.MINBoundryTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Boundry Type:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.MINBoundryTypeText.grid(row=40,column=0,padx=20,pady=10,sticky='w')
                    self.MINBoundryTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["xyz", "xy", "no"])
                    self.MINBoundryTypeSelection.grid(row=40,column=1,sticky='ew')
                    ToolTip(self.MINBoundryTypeSelection, msg='Specifies the dimensions periodic boundry conditions will be calculated in.',delay=1)

                    self.MINMDPSpacer = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text=" ", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.MINMDPSpacer.grid(row=41, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")


                    ### NVT ##
                    self.NVTMDPTitle = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="NVT MDP Options", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.NVTMDPTitle.grid(row=42, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    self.NVT_Restrain = '-DPOSRES'
                    self.NVTRestrainText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Restrain Proteins:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTRestrainText.grid(row=43,column=0,padx=20,pady=10,sticky='w')
                    NVTRestrain = customtkinter.StringVar(value='-DPOSRES')
                    self.NVTRestrainSwitch = customtkinter.CTkSwitch(self.AdvancedOptionsFrame,variable=NVTRestrain, text='', onvalue='-DPOSRES', offvalue='-DFLEXIBLE')
                    self.NVTRestrainSwitch.grid(row=43,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.NVTRestrainSwitch, msg="Prevents the protein from undergoing motion when enabled.", delay=1.0)

                    self.NVT_Integrator = "md"
                    self.NVTIntegratorText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Integration Method:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTIntegratorText.grid(row=44,column=0,padx=20,pady=10,sticky='w')
                    self.NVTIntegratorSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Steep", "md", "md-vv", "md-vv-avek", "sd", "bd", "cg", "l-bfgs", "nm", "tpi", "tpic", "mimic"])
                    self.NVTIntegratorSelection.set("md")
                    self.NVTIntegratorSelection.grid(row=44,column=1,sticky='ew')
                    ToolTip(self.NVTIntegratorSelection, msg='Specifies the integration method used for the NVT stage.',delay=1)

                    self.NVT_Granularity = 2
                    self.NVTGranularityText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Granularity (fs):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTGranularityText.grid(row=46,column=0,padx=20,pady=10,sticky='w')
                    self.NVTGranularityFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NVTGranularityFrame.grid(row=46,column=1,sticky='ew')
                    self.NVTGranularity = customtkinter.CTkSlider(self.NVTGranularityFrame, from_=0, to=10, command=self.NVTGranularityUpdate, number_of_steps=20, width=130)
                    self.NVTGranularity.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NVTGranularityText = customtkinter.CTkLabel(self.NVTGranularityFrame,text='2.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NVTGranularityText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NVTGranularity.set(2)
                    ToolTip(self.NVTGranularity, msg="The step size for newtonian equations when during NVT.", delay=1.0)

                    self.NVTForceUpdateLabel = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Update Rate (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTForceUpdateLabel.grid(row=47,column=0,padx=20,pady=10,sticky='w')
                    self.NVTForceUpdateFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NVTForceUpdateFrame.grid(row=47,column=1,sticky='ew')
                    self.NVTForceUpdate = customtkinter.CTkSlider(self.NVTForceUpdateFrame, from_=0, to=25, command=self.NVTForceUpdateUpdate, number_of_steps=50, width=130)
                    self.NVTForceUpdate.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NVTForceUpdateText = customtkinter.CTkLabel(self.NVTForceUpdateFrame,text='1.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NVTForceUpdateText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NVTForceUpdate.set(1)
                    ToolTip(self.NVTForceUpdate, msg="The rate at which an update will be written to the log file. (e.g. 2 = every 2 picoseconds).", delay=1.0)

                    self.NVT_Continued = False
                    self.NVTContinuedText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Continued Simulation:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTContinuedText.grid(row=48,column=0,padx=20,pady=10,sticky='w')
                    NVTContinued = customtkinter.StringVar(value='no')
                    self.NVTContinuedSwitch = customtkinter.CTkSwitch(self.AdvancedOptionsFrame,variable=NVTContinued, text='', onvalue='yes', offvalue='no')
                    self.NVTContinuedSwitch.grid(row=48,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.NVTContinuedSwitch, msg="Indicates whether this simulation is continued from a previous simulation.", delay=1.0)

                    self.NVT_ConstraintAlgorithm = "lincs"
                    self.NVTConstraintAlgorithmText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Constraint Algorithm:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTConstraintAlgorithmText.grid(row=49,column=0,padx=20,pady=10,sticky='w')
                    self.NVTConstraintAlgorithmSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["lincs", "SHAKE"])
                    self.NVTConstraintAlgorithmSelection.set("lincs")
                    self.NVTConstraintAlgorithmSelection.grid(row=49,column=1,sticky='ew')
                    ToolTip(self.NVTConstraintAlgorithmSelection, msg='Specifies the constraint algorithm used for the NVT stage.',delay=1)

                    self.NVT_Constraints = "h-bonds"
                    self.NVTConstraintTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Constrained Items:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTConstraintTypeText.grid(row=50,column=0,padx=20,pady=10,sticky='w')
                    self.NVTConstraintTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["h-bonds", "all-bonds", "h-angles", "all-angles", "none"])
                    self.NVTConstraintTypeSelection.set("h-bonds")
                    self.NVTConstraintTypeSelection.grid(row=50,column=1,sticky='ew')
                    ToolTip(self.NVTConstraintTypeSelection, msg='Specifies what simulated objects will be constrainedfor the NVT stage.',delay=1)

                    self.NVT_lincs_iter = 1
                    self.NVTlincsText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="LINCS Accuracy:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTlincsText.grid(row=51,column=0,padx=20,pady=10,sticky='w')
                    self.NVTlincsFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NVTlincsFrame.grid(row=51,column=1,sticky='ew')
                    self.NVTlincs = customtkinter.CTkSlider(self.NVTlincsFrame, from_=0, to=10, command=self.NVTlincsUpdate, number_of_steps=10, width=130)
                    self.NVTlincs.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NVTlincsText = customtkinter.CTkLabel(self.NVTlincsFrame,text='1.0' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NVTlincsText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NVTlincs.set(1)
                    ToolTip(self.NVTlincs, msg="Detirmines the accuracy of constraint algorithm.", delay=1.0)

                    self.NVT_Order_order = 4
                    self.NVTOrderText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="LINCS Order:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTOrderText.grid(row=52,column=0,padx=20,pady=10,sticky='w')
                    self.NVTOrderFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NVTOrderFrame.grid(row=52,column=1,sticky='ew')
                    self.NVTOrder = customtkinter.CTkSlider(self.NVTOrderFrame, from_=0, to=10, command=self.NVTOrderUpdate, number_of_steps=10, width=130)
                    self.NVTOrder.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NVTOrderText = customtkinter.CTkLabel(self.NVTOrderFrame,text='4.0' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NVTOrderText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NVTOrder.set(4)
                    ToolTip(self.NVTOrder, msg="Detirmines the order of constraint algorithm. Impacts accuracy.", delay=1.0)

                    self.NVT_NeighbourScheme = "Verlet"
                    self.NVTNeighbourSchemeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Neighbour Detection:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTNeighbourSchemeText.grid(row=53,column=0,padx=20,pady=10,sticky='w')
                    self.NVTNeighbourSchemeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Verlet", "group"])
                    self.NVTNeighbourSchemeSelection.grid(row=53,column=1,sticky='ew')
                    ToolTip(self.NVTNeighbourSchemeSelection, msg='Specifies the neighbour detection method used by the energy minimisation system.',delay=1)

                    self.NVT_NeighbourListMethod = "grid"
                    self.NVTNeighbourListText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Neighbour Search:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTNeighbourListText.grid(row=54,column=0,padx=20,pady=10,sticky='w')
                    self.NVTNeighbourListSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Grid"])
                    self.NVTNeighbourListSelection.grid(row=54,column=1,sticky='ew')
                    ToolTip(self.NVTNeighbourListSelection, msg='Specifies the neighbour searching method used by the energy minimisation system.',delay=1)

                    self.NVT_ColoumbCutoff = 1.4
                    self.NVTColoumbCutoffText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Range:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTColoumbCutoffText.grid(row=56,column=0,padx=20,pady=10,sticky='w')
                    self.NVTColoumbCutoffFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NVTColoumbCutoffFrame.grid(row=56,column=1,sticky='ew')
                    self.NVTColoumbCutoff = customtkinter.CTkSlider(self.NVTColoumbCutoffFrame, from_=0, to=5, command=self.NVTColoumbCutoffUpdate, number_of_steps=25, width=130)
                    self.NVTColoumbCutoff.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NVTColoumbCutoffText = customtkinter.CTkLabel(self.NVTColoumbCutoffFrame,text='1.4' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NVTColoumbCutoffText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NVTColoumbCutoff.set(1.4)
                    ToolTip(self.NVTColoumbCutoff, msg="The interaction cutoff range for electrostatic interactions. Measured in nm.", delay=1.0)

                    self.NVT_VanderwaalCutoff = 1.4
                    self.NVTVanderwaalCutoffText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Vanderwaal Range:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTVanderwaalCutoffText.grid(row=57,column=0,padx=20,pady=10,sticky='w')
                    self.NVTVanderwaalCutoffFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NVTVanderwaalCutoffFrame.grid(row=57,column=1,sticky='ew')
                    self.NVTVanderwaalCutoff = customtkinter.CTkSlider(self.NVTVanderwaalCutoffFrame, from_=0, to=5, command=self.NVTVanderwaalCutoffUpdate, number_of_steps=25, width=130)
                    self.NVTVanderwaalCutoff.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NVTVanderwaalCutoffText = customtkinter.CTkLabel(self.NVTVanderwaalCutoffFrame,text='1.4' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NVTVanderwaalCutoffText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NVTVanderwaalCutoff.set(1.4)
                    ToolTip(self.NVTVanderwaalCutoff, msg="The interaction cutoff range for van der Waals interactions. Measured in nm.", delay=1.0)

                    self.NVT_DispCorr = "EnerPres"
                    self.NVTDispCorrText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Dispersion Correction:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTDispCorrText.grid(row=58,column=0,padx=20,pady=10,sticky='w')
                    self.NVTDispCorrSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["EnerPres", "Ener", "no"])
                    self.NVTDispCorrSelection.grid(row=58,column=1,sticky='ew')
                    ToolTip(self.NVTDispCorrSelection, msg='Aids with Van der Waals cutoff scheme.',delay=1)

                    self.NVT_ColoumbType = "PME"
                    self.NVTColoumbTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Model:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTColoumbTypeText.grid(row=59,column=0,padx=20,pady=10,sticky='w')
                    self.NVTColoumbTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["PME", "Cut-off", "Ewald", "P3M-AD", "Reaction-Field"])
                    self.NVTColoumbTypeSelection.grid(row=59,column=1,sticky='ew')
                    ToolTip(self.NVTColoumbTypeSelection, msg='Specifies the type of model used for long range electrostatic calculations.',delay=1)

                    self.NVT_PMEOrder = 4
                    self.NVTPMEOrderText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Order:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTPMEOrderText.grid(row=60,column=0,padx=20,pady=10,sticky='w')
                    self.NVTPMEOrderFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NVTPMEOrderFrame.grid(row=60,column=1,sticky='ew')
                    self.NVTPMEOrder = customtkinter.CTkSlider(self.NVTPMEOrderFrame, from_=0, to=10, command=self.NVTPMEOrderUpdate, number_of_steps=10, width=130)
                    self.NVTPMEOrder.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NVTPMEOrderText = customtkinter.CTkLabel(self.NVTPMEOrderFrame,text='4.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NVTPMEOrderText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NVTPMEOrder.set(4)
                    ToolTip(self.NVTPMEOrder, msg="Order of interpolation for electrostatic model.", delay=1.0)

                    self.NVT_FourierSpacing = 0.1
                    self.NVTFourierSpacingText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Fourier Spacing:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTFourierSpacingText.grid(row=61,column=0,padx=20,pady=10,sticky='w')
                    self.NVTFourierSpacingFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NVTFourierSpacingFrame.grid(row=61,column=1,sticky='ew')
                    self.NVTFourierSpacing = customtkinter.CTkSlider(self.NVTFourierSpacingFrame, from_=0, to=1, command=self.NVTFourierSpacingUpdate, number_of_steps=10, width=130)
                    self.NVTFourierSpacing.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NVTFourierSpacingText = customtkinter.CTkLabel(self.NVTFourierSpacingFrame,text='0.1' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NVTFourierSpacingText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NVTFourierSpacing.set(0.1)
                    ToolTip(self.NVTFourierSpacing, msg="Grid spacing for FFT calculations.", delay=1.0)

                    self.NVT_TempCoupling = "V-rescale"
                    self.NVTTempCouplingText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Coupling Model [T]:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTTempCouplingText.grid(row=62,column=0,padx=20,pady=10,sticky='w')
                    self.NVTTempCouplingSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["V-rescale", "berendsen", "nose-hoover", "andersen", "andersen-massive", "no"])
                    self.NVTTempCouplingSelection.grid(row=62,column=1,sticky='ew')
                    ToolTip(self.NVTTempCouplingSelection, msg='Method of coupling temperature.',delay=1)

                    self.NVT_CouplingGroups = "Protein Non-Protein"
                    self.NVTCouplingGroupsText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Coupling Groups:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTCouplingGroupsText.grid(row=63,column=0,padx=20,pady=10,sticky='w')
                    self.NVTCouplingGroupsSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Protein Non-Protein"])
                    self.NVTCouplingGroupsSelection.grid(row=63,column=1,sticky='ew')
                    ToolTip(self.NVTCouplingGroupsSelection, msg='Determines which groups should be coupled.',delay=1)

                    self.NVT_TempTimeConstant = 0.1 #ps
                    self.NVTTempTimeConstantText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Time Constant (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTTempTimeConstantText.grid(row=64,column=0,padx=20,pady=10,sticky='w')
                    self.NVTTempTimeConstantFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NVTTempTimeConstantFrame.grid(row=64,column=1,sticky='ew')
                    self.NVTTempTimeConstant = customtkinter.CTkSlider(self.NVTTempTimeConstantFrame, from_=0, to=1, command=self.NVTTempTimeConstantUpdate, number_of_steps=10, width=130)
                    self.NVTTempTimeConstant.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NVTTempTimeConstantText = customtkinter.CTkLabel(self.NVTTempTimeConstantFrame,text='0.1' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NVTTempTimeConstantText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NVTTempTimeConstant.set(0.1)
                    ToolTip(self.NVTTempTimeConstant, msg="Time constant for temperature coupling.", delay=1.0)

                    self.NVT_BoundryType = 'xyz'
                    self.NVTBoundryTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Boundry Type:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTBoundryTypeText.grid(row=65,column=0,padx=20,pady=10,sticky='w')
                    self.NVTBoundryTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["xyz", "xy", "no"])
                    self.NVTBoundryTypeSelection.grid(row=65,column=1,sticky='ew')
                    ToolTip(self.NVTBoundryTypeSelection, msg='Specifies the dimensions periodic boundry conditions will be calculated in.',delay=1)

                    self.NVTGenVelocityText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Generate Velocity:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTGenVelocityText.grid(row=66,column=0,padx=20,pady=10,sticky='w')
                    NVTGenVelocity = customtkinter.StringVar(value='yes')
                    self.NVTGenVelocitySwitch = customtkinter.CTkSwitch(self.AdvancedOptionsFrame,variable=NVTGenVelocity, text='', onvalue='yes', offvalue='no')
                    self.NVTGenVelocitySwitch.grid(row=66,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.NVTGenVelocitySwitch, msg="Indicates whether to generate velocity values.", delay=1.0)

                    self.NVT_Seed = -1
                    self.NVTSeedText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Seed:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NVTSeedText.grid(row=67,column=0,padx=20,pady=10,sticky='w')
                    self.NVTSeed = customtkinter.CTkEntry(self.AdvancedOptionsFrame, placeholder_text="e.g. -1")
                    self.NVTSeed.configure(textvariable="-1")
                    self.NVTSeed.grid(row=67,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.NVTSeed, msg="Detirmines the seed for the simulation. -1 to set to random..", delay=1.0)

                    self.NVTMDPSpacer = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text=" ", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.NVTMDPSpacer.grid(row=68, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")



                    ### NPT ###
                    self.NPTMDPTitle = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="NPT MDP Options", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.NPTMDPTitle.grid(row=69, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    self.NPT_Restrain = '-DPOSRES'
                    self.NPTRestrainText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Restrain Proteins:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTRestrainText.grid(row=70,column=0,padx=20,pady=10,sticky='w')
                    NPTRestrain = customtkinter.StringVar(value='-DPOSRES')
                    self.NPTRestrainSwitch = customtkinter.CTkSwitch(self.AdvancedOptionsFrame,variable=NPTRestrain, text='', onvalue='-DPOSRES', offvalue='-DFLEXIBLE')
                    self.NPTRestrainSwitch.grid(row=70,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.NPTRestrainSwitch, msg="Prevents the protein from undergoing motion when enabled.", delay=1.0)

                    self.NPT_Integrator = "md"
                    self.NPTIntegratorText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Integration Method:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTIntegratorText.grid(row=71,column=0,padx=20,pady=10,sticky='w')
                    self.NPTIntegratorSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Steep", "md", "md-vv", "md-vv-avek", "sd", "bd", "cg", "l-bfgs", "nm", "tpi", "tpic", "mimic"])
                    self.NPTIntegratorSelection.set("md")
                    self.NPTIntegratorSelection.grid(row=71,column=1,sticky='ew')
                    ToolTip(self.NPTIntegratorSelection, msg='Specifies the integration method used for the NPT stage.',delay=1)

                    self.NPT_Granularity = 2
                    self.NPTGranularityText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Granularity (fs):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTGranularityText.grid(row=73,column=0,padx=20,pady=10,sticky='w')
                    self.NPTGranularityFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NPTGranularityFrame.grid(row=73,column=1,sticky='ew')
                    self.NPTGranularity = customtkinter.CTkSlider(self.NPTGranularityFrame, from_=0, to=10, command=self.NPTGranularityUpdate, number_of_steps=20, width=130)
                    self.NPTGranularity.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NPTGranularityText = customtkinter.CTkLabel(self.NPTGranularityFrame,text='2.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NPTGranularityText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NPTGranularity.set(2)
                    ToolTip(self.NPTGranularity, msg="The step size for newtonian equations when performing energy minimisation.", delay=1.0)

                    self.NPTForceUpdateLabel = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Update Rate (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTForceUpdateLabel.grid(row=74,column=0,padx=20,pady=10,sticky='w')
                    self.NPTForceUpdateFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NPTForceUpdateFrame.grid(row=74,column=1,sticky='ew')
                    self.NPTForceUpdate = customtkinter.CTkSlider(self.NPTForceUpdateFrame, from_=0, to=25, command=self.NPTForceUpdateUpdate, number_of_steps=50, width=130)
                    self.NPTForceUpdate.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NPTForceUpdateText = customtkinter.CTkLabel(self.NPTForceUpdateFrame,text='1.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NPTForceUpdateText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NPTForceUpdate.set(1)
                    ToolTip(self.NPTForceUpdate, msg="The rate at which an update will be written to the log file. (e.g. 2 = every 2 picoseconds).", delay=1.0)

                    self.NPT_Continued = True
                    self.NPTContinuedText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Continued Simulation:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTContinuedText.grid(row=75,column=0,padx=20,pady=10,sticky='w')
                    NPTContinued = customtkinter.StringVar(value='yes')
                    self.NPTContinuedSwitch = customtkinter.CTkSwitch(self.AdvancedOptionsFrame,variable=NPTContinued, text='', onvalue='yes', offvalue='no')
                    self.NPTContinuedSwitch.grid(row=75,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.NPTContinuedSwitch, msg="Indicates whether this simulation is continued from a previous simulation.", delay=1.0)

                    self.NPT_ConstraintAlgorithm = "lincs"
                    self.NPTConstraintAlgorithmText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Constraint Algorithm:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTConstraintAlgorithmText.grid(row=76,column=0,padx=20,pady=10,sticky='w')
                    self.NPTConstraintAlgorithmSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["lincs", "SHAKE"])
                    self.NPTConstraintAlgorithmSelection.set("lincs")
                    self.NPTConstraintAlgorithmSelection.grid(row=76,column=1,sticky='ew')
                    ToolTip(self.NPTConstraintAlgorithmSelection, msg='Specifies the constraint algorithm used for the NPT stage.',delay=1)

                    self.NPT_Constraints = "h-bonds"
                    self.NPTConstraintTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Constrained Items:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTConstraintTypeText.grid(row=77,column=0,padx=20,pady=10,sticky='w')
                    self.NPTConstraintTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["h-bonds", "all-bonds", "h-angles", "all-angles", "none"])
                    self.NPTConstraintTypeSelection.set("h-bonds")
                    self.NPTConstraintTypeSelection.grid(row=77,column=1,sticky='ew')
                    ToolTip(self.NPTConstraintTypeSelection, msg='Specifies what simulated objects will be constrainedfor the NPT stage.',delay=1)

                    self.NPT_lincs_iter = 1
                    self.NPTlincsText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="LINCS Accuracy:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTlincsText.grid(row=78,column=0,padx=20,pady=10,sticky='w')
                    self.NPTlincsFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NPTlincsFrame.grid(row=78,column=1,sticky='ew')
                    self.NPTlincs = customtkinter.CTkSlider(self.NPTlincsFrame, from_=0, to=10, command=self.NPTlincsUpdate, number_of_steps=10, width=130)
                    self.NPTlincs.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NPTlincsText = customtkinter.CTkLabel(self.NPTlincsFrame,text='1.0' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NPTlincsText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NPTlincs.set(1)
                    ToolTip(self.NPTlincs, msg="Detirmines the accuracy of constraint algorithm.", delay=1.0)

                    self.NPT_lincs_order = 4
                    self.NPTOrderText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="LINCS Order:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTOrderText.grid(row=79,column=0,padx=20,pady=10,sticky='w')
                    self.NPTOrderFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NPTOrderFrame.grid(row=79,column=1,sticky='ew')
                    self.NPTOrder = customtkinter.CTkSlider(self.NPTOrderFrame, from_=0, to=10, command=self.NPTOrderUpdate, number_of_steps=10, width=130)
                    self.NPTOrder.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NPTOrderText = customtkinter.CTkLabel(self.NPTOrderFrame,text='4.0' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NPTOrderText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NPTOrder.set(4)
                    ToolTip(self.NPTOrder, msg="Detirmines the order of constraint algorithm. Impacts accuracy.", delay=1.0)

                    self.NPT_NeighbourScheme = "Verlet"
                    self.NPTNeighbourSchemeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Neighbour Detection:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTNeighbourSchemeText.grid(row=80,column=0,padx=20,pady=10,sticky='w')
                    self.NPTNeighbourSchemeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Verlet", "group"])
                    self.NPTNeighbourSchemeSelection.grid(row=80,column=1,sticky='ew')
                    ToolTip(self.NPTNeighbourSchemeSelection, msg='Specifies the neighbour detection method used by the energy minimisation system.',delay=1)

                    self.NPT_NeighbourListMethod = "grid"
                    self.NPTNeighbourListText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Neighbour Search:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTNeighbourListText.grid(row=81,column=0,padx=20,pady=10,sticky='w')
                    self.NPTNeighbourListSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Grid"])
                    self.NPTNeighbourListSelection.grid(row=81,column=1,sticky='ew')
                    ToolTip(self.NPTNeighbourListSelection, msg='Specifies the neighbour searching method used by the energy minimisation system.',delay=1)

                    self.NPT_ColoumbCutoff = 1.4
                    self.NPTColoumbCutoffText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Range:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTColoumbCutoffText.grid(row=83,column=0,padx=20,pady=10,sticky='w')
                    self.NPTColoumbCutoffFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NPTColoumbCutoffFrame.grid(row=83,column=1,sticky='ew')
                    self.NPTColoumbCutoff = customtkinter.CTkSlider(self.NPTColoumbCutoffFrame, from_=0, to=5, command=self.NPTColoumbCutoffUpdate, number_of_steps=25, width=130)
                    self.NPTColoumbCutoff.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NPTColoumbCutoffText = customtkinter.CTkLabel(self.NPTColoumbCutoffFrame,text='1.4' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NPTColoumbCutoffText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NPTColoumbCutoff.set(1.4)
                    ToolTip(self.NPTColoumbCutoff, msg="The interaction cutoff range for electrostatic interactions. Measured in nm.", delay=1.0)

                    self.NPT_VanderwaalCutoff = 1.4
                    self.NPTVanderwaalCutoffText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Vanderwaal Range:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTVanderwaalCutoffText.grid(row=84,column=0,padx=20,pady=10,sticky='w')
                    self.NPTVanderwaalCutoffFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NPTVanderwaalCutoffFrame.grid(row=84,column=1,sticky='ew')
                    self.NPTVanderwaalCutoff = customtkinter.CTkSlider(self.NPTVanderwaalCutoffFrame, from_=0, to=5, command=self.NPTVanderwaalCutoffUpdate, number_of_steps=25, width=130)
                    self.NPTVanderwaalCutoff.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NPTVanderwaalCutoffText = customtkinter.CTkLabel(self.NPTVanderwaalCutoffFrame,text='1.4' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NPTVanderwaalCutoffText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NPTVanderwaalCutoff.set(1.4)
                    ToolTip(self.NPTVanderwaalCutoff, msg="The interaction cutoff range for van der Waals interactions. Measured in nm.", delay=1.0)

                    self.NPT_DispCorr = "EnerPres"
                    self.NPTDispCorrText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Dispersion Correction:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTDispCorrText.grid(row=85,column=0,padx=20,pady=10,sticky='w')
                    self.NPTDispCorrSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["EnerPres", "Ener", "no"])
                    self.NPTDispCorrSelection.grid(row=85,column=1,sticky='ew')
                    ToolTip(self.NPTDispCorrSelection, msg='Aids with Van der Waals cutoff scheme.',delay=1)

                    self.NPT_ColoumbType = "PME"
                    self.NPTColoumbTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Model:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTColoumbTypeText.grid(row=86,column=0,padx=20,pady=10,sticky='w')
                    self.NPTColoumbTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["PME", "Cut-off", "Ewald", "P3M-AD", "Reaction-Field"])
                    self.NPTColoumbTypeSelection.grid(row=86,column=1,sticky='ew')
                    ToolTip(self.NPTColoumbTypeSelection, msg='Specifies the type of model used for long range electrostatic calculations.',delay=1)

                    self.NPT_PMEOrder = 4
                    self.NPTPMEOrderText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Order:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTPMEOrderText.grid(row=87,column=0,padx=20,pady=10,sticky='w')
                    self.NPTPMEOrderFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NPTPMEOrderFrame.grid(row=87,column=1,sticky='ew')
                    self.NPTPMEOrder = customtkinter.CTkSlider(self.NPTPMEOrderFrame, from_=0, to=10, command=self.NPTPMEOrderUpdate, number_of_steps=10, width=130)
                    self.NPTPMEOrder.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NPTPMEOrderText = customtkinter.CTkLabel(self.NPTPMEOrderFrame,text='4.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NPTPMEOrderText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NPTPMEOrder.set(4)
                    ToolTip(self.NPTPMEOrder, msg="Order of interpolation for electrostatic model.", delay=1.0)

                    self.NPT_FourierSpacing = 0.1
                    self.NPTFourierSpacingText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Fourier Spacing:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTFourierSpacingText.grid(row=88,column=0,padx=20,pady=10,sticky='w')
                    self.NPTFourierSpacingFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NPTFourierSpacingFrame.grid(row=88,column=1,sticky='ew')
                    self.NPTFourierSpacing = customtkinter.CTkSlider(self.NPTFourierSpacingFrame, from_=0, to=1, command=self.NPTFourierSpacingUpdate, number_of_steps=10, width=130)
                    self.NPTFourierSpacing.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NPTFourierSpacingText = customtkinter.CTkLabel(self.NPTFourierSpacingFrame,text='0.1' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NPTFourierSpacingText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NPTFourierSpacing.set(0.1)
                    ToolTip(self.NPTFourierSpacing, msg="Grid spacing for FFT calculations.", delay=1.0)

                    self.NPT_TempCoupling = "V-rescale"
                    self.NPTTempCouplingText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Coupling Model [T]:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTTempCouplingText.grid(row=89,column=0,padx=20,pady=10,sticky='w')
                    self.NPTTempCouplingSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["V-rescale", "berendsen", "nose-hoover", "andersen", "andersen-massive", "no"])
                    self.NPTTempCouplingSelection.grid(row=89,column=1,sticky='ew')
                    ToolTip(self.NPTTempCouplingSelection, msg='Method of coupling temperature.',delay=1)

                    self.NPT_CouplingGroups = "Protein Non-Protein"
                    self.NPTCouplingGroupsText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Coupling Groups:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTCouplingGroupsText.grid(row=90,column=0,padx=20,pady=10,sticky='w')
                    self.NPTCouplingGroupsSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Protein Non-Protein"])
                    self.NPTCouplingGroupsSelection.grid(row=90,column=1,sticky='ew')
                    ToolTip(self.NPTCouplingGroupsSelection, msg='Determines which groups should be coupled.',delay=1)

                    self.NPT_TempTimeConstant = 0.1 #ps
                    self.NPTTempTimeConstantText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Time Constant (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTTempTimeConstantText.grid(row=91,column=0,padx=20,pady=10,sticky='w')
                    self.NPTTempTimeConstantFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.NPTTempTimeConstantFrame.grid(row=91,column=1,sticky='ew')
                    self.NPTTempTimeConstant = customtkinter.CTkSlider(self.NPTTempTimeConstantFrame, from_=0, to=1, command=self.NPTTempTimeConstantUpdate, number_of_steps=10, width=130)
                    self.NPTTempTimeConstant.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.NPTTempTimeConstantText = customtkinter.CTkLabel(self.NPTTempTimeConstantFrame,text='0.1' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.NPTTempTimeConstantText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.NPTTempTimeConstant.set(0.1)
                    ToolTip(self.NPTTempTimeConstant, msg="Time constant for temperature coupling.", delay=1.0)

                    self.NPTPressureCouplingText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Coupling Model [P]:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTPressureCouplingText.grid(row=92,column=0,padx=20,pady=10,sticky='w')
                    self.NPTPressureCouplingSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Berendsen", "Parrinello-Rahman", "C-rescale",  "MTTK", "no"])
                    self.NPTPressureCouplingSelection.grid(row=92,column=1,sticky='ew')
                    ToolTip(self.NPTPressureCouplingSelection, msg='Method of coupling pressure.',delay=1)

                    self.NPT_CoupleType = "isotropic"
                    self.NPTPressureCoupleTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Coupling Type [P]:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTPressureCoupleTypeText.grid(row=93,column=0,padx=20,pady=10,sticky='w')
                    self.NPTPressureCoupleTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["isotropic", "semiisotropic", "anisotropic", "surface-tension"])
                    self.NPTPressureCoupleTypeSelection.grid(row=93,column=1,sticky='ew')
                    ToolTip(self.NPTPressureCoupleTypeSelection, msg='Scale of pressure coupling.',delay=1)

                    self.NPT_Compressibility = "4.5e-5"
                    self.NPTWaterCompressibilityText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Water Compressibility:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTWaterCompressibilityText.grid(row=94,column=0,padx=20,pady=10,sticky='w')
                    self.NPTWaterCompressibility = customtkinter.CTkEntry(self.AdvancedOptionsFrame, placeholder_text="e.g. 4.5e-5")
                    self.NPTWaterCompressibility.configure(textvariable="4.5e-5")
                    self.NPTWaterCompressibility.grid(row=94,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.NPTWaterCompressibility, msg="The compressability of water.", delay=1.0)

                    self.NPTCoordScalingText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Coordinate Scaling:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTCoordScalingText.grid(row=95,column=0,padx=20,pady=10,sticky='w')
                    self.NPTCoordScalingSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["com", "all", "no"])
                    self.NPTCoordScalingSelection.grid(row=95,column=1,sticky='ew')
                    ToolTip(self.NPTCoordScalingSelection, msg='Scale of pressure coupling.',delay=1)

                    self.NPTBoundryTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Boundry Type:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTBoundryTypeText.grid(row=96,column=0,padx=20,pady=10,sticky='w')
                    self.NPTBoundryTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["xyz", "xy", "no"])
                    self.NPTBoundryTypeSelection.grid(row=96,column=1,sticky='ew')
                    ToolTip(self.NPTBoundryTypeSelection, msg='Specifies the dimensions periodic boundry conditions will be calculated in.',delay=1)

                    self.NPTGenVelocityText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Generate Velocity:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTGenVelocityText.grid(row=97,column=0,padx=20,pady=10,sticky='w')
                    NPTGenVelocity = customtkinter.StringVar(value='no')
                    self.NPTGenVelocitySwitch = customtkinter.CTkSwitch(self.AdvancedOptionsFrame,variable=NPTGenVelocity, text='', onvalue='yes', offvalue='no')
                    self.NPTGenVelocitySwitch.grid(row=97,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.NPTGenVelocitySwitch, msg="Indicates whether to generate velocity values.", delay=1.0)

                    self.NPT_Seed = -1
                    self.NPTSeedText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Seed:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.NPTSeedText.grid(row=98,column=0,padx=20,pady=10,sticky='w')
                    self.NPTSeed = customtkinter.CTkEntry(self.AdvancedOptionsFrame, placeholder_text="e.g. -1")
                    self.NPTSeed.configure(textvariable="-1")
                    self.NPTSeed.grid(row=98,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.NPTSeed, msg="Detirmines the seed for the simulation. -1 to set to random..", delay=1.0)

                    self.NPTMDPSpacer = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text=" ", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.NPTMDPSpacer.grid(row=99, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")
                    


                    # PROD #
                    self.PRODMDPTitle = customtkinter.CTkLabel(self.AdvancedOptionsFrame, text="PROD MDP Options", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.PRODMDPTitle.grid(row=100, column = 0, columnspan = 2, padx=20, pady=10,sticky="we")

                    self.PROD_Restrain = '-DPOSRES'
                    self.PRODRestrainText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Restrain Proteins:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODRestrainText.grid(row=101,column=0,padx=20,pady=10,sticky='w')
                    PRODRestrain = customtkinter.StringVar(value='-DPOSRES')
                    self.PRODRestrainSwitch = customtkinter.CTkSwitch(self.AdvancedOptionsFrame,variable=PRODRestrain, text='', onvalue='-DPOSRES', offvalue='-DFLEXIBLE')
                    self.PRODRestrainSwitch.grid(row=101,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.PRODRestrainSwitch, msg="Prevents the protein from undergoing motion when enabled.", delay=1.0)

                    self.PROD_Integrator = "md"
                    self.PRODIntegratorText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Integration Method:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODIntegratorText.grid(row=102,column=0,padx=20,pady=10,sticky='w')
                    self.PRODIntegratorSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Steep", "md", "md-vv", "md-vv-avek", "sd", "bd", "cg", "l-bfgs", "nm", "tpi", "tpic", "mimic"])
                    self.PRODIntegratorSelection.set("md")
                    self.PRODIntegratorSelection.grid(row=102,column=1,sticky='ew')
                    ToolTip(self.PRODIntegratorSelection, msg='Specifies the integration method used for the PROD stage.',delay=1)

                    self.PROD_Granularity = 2
                    self.PRODGranularityText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Granularity (fs):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODGranularityText.grid(row=103,column=0,padx=20,pady=10,sticky='w')
                    self.PRODGranularityFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.PRODGranularityFrame.grid(row=103,column=1,sticky='ew')
                    self.PRODGranularity = customtkinter.CTkSlider(self.PRODGranularityFrame, from_=0, to=10, command=self.PRODGranularityUpdate, number_of_steps=20, width=130)
                    self.PRODGranularity.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.PRODGranularityText = customtkinter.CTkLabel(self.PRODGranularityFrame,text='2.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.PRODGranularityText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.PRODGranularity.set(2)
                    ToolTip(self.PRODGranularity, msg="The step size for newtonian equations when performing energy minimisation.", delay=1.0)

                    self.PRODForceUpdateLabel = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Update Rate (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODForceUpdateLabel.grid(row=104,column=0,padx=20,pady=10,sticky='w')
                    self.PRODForceUpdateFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.PRODForceUpdateFrame.grid(row=104,column=1,sticky='ew')
                    self.PRODForceUpdate = customtkinter.CTkSlider(self.PRODForceUpdateFrame, from_=0, to=10, command=self.PRODForceUpdateUpdate, number_of_steps=50, width=130)
                    self.PRODForceUpdate.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.PRODForceUpdateText = customtkinter.CTkLabel(self.PRODForceUpdateFrame,text='10.0' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.PRODForceUpdateText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.PRODForceUpdate.set(10)
                    ToolTip(self.PRODForceUpdate, msg="The rate at which an update will be written to the log file. (e.g. 2 = every 2 picoseconds).", delay=1.0)

                    self.PROD_Compress = "System"
                    self.PRODCompressedGroupsText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Saved Groups:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODCompressedGroupsText.grid(row=105,column=0,padx=20,pady=10,sticky='w')
                    self.PRODCompressedGroupsSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["System"])
                    self.PRODCompressedGroupsSelection.set("System")
                    self.PRODCompressedGroupsSelection.grid(row=105,column=1,sticky='ew')
                    ToolTip(self.PRODCompressedGroupsSelection, msg='Specifies what data will be saved from simulation.',delay=1)

                    self.PROD_Continued = True
                    self.PRODContinuedText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Continued Simulation:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODContinuedText.grid(row=106,column=0,padx=20,pady=10,sticky='w')
                    PRODContinued = customtkinter.StringVar(value='yes')
                    self.PRODContinuedSwitch = customtkinter.CTkSwitch(self.AdvancedOptionsFrame,variable=PRODContinued, text='', onvalue='yes', offvalue='no')
                    self.PRODContinuedSwitch.grid(row=106,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.PRODContinuedSwitch, msg="Indicates whether this simulation is continued from a previous simulation.", delay=1.0)

                    self.PROD_ConstraintAlgorithm = "lincs"
                    self.PRODConstraintAlgorithmText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Constraint Algorithm:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODConstraintAlgorithmText.grid(row=107,column=0,padx=20,pady=10,sticky='w')
                    self.PRODConstraintAlgorithmSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["lincs", "SHAKE"])
                    self.PRODConstraintAlgorithmSelection.set("lincs")
                    self.PRODConstraintAlgorithmSelection.grid(row=107,column=1,sticky='ew')
                    ToolTip(self.PRODConstraintAlgorithmSelection, msg='Specifies the constraint algorithm used for the PROD stage.',delay=1)

                    self.PROD_Constraints = "h-bonds"
                    self.PRODConstraintTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Constrained Items:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODConstraintTypeText.grid(row=108,column=0,padx=20,pady=10,sticky='w')
                    self.PRODConstraintTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["h-bonds", "all-bonds", "h-angles", "all-angles", "none"])
                    self.PRODConstraintTypeSelection.set("h-bonds")
                    self.PRODConstraintTypeSelection.grid(row=108,column=1,sticky='ew')
                    ToolTip(self.PRODConstraintTypeSelection, msg='Specifies what simulated objects will be constrainedfor the PROD stage.',delay=1)

                    self.PROD_lincs_iter = 1
                    self.PRODlincsText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="LINCS Accuracy:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODlincsText.grid(row=109,column=0,padx=20,pady=10,sticky='w')
                    self.PRODlincsFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.PRODlincsFrame.grid(row=109,column=1,sticky='ew')
                    self.PRODlincs = customtkinter.CTkSlider(self.PRODlincsFrame, from_=0, to=10, command=self.PRODlincsUpdate, number_of_steps=10, width=130)
                    self.PRODlincs.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.PRODlincsText = customtkinter.CTkLabel(self.PRODlincsFrame,text='1.0' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.PRODlincsText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.PRODlincs.set(1)
                    ToolTip(self.PRODlincs, msg="Detirmines the accuracy of constraint algorithm.", delay=1.0)

                    self.PROD_lincs_order = 4
                    self.PRODOrderText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="LINCS Order:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODOrderText.grid(row=110,column=0,padx=20,pady=10,sticky='w')
                    self.PRODOrderFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.PRODOrderFrame.grid(row=110,column=1,sticky='ew')
                    self.PRODOrder = customtkinter.CTkSlider(self.PRODOrderFrame, from_=0, to=10, command=self.PRODOrderUpdate, number_of_steps=10, width=130)
                    self.PRODOrder.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.PRODOrderText = customtkinter.CTkLabel(self.PRODOrderFrame,text='4.0' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.PRODOrderText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.PRODOrder.set(4)
                    ToolTip(self.PRODOrder, msg="Detirmines the order of constraint algorithm. Impacts accuracy.", delay=1.0)

                    self.PROD_NeighbourScheme = "Verlet"
                    self.PRODNeighbourSchemeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Neighbour Detection:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODNeighbourSchemeText.grid(row=111,column=0,padx=20,pady=10,sticky='w')
                    self.PRODNeighbourSchemeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Verlet", "group"])
                    self.PRODNeighbourSchemeSelection.grid(row=111,column=1,sticky='ew')
                    ToolTip(self.PRODNeighbourSchemeSelection, msg='Specifies the neighbour detection method used by the energy minimisation system.',delay=1)

                    self.PROD_NeighbourListMethod = "grid"
                    self.PRODNeighbourListText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Neighbour Search:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODNeighbourListText.grid(row=112,column=0,padx=20,pady=10,sticky='w')
                    self.PRODNeighbourListSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Grid"])
                    self.PRODNeighbourListSelection.grid(row=112,column=1,sticky='ew')
                    ToolTip(self.PRODNeighbourListSelection, msg='Specifies the neighbour searching method used by the energy minimisation system.',delay=1)

                    self.PROD_ColoumbCutoff = 1.4
                    self.PRODColoumbCutoffText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Range:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODColoumbCutoffText.grid(row=114,column=0,padx=20,pady=10,sticky='w')
                    self.PRODColoumbCutoffFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.PRODColoumbCutoffFrame.grid(row=114,column=1,sticky='ew')
                    self.PRODColoumbCutoff = customtkinter.CTkSlider(self.PRODColoumbCutoffFrame, from_=0, to=5, command=self.PRODColoumbCutoffUpdate, number_of_steps=25, width=130)
                    self.PRODColoumbCutoff.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.PRODColoumbCutoffText = customtkinter.CTkLabel(self.PRODColoumbCutoffFrame,text='1.4' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.PRODColoumbCutoffText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.PRODColoumbCutoff.set(1.4)
                    ToolTip(self.PRODColoumbCutoff, msg="The interaction cutoff range for electrostatic interactions. Measured in nm.", delay=1.0)

                    self.PROD_VanderwaalCutoff = 1.4
                    self.PRODVanderwaalCutoffText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Vanderwaal Range:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODVanderwaalCutoffText.grid(row=115,column=0,padx=20,pady=10,sticky='w')
                    self.PRODVanderwaalCutoffFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.PRODVanderwaalCutoffFrame.grid(row=115,column=1,sticky='ew')
                    self.PRODVanderwaalCutoff = customtkinter.CTkSlider(self.PRODVanderwaalCutoffFrame, from_=0, to=5, command=self.PRODVanderwaalCutoffUpdate, number_of_steps=25, width=130)
                    self.PRODVanderwaalCutoff.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.PRODVanderwaalCutoffText = customtkinter.CTkLabel(self.PRODVanderwaalCutoffFrame,text='1.4' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.PRODVanderwaalCutoffText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.PRODVanderwaalCutoff.set(1.4)
                    ToolTip(self.PRODVanderwaalCutoff, msg="The interaction cutoff range for van der Waals interactions. Measured in nm.", delay=1.0)

                    self.PROD_DispCorr = "EnerPres"
                    self.PRODDispCorrText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Dispersion Correction:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODDispCorrText.grid(row=116,column=0,padx=20,pady=10,sticky='w')
                    self.PRODDispCorrSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["EnerPres", "Ener", "no"])
                    self.PRODDispCorrSelection.grid(row=116,column=1,sticky='ew')
                    ToolTip(self.PRODDispCorrSelection, msg='Aids with Van der Waals cutoff scheme.',delay=1)

                    self.PROD_ColoumbType = "PME"
                    self.PRODColoumbTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Model:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODColoumbTypeText.grid(row=117,column=0,padx=20,pady=10,sticky='w')
                    self.PRODColoumbTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["PME", "Cut-off", "Ewald", "P3M-AD", "Reaction-Field"])
                    self.PRODColoumbTypeSelection.grid(row=117,column=1,sticky='ew')
                    ToolTip(self.PRODColoumbTypeSelection, msg='Specifies the type of model used for long range electrostatic calculations.',delay=1)

                    self.PROD_PMEOrder = 4
                    self.PRODPMEOrderText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Electrostatic Order:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODPMEOrderText.grid(row=118,column=0,padx=20,pady=10,sticky='w')
                    self.PRODPMEOrderFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.PRODPMEOrderFrame.grid(row=118,column=1,sticky='ew')
                    self.PRODPMEOrder = customtkinter.CTkSlider(self.PRODPMEOrderFrame, from_=0, to=10, command=self.PRODPMEOrderUpdate, number_of_steps=10, width=130)
                    self.PRODPMEOrder.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.PRODPMEOrderText = customtkinter.CTkLabel(self.PRODPMEOrderFrame,text='4.00' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.PRODPMEOrderText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.PRODPMEOrder.set(4)
                    ToolTip(self.PRODPMEOrder, msg="Order of interpolation for electrostatic model.", delay=1.0)

                    self.PROD_FourierSpacing = 0.1
                    self.PRODFourierSpacingText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Fourier Spacing:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODFourierSpacingText.grid(row=119,column=0,padx=20,pady=10,sticky='w')
                    self.PRODFourierSpacingFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.PRODFourierSpacingFrame.grid(row=119,column=1,sticky='ew')
                    self.PRODFourierSpacing = customtkinter.CTkSlider(self.PRODFourierSpacingFrame, from_=0, to=1, command=self.PRODFourierSpacingUpdate, number_of_steps=10, width=130)
                    self.PRODFourierSpacing.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.PRODFourierSpacingText = customtkinter.CTkLabel(self.PRODFourierSpacingFrame,text='0.1' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.PRODFourierSpacingText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.PRODFourierSpacing.set(0.1)
                    ToolTip(self.PRODFourierSpacing, msg="Grid spacing for FFT calculations.", delay=1.0)

                    self.PROD_TempCoupling = "V-rescale"
                    self.PRODTempCouplingText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Coupling Model [T]:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODTempCouplingText.grid(row=120,column=0,padx=20,pady=10,sticky='w')
                    self.PRODTempCouplingSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["V-rescale", "berendsen", "nose-hoover", "andersen", "andersen-massive", "no"])
                    self.PRODTempCouplingSelection.grid(row=120,column=1,sticky='ew')
                    ToolTip(self.PRODTempCouplingSelection, msg='Method of coupling temperature.',delay=1)

                    self.PROD_CouplingGroups = "Protein Non-Protein"
                    self.PRODCouplingGroupsText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Coupling Groups:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODCouplingGroupsText.grid(row=121,column=0,padx=20,pady=10,sticky='w')
                    self.PRODCouplingGroupsSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Protein Non-Protein"])
                    self.PRODCouplingGroupsSelection.grid(row=121,column=1,sticky='ew')
                    ToolTip(self.PRODCouplingGroupsSelection, msg='Determines which groups should be coupled.',delay=1)

                    self.PROD_TempTimeConstant = 0.1 #ps
                    self.PRODTempTimeConstantText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Time Constant (ps):",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODTempTimeConstantText.grid(row=122,column=0,padx=20,pady=10,sticky='w')
                    self.PRODTempTimeConstantFrame = customtkinter.CTkFrame(self.AdvancedOptionsFrame)
                    self.PRODTempTimeConstantFrame.grid(row=122,column=1,sticky='ew')
                    self.PRODTempTimeConstant = customtkinter.CTkSlider(self.PRODTempTimeConstantFrame, from_=0, to=1, command=self.PRODTempTimeConstantUpdate, number_of_steps=10, width=130)
                    self.PRODTempTimeConstant.grid(row=0,column=1,padx=20,pady=10,sticky='w')
                    self.PRODTempTimeConstantText = customtkinter.CTkLabel(self.PRODTempTimeConstantFrame,text='0.1' ,fg_color="transparent",font=('arial',12),anchor='center')
                    self.PRODTempTimeConstantText.grid(row=0,column=0,padx=(10,0),pady=0,sticky='e')
                    self.PRODTempTimeConstant.set(0.1)
                    ToolTip(self.PRODTempTimeConstant, msg="Time constant for temperature coupling.", delay=1.0)

                    self.PROD_PressureCoupling = "Parrinello-Rahman"
                    self.PRODPressureCouplingText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="P Coupling Model [P]:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODPressureCouplingText.grid(row=123,column=0,padx=20,pady=10,sticky='w')
                    self.PRODPressureCouplingSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["Parrinello-Rahman", "Berendsen", "C-rescale",  "MTTK", "no"])
                    self.PRODPressureCouplingSelection.grid(row=123,column=1,sticky='ew')
                    ToolTip(self.PRODPressureCouplingSelection, msg='Method of coupling pressure.',delay=1)

                    self.PROD_CoupleType = "isotropic"
                    self.PRODPressureCoupleTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Coupling Type [P]:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODPressureCoupleTypeText.grid(row=124,column=0,padx=20,pady=10,sticky='w')
                    self.PRODPressureCoupleTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["isotropic", "semiisotropic", "anisotropic", "surface-tension"])
                    self.PRODPressureCoupleTypeSelection.grid(row=124,column=1,sticky='ew')
                    ToolTip(self.PRODPressureCoupleTypeSelection, msg='Scale of pressure coupling.',delay=1)

                    self.PROD_Compressibility = "4.5e-5"
                    self.PRODWaterCompressibilityText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Water Compressibility:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODWaterCompressibilityText.grid(row=125,column=0,padx=20,pady=10,sticky='w')
                    self.PRODWaterCompressibility = customtkinter.CTkEntry(self.AdvancedOptionsFrame, placeholder_text="e.g. 4.5e-5")
                    self.PRODWaterCompressibility.configure(textvariable="4.5e-5")
                    self.PRODWaterCompressibility.grid(row=125,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.PRODWaterCompressibility, msg="The compressability of water.", delay=1.0)

                    self.PROD_BoundryType = 'xyz'
                    self.PRODBoundryTypeText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Boundry Type:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODBoundryTypeText.grid(row=126,column=0,padx=20,pady=10,sticky='w')
                    self.PRODBoundryTypeSelection = customtkinter.CTkComboBox(self.AdvancedOptionsFrame, values=["xyz", "xy", "no"])
                    self.PRODBoundryTypeSelection.grid(row=126,column=1,sticky='ew')
                    ToolTip(self.PRODBoundryTypeSelection, msg='Specifies the dimensions periodic boundry conditions will be calculated in.',delay=1)

                    self.PRODGenVelocityText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Generate Velocity:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODGenVelocityText.grid(row=127,column=0,padx=20,pady=10,sticky='w')
                    PRODGenVelocity = customtkinter.StringVar(value='no')
                    self.PRODGenVelocitySwitch = customtkinter.CTkSwitch(self.AdvancedOptionsFrame,variable=PRODGenVelocity, text='', onvalue='yes', offvalue='no')
                    self.PRODGenVelocitySwitch.grid(row=127,column=1,sticky='e',padx=(0,25))
                    ToolTip(self.PRODGenVelocitySwitch, msg="Indicates whether to generate velocity values.", delay=1.0)

                    self.PRODSeedText = customtkinter.CTkLabel(self.AdvancedOptionsFrame,text="Seed:",fg_color="transparent",font=('arial',16),anchor='w')
                    self.PRODSeedText.grid(row=128,column=0,padx=20,pady=10,sticky='w')
                    self.PRODSeed = customtkinter.CTkEntry(self.AdvancedOptionsFrame, placeholder_text="e.g. -1")
                    self.PRODSeed.configure(textvariable="-1")
                    self.PRODSeed.grid(row=128,column=1,padx=0,pady=10,sticky='ew')
                    ToolTip(self.PRODSeed, msg="Detirmines the seed for the simulation. -1 to set to random..", delay=1.0)



                #-----------------------------------------------------### GENERATOR FUNCTIONS ###----------------------------------------------------------------------------#
                # Script Settings #
                def ToggleFilepath(self):
                    MainApp.PrintOutputs(self.PathSwitch.get())
                    if self.PathSwitch.get() == 'Automatic':
                        self.PathName.configure(placeholder_text="Set to Automatic",state='disabled')
                    else:
                        self.PathName.configure(state='normal',placeholder_text="e.g. /project/RDS-ABC-AB/...")

                def SelectProteinName(self):
                    global ProteinFilePath
                    global ProteinFileName
                    global ProteinSize
                    try:
                        ProteinFilePath = tkinter.filedialog.askopenfilename()
                        ProteinFileName = os.path.basename(ProteinFilePath)
                        self.Filename.configure(text=ProteinFileName)
                        MainApp.PrintOutputs(f"Found Protein!: {ProteinFileName}")
                        MainApp.PrintOutputs(f"Path to File: {ProteinFilePath}")
                        FileContents = open(ProteinFilePath, 'r')
                    except:
                         MainApp.PrintOutputs("No protein selected!")
                    ProteinSize = 0
                    try:
                        for line in FileContents:
                            words = line.split()
                            for i in words:
                                if(i=="ATOM"):
                                    ProteinSize +=1
                        MainApp.PrintOutputs(f"File has approximately {ProteinSize} atoms!")
                    except:
                         MainApp.PrintOutputs("Cannot determine perotein size.")

                def SimTypeSelection(self,option):
                    if option == 'Multi-Protein':
                        self.ProteinQuantity.configure(state='normal')
                        self.ProteinQuantity.configure(button_color='blue')
                    else:
                        self.ProteinQuantity.set(1)
                        self.QuantityText.configure(text='01')
                        self.ProteinQuantity.configure(state='disabled')
                        self.ProteinQuantity.configure(button_color='grey')

                def ProteinCountUpdate(self, value):
                    self.QuantityText.configure(text=(str((int(value)))).zfill(2))
                
                # Hardware Options #
                def ParallelOptionToggle(self):
                    if self.ParallelSwitch.get() == 'Parallel':
                        self.NodeCount.configure(state='normal')
                    else:
                        self.NodeCount.set(1)
                        self.NodeCountText.configure(text='01')
                        self.NodeCount.configure(state='disabled')

                def CPUCountUpdate(self, value):
                    self.CPUCountText.configure(text=(str((int(value)))).zfill(2))

                def GPUCountUpdate(self, value):
                    self.GPUCountText.configure(text=(str((int(value)))).zfill(1))

                def MemoryAllocationUpdate(self, value):
                    self.MemoryAllocationText.configure(text=(str((int(value)))).zfill(2))

                def NodeCountUpdate(self, value):
                    self.NodeCountText.configure(text=(str((int(value)))).zfill(2))

                # Advanced Options #
                def BoundryGapUpdate(self, value):
                    self.BoundryGapText.configure(text=(str((float(value)))).ljust(4,'0'))

                #ION MDP
                def IONLimitUpdate(self, value):
                    self.IONLimitText.configure(text=(str((int(value)))).ljust(5,'_'))
                    
                def IONGranularityUpdate(self, value):
                    self.IONGranularityText.configure(text=(str((float(value)))).ljust(4,'0'))

                def IONForceUpdateUpdate(self, value):
                    self.IONForceUpdateText.configure(text=(str((float(value)))).ljust(4,'0'))

                def IONColoumbCutoffUpdate(self, value):
                    self.IONColoumbCutoffText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def IONVanderwaalCutoffUpdate(self, value):
                    self.IONVanderwaalCutoffText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                #MIN MDP
                def MINLimitUpdate(self, value):
                    self.MINLimitText.configure(text=(str((int(value)))).ljust(5,'_'))

                def MINGranularityUpdate(self, value):
                    self.MINGranularityText.configure(text=(str((float(value)))).ljust(4,'0'))

                def MINForceUpdateUpdate(self, value):
                    self.MINForceUpdateText.configure(text=(str((float(value)))).ljust(4,'0'))

                def MINColoumbCutoffUpdate(self, value):
                    self.MINColoumbCutoffText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def MINVanderwaalCutoffUpdate(self, value):
                    self.MINVanderwaalCutoffText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                #NVT MDP
                def NVTGranularityUpdate(self, value):
                    self.NVTGranularityText.configure(text=(str((float(value)))).ljust(4,'0'))

                def NVTForceUpdateUpdate(self, value):
                    self.NVTForceUpdateText.configure(text=(str((float(value)))).ljust(4,'0'))

                def NVTlincsUpdate(self, value):
                    self.NVTlincsText.configure(text=(str((float(value)))).ljust(4,'0'))

                def NVTOrderUpdate(self, value):
                    self.NVTOrderText.configure(text=(str((float(value)))).ljust(4,'0'))

                def NVTColoumbCutoffUpdate(self, value):
                    self.NVTColoumbCutoffText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def NVTVanderwaalCutoffUpdate(self, value):
                    self.NVTVanderwaalCutoffText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def NVTPMEOrderUpdate(self, value):
                    self.NVTPMEOrderText.configure(text=(str((float(value)))).ljust(4,'0'))

                def NVTFourierSpacingUpdate(self, value):
                    self.NVTFourierSpacingText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def NVTTempTimeConstantUpdate(self, value):
                    self.NVTTempTimeConstantText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                #NPT MDP
                def NPTGranularityUpdate(self, value):
                    self.NPTGranularityText.configure(text=(str((float(value)))).ljust(4,'0'))

                def NPTForceUpdateUpdate(self, value):
                    self.NPTForceUpdateText.configure(text=(str((float(value)))).ljust(4,'0'))

                def NPTlincsUpdate(self, value):
                    self.NPTlincsText.configure(text=(str((float(value)))).ljust(4,'0'))

                def NPTOrderUpdate(self, value):
                    self.NPTOrderText.configure(text=(str((float(value)))).ljust(4,'0'))

                def NPTColoumbCutoffUpdate(self, value):
                    self.NPTColoumbCutoffText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def NPTVanderwaalCutoffUpdate(self, value):
                    self.NPTVanderwaalCutoffText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def NPTPMEOrderUpdate(self, value):
                    self.NPTPMEOrderText.configure(text=(str((float(value)))).ljust(4,'0'))

                def NPTFourierSpacingUpdate(self, value):
                    self.NPTFourierSpacingText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def NPTTempTimeConstantUpdate(self, value):
                    self.NPTTempTimeConstantText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                #SIM MDP
                def PRODGranularityUpdate(self, value):
                    self.PRODGranularityText.configure(text=(str((float(value)))).ljust(4,'0'))

                def PRODForceUpdateUpdate(self, value):
                    self.PRODForceUpdateText.configure(text=(str((float(value)))).ljust(4,'0'))

                def PRODlincsUpdate(self, value):
                    self.PRODlincsText.configure(text=(str((float(value)))).ljust(4,'0'))

                def PRODOrderUpdate(self, value):
                    self.PRODOrderText.configure(text=(str((float(value)))).ljust(4,'0'))

                def PRODColoumbCutoffUpdate(self, value):
                    self.PRODColoumbCutoffText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def PRODVanderwaalCutoffUpdate(self, value):
                    self.PRODVanderwaalCutoffText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def PRODPMEOrderUpdate(self, value):
                    self.PRODPMEOrderText.configure(text=(str((float(value)))).ljust(4,'0'))

                def PRODFourierSpacingUpdate(self, value):
                    self.PRODFourierSpacingText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))

                def PRODTempTimeConstantUpdate(self, value):
                    self.PRODTempTimeConstantText.configure(text=(str((float(round(value,1))))).ljust(3,'0'))
               
                    

                    





class ScriptWindow(customtkinter.CTkToplevel):
                def __init__(self, *args, **kwargs):
                    super().__init__()


                    ### Window Setup ###
                    self.title("MDS Script Generator")
                    self.geometry("480x720")
                    self.grid_columnconfigure((0, 0), weight=1)
                    self.grid_rowconfigure((0, 0), weight=1)
                    self.appearance = customtkinter.set_appearance_mode("system")
                    self.colourtheme = customtkinter.set_default_color_theme("blue")
                    self.grab_set()

                    self.ScriptWindowTabs = ScriptTabs(self)
                    self.ScriptWindowTabs.grid(row=0,column=0,sticky="nsew",padx=20, pady=(0,20))

                    self.ConfirmScriptButton = customtkinter.CTkButton(self, text="Generate Script",font=('arial',20), command=self.GenerateScriptButton)
                    self.ConfirmScriptButton.grid(row=1,column=0, padx=20, pady=(0,20),sticky='sew')


                ### SELECTION VALIDATION ###
                def GenerateScriptButton(self):
                    MainApp.PrintOutputs("Generating Script!")
                    try:
                        ScriptOptions = {
                            "Script Name":self.ScriptWindowTabs.ScriptName.get(),
                            "Path Option":self.ScriptWindowTabs.PathSwitch.get(),
                            "Path Text":self.ScriptWindowTabs.PathName.get(),
                            "Protein Filepath":ProteinFilePath,
                            "Protein Filename":ProteinFileName,
                            "Protein Size":ProteinSize,
                            "ML Generated":self.ScriptWindowTabs.GeneratedStructure.get(),
                            "Sim Type":self.ScriptWindowTabs.SimType.get(),
                            "Protein Count":round(self.ScriptWindowTabs.ProteinQuantity.get(),0),
                            "Email Address":self.ScriptWindowTabs.Email.get()
                            }
                        MDSOptions = {
                            "Sim Temperature":self.ScriptWindowTabs.Temperature.get(),
                            "Sim Pressure":self.ScriptWindowTabs.Pressure.get(),
                            "Solvent Selected":self.ScriptWindowTabs.SolventType.get(),
                            "Force Field":self.ScriptWindowTabs.ForceFieldSelection.get(),
                            "Minimisation Time":self.ScriptWindowTabs.MinimisationTime.get(),
                            "NVT Time":self.ScriptWindowTabs.NVTTime.get(),
                            "NPT Time":self.ScriptWindowTabs.NPTTime.get(),
                            "Production Time":self.ScriptWindowTabs.ProductionTime.get()
                            }
                        HardwareOptions = {
                            "Node Mode":self.ScriptWindowTabs.ParallelSwitch.get(),
                            "Node Count":round(self.ScriptWindowTabs.NodeCount.get(),0),
                            "CPU Count":round(self.ScriptWindowTabs.CPUCount.get(),0),
                            "GPU Count":round(self.ScriptWindowTabs.GPUCount.get(),0),
                            "Memory Allocation":round(self.ScriptWindowTabs.MemoryAllocation.get(),0),
                            "Walltime Hours":self.ScriptWindowTabs.WalltimeHours.get(),
                            "Walltime Minutes":self.ScriptWindowTabs.WalltimeMinutes.get(),
                            "Walltime Seconds":self.ScriptWindowTabs.WalltimeSeconds.get()
                            }
                        AdvancedOptions = {
                            "Gromacs Build":self.ScriptWindowTabs.GromacsModuleSelection.get(),
                            "Remove Water":self.ScriptWindowTabs.RemoveWaterSwitch.get(),
                            "Water Model":self.ScriptWindowTabs.WaterModelSelection.get(),
                            "System Charge":self.ScriptWindowTabs.SystemChargeSelection.get(),
                            "Positive Charge":self.ScriptWindowTabs.PositiveChargeSelection.get(),
                            "Negative Charge":self.ScriptWindowTabs.NegativeChargeSelection.get(),
                            "Boundry Option":self.ScriptWindowTabs.BoundryTypeSelection.get(),
                            "Boundry Gap":round(self.ScriptWindowTabs.BoundryGap.get(),2)
                            }
                        ION_MDP = {
                            "ION Integrator":self.ScriptWindowTabs.IONIntegratorSelection.get(),
                            "ION Minimum Limit":round(self.ScriptWindowTabs.IONLimit.get(),0),
                            "ION Time":self.ScriptWindowTabs.IONTime.get(),
                            "ION Granularity":round(self.ScriptWindowTabs.IONGranularity.get(),1),
                            "ION Update Frequency":round(self.ScriptWindowTabs.IONForceUpdate.get(),1),
                            "ION Neighbour Scheme":self.ScriptWindowTabs.IONNeighbourSchemeSelection.get(),
                            "ION Neighbour Method":self.ScriptWindowTabs.IONNeighbourListSelection.get(),
                            "ION Coloumb Type":self.ScriptWindowTabs.IONColoumbTypeSelection.get(),
                            "ION Coloumb Cutoff":round(self.ScriptWindowTabs.IONColoumbCutoff.get(),1),
                            "ION Van der Waal Cutoff":round(self.ScriptWindowTabs.IONVanderwaalCutoff.get(),1),
                            "ION Boundry Type":self.ScriptWindowTabs.IONBoundryTypeSelection.get()
                            }
                        MIN_MDP = {
                            "MIN Integrator":self.ScriptWindowTabs.MINIntegratorSelection.get(),
                            "MIN Minimum Limit":round(self.ScriptWindowTabs.MINLimit.get(),0),
                            "MIN Granularity":round(self.ScriptWindowTabs.MINGranularity.get(),1),
                            "MIN Update Frequency":round(self.ScriptWindowTabs.MINForceUpdate.get(),1),
                            "MIN Neighbour Scheme":self.ScriptWindowTabs.MINNeighbourSchemeSelection.get(),
                            "MIN Neighbour Method":self.ScriptWindowTabs.MINNeighbourListSelection.get(),
                            "MIN Coloumb Type":self.ScriptWindowTabs.MINColoumbTypeSelection.get(),
                            "MIN Coloumb Cutoff":round(self.ScriptWindowTabs.MINColoumbCutoff.get(),1),
                            "MIN Van der Waal Cutoff":round(self.ScriptWindowTabs.MINVanderwaalCutoff.get(),1),
                            "MIN Boundry Type":self.ScriptWindowTabs.MINBoundryTypeSelection.get()
                            }
                        NVT_MDP = {
                            "NVT Restrain":self.ScriptWindowTabs.NVTRestrainSwitch.get(),
                            "NVT Integrator":self.ScriptWindowTabs.NVTIntegratorSelection.get(),
                            "NVT Granularity":round(self.ScriptWindowTabs.NVTGranularity.get(),1),
                            "NVT Update Frequency":round(self.ScriptWindowTabs.NVTForceUpdate.get(),1),
                            "NVT Continued":self.ScriptWindowTabs.NVTContinuedSwitch.get(),
                            "NVT Constraint Algorithm":self.ScriptWindowTabs.NVTConstraintAlgorithmSelection.get(),
                            "NVT Constraints":self.ScriptWindowTabs.NVTConstraintTypeSelection.get(),
                            "NVT LINCS Iterations":round(self.ScriptWindowTabs.NVTlincs.get(),0),
                            "NVT LINCS Order":round(self.ScriptWindowTabs.NVTOrder.get(),0),
                            "NVT Neighbour Scheme":self.ScriptWindowTabs.NVTNeighbourSchemeSelection.get(),
                            "NVT Neighbour Method":self.ScriptWindowTabs.NVTNeighbourListSelection.get(),
                            "NVT Coloumb Cutoff":round(self.ScriptWindowTabs.NVTColoumbCutoff.get(),1),
                            "NVT Van der Waal Cutoff":round(self.ScriptWindowTabs.NVTVanderwaalCutoff.get(),1),
                            "NVT VdW Correction":self.ScriptWindowTabs.NVTDispCorrSelection.get(),
                            "NVT Coloumb Type":self.ScriptWindowTabs.NVTColoumbTypeSelection.get(),
                            "NVT PME Order":round(self.ScriptWindowTabs.NVTPMEOrder.get(),0),
                            "NVT Fourier Spacing":round(self.ScriptWindowTabs.NVTFourierSpacing.get(),1),
                            "NVT Temperature Coupling":self.ScriptWindowTabs.NVTTempCouplingSelection.get(),
                            "NVT Coupling Groups":self.ScriptWindowTabs.NVTCouplingGroupsSelection.get(),
                            "NVT Temp Time Constant":round(self.ScriptWindowTabs.NVTTempTimeConstant.get(),1),
                            "NVT Boundry Type":self.ScriptWindowTabs.NVTBoundryTypeSelection.get(),
                            "NVT Gen Velocity":self.ScriptWindowTabs.NVTGenVelocitySwitch.get(),
                            "NVT Seed":self.ScriptWindowTabs.NVTSeed.get()
                            }
                        NPT_MDP = {
                            "NPT Restrain":self.ScriptWindowTabs.NPTRestrainSwitch.get(),
                            "NPT Integrator":self.ScriptWindowTabs.NPTIntegratorSelection.get(),
                            "NPT Granularity":round(self.ScriptWindowTabs.NPTGranularity.get(),1),
                            "NPT Update Frequency":round(self.ScriptWindowTabs.NPTForceUpdate.get(),1),
                            "NPT Continued":self.ScriptWindowTabs.NPTContinuedSwitch.get(),
                            "NPT Constraint Algorithm":self.ScriptWindowTabs.NPTConstraintAlgorithmSelection.get(),
                            "NPT Constraints":self.ScriptWindowTabs.NPTConstraintTypeSelection.get(),
                            "NPT LINCS Iterations":round(self.ScriptWindowTabs.NPTlincs.get(),0),
                            "NPT LINCS Order":round(self.ScriptWindowTabs.NPTOrder.get(),0),
                            "NPT Neighbour Scheme":self.ScriptWindowTabs.NPTNeighbourSchemeSelection.get(),
                            "NPT Neighbour Method":self.ScriptWindowTabs.NPTNeighbourListSelection.get(),
                            "NPT Coloumb Cutoff":round(self.ScriptWindowTabs.NPTColoumbCutoff.get(),1),
                            "NPT Van der Waal Cutoff":round(self.ScriptWindowTabs.NPTVanderwaalCutoff.get(),1),
                            "NPT VdW Correction":self.ScriptWindowTabs.NPTDispCorrSelection.get(),
                            "NPT Coloumb Type":self.ScriptWindowTabs.NPTColoumbTypeSelection.get(),
                            "NPT PME Order":round(self.ScriptWindowTabs.NPTPMEOrder.get(),0),
                            "NPT Fourier Spacing":round(self.ScriptWindowTabs.NPTFourierSpacing.get(),1),
                            "NPT Temperature Coupling":self.ScriptWindowTabs.NPTTempCouplingSelection.get(),
                            "NPT Coupling Groups":self.ScriptWindowTabs.NPTCouplingGroupsSelection.get(),
                            "NPT Temp Time Constant":round(self.ScriptWindowTabs.NPTTempTimeConstant.get(),1),
                            "NPT Pressure Coupling":self.ScriptWindowTabs.NPTPressureCouplingSelection.get(),
                            "NPT Pressure Coupling Type":self.ScriptWindowTabs.NPTPressureCoupleTypeSelection.get(),
                            "NPT Water Compressibility":self.ScriptWindowTabs.NPTWaterCompressibility.get(),
                            "NPT Coordinate Scaling":self.ScriptWindowTabs.NPTCoordScalingSelection.get(),
                            "NPT Boundry Type":self.ScriptWindowTabs.NPTBoundryTypeSelection.get(),
                            "NPT Gen Velocity":self.ScriptWindowTabs.NPTGenVelocitySwitch.get(),
                            "NPT Seed":self.ScriptWindowTabs.NPTSeed.get()
                            }
                        PROD_MDP = {
                            "PROD Restrain":self.ScriptWindowTabs.PRODRestrainSwitch.get(),
                            "PROD Integrator":self.ScriptWindowTabs.PRODIntegratorSelection.get(),
                            "PROD Granularity":round(self.ScriptWindowTabs.PRODGranularity.get(),1),
                            "PROD Update Frequency":round(self.ScriptWindowTabs.PRODForceUpdate.get(),1),
                            "PROD Compress":self.ScriptWindowTabs.PRODCompressedGroupsSelection.get(),
                            "PROD Continued":self.ScriptWindowTabs.PRODContinuedSwitch.get(),
                            "PROD Constraint Algorithm":self.ScriptWindowTabs.PRODConstraintAlgorithmSelection.get(),
                            "PROD Constraints":self.ScriptWindowTabs.PRODConstraintTypeSelection.get(),
                            "PROD LINCS Iterations":round(self.ScriptWindowTabs.PRODlincs.get(),0),
                            "PROD LINCS Order":round(self.ScriptWindowTabs.PRODOrder.get(),0),
                            "PROD Neighbour Scheme":self.ScriptWindowTabs.PRODNeighbourSchemeSelection.get(),
                            "PROD Neighbour Method":self.ScriptWindowTabs.PRODNeighbourListSelection.get(),
                            "PROD Coloumb Cutoff":round(self.ScriptWindowTabs.PRODColoumbCutoff.get(),1),
                            "PROD Van der Waal Cutoff":round(self.ScriptWindowTabs.PRODVanderwaalCutoff.get(),1),
                            "PROD VdW Correction":self.ScriptWindowTabs.PRODDispCorrSelection.get(),
                            "PROD Coloumb Type":self.ScriptWindowTabs.PRODColoumbTypeSelection.get(),
                            "PROD PME Order":round(self.ScriptWindowTabs.PRODPMEOrder.get(),0),
                            "PROD Fourier Spacing":round(self.ScriptWindowTabs.PRODFourierSpacing.get(),1),
                            "PROD Temperature Coupling":self.ScriptWindowTabs.PRODTempCouplingSelection.get(),
                            "PROD Coupling Groups":self.ScriptWindowTabs.PRODCouplingGroupsSelection.get(),
                            "PROD Temp Time Constant":round(self.ScriptWindowTabs.PRODTempTimeConstant.get(),1),
                            "PROD Pressure Coupling":self.ScriptWindowTabs.PRODPressureCouplingSelection.get(),
                            "PROD Pressure Coupling Type":self.ScriptWindowTabs.PRODPressureCoupleTypeSelection.get(),
                            "PROD Water Compressibility":self.ScriptWindowTabs.PRODWaterCompressibility.get(),
                            "PROD Boundry Type":self.ScriptWindowTabs.PRODBoundryTypeSelection.get(),
                            "PROD Gen Velocity":self.ScriptWindowTabs.PRODGenVelocitySwitch.get(),
                            "PROD Seed":self.ScriptWindowTabs.PRODSeed.get()
                        }

                        MainApp.PrintOutputs('Checking Inputs...')
                        MainApp.PrintOutputs("     LISTING RAW INPUTS     ")
                        MainApp.PrintOutputs("\nScript Options Inputs:")
                        MainApp.PrintOutputs(pprint.pformat(ScriptOptions))
                        MainApp.PrintOutputs("\nMDS Option Inputs:")
                        MainApp.PrintOutputs(pprint.pformat(MDSOptions))
                        MainApp.PrintOutputs("\nHardware Option Inputs:")
                        MainApp.PrintOutputs(pprint.pformat(HardwareOptions))
                        MainApp.PrintOutputs("\nAdvanced Options:")
                        MainApp.PrintOutputs(pprint.pformat(AdvancedOptions))
                        MainApp.PrintOutputs("\nION MDP Inputs:")
                        MainApp.PrintOutputs(pprint.pformat(ION_MDP))
                        MainApp.PrintOutputs("\nMinimisation MDP Inputs:")
                        MainApp.PrintOutputs(pprint.pformat(MIN_MDP))
                        MainApp.PrintOutputs("\nNVT MDP Inputs:")
                        MainApp.PrintOutputs(pprint.pformat(NVT_MDP))
                        MainApp.PrintOutputs("\nNPT MDP Inputs:")
                        MainApp.PrintOutputs(pprint.pformat(NPT_MDP))
                        MainApp.PrintOutputs("\nProduction MDP Inputs:")
                        MainApp.PrintOutputs(pprint.pformat(PROD_MDP))
                        MainApp.PrintOutputs("")

                        print("\nChecking  for Errors in Raw Inputs...")
                        TranslatedInputs = CheckScriptInputs(ScriptOptions, MDSOptions, HardwareOptions, AdvancedOptions, ION_MDP, MIN_MDP, NVT_MDP, NPT_MDP, PROD_MDP)
                        if TranslatedInputs["Error Check"] == "Passed":
                            ScriptFile = SG.MDSScriptGen(TranslatedInputs["Script Settings"], TranslatedInputs["MDS Options"], TranslatedInputs["Hardware Options"], TranslatedInputs["Advanced Options"],
                                                        TranslatedInputs["ION MDP"], TranslatedInputs["MIN MDP"], TranslatedInputs["NVT MDP"], TranslatedInputs["NPT MDP"], TranslatedInputs["PROD MDP"]) 
                            ScriptFile.Generate_MDS_Setup_Script()

                            print("     LISTING CHECKED INPUTS     ")
                            print("\nScript Options Inputs:")
                            print(pprint.pformat(TranslatedInputs["Script Settings"]))
                            print("\nMDS Option Inputs:")
                            print(pprint.pformat(TranslatedInputs["MDS Options"]))
                            print("\nHardware Option Inputs:")
                            print(pprint.pformat(TranslatedInputs["Hardware Options"]))
                            print("\nAdvanced Options:")
                            print(pprint.pformat(TranslatedInputs["Advanced Options"]))
                            print("\nION MDP Inputs:")
                            print(pprint.pformat(TranslatedInputs["ION MDP"]))
                            print("\nMinimisation MDP Inputs:")
                            print(pprint.pformat(TranslatedInputs["MIN MDP"]))
                            print("\nNVT MDP Inputs:")
                            print(pprint.pformat(TranslatedInputs["NVT MDP"]))
                            print("\nNPT MDP Inputs:")
                            print(pprint.pformat(TranslatedInputs["NPT MDP"]))
                            print("\nProduction MDP Inputs:")
                            print(pprint.pformat(TranslatedInputs["PROD MDP"]))
                            print("")

                            MainApp.PrintOutputs("MDS SCRIPT SUCCESSFULLY GENERATED!")
                            
                            MainApp.PrintOutputs("Closing Script Generator window.")
                            self.destroy()
                        else:
                            MainApp.PrintOutputs("Inputs are Incorrect. Please Fix!")

                    except:
                        MainApp.PrintOutputs("Some inputs are missing, please check that all input fields are completed!")
                         

class AnalysisWindow(customtkinter.CTkToplevel):
                def __init__(self, *args, **kwargs):
                    super().__init__()


                    ### Window Setup ###
                    self.title("MDS Analysis")
                    self.geometry("480x720")
                    self.grid_columnconfigure((0,0,0), weight=1)
                    self.grid_rowconfigure((0,0,0), weight=0)
                    self.appearance = customtkinter.set_appearance_mode("system")
                    self.colourtheme = customtkinter.set_default_color_theme("blue")
                    self.grab_set()

                    self.Header = customtkinter.CTkLabel(self, text="MD Analysis", fg_color = "transparent", font=('arial',20),anchor=("center"))
                    self.Header.grid(row=0,column=0,columnspan=3, pady=(20,0),sticky="nsew")

                    self.FileSelectTabs = customtkinter.CTkTabview(self)
                    self.FileSelectTabs.grid(row=1,column=0,columnspan=3,sticky="nsew",padx=15)
                    self.FileSelectTabs.add("Single MDS")
                    self.FileSelectTabs.add("Comparative MDS")

                    self.FileSelectFrame = customtkinter.CTkFrame(self.FileSelectTabs.tab("Single MDS"))
                    self.FileSelectFrame.grid(row=0,column=0,sticky='nsew',padx=15)
                    self.FileSelectFrame.grid_columnconfigure((1,3,3), weight=1)
                    self.FileSelectFrame.grid_rowconfigure((0,0), weight=1)

                    self.AnalysisFolderText = customtkinter.CTkLabel(self.FileSelectFrame, text="Analysis Folder:",fg_color="transparent",font=('arial',16),anchor='center')
                    self.AnalysisFolderText.grid(row=0,column=0,columnspan=2,padx=20,sticky='ew')
                    self.AnalysisFolder = customtkinter.CTkButton(self.FileSelectFrame, text="Select File", command=self.SelectAnalysisFolder)
                    self.AnalysisFolder.grid(row=1,column=0,columnspan=2,padx=5,sticky='ew')
                    ToolTip(self.AnalysisFolder, msg="The generated anlysis folder from simulations.", delay=1.0)
                    self.AnalysisFolderEntryText = customtkinter.CTkLabel(self.FileSelectFrame, text="Entry Name:", font=('arial',14),fg_color='transparent')
                    self.AnalysisFolderEntryText.grid(row=2,column=0, padx=5, pady=5,sticky='ew')
                    self.AnalysisFolderEntry = customtkinter.CTkEntry(self.FileSelectFrame)
                    self.AnalysisFolderEntry.grid(row=2, column=1,padx=5,pady=5,sticky='ew')

                    self.AnalysisFolderNPTgro = customtkinter.CTkCheckBox(self.FileSelectFrame, text="Start Structure", state='disabled')
                    self.AnalysisFolderNPTgro.grid(row=0,column=2,padx=5,sticky='e')
                    self.AnalysisFolderPRODgro = customtkinter.CTkCheckBox(self.FileSelectFrame, text="End Structure", state='disabled')
                    self.AnalysisFolderPRODgro.grid(row=1,column=2,padx=10,sticky='e')
                    self.AnalysisFolderTraj = customtkinter.CTkCheckBox(self.FileSelectFrame, text="Simulation Trajectory", state='disabled')
                    self.AnalysisFolderTraj.grid(row=2,column=2,padx=10, columnspan=2,sticky='e')





                    self.MultiFileSelectFrame = customtkinter.CTkFrame(self.FileSelectTabs.tab("Comparative MDS"), width=400)
                    self.MultiFileSelectFrame.grid(row=0,column=0,sticky='nsew')
                    self.MultiFileSelectFrame.grid_columnconfigure((1,3,3), weight=1)
                    self.MultiFileSelectFrame.grid_rowconfigure((0,0), weight=1)


                    self.MultiAnalysis1FolderText = customtkinter.CTkLabel(self.MultiFileSelectFrame, text="Analysis Folder 1:",fg_color="transparent",font=('arial',16),anchor='center')
                    self.MultiAnalysis1FolderText.grid(row=0,column=0,columnspan=2,padx=20,sticky='ew')
                    self.MultiAnalysis1Folder = customtkinter.CTkButton(self.MultiFileSelectFrame, text="Select File", command=self.SelectMultiAnalysis1Folder)
                    self.MultiAnalysis1Folder.grid(row=1,column=0,columnspan=2,padx=5,sticky='ew')
                    ToolTip(self.MultiAnalysis1Folder, msg="The generated anlysis folder from simulations.", delay=1.0)
                    self.MultiAnalysis1FolderEntryText = customtkinter.CTkLabel(self.MultiFileSelectFrame, text="Entry Name:", font=('arial',14),fg_color='transparent')
                    self.MultiAnalysis1FolderEntryText.grid(row=2,column=0, padx=5, pady=5,sticky='ew')
                    self.MultiAnalysis1FolderEntry = customtkinter.CTkEntry(self.MultiFileSelectFrame)
                    self.MultiAnalysis1FolderEntry.grid(row=2, column=1,padx=5,pady=5,sticky='ew')

                    self.MultiAnalysis1FolderNPTgro = customtkinter.CTkCheckBox(self.MultiFileSelectFrame, text="Start Structure", state='disabled')
                    self.MultiAnalysis1FolderNPTgro.grid(row=0,column=2,padx=5,sticky='e')
                    self.MultiAnalysis1FolderPRODgro = customtkinter.CTkCheckBox(self.MultiFileSelectFrame, text="End Structure", state='disabled')
                    self.MultiAnalysis1FolderPRODgro.grid(row=1,column=2,padx=10,sticky='e')
                    self.MultiAnalysis1FolderTraj = customtkinter.CTkCheckBox(self.MultiFileSelectFrame, text="Simulation Trajectory", state='disabled')
                    self.MultiAnalysis1FolderTraj.grid(row=2,column=2,padx=10, columnspan=2,sticky='e')


                    self.MultiAnalysis2FolderText = customtkinter.CTkLabel(self.MultiFileSelectFrame, text="Analysis Folder 2:",fg_color="transparent",font=('arial',16),anchor='center')
                    self.MultiAnalysis2FolderText.grid(row=3,column=0,columnspan=2,padx=20,pady=(10,0),sticky='ew')
                    self.MultiAnalysis2Folder = customtkinter.CTkButton(self.MultiFileSelectFrame, text="Select File", command=self.SelectMultiAnalysis2Folder)
                    self.MultiAnalysis2Folder.grid(row=4,column=0,columnspan=2,padx=5,sticky='ew')
                    ToolTip(self.MultiAnalysis2Folder, msg="The generated anlysis folder from simulations.", delay=1.0)
                    self.MultiAnalysis2FolderEntryText = customtkinter.CTkLabel(self.MultiFileSelectFrame, text="Entry Name:", font=('arial',14),fg_color='transparent')
                    self.MultiAnalysis2FolderEntryText.grid(row=5,column=0, padx=5, pady=5,sticky='ew')
                    self.MultiAnalysis2FolderEntry = customtkinter.CTkEntry(self.MultiFileSelectFrame)
                    self.MultiAnalysis2FolderEntry.grid(row=5, column=1,padx=5,pady=5,sticky='ew')

                    self.MultiAnalysis2FolderNPTgro = customtkinter.CTkCheckBox(self.MultiFileSelectFrame, text="Start Structure", state='disabled')
                    self.MultiAnalysis2FolderNPTgro.grid(row=3,column=2,padx=5,pady=(10,0),sticky='e')
                    self.MultiAnalysis2FolderPRODgro = customtkinter.CTkCheckBox(self.MultiFileSelectFrame, text="End Structure", state='disabled')
                    self.MultiAnalysis2FolderPRODgro.grid(row=4,column=2,padx=10,sticky='e')
                    self.MultiAnalysis2FolderTraj = customtkinter.CTkCheckBox(self.MultiFileSelectFrame, text="Simulation Trajectory", state='disabled')
                    self.MultiAnalysis2FolderTraj.grid(row=5,column=2,padx=10, columnspan=2,sticky='e')



                    self.AnalysisHeader = customtkinter.CTkLabel(self, text="Analysis to Perform:", font=('arial',16),anchor="center",fg_color="transparent")
                    self.AnalysisHeader.grid(row=2,column=0,columnspan=3,pady=(20,0))

                    self.AnalysisChecksFrame = customtkinter.CTkScrollableFrame(self,width=400,height=250)
                    self.AnalysisChecksFrame.grid(row=3,column=0,columnspan=3,sticky="nsew",padx=15)
                    self.AnalysisChecksFrame.grid_columnconfigure((1,1,1),weight=1)
                    self.AnalysisChecksFrame.grid_rowconfigure((0,0,0),weight=1)

                    self.RMSD = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="RMSD",font=('arial',11))
                    self.RMSD.grid(row=0,column=0, pady=5)

                    self.RMSF = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="RMSF",font=('arial',11))
                    self.RMSF.grid(row=0,column=1, pady=5)

                    self.RoG = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="Radius of Gyration",font=('arial',11))
                    self.RoG.grid(row=0,column=2, pady=5)

                    self.PCA = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="PCA",font=('arial',11))
                    self.PCA.grid(row=1,column=0, pady=5)

                    self.SASA = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="SASA",font=('arial',11))
                    self.SASA.grid(row=1,column=1, pady=5)

                    
                    self.HBonds = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="H-Bonds",font=('arial',11),state="disabled")
                    self.HBonds.grid(row=1,column=2, pady=5)

                    
                    self.ComparativeAnalysisHeader = customtkinter.CTkLabel(self.AnalysisChecksFrame, text="Below is Only Available with Comparative Analysis:", font=('arial',16),anchor="center",fg_color="transparent")
                    self.ComparativeAnalysisHeader.grid(row=2,column=0,columnspan=3, pady=(20,0))

                    self.ComparativeAnalysisDesc = customtkinter.CTkLabel(self.AnalysisChecksFrame, text=("Comparative Analysis will compare the results of analysis data in folder 1 to\nthat of folder 2 on a single chart and is intended to be used for cases\nwhere only the environmental variables have been adjusted."), font=('arial',13), anchor="center",fg_color="transparent")
                    self.ComparativeAnalysisDesc.grid(row=3,column=0,columnspan=3)                    

                    self.ComparativeRMSD = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="Comparative RMSD")
                    self.ComparativeRMSD.grid(row=4,column=0, pady=5)

                    self.ComparativeRMSF = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="Comparative RMSF",font=('arial',11))
                    self.ComparativeRMSF.grid(row=4,column=1, pady=5)

                    self.ComparativeRoG = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="Comparative RoG",font=('arial',11))
                    self.ComparativeRoG.grid(row=4,column=2, pady=5)

                    self.ComparativeSASA = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="Comparative SASA",font=('arial',11))
                    self.ComparativeSASA.grid(row=5,column=0, pady=5)

                    self.ComparativeHBonds = customtkinter.CTkCheckBox(self.AnalysisChecksFrame,text="Comparative H-Bonds",font=('arial',11))
                    self.ComparativeHBonds.grid(row=5,column=0, pady=5)


                    self.AnalysisButton = customtkinter.CTkButton(self, text="Analyse Results", font=('arial',20), command=self.AnalyseResultsButton, state="disabled")
                    self.AnalysisButton.grid(row=5, column=0, columnspan=3, pady=20)



                def SelectAnalysisFolder(self):
                    global AnalysisFolderFilepath
                    global NPT_Structure
                    global PROD_Structure
                    global PROD_Traj
                    global AnalysisSelection 

                    MainApp.PrintOutputs("      Looking for Analysis Folder...")
                    AnalysisFolderFilepath = tkinter.filedialog.askdirectory()
                    MainApp.PrintOutputs(f"Found Folder!: {AnalysisFolderFilepath}")
                    FilesFound = 0
                    for i in os.listdir(AnalysisFolderFilepath):
                         if i.endswith("NPT.gro"):
                              NPT_Structure = AnalysisFolderFilepath + "/" + i
                              FilesFound +=1
                              MainApp.PrintOutputs("NPT structure found!")
                              self.AnalysisFolderNPTgro.select()
                         if i.endswith("PROD.gro"):
                              PROD_Structure = AnalysisFolderFilepath + "/" + i
                              FilesFound +=1
                              MainApp.PrintOutputs("PROD structure found!")
                              self.AnalysisFolderPRODgro.select()
                         if i.endswith("PROD.xtc"):
                              PROD_Traj = AnalysisFolderFilepath + "/" + i
                              FilesFound +=1
                              MainApp.PrintOutputs("Prod trajectory found!")
                              self.AnalysisFolderTraj.select()
                    MainApp.PrintOutputs(f"Found {FilesFound} files in analysis folder.")
                    self.AnalysisButton.configure(state='normal')
                    AnalysisSelection = "Single"


                def SelectMultiAnalysis1Folder(self):
                    global MultiAnalysis1FolderFilepath
                    global Multi1_NPT_Structure
                    global Multi1_PROD_Structure
                    global Multi1_PROD_Traj 

                    MainApp.PrintOutputs("      Looking for Analysis Folder 1...")
                    MultiAnalysis1FolderFilepath = tkinter.filedialog.askdirectory()
                    MainApp.PrintOutputs(f"Found Folder!: {MultiAnalysis1FolderFilepath}")
                    FilesFound = 0
                    for i in os.listdir(MultiAnalysis1FolderFilepath):
                         if i.endswith("NPT.gro"):
                              Multi1_NPT_Structure = MultiAnalysis1FolderFilepath + "/" + i
                              FilesFound +=1
                              MainApp.PrintOutputs("NPT structure found!")
                              self.MultiAnalysis1FolderNPTgro.select()
                         if i.endswith("PROD.gro"):
                              Multi1_PROD_Structure = MultiAnalysis1FolderFilepath + "/" + i
                              FilesFound +=1
                              MainApp.PrintOutputs("PROD structure found!")
                              self.MultiAnalysis1FolderPRODgro.select()
                         if i.endswith("PROD.xtc"):
                              Multi1_PROD_Traj = MultiAnalysis1FolderFilepath + "/" + i
                              FilesFound +=1
                              MainApp.PrintOutputs("Prod trajectory found!")
                              self.MultiAnalysis1FolderTraj.select()
                    MainApp.PrintOutputs(f"Found {FilesFound} files in analysis folder.")
                    self.MultiAnalysis2Folder.configure(state='normal')


                def SelectMultiAnalysis2Folder(self):
                    global MultiAnalysis2FolderFilepath
                    global Multi2_NPT_Structure
                    global Multi2_PROD_Structure
                    global Multi2_PROD_Traj
                    global AnalysisSelection 

                    MainApp.PrintOutputs("      Looking for Analysis Folder 2...")
                    MultiAnalysis2FolderFilepath = tkinter.filedialog.askdirectory()
                    MainApp.PrintOutputs(f"Found Folder!: {MultiAnalysis2FolderFilepath}")
                    FilesFound = 0
                    for i in os.listdir(MultiAnalysis2FolderFilepath):
                        if i.endswith("NPT.gro"):
                            Multi2_NPT_Structure = MultiAnalysis2FolderFilepath + "/" + i
                            FilesFound +=1
                            MainApp.PrintOutputs("NPT structure found!")
                            self.MultiAnalysis2FolderNPTgro.select()
                        if i.endswith("PROD.gro"):
                            Multi2_PROD_Structure = MultiAnalysis2FolderFilepath + "/" + i
                            FilesFound +=1
                            MainApp.PrintOutputs("PROD structure found!")
                            self.MultiAnalysis2FolderPRODgro.select()
                        if i.endswith("PROD.xtc"):
                            Multi2_PROD_Traj = MultiAnalysis2FolderFilepath + "/" + i
                            FilesFound +=1
                            MainApp.PrintOutputs("Prod trajectory found!")
                            self.MultiAnalysis2FolderTraj.select()
                    MainApp.PrintOutputs(f"Found {FilesFound} files in analysis folder.")
                    self.AnalysisButton.configure(state='normal')
                    AnalysisSelection = "Comparative"

                def AnalyseResultsButton(self):
                     global AnalysisSelection
                     global NPT_Structure
                     global PROD_Structure
                     global PROD_Traj
                     global Multi1_NPT_Structure
                     global Multi1_PROD_Structure
                     global Multi1_PROD_Traj 
                     global Multi2_NPT_Structure
                     global Multi2_PROD_Structure
                     global Multi2_PROD_Traj
                     Analysis_Methods = []
                     GraphCount = 0
                     WarningText = ""
                     AnalysisFiles = {}
                     MainApp.PrintOutputs("Verifying analysis methods...")
                     print(AnalysisSelection)
                     if AnalysisSelection == "Single":
                          Analysis_Methods.append("Single")
                          AnalysisFiles["NPT.gro"] = NPT_Structure
                          AnalysisFiles["PROD.gro"] = PROD_Structure
                          AnalysisFiles["PROD.xtc"] = PROD_Traj
                          AnalysisName = self.AnalysisFolderEntry.get()
                          if AnalysisName == "":
                               AnalysisName = "Simulation"
                          AnalysisFiles["Name"] = str(AnalysisName)
                     elif AnalysisSelection == "Comparative":
                          Analysis_Methods.append("Comparative")
                          AnalysisFiles["NPT1.gro"] = Multi1_NPT_Structure
                          AnalysisFiles["PROD1.gro"] = Multi1_PROD_Structure
                          AnalysisFiles["PROD1.xtc"] = Multi1_PROD_Traj
                          AnalysisName1 = self.MultiAnalysis1FolderEntry.get()
                          if AnalysisName1 == "":
                               AnalysisName1 = "Simulation 1"
                          AnalysisFiles["Name1"] = str(AnalysisName1)
                          AnalysisFiles["NPT2.gro"] = Multi2_NPT_Structure
                          AnalysisFiles["PROD2.gro"] = Multi2_PROD_Structure
                          AnalysisFiles["PROD2.xtc"] = Multi2_PROD_Traj
                          AnalysisName2 = self.MultiAnalysis2FolderEntry.get()
                          if AnalysisName2 == "":
                               AnalysisName2 = "Simulation 2"
                          AnalysisFiles["Name2"] = str(AnalysisName2)
                          

                     if self.RMSD.get() == 1:
                          Analysis_Methods.append("RMSD")
                          GraphCount +=1
                     if self.RMSF.get() ==1:
                          Analysis_Methods.append("RMSF")
                          GraphCount +=1
                     if self.RoG.get() ==1:
                          Analysis_Methods.append("RoG")
                          GraphCount +=1
                     if self.PCA.get() ==1:
                          Analysis_Methods.append("PCA")
                          GraphCount+2
                     if self.SASA.get() ==1:
                          Analysis_Methods.append("SASA")
                          GraphCount+1
                     if self.HBonds.get() ==1:
                          Analysis_Methods.append("H-Bonds")
                          GraphCount+1
                     if AnalysisSelection == "Comparative":
                          GraphCount = GraphCount*2
                          if self.ComparativeRMSD.get() == 1:
                              Analysis_Methods.append("Comparative RMSD")
                              GraphCount +=1
                          if self.ComparativeRMSF.get() ==1:
                              Analysis_Methods.append("Comparative RMSF")
                              GraphCount +=1
                          if self.ComparativeRoG.get() ==1:
                              Analysis_Methods.append("Comparative RoG")
                              GraphCount +=1
                          if self.ComparativeSASA.get() ==1:
                              Analysis_Methods.append("Comparative SASA")
                              GraphCount +=1
                          if self.ComparativeHBonds.get() ==1:
                              Analysis_Methods.append("Comparative H-Bonds")
                              GraphCount +=1
                          

                     print("Analysis methods selected: " + str(Analysis_Methods))
                     print("Analysis files selected: " + str(pprint.pformat(AnalysisFiles)))
                     if ("Comparative" in Analysis_Methods) and (("RMSD" or "RMSF" or "RoG" or "PCA") in Analysis_Methods):
                          WarningText += ("It appears you are attempting to include simple analysis methods during comparative analysis.\n" +
                                          "Be warned this will perform the selected analysis methods on both selected simulations.\n\n")
                     if ("PCA" or "Comparative PCA") in Analysis_Methods:
                          WarningText += ("Be warned Principle Component Analysis (PCA) is an extremely computationally expensive process!\n" +
                                          "Keeping PCA selected will SIGNIFICANTLY increase analysis time.\n\n")
                     WarningText += "Are you sure you wish to continue with the currently selected analysis methods?\n"
                     self.AnalysisButton.configure(text="Please Wait...")
                     self.AnalysisButton.configure(state='disabled')
                     if WarningText != "Are you sure you wish to continue with the currently selected analysis methods?\n":
                        if tkinter.messagebox.askyesno(title="Analysis Method Warnings!", message=WarningText, ) == True:
                            MainApp.PrintOutputs('Performing Analysis... \nThis will likely take some time.')
                            self.AnalysisButton.configure(state='disabled')
                            time1 = time.localtime()
                            self.analysisstart = time.time()
                            MainApp.PrintOutputs(f"Analysis started at {time.asctime(time1)}")
                            try:
                                self.AnalysisThread = threading.Thread(target=ExecuteAnalysis, daemon=True,  args=(Analysis_Methods, AnalysisFiles, GraphCount))
                                self.AnalysisThread.start()
                                #ExecuteAnalysis(Analysis_Methods, AnalysisFiles, GraphCount)
                            except:
                                 MainApp.PrintOutputs("Error when performing analysis.\nPlease Ensure all input files are present and match!")
                            self.AnalysisButton.configure(state='normal')
                        else:
                            MainApp.PrintOutputs("User chose to reselect analysis methods.")
                     else:
                        MainApp.PrintOutputs('Performing Analysis... \nThis will likely take some time. ')
                        self.AnalysisButton.configure(state='disabled')
                        time1 = time.localtime()
                        analysisstart = time.time()
                        MainApp.PrintOutputs(f"Analysis started at {time.asctime(time1)}")
                        self.AnalysisThread = threading.Thread(target=ExecuteAnalysis, daemon=True, args=(Analysis_Methods, AnalysisFiles, GraphCount))
                        self.AnalysisThread.start()
                        #ExecuteAnalysis(Analysis_Methods, AnalysisFiles, GraphCount)
                        '''
                        try:
                            ExecuteAnalysis(Analysis_Methods, AnalysisFiles, GraphCount)
                        except:
                             MainApp.PrintOutputs("Error when performing analysis.\nPlease Ensure all input files are present and match!")
                                                  
                     time2 = time.localtime()
                     analysisend = time.time()
                     analysistime = (time.gmtime(analysisend - analysisstart))
                     MainApp.PrintOutputs(f"Analysis finished at {time.asctime(time2)}")
                     MainApp.PrintOutputs("Analysis took {}".format(time.strftime("%H hours, %M minutes and %S seconds!", analysistime)))
                     MainApp.PrintOutputs("Analysis is Complete!")
                     self.AnalysisButton.configure(state='normal')
                     self.AnalysisButton.configure(text="Analyse Results")
                     '''
                     self.analysisstart =time.time()
                     self.AnalysisTimer()

                def AnalysisTimer(self):
                     CurrentTime = time.time()
                     RunTime = (time.gmtime(CurrentTime - self.analysisstart))
                     if self.AnalysisThread.is_alive() == True:
                        MainApp.TerminalOutput.configure(state='normal')
                        MainApp.TerminalOutput.delete(index1='end -1 lines linestar', index2="end")
                        MainApp.TerminalOutput.insert(index="end", text=("\nAnalysis Runtime: {}".format(time.strftime("%H hours, %M minutes and %S seconds!", RunTime))))
                        MainApp.TerminalOutput.see(index='end')
                        MainApp.TerminalOutput.configure(state='disabled')
                        self.after(1000, self.AnalysisTimer)
                     else:
                          MainApp.PrintOutputs(f"\nAnalysis finished at {time.asctime(time.localtime())}")
                          MainApp.PrintOutputs("Analysis took {}".format(time.strftime("%H hours, %M minutes and %S seconds!", RunTime)))
                          MainApp.PrintOutputs("Analysis is Complete!")
                          self.AnalysisButton.configure(state='normal')
                          self.AnalysisButton.configure(text="Analyse Results")
                    
                          
                     

                     
                    


                    






        

class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        ### Window Setup ###
        self.title("MDS Script Generator & Analysis Tool")
        self.geometry("1280x720")
        self.grid_columnconfigure((1, 1), weight=1)
        #self.columnconfigure(0, weight=3)
        #self.columnconfigure(1,weight=1)
        self.grid_rowconfigure((0, 1), weight=0)
        self.appearance = customtkinter.set_appearance_mode("system")
        self.colourtheme = customtkinter.set_default_color_theme("blue")

        # Information Tabs
        self.GuideFrame = customtkinter.CTkFrame(self, width=800)
        self.GuideFrame.grid(row=0,column=0,rowspan=2,sticky='nsew')
        self.GuideFrame.rowconfigure((0,0), weight=0)
        self.GuideHeader = customtkinter.CTkLabel(self.GuideFrame, text="MDSGAT Guide",fg_color="transparent",font=('arial',24),anchor='center',height=40)
        self.GuideHeader.grid(row=0,column=0,pady=(5,0),sticky='ew')
        self.InfoTabs = customtkinter.CTkTabview(self.GuideFrame,width=600, height=650)
        self.InfoTabs.grid(row=1,column=0,padx=20,pady=(0,5),sticky="nsew")
        self.InfoTabs.add("Setup Instructions")
        self.InfoTabs.add("Script Generator")
        self.InfoTabs.add("MDS Analysis")

        # Instructions
        self.InstructionsFrame = customtkinter.CTkScrollableFrame(self.InfoTabs.tab("Setup Instructions"), width=550, height=575)
        self.InstructionsFrame.grid(row=0,column=0,padx=0)
        self.InstructionsFrame.grid_rowconfigure(0, weight=0)
        self.InstructionsFrame.grid_columnconfigure(0,weight=0)
        self.SetupInstructionsText = customtkinter.CTkLabel(self.InstructionsFrame, text=Introduction_Instructions,fg_color="transparent",font=('arial',13),anchor='w', justify='left')
        self.SetupInstructionsText.grid(row=0,column=0,sticky='w')

        self.GeneratorFrame = customtkinter.CTkScrollableFrame(self.InfoTabs.tab("Script Generator"), width=550, height=575)
        self.GeneratorFrame.grid(row=0,column=0,padx=0)
        self.GeneratorFrame.grid_rowconfigure(0, weight=0)
        self.GeneratorFrame.grid_columnconfigure(0,weight=0)
        self.SetupGeneratorText = customtkinter.CTkLabel(self.GeneratorFrame, text=Generator_Instructions,fg_color="transparent",font=('arial',13),anchor='w', justify='left')
        self.SetupGeneratorText.grid(row=0,column=0,sticky='w')

        self.AnalysisFrame = customtkinter.CTkScrollableFrame(self.InfoTabs.tab("MDS Analysis"), width=550, height=575)
        self.AnalysisFrame.grid(row=0,column=0,padx=0)
        self.AnalysisFrame.grid_rowconfigure(0, weight=0)
        self.AnalysisFrame.grid_columnconfigure(0,weight=0)
        self.SetupAnalysisText = customtkinter.CTkLabel(self.AnalysisFrame, text=Analysis_Instructions,fg_color="transparent",font=('arial',13),anchor='w', justify='left')
        self.SetupAnalysisText.grid(row=0,column=0,sticky='w')








        # Terminal Output
        self.TerminalOutput = customtkinter.CTkTextbox(self, height=575, fg_color="black", text_color="white", wrap='word')
        self.TerminalOutput.insert('0.0', "Command Line Output Starts Here:\n")
        self.TerminalOutput.configure(state="disabled")
        self.TerminalOutput.grid(row=0,column=1,sticky="nsew", pady=(20,0),padx=0)

        ### UI Elements (Main Window) ###
        self.ButtonFrame = customtkinter.CTkFrame(self, height=120)
        self.ButtonFrame.grid(row=1,column=1,sticky="nsew")
        self.ButtonFrame.grid_columnconfigure((0,1,2), weight=1)
        self.ButtonFrame.grid_rowconfigure((0), weight=0)

        self.ScriptGenButton = customtkinter.CTkButton(self.ButtonFrame, text="Configure Script", height=100, command=self.OpenScriptGenerator)
        self.ScriptGenButton.grid(row=0, column=0, padx=10, pady=10, sticky="snew")
        ToolTip(self.ScriptGenButton, msg="Opens the MDS Script Generator Window.", delay=1.0)
        self.OpenScriptGenerator = None
        

        self.AnalysisButton = customtkinter.CTkButton(self.ButtonFrame,text="Analyse MDS", height=100,  command=self.OpenAnalysisWindow)
        self.AnalysisButton.grid(row=0,column=1, padx=10, pady=10, sticky="snew")
        ToolTip(self.AnalysisButton, msg="Opens the MDS Analysis Window", delay = 1.0)
        self.OpenAnalysisWindow = None

        self.SettingsButton = customtkinter.CTkButton(self.ButtonFrame,text="Settings", height=100, width=100, command=self.OpenConfiguration)
        self.SettingsButton.grid(row=0,column=3, padx=10, pady=10, sticky="snew")
        


        

    ##### UI Callbacks #####
        
    # Script Generator #
    def OpenScriptGenerator(self):
        if self.OpenScriptGenerator is None or not self.OpenScriptGenerator.winfo_exists():
            self.OpenScriptGenerator = ScriptWindow(self)
            self.PrintOutputs("Opening Script Generator")
        else:
             self.OpenScriptGenerator.focus()

    # Analysis #
    def OpenAnalysisWindow(self):
        if self.OpenAnalysisWindow is None or not self.OpenAnalysisWindow.winfo_exists():
            self.OpenAnalysisWindow = AnalysisWindow(self)
        else:
             self.OpenAnalysisWindow.focus()

    def PrintOutputs(self, Text):
        print(Text)
        self.TerminalOutput.configure(state='normal')
        self.TerminalOutput.insert(index="end", text=(Text + "\n"))
        self.TerminalOutput.see(index='end')
        self.TerminalOutput.configure(state='disabled')

    def OpenConfiguration(self):
         try:
            # Tries to open with default editor
            os.startfile("Config.py",'edit')
         except:
              try:
                  # Tried Windows Notepad
                  subprocess.Popen(['notepad.exe','Config.py'])
              except:
                   try:
                        # Tries Mac TextEdit
                        subprocess.Popen(['TextEdit.app','Config.py'])
                   except:
                        MainApp.PrintOutputs("No suitable text editor found. Please manually configure 'Config.py' within the install directory")
                        


### Main GUI Runtime ###
MainApp = MainWindow()
MainApp.mainloop()


