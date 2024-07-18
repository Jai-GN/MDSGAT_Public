import os
import shutil
import Config

class MDSScriptGen:
    def __init__(self, Script_Settings, MDS_Options, Hardware_Options, Advanced_Options, ION_MDP, MIN_MDP, NVT_MDP, NPT_MDP,  PROD_MDP):
                 self.Script_Settings = Script_Settings
                 self.MDS_Options = MDS_Options
                 self.Hardware_Options = Hardware_Options
                 self.Advanced_Options = Advanced_Options
                 self.ION_MDP = ION_MDP
                 self.MIN_MDP = MIN_MDP
                 self.NVT_MDP = NVT_MDP
                 self.NPT_MDP = NPT_MDP
                 self.PROD_MDP = PROD_MDP

                 
    def Generate_MDS_Setup_Script(self):
        if os.path.isdir("Script_Files")!=True:
            os.makedirs('Script_Files/')
        try:
            os.makedirs('Script_Files/MDS_{}/'.format(self.Script_Settings["Script Name"]))
        except:
              print("Folder already Exists!")
        shutil.copy2(self.Script_Settings["Protein Filepath"], 'Script_Files/MDS_{}/'.format(self.Script_Settings["Script Name"]))
        SetupScript = open("Script_Files/MDS_{}/{}_Setup_Script.py".format(self.Script_Settings["Script Name"], self.Script_Settings["Script Name"]), "a")
        ScriptContents = ''

        Config_Data = Config.Selected_Config
        MDS_Builds = Config_Data["Builds"]

        ScriptImports = ("# Imports #\n" +
                         "import os \n\n")
        

        Variables = ("### Assign User Generated Variables ###\n" +
                     "# Script Settings #\n" +
                     f"ScriptName = '{self.Script_Settings["Script Name"]}'\n" + 
                     f"Path_Options = '{self.Script_Settings["Path Option"]}'\n" + 
                     f"Path_Directory = '{self.Script_Settings["Path Text"]}'\n" + 
                     f"ProteinFilename = '{self.Script_Settings["Protein Filename"]}'\n" + 
                     f"ProteinSize = '{self.Script_Settings["Protein Size"]}'\n" + 
                     f"GeneratedStructure = '{self.Script_Settings["ML Generated"]}'\n" + 
                     f"Simulation_Type = '{self.Script_Settings["Sim Type"]}'\n" + 
                     f"Protein_Count = {self.Script_Settings["Protein Count"]}\n" + 
                     f"Email = '{self.Script_Settings["Email Address"]}'\n\n" + 

                     "# Hardware Options #\n" +
                     f"Node_Mode = '{self.Hardware_Options["Node Mode"]}'\n" + 
                     f"Node_Count = {self.Hardware_Options["Node Count"]}\n" + 
                     f"CPU_Count = {self.Hardware_Options["CPU Count"]}\n" + 
                     f"GPU_Count = {self.Hardware_Options["GPU Count"]}\n" + 
                     f"Memory_Allocation = {self.Hardware_Options["Memory Allocation"]}\n" + 
                     f"Walltime_Hours = {self.Hardware_Options["Walltime Hours"]}\n" + 
                     f"Walltime_Minutes = {self.Hardware_Options["Walltime Minutes"]}\n" + 
                     f"Walltime_Seconds = {self.Hardware_Options["Walltime Seconds"]}\n\n" + 

                     "# Advanced Options #\n" +
                     f"Remove_Water = '{self.Advanced_Options["Remove Water"]}'\n" +
                     f"Water_Model = '{self.Advanced_Options["Water Model"]}'\n" +
                     f"System_Charge = '{self.Advanced_Options["System Charge"]}'\n" +
                     f"Positive_Atom = '{self.Advanced_Options["Positive Charge"]}'\n" +
                     f"Negative_Atom = '{self.Advanced_Options["Negative Charge"]}'\n" +
                     f"Boundry_Shape = '{self.Advanced_Options["Boundry Options"]}'\n" +
                     f"Boundry_Gap = {self.Advanced_Options["Boundry Gap"]}\n\n" +

                     "# MDS & MDP Options #\n" +
                     f"Temperature = {self.MDS_Options["Sim Temperature"]}\n" + 
                     f"Pressure = {self.MDS_Options["Sim Pressure"]}\n" + 
                     f"Solvent = '{self.MDS_Options["Solvent Selected"]}'\n" + 
                     f"ForceField = '{self.MDS_Options["Force Field"]}'\n" + 
                     f"ION_Integrator = '{self.ION_MDP["ION Integrator"]}'\n" +
                     f"ION_MinLimit = {self.ION_MDP["ION Minimum Limit"]}\n" +
                     f"ION_Time = ({self.ION_MDP["ION Time"]} * 1000) # ps --> fs\n" +
                     f"ION_Granularity = {self.ION_MDP["ION Granularity"]}\n" +
                     f"ION_UpdateFreq = {self.ION_MDP["ION Update Frequency"]} * 1000 # ps --> fs\n" +
                     f"ION_NeighbourScheme = '{self.ION_MDP["ION Neighbour Scheme"]}'\n" +
                     f"ION_NeighbourMethod = '{self.ION_MDP["ION Neighbour Method"]}'\n" +
                     f"ION_ColoumbType = '{self.ION_MDP["ION Coloumb Type"]}'\n" +
                     f"ION_ColoumbCutoff = {self.ION_MDP["ION Coloumb Cutoff"]}\n" +
                     f"ION_VdWCutoff = {self.ION_MDP["ION Van der Waal Cutoff"]}\n" +
                     f"ION_BoundryType = '{self.ION_MDP["ION Boundry Type"]}'\n" +
                     f"MIN_Integrator = '{self.MIN_MDP["MIN Integrator"]}'\n" +
                     f"MIN_MinLimit = {self.MIN_MDP["MIN Minimum Limit"]}\n" +
                     f"MIN_Time = ({self.MDS_Options["MIN Time"]} * 1000) # ps --> fs\n" +
                     f"MIN_Granularity = {self.MIN_MDP["MIN Granularity"]}\n" +
                     f"MIN_UpdateFreq = {self.MIN_MDP["MIN Update Frequency"]} * 1000 # ps --> fs\n" +
                     f"MIN_NeighbourScheme = '{self.MIN_MDP["MIN Neighbour Scheme"]}'\n" +
                     f"MIN_NeighbourMethod = '{self.MIN_MDP["MIN Neighbour Method"]}'\n" +
                     f"MIN_ColoumbType = '{self.MIN_MDP["MIN Coloumb Type"]}'\n" +
                     f"MIN_ColoumbCutoff = {self.MIN_MDP["MIN Coloumb Cutoff"]}\n" +
                     f"MIN_VdWCutoff = {self.MIN_MDP["MIN Van der Waal Cutoff"]}\n" +
                     f"MIN_BoundryType = '{self.MIN_MDP["MIN Boundry Type"]}'\n" +
                     f"NVT_Restrain = '{self.NVT_MDP["NVT Restrain"]}'\n" +
                     f"NVT_Integrator = '{self.NVT_MDP["NVT Integrator"]}'\n" +
                     f"NVT_Time = ({self.MDS_Options["NVT Time"]} * 1000) # ps --> fs\n" +
                     f"NVT_Granularity = {self.NVT_MDP["NVT Granularity"]}\n" +
                     f"NVT_UpdateFreq = {self.NVT_MDP["NVT Update Frequency"]} * 1000 # ps --> fs\n" +
                     f"NVT_Continued = '{self.NVT_MDP["NVT Continued"]}'\n" +
                     f"NVT_ConstraintAlgorithm = '{self.NVT_MDP["NVT Constraint Algorithm"]}'\n" +
                     f"NVT_Constraints = '{self.NVT_MDP["NVT Constraints"]}'\n" +
                     f"NVT_LINCSIter = {self.NVT_MDP["NVT LINCS Iterations"]}\n" +
                     f"NVT_LINCSOrder = {self.NVT_MDP["NVT LINCS Order"]}\n" +
                     f"NVT_NeighbourScheme = '{self.NVT_MDP["NVT Neighbour Scheme"]}'\n" +
                     f"NVT_NeighbourMethod = '{self.NVT_MDP["NVT Neighbour Method"]}'\n" +
                     f"NVT_ColoumbType = '{self.NVT_MDP["NVT Coloumb Type"]}'\n" +
                     f"NVT_ColoumbCutoff = {self.NVT_MDP["NVT Coloumb Cutoff"]}\n" +
                     f"NVT_VdWCutoff = {self.NVT_MDP["NVT Van der Waal Cutoff"]}\n" +
                     f"NVT_VdWCorrection = '{self.NVT_MDP["NVT VdW Correction"]}'\n" +
                     f"NVT_PMEOrder = {self.NVT_MDP["NVT PME Order"]}\n" +
                     f"NVT_FourierSpacing = {self.NVT_MDP["NVT Fourier Spacing"]}\n" +
                     f"NVT_TempCoupling = '{self.NVT_MDP["NVT Temperature Coupling"]}'\n" +
                     f"NVT_CouplingGroups = '{self.NVT_MDP["NVT Coupling Groups"]}'\n" +
                     f"NVT_TempTimeConstant = {self.NVT_MDP["NVT Temp Time Constant"]}\n" +
                     f"NVT_BoundryType = '{self.NVT_MDP["NVT Boundry Type"]}'\n" +
                     f"NVT_GenVelocity = '{self.NVT_MDP["NVT Gen Velocity"]}'\n" +
                     f"NVT_Seed = '{self.NVT_MDP["NVT Seed"]}'\n" +
                     f"NPT_Restrain = '{self.NPT_MDP["NPT Restrain"]}'\n" +
                     f"NPT_Integrator = '{self.NPT_MDP["NPT Integrator"]}'\n" +
                     f"NPT_Time = ({self.MDS_Options["NPT Time"]} * 1000) # ps --> fs\n" +
                     f"NPT_Granularity = {self.NPT_MDP["NPT Granularity"]}\n" +
                     f"NPT_UpdateFreq = {self.NPT_MDP["NPT Update Frequency"]} * 1000 # ps --> fs\n" +
                     f"NPT_Continued = '{self.NPT_MDP["NPT Continued"]}'\n" +
                     f"NPT_ConstraintAlgorithm = '{self.NPT_MDP["NPT Constraint Algorithm"]}'\n" +
                     f"NPT_Constraints = '{self.NPT_MDP["NPT Constraints"]}'\n" +
                     f"NPT_LINCSIter = {self.NPT_MDP["NPT LINCS Iterations"]}\n" +
                     f"NPT_LINCSOrder = {self.NPT_MDP["NPT LINCS Order"]}\n" +
                     f"NPT_NeighbourScheme = '{self.NPT_MDP["NPT Neighbour Scheme"]}'\n" +
                     f"NPT_NeighbourMethod = '{self.NPT_MDP["NPT Neighbour Method"]}'\n" +
                     f"NPT_ColoumbType = '{self.NPT_MDP["NPT Coloumb Type"]}'\n" +
                     f"NPT_ColoumbCutoff = {self.NPT_MDP["NPT Coloumb Cutoff"]}\n" +
                     f"NPT_VdWCutoff = {self.NPT_MDP["NPT Van der Waal Cutoff"]}\n" +
                     f"NPT_VdWCorrection = '{self.NPT_MDP["NPT VdW Correction"]}'\n" +
                     f"NPT_PMEOrder = {self.NPT_MDP["NPT PME Order"]}\n" +
                     f"NPT_FourierSpacing = {self.NPT_MDP["NPT Fourier Spacing"]}\n" +
                     f"NPT_TempCoupling = '{self.NPT_MDP["NPT Temperature Coupling"]}'\n" +
                     f"NPT_CouplingGroups = '{self.NPT_MDP["NPT Coupling Groups"]}'\n" +
                     f"NPT_TempTimeConstant = {self.NPT_MDP["NPT Temp Time Constant"]}\n" +
                     f"NPT_PressureCoupling = '{self.NPT_MDP["NPT Pressure Coupling"]}'\n" +
                     f"NPT_PressureCouplingType = '{self.NPT_MDP["NPT Pressure Coupling Type"]}'\n" +
                     f"NPT_WaterCompressibility = '{self.NPT_MDP["NPT Water Compressibility"]}'\n" +
                     f"NPT_CoordinateScaling = '{self.NPT_MDP["NPT Coordinate Scaling"]}'\n" +
                     f"NPT_BoundryType = '{self.NPT_MDP["NPT Boundry Type"]}'\n" +
                     f"NPT_GenVelocity = '{self.NPT_MDP["NPT Gen Velocity"]}'\n" +
                     f"NPT_Seed = '{self.NPT_MDP["NPT Seed"]}'\n" +
                     f"PROD_Restrain = '{self.PROD_MDP["PROD Restrain"]}'\n" +
                     f"PROD_Integrator = '{self.PROD_MDP["PROD Integrator"]}'\n" +
                     f"PROD_Time = ({self.MDS_Options["PROD Time"]} * 1000000) # ns --> fs\n" +
                     f"PROD_Granularity = {self.PROD_MDP["PROD Granularity"]}\n" +
                     f"PROD_UpdateFreq = {self.PROD_MDP["PROD Update Frequency"]} * 1000 # ps --> fs\n" +
                     f"PROD_Compression = '{self.PROD_MDP["PROD Compress"]}'\n" +
                     f"PROD_Continued = '{self.PROD_MDP["PROD Continued"]}'\n" +
                     f"PROD_ConstraintAlgorithm = '{self.PROD_MDP["PROD Constraint Algorithm"]}'\n" +
                     f"PROD_Constraints = '{self.PROD_MDP["PROD Constraints"]}'\n" +
                     f"PROD_LINCSIter = {self.PROD_MDP["PROD LINCS Iterations"]}\n" +
                     f"PROD_LINCSOrder = {self.PROD_MDP["PROD LINCS Order"]}\n" +
                     f"PROD_NeighbourScheme = '{self.PROD_MDP["PROD Neighbour Scheme"]}'\n" +
                     f"PROD_NeighbourMethod = '{self.PROD_MDP["PROD Neighbour Method"]}'\n" +
                     f"PROD_ColoumbType = '{self.PROD_MDP["PROD Coloumb Type"]}'\n" +
                     f"PROD_ColoumbCutoff = {self.PROD_MDP["PROD Coloumb Cutoff"]}\n" +
                     f"PROD_VdWCutoff = {self.PROD_MDP["PROD Van der Waal Cutoff"]}\n" +
                     f"PROD_VdWCorrection = '{self.PROD_MDP["PROD VdW Correction"]}'\n" +
                     f"PROD_PMEOrder = {self.PROD_MDP["PROD PME Order"]}\n" +
                     f"PROD_FourierSpacing = {self.PROD_MDP["PROD Fourier Spacing"]}\n" +
                     f"PROD_TempCoupling = '{self.PROD_MDP["PROD Temperature Coupling"]}'\n" +
                     f"PROD_CouplingGroups = '{self.PROD_MDP["PROD Coupling Groups"]}'\n" +
                     f"PROD_TempTimeConstant = {self.PROD_MDP["PROD Temp Time Constant"]}\n" +
                     f"PROD_PressureCoupling = '{self.PROD_MDP["PROD Pressure Coupling"]}'\n" +
                     f"PROD_PressureCouplingType = '{self.PROD_MDP["PROD Pressure Coupling Type"]}'\n" +
                     f"PROD_WaterCompressibility = '{self.PROD_MDP["PROD Water Compressibility"]}'\n" +
                     f"PROD_BoundryType = '{self.PROD_MDP["PROD Boundry Type"]}'\n" +
                     f"PROD_GenVelocity = '{self.PROD_MDP["PROD Gen Velocity"]}'\n" +
                     f"PROD_Seed = '{self.PROD_MDP["PROD Seed"]}'\n\n" +

                     "# User Configuration Values #\n" +
                     f"Project = '{Config_Data["Project"]}'\n" +
                     f"Default_Build = '{MDS_Builds["Default Build"]}'\n" +
                     f"GPU_Build = '{MDS_Builds["GPU Build"]}'\n" +
                     f"MPI_Build = '{MDS_Builds["MPI Build"]}'\n" +
                     f"MPI_GPU_Build = '{MDS_Builds["MPI + GPU Build"]}'\n\n"
                     )



        NameGeneration = ("### Generate File Names ###\n" +
                          "ProteinName=os.path.splitext(ProteinFilename)\n" +
                          "ProteinName = ProteinName[0]\n\n" +
                          "# Generate Configuration File Names and File Structure: \n" +
                          "config_dir = \"Configuration_Files/\"\n" +
                          "data_dir = \"Data/\"\n" +
                          "preprocessing_dir = data_dir + \"Preprocessing/\"\n" +
                          "sim_dir = data_dir + \"Simulation/\"\n" +
                          "analysis_dir = \"Analysis/\"\n" +
                          "os.makedirs(config_dir)\n" +
                          "os.makedirs(data_dir)\n" +
                          "os.makedirs(preprocessing_dir)\n" +
                          "os.makedirs(sim_dir)\n" +
                          "os.makedirs(analysis_dir)\n" +
                          r'IonConfig = config_dir + f"Ion_Configuration_{ScriptName}"' + "\n" +
                          r'EnergyConfig = config_dir + f"EnergyMinim_Configuration_{ScriptName}"' + "\n" +
                          r'NVTConfig = config_dir + f"NVT_Configuration_{ScriptName}"' + "\n" +
                          r'NPTConfig = config_dir + f"NPT_Configuration_{ScriptName}"' + "\n" + 
                          r'SimulationConfig = config_dir + f"Sim_Configuration_{ScriptName}"' + "\n" + 
                          "\n\n")

        PBS_File_Setup = ("### Generate PBS File ###\n" +
                          r'PBSTextFile = open(f"Gro_{ScriptName}.pbs", "a")' + "\n" +
                          r'PBSTextFile.close()' + "\n\n" +

                          "# Specify \"#PBS\" Inputs\n" + 
                          r'PBS_JobInputs = f"#!/bin/bash \n#PBS -P {Project} \n#PBS -N {ScriptName} \n#PBS -l select={Node_Count}:ncpus={CPU_Count}:mem={Memory_Allocation}GB:ngpus={GPU_Count}\n' + 
                          r'#PBS -l walltime={Walltime_Hours}:{Walltime_Minutes}:{Walltime_Seconds} \n#PBS -M {Email} \n#PBS -m abe \n\n"' + "\n" +
                          r'PBSTextFile = open(f"Gro_{ScriptName}.pbs", "a")' + "\n" +
                          "PBSTextFile.write(PBS_JobInputs)\n\n")

        PerformanceModules = ("# Load Modules #\n" +
                              "if Path_Options == 'Automatic':\n" +
                              "    Current_Dir = os.getcwd()\n" +
                              "else:\n" +
                              "    Current_Dir = Path_Directory\n\n" +

                              "if Node_Mode==\"Parallel\" and GPU_Count > 0:\n" +
                              r'    PBS_LoadModules = f"#Load Modules \ncd ..\ncd ..\ncd {Current_Dir} \nmodule load {MPI_GPU_Build}\n\n"' + "\n" +
                              r'    gmx = "gmx_mpi"' + "\n" +
                              "elif Node_Mode==\"Parallel\":\n" +
                              r'    PBS_LoadModules = f"#Load Modules \ncd ..\ncd ..\ncd {Current_Dir} \nmodule load {MPI_Build}\n\n"' + "\n" +
                              r'    gmx = "gmx_mpi"' + "\n" +
                              "elif GPU_Count > 0:\n" +
                              r'    PBS_LoadModules = f"#Load Modules \ncd ..\ncd ..\ncd {Current_Dir} \nmodule load {GPU_Build}\n\n"' + "\n" +
                              r'    gmx = "gmx"' + "\n" +
                              "else:\n"
                              r'    PBS_LoadModules = f"#Load Modules \ncd ..\ncd ..\ncd {Current_Dir} \nmodule load {Default_Build}\n\n"' + "\n" +
                              r'    gmx = "gmx"' + "\n" +
                              "PBSTextFile.write(PBS_LoadModules)\n" +
                              "Current_Dir = Current_Dir + '/'\n\n")


        MDS_Setup = ("# Gromacs Setup and Config Commands:\n" +
                     "BoxEstimation = (int((int(ProteinSize)/4000)) + 2)*Protein_Count\n" +
                     "if Remove_Water == \"True\":\n" +
                     r'    Strip_Water = f"#Strip Water \ngrep -v HOH {ProteinName}.pdb > {Current_Dir + preprocessing_dir + ProteinName}_Clean.pdb \ncd {data_dir}\n\n"' + "\n" +
                     r'    Insert_Molecules = f"#Insert Proteins \n{gmx} insert-molecules -ci {Current_Dir + preprocessing_dir + ProteinName}_Clean.pdb -nmol {Protein_Count} -box {BoxEstimation} {BoxEstimation} {BoxEstimation} -try 100 -rot xyz -o {Current_Dir + preprocessing_dir + ProteinName}_Multi.pdb \n\n"' + "\n" +
                     r'    MultiCoordinateFiles = f"#Get Coordinate and Topology Files \n{gmx} pdb2gmx -f {Current_Dir + preprocessing_dir + ProteinName}_Multi.pdb -o {Current_Dir +  data_dir + ScriptName}.gro -p {Current_Dir +  data_dir + ScriptName}.top -i {Current_Dir + preprocessing_dir + ScriptName}.itp -water {Water_Model} -ff {ForceField} -ignh \n\n"' + "\n" +
                     r'    SingleCoordinateFiles = f"#Get Coordinate and Topology Files \n{gmx} pdb2gmx -f {Current_Dir + preprocessing_dir + ProteinName}_Clean.pdb -o {Current_Dir +  data_dir + ScriptName}.gro -p {Current_Dir +  data_dir + ScriptName}.top -i {Current_Dir + preprocessing_dir + ScriptName}.itp -water {Water_Model} -ff {ForceField} -ignh \n\n"' + "\n" +
                     r'    CubicBounds = f"#Set Simulation Bounds \n{gmx} editconf -f {Current_Dir +  data_dir + ScriptName}.gro -o {Current_Dir + preprocessing_dir + ScriptName}_{Boundry_Shape}.gro -c -d {Boundry_Gap} -bt {Boundry_Shape} \n\n"' + "\n" +
                     r'    SolventFill = f"#Fill Solvent \n{gmx} solvate -cp {Current_Dir + preprocessing_dir + ScriptName}_{Boundry_Shape}.gro -cs spc216.gro -o {Current_Dir + preprocessing_dir + ScriptName}_SOLV.gro -p {Current_Dir +  data_dir + ScriptName}.top \n\n"' + "\n\n" +
                     "else:\n" +
                     r'    Strip_Water = "#Copy Protein \ncp {ProteinName}.pdb {Current_Dir + preprocessing_dir + ProteinName}.pdb \ncd {data_dir}\n\n"' + "\n" +
                     r'    Insert_Molecules = f"#Insert Proteins \n{gmx} insert-molecules -ci {Current_Dir + preprocessing_dir + ProteinName}.pdb -nmol {Protein_Count} -box {BoxEstimation} {BoxEstimation} {BoxEstimation} -try 100 -rot xyz -o {Current_Dir + preprocessing_dir + ProteinName}_Multi.pdb \n\n"' + "\n" +
                     r'    MultiCoordinateFiles = f"#Get Coordinate and Topology Files \n{gmx} pdb2gmx -f {Current_Dir + preprocessing_dir + ProteinName}_Multi.pdb -o {Current_Dir +  data_dir + ScriptName}.gro -p {Current_Dir +  data_dir + ScriptName}.top -i {Current_Dir + preprocessing_dir + ScriptName}.itp -water {Water_Model} -ff {ForceField} -ignh \n\n"' + "\n" +
                     r'    SingleCoordinateFiles = f"#Get Coordinate and Topology Files \n{gmx} pdb2gmx -f {Current_Dir + preprocessing_dir + ProteinName}.pdb -o {Current_Dir +  data_dir + ScriptName}.gro -p {Current_Dir +  data_dir + ScriptName}.top -i {Current_Dir + preprocessing_dir + ScriptName}.itp -water {Water_Model} -ff {ForceField} -ignh \n\n"' + "\n" +
                     r'    CubicBounds = f"#Set Simulation Bounds \n{gmx} editconf -f {Current_Dir +  data_dir + ScriptName}.gro -o {Current_Dir + preprocessing_dir + ScriptName}_{Boundry_Shape}.gro -c -d {Boundry_Gap} -bt {Boundry_Shape} \n\n"' + "\n" +
                     r'    SolventFill = f"#Fill Solvent \n{gmx} solvate -cp {Current_Dir + preprocessing_dir + ScriptName}_{Boundry_Shape}.gro -cs spc216.gro -o {Current_Dir + preprocessing_dir + ScriptName}_SOLV.gro -p {Current_Dir +  data_dir + ScriptName}.top \n\n"' + "\n\n" +

                     "if GeneratedStructure == 1 or '1':\n" +
                     "    ReformatString = \"sed -i 's/OXT/O  /g'\"\n" +
                     r'    ReformatPDB = f"#Adjust AlphaFold PDB File\n{ReformatString} {ProteinName}.pdb\n\n"' + "\n" +
                     "    PBSTextFile.write(ReformatPDB)\n\n" + 

                     "PBSTextFile.write(Strip_Water)\n" +
                     "if Protein_Count > 1:\n" +
                     "    PBSTextFile.write(Insert_Molecules)\n" +
                     "    PBSTextFile.write(MultiCoordinateFiles)\n" +
                     "else:\n" +
                     "    PBSTextFile.write(SingleCoordinateFiles)\n" +
                     "PBSTextFile.write(CubicBounds)\n" +
                     "PBSTextFile.write(SolventFill)\n\n")

        SimulationPreprocessing = ("# Gromacs Preprocessing and Simulation Commands:\n" +
                                   r'BalanceCharges = f"#Balance Charges \n{gmx} grompp -f {Current_Dir + IonConfig}.mdp -c {Current_Dir + preprocessing_dir + ScriptName}_SOLV.gro -p {Current_Dir +  data_dir + ScriptName}.top -o {Current_Dir + preprocessing_dir + ScriptName}_IONS.tpr -po {Current_Dir + preprocessing_dir}mdout.mdp -maxwarn 1\n"' + "\n" +
                                   r'GenIons = f"echo SOL | {gmx} genion -s {Current_Dir + preprocessing_dir + ScriptName}_IONS.tpr -o {Current_Dir + preprocessing_dir + ScriptName}_SOLV.gro -p {Current_Dir +  data_dir + ScriptName}.top -pname {Positive_Atom} -nname {Negative_Atom} -{System_Charge} \n\n"' + "\n" +
                                   r'EnergyMinimisation = f"#Minimise Energy \n{gmx} grompp -f {Current_Dir + EnergyConfig}.mdp -c {Current_Dir + preprocessing_dir + ScriptName}_SOLV.gro -p {Current_Dir +  data_dir + ScriptName}.top -o {Current_Dir +  sim_dir + ScriptName}_MINIM.tpr -po {Current_Dir + preprocessing_dir}mdout.mdp \n"' + "\n" +
                                   r'NVTSetup = f"#NVT \n{gmx} grompp -f {Current_Dir + NVTConfig}.mdp -c {Current_Dir +  sim_dir + ScriptName}_MINIM.gro -r {Current_Dir +  sim_dir + ScriptName}_MINIM.gro -p {Current_Dir +  data_dir + ScriptName}.top -o {Current_Dir +  sim_dir + ScriptName}_NVT.tpr -po {Current_Dir + preprocessing_dir}mdout.mdp \n"' + "\n" +
                                   r'NPTSetup  = f"#NPT \n{gmx} grompp -f {Current_Dir + NPTConfig}.mdp -c {Current_Dir +  sim_dir + ScriptName}_NVT.gro  -r {Current_Dir +  sim_dir + ScriptName}_NVT.gro -p {Current_Dir +  data_dir + ScriptName}.top -o {Current_Dir +  sim_dir + ScriptName}_NPT.tpr -po {Current_Dir + preprocessing_dir}mdout.mdp \n"' + "\n" +
                                   r'Simulation = f"#Production Run \n{gmx} grompp -f {Current_Dir + SimulationConfig}.mdp -c {Current_Dir +  sim_dir + ScriptName}_NPT.gro -t {Current_Dir +  sim_dir + ScriptName}_NPT.cpt -p {Current_Dir +  data_dir + ScriptName}.top -o {Current_Dir +  sim_dir + ScriptName}_PROD.tpr -po {Current_Dir + preprocessing_dir}mdout.mdp \n"' + "\n" +
                                   r'if PROD_PressureCoupling == "Parrinello-Rahman":' + "\n" +
                                   r'   Simulation = f"#Production Run \n{gmx} grompp -f {Current_Dir + SimulationConfig}.mdp -c {Current_Dir +  sim_dir + ScriptName}_NPT.gro -t {Current_Dir +  sim_dir + ScriptName}_NPT.cpt -p {Current_Dir +  data_dir + ScriptName}.top -o {Current_Dir +  sim_dir + ScriptName}_PROD.tpr -po {Current_Dir + preprocessing_dir}mdout.mdp -maxwarn 1\n"' + "\n\n")

        Orginise = ("# Move Data to Analysis Folder\n" + 
                    r'OrginiseData = f"mv {Current_Dir +  sim_dir + ScriptName}_NPT.gro {Current_Dir +  analysis_dir + ScriptName}_NPT.gro\n"' + 
                    r'f"mv {Current_Dir +  sim_dir + ScriptName}_PROD.gro {Current_Dir +  analysis_dir + ScriptName}_PROD.gro\n"' +
                    r'f"mv {Current_Dir +  sim_dir + ScriptName}_PROD.xtc {Current_Dir +  analysis_dir + ScriptName}_PROD.xtc\n"' + "\n\n")
        
        MDRunSetup = ("# Setup mdrun commands: \n" +
                      r'os.makedirs("Logs")' + "\n" +
                      "if GPU_Count > 0:\n"
                      r'  EMRun = f"{gmx} mdrun -v -deffnm {Current_Dir +  sim_dir + ScriptName}_MINIM -nb gpu -g {Current_Dir}/Logs/{ScriptName}_EM.log"' + "\n" +
                      r'  NVTRun = f"{gmx} mdrun -deffnm {Current_Dir +  sim_dir + ScriptName}_NVT -nb gpu -g {Current_Dir}/Logs/{ScriptName}_NVT.log"' + "\n" +
                      r'  NPTRun = f"{gmx} mdrun -deffnm {Current_Dir +  sim_dir + ScriptName}_NPT -nb gpu -g {Current_Dir}/Logs/{ScriptName}_NPT.log"' + "\n" +
                      r'  SimRun = f"{gmx} mdrun -deffnm {Current_Dir +  sim_dir + ScriptName}_PROD -nb gpu -g {Current_Dir}/Logs/{ScriptName}_PROD.log"' + "\n" +
                      "else:\n" +
                      r'  EMRun = f"{gmx} mdrun -v -deffnm {Current_Dir +  sim_dir + ScriptName}_MINIM -g {Current_Dir}/Logs/{ScriptName}_EM.log"' + "\n" +
                      r'  NVTRun = f"{gmx} mdrun -deffnm {Current_Dir +  sim_dir + ScriptName}_NVT -g {Current_Dir}/Logs/{ScriptName}_NVT.log"' + "\n" +
                      r'  NPTRun = f"{gmx} mdrun -deffnm {Current_Dir +  sim_dir + ScriptName}_NPT -g {Current_Dir}/Logs/{ScriptName}_NPT.log"' + "\n" +
                      r'  SimRun = f"{gmx} mdrun -deffnm {Current_Dir +  sim_dir + ScriptName}_PROD -g {Current_Dir}/Logs/{ScriptName}_PROD.log"' + "\n\n" +
                      "if Node_Mode==\"Parallel\":\n" +
                      r'    EMRun = EMRun + f" -ntomp {CPU_Count}"' + "\n" +
                      r'    NVTRun = NVTRun + f" -ntomp {CPU_Count}"' + "\n" +
                      r'    NPTRun = NPTRun + f" -ntomp {CPU_Count}"' + "\n" +
                      r'    SimRun = SimRun + f" -ntomp {CPU_Count}"' + "\n" +
                      "elif GPU_Count > 0:\n" +
                      r'    EMRun = EMRun + f" -ntmpi {GPU_Count} -ntomp {CPU_Count}"' + "\n" +
                      r'    NVTRun = NVTRun + f" -ntmpi {GPU_Count} -ntomp {CPU_Count}"' + "\n" +
                      r'    NPTRun = NPTRun + f" -ntmpi {GPU_Count} -ntomp {CPU_Count}"' + "\n" +
                      r'    SimRun = SimRun + f" -ntmpi {GPU_Count} -ntomp {CPU_Count}"' + "\n" +
                      r'EMRun = EMRun + "\n\n"' + "\n" +
                      r'NVTRun = NVTRun + "\n\n"' + "\n" +
                      r'NPTRun = NPTRun + "\n\n"' + "\n" +
                      r'SimRun = SimRun + "\n\n"' + "\n" +
                      "PBSTextFile.write(BalanceCharges)\n" +
                      "PBSTextFile.write(GenIons)\n" +
                      "PBSTextFile.write(EnergyMinimisation)\n" +
                      "PBSTextFile.write(EMRun)\n" +
                      "PBSTextFile.write(NVTSetup)\n" +
                      "PBSTextFile.write(NVTRun)\n" +
                      "PBSTextFile.write(NPTSetup)\n" +
                      "PBSTextFile.write(NPTRun)\n" +
                      "PBSTextFile.write(Simulation)\n" +
                      "PBSTextFile.write(SimRun)\n" +
                      "PBSTextFile.write(OrginiseData)\n" +
                      "PBSTextFile.close()\n\n")



        CreateMDPVars = ("# Setup MDP Variables: \n"
                          "ION_Timestep_Size = ION_Granularity/100\n" +
                          "Minimisation_Timestep_Size = MIN_Granularity/1000\n" +
                          "Simulation_Timestep_Size = PROD_Granularity/1000 \n" +
                          "Timestep_Max_ION = int(ION_Time/MIN_Granularity)\n" +
                          "Timestep_Max_MIN = int(MIN_Time/MIN_Granularity)\n" +
                          "Timestep_Total_NVT = int(NVT_Time/NVT_Granularity)\n" +
                          "Timestep_Total_NPT = int(NPT_Time/NPT_Granularity)\n" +
                          "Timestep_Total_PROD = int(PROD_Time/PROD_Granularity)\n" +
                          "ION_Update_Timestep = int(ION_UpdateFreq/ION_Granularity)\n" +
                          "MIN_Update_Timestep = int(MIN_UpdateFreq/MIN_Granularity)\n" +
                          "NVT_Update_Timestep = int(NVT_UpdateFreq/NVT_Granularity)\n" +
                          "NPT_Update_Timestep = int(NPT_UpdateFreq/NPT_Granularity)\n" +
                          "PROD_Update_Timestep = int(PROD_UpdateFreq/PROD_Granularity)\n\n")

        ConfigureIONMDP = ("# Configure the ION MDP file values: \n" + 
                           r'ION_MDP = open(f"{Current_Dir + IonConfig}.mdp", "a") ' + "\n" +
                           r'ION_MDP.close() ' + "\n" +
                           r'ION_MDP = open(f"{Current_Dir + IonConfig}.mdp", "a") ' + "\n\n" +

                           r'ION_MDP.write(f"; ions.mdp file - used as input into grompp to generate ions.tpr file\n''\\' + "\n" +
                           r'; Parameters describing what to do, when to stop and what to save\n''\\' + "\n" +
                           r'integrator  = {ION_Integrator}         ; Algorithm (steep = steepest descent minimization)\n''\\' + "\n" +
                           r'emtol       = {ION_MinLimit}        ; Stop minimization when the maximum force < 1000.0 kJ/mol/nm\n''\\' + "\n" +
                           r'emstep      = {ION_Timestep_Size}          ; Minimization step size\n''\\' + "\n" +
                           r'nsteps      = {Timestep_Max_ION}         ; Maximum number of (minimization) steps to perform\n\n''\\' + "\n" +
                           r'; Parameters describing how to find the neighbors of each atom and how to calculate the interactions\n''\\' + "\n" +
                           r'nstlist         = 20         ; Frequency to update the neighbor list and long range forces\n''\\' + "\n" +
                           r'cutoff-scheme	= {ION_NeighbourScheme}    ; Buffered neighbor searching \n''\\' + "\n" +
                           r'ns_type         = {ION_NeighbourMethod}      ; Method to determine neighbor list (simple, grid)\n''\\' + "\n" +
                           r'coulombtype     = {ION_ColoumbType}    ; Treatment of long range electrostatic interactions\n''\\' + "\n" +
                           r'rcoulomb        = {ION_ColoumbCutoff}       ; Short-range electrostatic cut-off\n''\\' + "\n" +
                           r'rvdw            = {ION_VdWCutoff}       ; Short-range Van der Waals cut-off\n''\\' + "\n" +
                           r'pbc             = {ION_BoundryType}       ; Periodic Boundary Conditions in all 3 dimensions")' + "\n\n" +

                           r'ION_MDP.close() ' + "\n\n\n")


        ConfigureMINMDP = ("# Configure the Minimisation MDP file values: \n" +
                           r'MINIM_MDP = open(f"{Current_Dir + EnergyConfig}.mdp", "a") ' + "\n" +
                           r'MINIM_MDP.close() ' + "\n" +
                           r'MINIM_MDP = open(f"{Current_Dir + EnergyConfig}.mdp", "a") ' + "\n\n" +

                           r'MINIM_MDP.write(f"; minim.mdp file - used as input into grompp to generate em.tpr file\n''\\' + "\n" +
                           r'; Parameters describing what to do, when to stop and what to save\n''\\' + "\n" +
                           r'integrator  = {MIN_Integrator}         ; Algorithm (steep = steepest descent minimization)\n''\\' + "\n" +
                           r'emtol       = {MIN_MinLimit}        ; Stop minimization when the maximum force < 1000.0 kJ/mol/nm\n''\\' + "\n" +
                           r'emstep      = {Minimisation_Timestep_Size}          ; Minimization step size\n''\\' + "\n" +
                           r'nsteps      = {Timestep_Max_MIN}         ; Maximum number of (minimization) steps to perform\n\n''\\' + "\n" +
                           r'; Parameters describing how to find the neighbors of each atom and how to calculate the interactions\n''\\' + "\n" +
                           r'nstlist         = 20        ; Frequency to update the neighbor list and long range forces\n''\\' + "\n" +
                           r'cutoff-scheme   = {MIN_NeighbourScheme}    ; Buffered neighbor searching\n''\\' + "\n" +
                           r'ns_type         = {MIN_NeighbourMethod}      ; Method to determine neighbor list (simple, grid)\n''\\' + "\n" +
                           r'coulombtype     = {MIN_ColoumbType}       ; Treatment of long range electrostatic interactions\n''\\' + "\n" +
                           r'rcoulomb        = {MIN_ColoumbCutoff}       ; Short-range electrostatic cut-off\n''\\' + "\n" +
                           r'rvdw            = {MIN_VdWCutoff}       ; Short-range Van der Waals cut-off\n''\\' + "\n" +
                           r'pbc             = {MIN_BoundryType}       ; Periodic Boundary Conditions in all 3 dimensions")' + "\n\n" +

                           r'MINIM_MDP.close() ' + "\n\n\n")
        

        ConfigureNVTMDP = ("# Configure the NVT MDP file values: \n" +
                           r'NVT_MDP = open(f"{Current_Dir + NVTConfig}.mdp", "a")' + "\n" +
                           r'NVT_MDP.close()' + "\n" +
                           r'NVT_MDP = open(f"{Current_Dir + NVTConfig}.mdp", "a")' + "\n\n" +

                           r'NVT_MDP.write(f"title                   = NVT equilibration \n''\\' + "\n" +
                           r'define                  = {NVT_Restrain}  ; position restrain the protein \n''\\' + "\n" +
                           r'; Run parameters\n''\\' + "\n" +
                           r'integrator              = {NVT_Integrator}        ; leap-frog integrator\n''\\' + "\n" +
                           r'nsteps                  = {Timestep_Total_NVT}     ; 2 * 50000 = 100 ps\n''\\' + "\n" +
                           r'dt                      = {Simulation_Timestep_Size}     ; x fs\n''\\' + "\n" +
                           r'; Output control\n''\\' + "\n" +
                           r'nstxout                 = {NVT_Update_Timestep}       ; save coordinates every x ps\n''\\' + "\n" +
                           r'nstvout                 = {NVT_Update_Timestep}       ; save velocities every x ps\n''\\' + "\n" +
                           r'nstenergy               = {NVT_Update_Timestep}       ; save energies every x ps\n''\\' + "\n" +
                           r'nstlog                  = {NVT_Update_Timestep}       ; update log file every x ps\n''\\' + "\n" +
                           r'; Bond parameters\n''\\' + "\n" +
                           r'continuation            = {NVT_Continued}       ; Restarting after NVT \n''\\' + "\n" +
                           r'constraint_algorithm    = {NVT_ConstraintAlgorithm}     ; holonomic constraints\n''\\' + "\n" +
                           r'constraints             = {NVT_Constraints}   ; bonds involving H are constrained\n''\\' + "\n" +
                           r'lincs_iter              = {NVT_LINCSIter}         ; accuracy of LINCS\n''\\' + "\n" +
                           r'lincs_order             = {NVT_LINCSOrder}         ; also related to accuracy\n''\\' + "\n" +
                           r'; Nonbonded settings\n''\\' + "\n" +
                           r'cutoff-scheme           = {NVT_NeighbourScheme}    ; Buffered neighbor searching\n''\\' + "\n" +
                           r'ns_type                 = {NVT_NeighbourMethod}      ; search neighboring grid cells\n''\\' + "\n" +
                           r'nstlist                 = 20        ; 20 fs, largely irrelevant with Verlet scheme\n''\\' + "\n" +
                           r'rcoulomb                = {NVT_ColoumbCutoff}       ; short-range electrostatic cutoff (in nm)\n''\\' + "\n" +
                           r'rvdw                    = {NVT_VdWCutoff}       ; short-range van der Waals cutoff (in nm)\n''\\' + "\n" +
                           r'DispCorr                = {NVT_VdWCorrection}  ; account for cut-off vdW scheme\n''\\' + "\n" +
                           r'; Electrostatics\n''\\' + "\n" +
                           r'coulombtype             = {NVT_ColoumbType}       ; Particle Mesh Ewald for long-range electrostatics\n''\\' + "\n" +
                           r'pme_order               = {NVT_PMEOrder}         ; cubic interpolation\n''\\' + "\n" +
                           r'fourierspacing          = {NVT_FourierSpacing}      ; grid spacing for FFT\n''\\' + "\n" +
                           r'; Temperature coupling is on\n''\\' + "\n" +
                           r'tcoupl                  = {NVT_TempCoupling}             ; modified Berendsen thermostat\n''\\' + "\n" +
                           r'tc-grps                 = {NVT_CouplingGroups}   ; two coupling groups - more accurate\n''\\' + "\n" +
                           r'tau_t                   = {NVT_TempTimeConstant}     {NVT_TempTimeConstant}           ; time constant, in ps\n''\\' + "\n" +
                           r'ref_t                   = {Temperature}     {Temperature}           ; reference temperature, one for each group, in K\n''\\' + "\n" +
                           r'; Pressure coupling is off\n''\\' + "\n" +
                           r'pcoupl                  = no     ; Pressure coupling off in NVT\n''\\' + "\n" +
                           r'; Periodic boundary conditions\n''\\' + "\n" +
                           r'pbc                     = {NVT_BoundryType}       ; 3-D PBC\n''\\' + "\n" +
                           r'; Velocity generation\n''\\' + "\n" +
                           r'gen_vel                 = {NVT_GenVelocity}        ; Velocity generation is yes\n''\\' + "\n" +
                           r'gen_temp                = {Temperature}         ; Temperature for Maxwell distribution\n''\\' + "\n" +
                           r'gen_seed                = {NVT_Seed}         ; Generate a random seed")' + "\n\n"

                           r'NVT_MDP.close()' + "\n\n\n\n")





        ConfigureNPTMDP = ("# Configure the NPT MDP file values: \n" +
                           r'NPT_MDP = open(f"{Current_Dir + NPTConfig}.mdp", "a")' + "\n" +
                           r'NPT_MDP.close()' + "\n" +
                           r'NPT_MDP = open(f"{Current_Dir + NPTConfig}.mdp", "a")' + "\n\n" +

                           r'NPT_MDP.write(f"title                   = NPT equilibration \n''\\' + "\n" +
                           r'define                  = {NPT_Restrain}  ; position restrain the protein \n''\\' + "\n" +
                           r'; Run parameters\n''\\' + "\n" +
                           r'integrator              = {NPT_Integrator}        ; leap-frog integrator\n''\\' + "\n" +
                           r'nsteps                  = {Timestep_Total_NPT}     ; 2 * 50000 = 100 ps\n''\\' + "\n" +
                           r'dt                      = {Simulation_Timestep_Size}     ; 2 fs\n''\\' + "\n" +
                           r'; Output control\n''\\' + "\n" +
                           r'nstxout                 = {NPT_Update_Timestep}       ; save coordinates every 1.0 ps\n''\\' + "\n" +
                           r'nstvout                 = {NPT_Update_Timestep}       ; save velocities every 1.0 ps\n''\\' + "\n" +
                           r'nstenergy               = {NPT_Update_Timestep}       ; save energies every 1.0 ps\n''\\' + "\n" +
                           r'nstlog                  = {NPT_Update_Timestep}       ; update log file every 1.0 ps\n''\\' + "\n" +
                           r'; Bond parameters\n''\\' + "\n" +
                           r'continuation            = {NPT_Continued}       ; Restarting after NPT \n''\\' + "\n" +
                           r'constraint_algorithm    = {NPT_ConstraintAlgorithm}     ; holonomic constraints\n''\\' + "\n" +
                           r'constraints             = {NPT_Constraints}   ; bonds involving H are constrained\n''\\' + "\n" +
                           r'lincs_iter              = {NPT_LINCSIter}         ; accuracy of LINCS\n''\\' + "\n" +
                           r'lincs_order             = {NPT_LINCSOrder}         ; also related to accuracy\n''\\' + "\n" +
                           r'; Nonbonded settings\n''\\' + "\n" +
                           r'cutoff-scheme           = {NPT_NeighbourScheme}    ; Buffered neighbor searching\n''\\' + "\n" +
                           r'ns_type                 = {NPT_NeighbourMethod}      ; search neighboring grid cells\n''\\' + "\n" +
                           r'nstlist                 = 20        ; 20 fs, largely irrelevant with Verlet scheme\n''\\' + "\n" +
                           r'rcoulomb                = {NPT_ColoumbCutoff}       ; short-range electrostatic cutoff (in nm)\n''\\' + "\n" +
                           r'rvdw                    = {NPT_VdWCutoff}       ; short-range van der Waals cutoff (in nm)\n''\\' + "\n" +
                           r'DispCorr                = {NPT_VdWCorrection}  ; account for cut-off vdW scheme\n''\\' + "\n" +
                           r'; Electrostatics\n''\\' + "\n" +
                           r'coulombtype             = {NPT_ColoumbType}       ; Particle Mesh Ewald for long-range electrostatics\n''\\' + "\n" +
                           r'pme_order               = {NPT_PMEOrder}         ; cubic interpolation\n''\\' + "\n" +
                           r'fourierspacing          = {NPT_FourierSpacing}      ; grid spacing for FFT\n''\\' + "\n" +
                           r'; Temperature coupling is on\n''\\' + "\n" +
                           r'tcoupl                  = {NPT_TempCoupling}             ; modified Berendsen thermostat\n''\\' + "\n" +
                           r'tc-grps                 = {NPT_CouplingGroups}   ; two coupling groups - more accurate\n''\\' + "\n" +
                           r'tau_t                   = {NPT_TempTimeConstant}     {NPT_TempTimeConstant}           ; time constant, in ps\n''\\' + "\n" +
                           r'ref_t                   = {Temperature}     {Temperature}           ; reference temperature, one for each group, in K\n''\\' + "\n" +
                           r'; Pressure coupling is on\n''\\' + "\n" +
                           r'pcoupl                  = {NPT_PressureCoupling}     ; Pressure coupling on in NPT\n''\\' + "\n" +
                           r'pcoupltype              = {NPT_PressureCouplingType}             ; uniform scaling of box vectors\n''\\' + "\n" +
                           r'tau_p                   = {10 * NPT_TempTimeConstant}                  ; time constant, in ps\n''\\' + "\n" +
                           r'ref_p                   = {Pressure}                   ; reference pressure, in bar\n''\\' + "\n" +
                           r'compressibility         = {NPT_WaterCompressibility}                ; isothermal compressibility of water, bar^-1\n''\\' + "\n" +
                           r'refcoord_scaling        = {NPT_CoordinateScaling}\n''\\' + "\n" +
                           r'; Periodic boundary conditions\n''\\' + "\n" +
                           r'pbc                     = {NPT_BoundryType}       ; 3-D PBC\n''\\' + "\n" +
                           r'; Velocity generation\n''\\' + "\n" +
                           r'gen_vel                 = {NPT_GenVelocity}        ; Velocity generation is off")' + "\n\n" +

                           r'NPT_MDP.close() ' + "\n\n\n\n")

        

        

        ConfigurePRODMDP = ("# Configure the Production MDP file values: \n" +
                            r'PROD_MDP = open(f"{Current_Dir + SimulationConfig}.mdp", "a") ' + "\n" +
                            r'PROD_MDP.close() ' + "\n" +
                            r'PROD_MDP = open(f"{Current_Dir + SimulationConfig}.mdp", "a") ' + "\n\n" +

                            r'PROD_MDP.write(f"title                   = MD production \n''\\' + "\n" +
                            r'; Run parameters\n''\\' + "\n" +
                            r'integrator              = {PROD_Integrator}        ; leap-frog integrator\n''\\' + "\n" +
                            r'nsteps                  = {Timestep_Total_PROD}    ; 2 * 5000000 = 10000 ps (10 ns)\n''\\' + "\n" +
                            r'dt                      = {Simulation_Timestep_Size}     ; 2 fs\n''\\' + "\n" +
                            r'; Output control\n''\\' + "\n" +
                            r'nstvout                 = 0         ; 0 for output frequency of nstxout,\n''\\' + "\n" +
                            r'nstfout                 = 0         ; nstvout, and nstfout\n''\\' + "\n" +
                            r'nstenergy               = {PROD_Update_Timestep}      ; save energies every 10.0 ps\n''\\' + "\n" +
                            r'nstlog                  = {PROD_Update_Timestep}      ; update log file every 10.0 ps\n''\\' + "\n" +
                            r'nstxout-compressed      = {PROD_Update_Timestep}      ; save compressed coordinates every 10.0 ps\n''\\' + "\n" +
                            r'compressed-x-grps       = {PROD_Compression}    ; save the whole system\n''\\' + "\n" +
                            r'; Bond parameters\n''\\' + "\n" +
                            r'continuation            = {PROD_Continued}       ; Restarting after NPT \n''\\' + "\n" +
                            r'constraint_algorithm    = {PROD_ConstraintAlgorithm}     ; holonomic constraints \n''\\' + "\n" +
                            r'constraints             = {PROD_Constraints}   ; bonds involving H are constrained\n''\\' + "\n" +
                            r'lincs_iter              = {PROD_LINCSIter}         ; accuracy of LINCS\n''\\' + "\n" +
                            r'lincs_order             = {PROD_LINCSOrder}         ; also related to accuracy\n''\\' + "\n" +
                            r'; Neighborsearching\n''\\' + "\n" +
                            r'cutoff-scheme           = {PROD_NeighbourScheme}    ; Buffered neighbor searching\n''\\' + "\n" +
                            r'ns_type                 = {PROD_NeighbourMethod}      ; search neighboring grid cells\n''\\' + "\n" +
                            r'nstlist                 = 20        ; 20 fs, largely irrelevant with Verlet scheme\n''\\' + "\n" +
                            r'rcoulomb                = {PROD_ColoumbCutoff}       ; short-range electrostatic cutoff (in nm)\n''\\' + "\n" +
                            r'rvdw                    = {PROD_VdWCutoff}       ; short-range van der Waals cutoff (in nm)\n''\\' + "\n" +
                            r'; Electrostatics\n''\\' + "\n" +
                            r'coulombtype             = {PROD_ColoumbType}       ; Particle Mesh Ewald for long-range electrostatics\n''\\' + "\n" +
                            r'pme_order               = {PROD_PMEOrder}         ; cubic interpolation\n''\\' + "\n" +
                            r'fourierspacing          = {PROD_FourierSpacing}      ; grid spacing for FFT\n''\\' + "\n" +
                            r'; Temperature coupling is on\n''\\' + "\n" +
                            r'tcoupl                  = {PROD_TempCoupling}             ; modified Berendsen thermostat\n''\\' + "\n" +
                            r'tc-grps                 = {PROD_CouplingGroups}   ; two coupling groups - more accurate\n''\\' + "\n" +
                            r'tau_t                   = {PROD_TempTimeConstant}     {PROD_TempTimeConstant}           ; time constant, in ps\n''\\' + "\n" +
                            r'ref_t                   = {Temperature}     {Temperature}           ; reference temperature, one for each group, in K\n''\\' + "\n" +
                            r'; Pressure coupling is on\n''\\' + "\n" +
                            r'pcoupl                  = {PROD_PressureCoupling}     ; Pressure coupling on in NPT\n''\\' + "\n" +
                            r'pcoupltype              = {PROD_PressureCouplingType}             ; uniform scaling of box vectors\n''\\' + "\n" +
                            r'tau_p                   = {10 * PROD_TempTimeConstant}                   ; time constant, in ps\n''\\' + "\n" +
                            r'ref_p                   = {Pressure}                   ; reference pressure, in bar\n''\\' + "\n" +
                            r'compressibility         = {PROD_WaterCompressibility}                ; isothermal compressibility of water, bar^-1\n''\\' + "\n" +
                            r'; Periodic boundary conditions\n''\\' + "\n" +
                            r'pbc                     = {PROD_BoundryType}       ; 3-D PBC\n''\\' + "\n" +
                            r'; Dispersion correction\n''\\' + "\n" +
                            r'DispCorr                = {PROD_VdWCorrection}  ; account for cut-off vdW scheme\n''\\' + "\n" +
                            r'; Velocity generation\n''\\' + "\n" +
                            r'gen_vel                 = {PROD_GenVelocity}        ; Velocity generation is off")' + "\n" +
                            r'PROD_MDP.close()')
        
        
        SetupScript.write(ScriptImports)
        SetupScript.write(Variables)
        SetupScript.write(NameGeneration)
        SetupScript.write(PBS_File_Setup)
        SetupScript.write(PerformanceModules)
        SetupScript.write(MDS_Setup)
        SetupScript.write(SimulationPreprocessing)
        SetupScript.write(Orginise)
        SetupScript.write(MDRunSetup)
        SetupScript.write(CreateMDPVars)
        SetupScript.write(ConfigureIONMDP)
        SetupScript.write(ConfigureMINMDP)
        SetupScript.write(ConfigureNVTMDP)                  
        SetupScript.write(ConfigureNPTMDP)
        SetupScript.write(ConfigurePRODMDP)
        SetupScript.close()

