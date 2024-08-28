Default_Config = """
{
    "Organisations": 
    [
        {
            "Organisation Name": "The University of Sydney, Australia",
            "Systems":
            [ 
                {
                    "System Name": "Artemis",
                    "Default Build": "gromacs/2021.4",
                    "GPU Build": "gromacs/2021.4-gpu", 
                    "MPI Build": "gromacs/2021.4-mpi",
                    "MPI + GPU Build": "gromacs/2020.1-intel-mpi-gpu",
                    "Projects": ["proteinDynamics", "FEL-ML"]
                }
            ]
        },
        {
            "Organisation Name": "Example Orginisation",
            "Systems":[
                {
                    "System Name": "Example System 1",
                    "Default Build": "Path to Default Gromacs Build",
                    "GPU Build": "Path to Gromacs Build with GPU Enabled (CMAKE)",
                    "MPI Build": "Path to Gromacs Build with MPI Enabled (CMAKE)",
                    "MPI + GPU Build": "Path to Gromacs Build with both GPU and MPI Enabled (CMAKE)",
                    "Projects": ["Example Project 1", "Example Project 2"]
                },
                {
                
                    "System Name": "Example System 2",
                    "Default Build": "Path to Default Gromacs Build",
                    "GPU Build": "Path to Gromacs Build with GPU Enabled (CMAKE)",
                    "MPI Build": "Path to Gromacs Build with MPI Enabled (CMAKE)",
                    "MPI + GPU Build": "Path to Gromacs Build with both GPU and MPI Enabled (CMAKE)",
                    "Projects": ["Example Project 1", "Example Project 2"]
                
                }
            ]
        }
    ],
  
    "Selected Configuration":
    {
        "Organisation Name": "NO ORGANISATION SELECTED",
        "System Name": "NO SYSTEM SELECTED",
        "Project Name": "NO PROJECT SELECTED",
        "Default Build": "NO BUILD SELECTED",
        "GPU Build": "NO BUILD SELECTED",
        "MPI Build": "NO BUILD SELECTED",
        "MPI + GPU Build": "NO BUILD SELECTED"
    }
}
    """