import json
from pprint import pprint



def CheckConfig():
    FolderName = "MDSGAT"
    ConfigName = "MDSGAT_Configuration"

    Filename = ConfigName + ".py"
    FolderName = FolderName + "/"
    Config_Default = """
# MDSGAT Configuration Settings#

### Gromacs Build Environemnts ###
# Please copy the below example when configuring new installations!
Artemis = {
    "Organisation":"The University of Sydney, Australia", # This is optional, but useful for tracking
    "Default Build":"gromacs/2021.4", # Default GROMACS build for single node, CPU only simulaitons
    "GPU Build":"gromacs/2021.4-gpu", # Defauly GROMACS build for single node, CPU & GPU simulations - Must have the GROMACS GPU CMAKE installation variable enabled (This should be done by your HPC administrator).
    "MPI Build":"gromacs/2021.4-mpi", # Default GROMACS build for multi-node, CPU only simulations - Must have MPI CMAKE installation variable enabled (This should be done by your HPC administrator).
    "MPI + GPU Build":"gromacs/2020.1-intel-mpi-gpu" # Default GROMACS build for multi-node, CPU & GPU simulations - Must have both the MPI & GPU CMAKE installation variables enabled (This should be done by your HPC administrator).
    }


### Saved Values ###
# Remember to Change these as well!
Selected_Config = {
    "Builds":Artemis,
    "Project":"PROJECT" # Please change "PROJECT" to "<YOUR PROJECT>" before generating a script 
    }
    """


    if sys.platform == "win32":
        ConfigFolder = os.path.join(os.path.expanduser("~"), "AppData", "Local", FolderName)
    else:
        ConfigFolder = os.path.join(os.path.expanduser("~"), "." + FolderName)
    
    if os.path.isdir(ConfigFolder)!=True:
        os.makedirs(ConfigFolder)

    Filepath = ConfigFolder + Filename
    if os.path.isfile(Filepath) != True:
        Config = open(Filepath, "a")
        Config.write(Config_Default)
        Config.close
        OpenConfig(Filepath)

    return Filepath

def OpenConfig(Filepath):
    try:
            # Tries to open with default editor
            os.startfile(Filepath,'edit')
    except:
        try:
            # Tried Windows Notepad
            subprocess.Popen(['notepad.exe',Filepath])
        except:
            try:
                # Tries Mac TextEdit
                subprocess.Popen(['TextEdit.app',Filepath])
            except:
                MainApp.PrintOutputs("No suitable text editor found. Please manually configure 'MDSGAT/MDS_Configuration.py' within the users appdata directory.")

    return


with open("config.json", mode="r+", encoding ="utf-8") as read_file:
    Config_Options = json.load(read_file)

#The following feels fucking redundant
#copy JSON file:

#print(((Config_Options["Organisations"][0])["Systems"][0])["Projects"][0])

EX_Projects = ["Dummy Project 1", "Dummy Project 2"]
EX_Build = "Gromacs Dummy Default"
EX_GPU = "Gromacs Dummy GPU"
EX_MPI = "Gromacs Dummy MPI"
EX_GPUandMPI = "Gromacs Dummy MPI + GPU"
EX_SystemName = "Dummy System"
EX_OrganisationName = "Dummy Org"

# Create Entry:
Config_Dupe = Config_Options
#print(type(Config_Dupe["Organisations"][0]))
#print(Config_Dupe["Organisations"][0])
#Config_Dupe["Organisations"].append(EX_OrganisationName)

#build subsystem:
System = {
    "System Name":EX_SystemName,
    "Default Build":EX_Build,
    "GPU Build":EX_GPU,
    "MPI Build":EX_MPI,
    "MPI + GPU Build":EX_GPUandMPI,
    "Projects":EX_Projects
}
print("System is:")
pprint(System)
print()

#build organisation
Systems = []
Systems.append(System)

Organisation = {
    "Organisation Name":EX_OrganisationName,
    "Systems":Systems
}

print("Organisation is:")
pprint(Organisation)
print()

Organisations = []
Organisations.append(Organisation)


print("Before Addition:")
pprint(Config_Dupe)
print()

print("After Addition")
Config_Dupe["Organisations"].append(Organisation)
pprint(Config_Dupe)

with open("test_config.json", "w") as json_file:
    json.dump(Config_Dupe,json_file,indent=4)
    print("Save Complete")

print(((Config_Options["Organisations"][0])["Systems"][0])["Projects"][0])











"""
#pulling data out:

Selected_Config = Config_Options["Selected Configuration"]

Stored_Configs = Config_Options["Organisations"]

Org_Options = []

for i in range(len(Stored_Configs)):
    Org_Options.append((Stored_Configs[i])["Organisation Name"])

#Org Selected --> Display subsystems
print("Available Organisations are:")
for i in range(len(Org_Options)):
    print(Org_Options[i])
print()
System_Options = []
x_select = 1
for i in range(len(Stored_Configs)):
    if Org_Options[x_select] == ((Stored_Configs[i])["Organisation Name"]):
        Selected_Org = (Stored_Configs[i])["System"]

#Select and Display systems
for i in range(len(Selected_Org)):
    System_Options.append(Selected_Org[i]["System Name"])

print("Available Systems are: ")
for i in range(len(System_Options)):
    print(System_Options[i])
print()

y_select = 0
for i in range(len(Selected_Org)):
    if System_Options[y_select] == ((Selected_Org[i])["System Name"]):
        Selected_System = Selected_Org[i]

#select and display projects

Project_Options = []
for i in range(len(Selected_System["Projects"])):
    Project_Options.append((Selected_System["Projects"])[i])

print("Available Projects are:")
for i in range(len(Project_Options)):
    print(Project_Options[i])
print()

z_select = 0

for i in range(len(Selected_System["Projects"])):
    if Project_Options[z_select] == (Selected_System["Projects"])[i]:
        Selected_Project = (Selected_System["Projects"])[i]





print("Please Confirm the Following:")
print("Organisation Name: " + Org_Options[x_select])
print("Subsystem Name: " + Selected_System["System Name"])
print("Default GROMACS Build: " + Selected_System["Default Build"])
print("GROMACS GPU Build: " + Selected_System["GPU Build"])
print("GROMACS MPI Buiild: " + Selected_System["MPI Build"])
print("GROMACS GPU + MPI Build: " + Selected_System["MPI + GPU Build"])
print("Selected Project: " + Selected_Project)

    
        




#print((((Stored_Configs[0])["System"])[0])["System Name"])






"""