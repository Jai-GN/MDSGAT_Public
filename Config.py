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
    "Project":"PROJECT" # Please change "PROJECT" to "<YOUR PROJECT>" before 
}



