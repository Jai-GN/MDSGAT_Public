import pprint
import tkinter
from tkinter import messagebox
import os

def CheckScriptInputs(ScriptInputs, MDSInputs, HardwareInputs, AdvancedInputs, IONInputs, MINInputs, NVTInputs, NPTInputs, PRODInputs):
    print("     LISTING RAW INPUTS     ")
    print("\nScript Options Inputs:")
    print(pprint.pformat(ScriptInputs))
    print("\nMDS Option Inputs:")
    print(pprint.pformat(MDSInputs))
    print("\nHardware Option Inputs:")
    print(pprint.pformat(HardwareInputs))
    print("\nAdvanced Options:")
    print(pprint.pformat(AdvancedInputs))
    print("\nION MDP Inputs:")
    print(pprint.pformat(IONInputs))
    print("\nMinimisation MDP Inputs:")
    print(pprint.pformat(MINInputs))
    print("\nNVT MDP Inputs:")
    print(pprint.pformat(NVTInputs))
    print("\nNPT MDP Inputs:")
    print(pprint.pformat(NPTInputs))
    print("\nProduction MDP Inputs:")
    print(pprint.pformat(PRODInputs))
    print("")

    print("\nChecking  for Errors in Raw Inputs...")

    ErrorFound = 0

    
    CheckedScriptInputs = {}
    CheckedMDSInputs = {}
    CheckedHardwareInputs = {}
    CheckedAdvancedInputs = {}
    CheckedIONInputs = {}
    CheckedMINInputs  = {}
    CheckedNVTInputs = {}
    CheckedNPTInputs = {}
    CheckedPRODInputs =  {}

    OutputDict = {
        "Error Check":"Incomplete"
    }
    print("Input Updates:")
    ### Script Inputs ###
    Warning_String = "Script Settings Errors:\n"
    if ScriptInputs["Script Name"] == '':
        Warning_String += "Script Name is Empty!\n"
        ErrorFound+=1
    elif ' ' in ScriptInputs['Script Name'] == True:
        Warning_String += "Script Name cannot contain spaces! Try \"_\" instead.\n"
        ErrorFound+=1
    elif os.path.isdir(f"Script_Files/MDS_{ScriptInputs["Script Name"]}")==True:
        Warning_String += "Script Name already exists. Cannot have duplicate Script Names!"
        ErrorFound+=1
    else:
        CheckedScriptInputs["Script Name"] = ScriptInputs['Script Name']

    CheckedScriptInputs["Path Option"] = ScriptInputs["Path Option"] 
    CheckedScriptInputs["Path Text"] = ScriptInputs["Path Text"]

    CheckedScriptInputs["Protein Filepath"] = ScriptInputs["Protein Filepath"]

    CheckedScriptInputs["ML Generated"] = ScriptInputs["ML Generated"]

    try:
        if os.path.splitext(ScriptInputs["Protein Filename"])[1] != '.pdb':
            Warning_String += "Protein file must be a .pdb file!\n"
            ErrorFound+=1
        else:
            CheckedScriptInputs["Protein Filename"] = ScriptInputs["Protein Filename"]
    except:
        Warning_String += "Protein file must be a valid .pdb file!\n"
        ErrorFound+=1
    
    if ScriptInputs["Protein Size"] == 0:
        Warning_String += "The selected .pdb file is invalid as it contains no atoms. Please ensure you have selected the correct file.\n"
        ErrorFound+=1
    else:
        CheckedScriptInputs["Protein Size"] = ScriptInputs["Protein Size"]

    CheckedScriptInputs["Sim Type"] = ScriptInputs["Sim Type"]
    CheckedScriptInputs["Protein Count"] = int(ScriptInputs["Protein Count"])

    CheckedScriptInputs["Email Address"] = ScriptInputs["Email Address"]

    ### MDS Inputs ###
    Warning_String += "\nMDS Options Errors:\n"
    try:
        float(MDSInputs["Sim Temperature"])
    except:
        Warning_String += "Simulation Temperature must be a valid number!\n"
        ErrorFound+=1
    else:
        CheckedMDSInputs["Sim Temperature"] = MDSInputs["Sim Temperature"]

    try:
        float(MDSInputs["Sim Pressure"])
    except:
        Warning_String += "Simulation Pressure must be a valid number!\n"
        ErrorFound+=1
    else:
        CheckedMDSInputs["Sim Pressure"] = MDSInputs["Sim Pressure"]
    
    CheckedMDSInputs["Solvent Selected"] = MDSInputs["Solvent Selected"]

    CheckedMDSInputs["Force Field"] = MDSInputs["Force Field"]

    try:
        int(MDSInputs["Minimisation Time"])
    except:
        Warning_String += "Minimisation Time must be a valid whole number!\n"
        ErrorFound+=1
    else:
        CheckedMDSInputs["MIN Time"] = int(MDSInputs["Minimisation Time"])
    
    try:
        int(MDSInputs["NVT Time"])
    except:
        Warning_String += "NVT Time must be a valid whole number!\n"
        ErrorFound+=1
    else:
        CheckedMDSInputs["NVT Time"] = int(MDSInputs["NVT Time"])

    try:
        int(MDSInputs["NPT Time"])
    except:
        Warning_String += "NPT Time must be a valid whole number!\n"
        ErrorFound+=1
    else:
        CheckedMDSInputs["NPT Time"] = int(MDSInputs["NPT Time"])

    try:
        int(MDSInputs["Production Time"])
    except:
        Warning_String += "Production Time must be a valid whole number!\n"
        ErrorFound+=1
    else:
        CheckedMDSInputs["PROD Time"] = int(MDSInputs["Production Time"])

    ### Hardware Inputs ###
    Warning_String += "\nHardware Options Errors:\n"
    CheckedHardwareInputs["Node Mode"] = HardwareInputs["Node Mode"]
    CheckedHardwareInputs["Node Count"] = int(HardwareInputs["Node Count"])

    CheckedHardwareInputs["CPU Count"] = int(HardwareInputs["CPU Count"])

    CheckedHardwareInputs["GPU Count"] = int(HardwareInputs["GPU Count"])

    CheckedHardwareInputs["Memory Allocation"] = int(HardwareInputs["Memory Allocation"])

    try:
        int(HardwareInputs["Walltime Hours"])
        int(HardwareInputs["Walltime Minutes"])
        int(HardwareInputs["Walltime Seconds"])

    except:
        Warning_String += "Walltime inputs must be valid whole numbers!\n"
        ErrorFound+=1
    else:
        CheckedHardwareInputs["Walltime Hours"] = int(HardwareInputs["Walltime Hours"])
        CheckedHardwareInputs["Walltime Minutes"] = int(HardwareInputs["Walltime Minutes"])
        CheckedHardwareInputs["Walltime Seconds"] = int(HardwareInputs["Walltime Seconds"])

    ### Advanced Inputs ###
    Warning_String += "\nAdvanced Options Errors:\n"
    CheckedAdvancedInputs["Gromacs Build"] = AdvancedInputs["Gromacs Build"]

    CheckedAdvancedInputs["Remove Water"] = AdvancedInputs["Remove Water"]

    CheckedAdvancedInputs["Water Model"] = AdvancedInputs["Water Model"]

    if AdvancedInputs["System Charge"] == "Neutral":
        CheckedAdvancedInputs["System Charge"] = "neutral"
        print("System Charge was changed from Neutral to neutral.")
    else:
        CheckedAdvancedInputs["System Charge"] = AdvancedInputs["System Charge"]
    if AdvancedInputs["Positive Charge"] == "[+1] Na":
        CheckedAdvancedInputs["Positive Charge"] = "NA"
        print("Positive Charge was changed from [+1] Na to NA.")
    else:
        CheckedAdvancedInputs["Positive Charge"] = AdvancedInputs["Positive Charge"]
    if AdvancedInputs["Negative Charge"] == "[-1] Cl":
        CheckedAdvancedInputs["Negative Charge"] = "CL"
        print("Negative Charge was changed from [-1] Cl to CL.")
    else:
        CheckedAdvancedInputs["Negative Charge"] = AdvancedInputs["Negative Charge"]

    CheckedAdvancedInputs["Boundry Options"] = AdvancedInputs["Boundry Option"]
    CheckedAdvancedInputs["Boundry Gap"] = AdvancedInputs["Boundry Gap"]

    ### ION Inputs ###
    Warning_String += "\n   ION Errors:\n"
    CheckedIONInputs["ION Integrator"] = IONInputs["ION Integrator"]

    CheckedIONInputs["ION Minimum Limit"] = int(IONInputs["ION Minimum Limit"])

    if IONInputs["ION Time"] ==  '':
        CheckedIONInputs["ION Time"] = 5
        print("ION Time was changed from None to 5.")
    else:
        try:
            int(IONInputs["ION Time"])
        except:
            Warning_String += "ION Time must be a valid whole number!\n"
            ErrorFound+=1
        else:
            CheckedIONInputs["ION Time"] = IONInputs["ION Time"]

    CheckedIONInputs["ION Granularity"] = IONInputs["ION Granularity"]

    CheckedIONInputs["ION Update Frequency"] = int(IONInputs["ION Update Frequency"])

    CheckedIONInputs["ION Neighbour Scheme"] = IONInputs["ION Neighbour Scheme"]
    CheckedIONInputs["ION Neighbour Method"] = IONInputs["ION Neighbour Method"]

    CheckedIONInputs["ION Coloumb Type"] = IONInputs["ION Coloumb Type"]
    CheckedIONInputs["ION Coloumb Cutoff"] = round(IONInputs["ION Coloumb Cutoff"],2)

    CheckedIONInputs["ION Van der Waal Cutoff"] = round(IONInputs["ION Van der Waal Cutoff"],2)

    CheckedIONInputs["ION Boundry Type"] = IONInputs["ION Boundry Type"]

    ### MIN Inputs ###
    Warning_String += "\n   Minimisation Errors:\n"
    CheckedMINInputs["MIN Integrator"] = MINInputs["MIN Integrator"]

    CheckedMINInputs["MIN Minimum Limit"] = int(MINInputs["MIN Minimum Limit"])

    CheckedMINInputs["MIN Granularity"] = MINInputs["MIN Granularity"]

    CheckedMINInputs["MIN Update Frequency"] = int(MINInputs["MIN Update Frequency"])

    CheckedMINInputs["MIN Neighbour Scheme"] = MINInputs["MIN Neighbour Scheme"]
    CheckedMINInputs["MIN Neighbour Method"] = MINInputs["MIN Neighbour Method"]

    CheckedMINInputs["MIN Coloumb Type"] = MINInputs["MIN Coloumb Type"]
    CheckedMINInputs["MIN Coloumb Cutoff"] = MINInputs["MIN Coloumb Cutoff"]

    CheckedMINInputs["MIN Van der Waal Cutoff"] = MINInputs["MIN Van der Waal Cutoff"]

    CheckedMINInputs["MIN Boundry Type"] = MINInputs["MIN Boundry Type"]

    ### NVT Inputs ###
    Warning_String += "\n   NVT Errors:\n"

    CheckedNVTInputs["NVT Restrain"] = NVTInputs["NVT Restrain"]

    CheckedNVTInputs["NVT Integrator"] = NVTInputs["NVT Integrator"]

    CheckedNVTInputs["NVT Granularity"] = NVTInputs["NVT Granularity"]

    CheckedNVTInputs["NVT Update Frequency"] = int(NVTInputs["NVT Update Frequency"])

    CheckedNVTInputs["NVT Continued"] = NVTInputs["NVT Continued"]

    CheckedNVTInputs["NVT Constraint Algorithm"] = NVTInputs["NVT Constraint Algorithm"]
    CheckedNVTInputs["NVT Constraints"] = NVTInputs["NVT Constraints"]

    CheckedNVTInputs["NVT LINCS Iterations"] = int(NVTInputs["NVT LINCS Iterations"])
    CheckedNVTInputs["NVT LINCS Order"] = int(NVTInputs["NVT LINCS Order"])

    CheckedNVTInputs["NVT Neighbour Scheme"] = NVTInputs["NVT Neighbour Scheme"]
    CheckedNVTInputs["NVT Neighbour Method"] = NVTInputs["NVT Neighbour Method"]

    CheckedNVTInputs["NVT Coloumb Type"] = NVTInputs["NVT Coloumb Type"]
    CheckedNVTInputs["NVT Coloumb Cutoff"] = NVTInputs["NVT Coloumb Cutoff"]

    CheckedNVTInputs["NVT Van der Waal Cutoff"] = NVTInputs["NVT Van der Waal Cutoff"]
    CheckedNVTInputs["NVT VdW Correction"] = NVTInputs["NVT VdW Correction"]

    CheckedNVTInputs["NVT PME Order"] = int(NVTInputs["NVT PME Order"])

    CheckedNVTInputs["NVT Fourier Spacing"] = NVTInputs["NVT Fourier Spacing"]

    CheckedNVTInputs["NVT Temperature Coupling"] = NVTInputs["NVT Temperature Coupling"]
    CheckedNVTInputs["NVT Coupling Groups"] = NVTInputs["NVT Coupling Groups"]
    CheckedNVTInputs["NVT Temp Time Constant"] = NVTInputs["NVT Temp Time Constant"]

    CheckedNVTInputs["NVT Boundry Type"] = NVTInputs["NVT Boundry Type"]

    CheckedNVTInputs["NVT Gen Velocity"] = NVTInputs["NVT Gen Velocity"]

    if NVTInputs["NVT Seed"] == '':
        CheckedNVTInputs["NVT Seed"] = -1
        print("NVT Seed was changed from None to -1.")
    else:
        CheckedNVTInputs["NVT Seed"] = NVTInputs["NVT Seed"]

    ### NPT Inputs ###
    Warning_String += "\n   NPT Errors:\n"
    CheckedNPTInputs["NPT Restrain"] = NPTInputs["NPT Restrain"]

    CheckedNPTInputs["NPT Integrator"] = NPTInputs["NPT Integrator"]

    CheckedNPTInputs["NPT Granularity"] = NPTInputs["NPT Granularity"]

    CheckedNPTInputs["NPT Update Frequency"] = int(NPTInputs["NPT Update Frequency"])

    CheckedNPTInputs["NPT Continued"] = NPTInputs["NPT Continued"]

    CheckedNPTInputs["NPT Constraint Algorithm"] = NPTInputs["NPT Constraint Algorithm"]
    CheckedNPTInputs["NPT Constraints"] = NPTInputs["NPT Constraints"]

    CheckedNPTInputs["NPT LINCS Iterations"] = int(NPTInputs["NPT LINCS Iterations"])
    CheckedNPTInputs["NPT LINCS Order"] = int(NPTInputs["NPT LINCS Order"])

    CheckedNPTInputs["NPT Neighbour Scheme"] = NPTInputs["NPT Neighbour Scheme"]
    CheckedNPTInputs["NPT Neighbour Method"] = NPTInputs["NPT Neighbour Method"]

    CheckedNPTInputs["NPT Coloumb Type"] = NPTInputs["NPT Coloumb Type"]
    CheckedNPTInputs["NPT Coloumb Cutoff"] = NPTInputs["NPT Coloumb Cutoff"]

    CheckedNPTInputs["NPT Van der Waal Cutoff"] = NPTInputs["NPT Van der Waal Cutoff"]
    CheckedNPTInputs["NPT VdW Correction"] = NPTInputs["NPT VdW Correction"]

    CheckedNPTInputs["NPT PME Order"] = int(NPTInputs["NPT PME Order"])

    CheckedNPTInputs["NPT Fourier Spacing"] = NPTInputs["NPT Fourier Spacing"]

    CheckedNPTInputs["NPT Temperature Coupling"] = NPTInputs["NPT Temperature Coupling"]
    CheckedNPTInputs["NPT Coupling Groups"] = NPTInputs["NPT Coupling Groups"]
    CheckedNPTInputs["NPT Temp Time Constant"] = NPTInputs["NPT Temp Time Constant"]

    CheckedNPTInputs["NPT Pressure Coupling"] = NPTInputs["NPT Pressure Coupling"]
    CheckedNPTInputs["NPT Pressure Coupling Type"] = NPTInputs["NPT Pressure Coupling Type"]

    if NPTInputs["NPT Water Compressibility"] == '':
        CheckedNPTInputs["NPT Water Compressibility"] = '4.5e-5'
    else:
        CheckedNPTInputs["NPT Water Compressibility"] = NPTInputs["NPT Water Compressibility"]

    CheckedNPTInputs["NPT Coordinate Scaling"] = NPTInputs["NPT Coordinate Scaling"]

    CheckedNPTInputs["NPT Boundry Type"] = NPTInputs["NPT Boundry Type"]

    CheckedNPTInputs["NPT Gen Velocity"] = NPTInputs["NPT Gen Velocity"]

    if NPTInputs["NPT Seed"] == '':
        CheckedNPTInputs["NPT Seed"] = -1
        print("NPT Seed was changed from None to -1.")
    else:
        CheckedNPTInputs["NPT Seed"] = NPTInputs["NPT Seed"]
    

    ### PROD Inputs ###
    Warning_String += "\n   Production Errors:\n"
    CheckedPRODInputs["PROD Restrain"] = PRODInputs["PROD Restrain"]

    CheckedPRODInputs["PROD Integrator"] = PRODInputs["PROD Integrator"]

    CheckedPRODInputs["PROD Granularity"] = PRODInputs["PROD Granularity"]

    CheckedPRODInputs["PROD Update Frequency"] = int(PRODInputs["PROD Update Frequency"])

    CheckedPRODInputs["PROD Compress"] = PRODInputs["PROD Compress"]

    CheckedPRODInputs["PROD Continued"] = PRODInputs["PROD Continued"]

    CheckedPRODInputs["PROD Constraint Algorithm"] = PRODInputs["PROD Constraint Algorithm"]
    CheckedPRODInputs["PROD Constraints"] = PRODInputs["PROD Constraints"]

    CheckedPRODInputs["PROD LINCS Iterations"] = int(PRODInputs["PROD LINCS Iterations"])
    CheckedPRODInputs["PROD LINCS Order"] = int(PRODInputs["PROD LINCS Order"])

    CheckedPRODInputs["PROD Neighbour Scheme"] = PRODInputs["PROD Neighbour Scheme"]
    CheckedPRODInputs["PROD Neighbour Method"] = PRODInputs["PROD Neighbour Method"]

    CheckedPRODInputs["PROD Coloumb Type"] = PRODInputs["PROD Coloumb Type"]
    CheckedPRODInputs["PROD Coloumb Cutoff"] = PRODInputs["PROD Coloumb Cutoff"]

    CheckedPRODInputs["PROD Van der Waal Cutoff"] = PRODInputs["PROD Van der Waal Cutoff"]
    CheckedPRODInputs["PROD VdW Correction"] = PRODInputs["PROD VdW Correction"]

    CheckedPRODInputs["PROD PME Order"] = int(PRODInputs["PROD PME Order"])

    CheckedPRODInputs["PROD Fourier Spacing"] = PRODInputs["PROD Fourier Spacing"]

    CheckedPRODInputs["PROD Temperature Coupling"] = PRODInputs["PROD Temperature Coupling"]
    CheckedPRODInputs["PROD Coupling Groups"] = PRODInputs["PROD Coupling Groups"]
    CheckedPRODInputs["PROD Temp Time Constant"] = PRODInputs["PROD Temp Time Constant"]

    CheckedPRODInputs["PROD Pressure Coupling"] = PRODInputs["PROD Pressure Coupling"]
    CheckedPRODInputs["PROD Pressure Coupling Type"] = PRODInputs["PROD Pressure Coupling Type"]

    if PRODInputs["PROD Water Compressibility"] == '':
        CheckedPRODInputs["PROD Water Compressibility"] = '4.5e-5'
    else:
        CheckedPRODInputs["PROD Water Compressibility"] = PRODInputs["PROD Water Compressibility"]

    CheckedPRODInputs["PROD Boundry Type"] = PRODInputs["PROD Boundry Type"]

    CheckedPRODInputs["PROD Gen Velocity"] = PRODInputs["PROD Gen Velocity"]

    if PRODInputs["PROD Seed"] == '':
        CheckedPRODInputs["PROD Seed"] = -1
        print("PROD Seed was changed from None to -1.")
    else:
        CheckedPRODInputs["PROD Seed"] = PRODInputs["PROD Seed"]
    


    ### Error Warning ###
    if ErrorFound > 0:
        print(f"Found {ErrorFound} Errors!")
        tkinter.messagebox.showerror(title=f"{ErrorFound} Errors Found!", message=(Warning_String + "\n\nPlease fix the above errors and try again!"))
        OutputDict["Error Check"] = "Failed"
    else:
        print("     LISTING CHECKED INPUTS     ")
        print("\nScript Options Inputs:")
        print(pprint.pformat(CheckedScriptInputs))
        print("\nMDS Option Inputs:")
        print(pprint.pformat(CheckedMDSInputs))
        print("\nHardware Option Inputs:")
        print(pprint.pformat(CheckedHardwareInputs))
        print("\nAdvanced Options:")
        print(pprint.pformat(CheckedAdvancedInputs))
        print("\nION MDP Inputs:")
        print(pprint.pformat(CheckedIONInputs))
        print("\nMinimisation MDP Inputs:")
        print(pprint.pformat(CheckedMINInputs))
        print("\nNVT MDP Inputs:")
        print(pprint.pformat(CheckedNVTInputs))
        print("\nNPT MDP Inputs:")
        print(pprint.pformat(CheckedNPTInputs))
        print("\nProduction MDP Inputs:")
        print(pprint.pformat(CheckedPRODInputs))
        print("")
        OutputDict["Error Check"] = "Passed"
        OutputDict["Script Settings"] = CheckedScriptInputs
        OutputDict["MDS Options"] = CheckedMDSInputs
        OutputDict["Hardware Options"] = CheckedHardwareInputs
        OutputDict["Advanced Options"] = CheckedAdvancedInputs
        OutputDict["ION MDP"] = CheckedIONInputs
        OutputDict["MIN MDP"] = CheckedMINInputs
        OutputDict["NVT MDP"] = CheckedNVTInputs
        OutputDict["NPT MDP"] = CheckedNPTInputs
        OutputDict["PROD MDP"] = CheckedPRODInputs 
        print("No Errors Found!\nProceeding with Script Generation...")

    return OutputDict 
