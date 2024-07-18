Introduction_Instructions = """Introduction:
Welcome to the Molecular Dynamics Script Generator and Analysis Tool or the (MDSGAT) v1.0.
Currently this version only supports the GROMACS simulation environment on High
Performance Computer (HPC) systems running the PBS job submission system.

This being said, the MDSGAT is likely to aid any researcher in expediting the
creation of their GROMACS MDS scripts with advanced users capable of 
generating and starting simulations in as little as 2 minutes!

It is recommended that you read through all of this introductory material
as you compile your first GROMACS script.

BEFORE YOU START:
Please ensure you configure the 'Settings' with the appropriate 
information relating to YOUR HPC system! This is very important!
This details important information such as available GROMACS
installations and relevant projects. Please refer to your HPC
documentation if you are unsure of the module syntax. 
This process only needs to be performed once per installation!

Please note that this in in no way an official GROMACS project
nor am I claiming any ownership or property of the GROMACS
simulation environment.


General Tips & Tricks:
Hovering your mouse over most elements in MDSGAT will reveal a brief summary
informing you of that components function or inputs.
If you are unable to generate any setup scripts this is most likely due
to the program not having the permissions to read/write files.
To continue and generate your first GROMACS setup script please select the
'Generator' tab above this window."""

Generator_Instructions = """Script Generator:
This section outlines the script generator function of MDSGAT that will
automatically compile a setup python script to run on your HPC system
to generate a job submission file alongside all required configuration
.mdp files.

To begin this process you will need to select the 'Configure Script'
button in the bottom right of the main program.
In the newly created window you should see a number of entry fields alongside
a number of tabs at the top. For now we will only concern ourselves with
the 'Script Setup', 'MDS Options' and 'Hardware Options' tabs. You should have
a look through the 'Advanced Options' tab after you have created a number of
scripts and have gained confidence in MDS.

Starting in the 'Script Setup' tab we need to enter in some basic information
about our job/simulation. The majority of this information feeds directly into
the PBS job submission script and is important for tracking purposes.
You can use any .pdb file here however smaller structures will require less
hardware to simulate and allow to learn and experiment more rapidly. For
this same reason it is suggested that you also avoid multi-protein simulations
for now.

Remember you can hover over entry fields to gain more of an idea of what to
enter!

After filling out all fields in the 'Script Settings' tab (except for 'Manual 
Filepath' if you opted for the automatic detection) make your way to the 
'MDS Options' tab. This tab details some of the required information regarding the 
backend configuration files. For your first time I would recommend filling in all 
fields with the default recommended values. This should deliver a stock standard 
simulation for 10 ns. After this please move onto the 'Hardware Options' tab.

This section is dedicated to the hardware requested from your HPC system to run our
simulation. Please take this time to familiarise yourself with you HPC capabilities 
and limitations. Some of the sliders within this section may exceed the capabilities
of your HPC system and will result in failed jobs!
This section is rather self explanatory however please take note that requesting
many resources or expensive resources such as GPUs will result in longer job queue 
times on most HPC services. Also note that parallelisation performance is quite weak
on older GROMACS installations.

As mentioned earlier we will not worry with the 'Advanced Options' tab for now until
you are familiar with the basics of MDS and GROMACS. If you wish to learn more about
this and more later, please refer to the 'More Information" tab above these instructions.
You can now press the 'Generate Script' button, if everything goes well the newly
created window should close itself. If not, please address any of the error messages
generated and try again.

The final steps to get your simulation up and running will require a file transfer
service that can transfer files to your HPC such as 'FileZilla', please refer to 
your institutions ICT team for assistance in connecting to your HPC system.
Once connection is established you will be able to find your setup script inside
of the same install directory as this program in the folder labelled 'Script_Files'.
Inside this folder you should see a newly generated folder titled 
'MDS_<YOUR SCRIPT NAME>'. Please copy this entire folder onto the HPC as it also
contains the .pdb file that serves as the starting reference of the simulation.

You're nearly there!
Now you will need an SSH terminal service such as 'PuTTY' to connect to your HPC
service, this process should be similar to that of connecting the file transfer
tool in the prior step. Once connected, login and navigate into the directory
you copied the MDS folder to earlier. Once inside the MDS folder you will need
to load a python module of version 3.6 or later. Once complete simply type
'python <YOUR SCRIPT NAME>_Setup_Script.py'.
This should automatically generate several folders alongside a .pbs job
submission script. To begin your simulation simply queue the generated .pbs file
into your HPCs job submission system (e.g. 'qsub Gro_<YOUR SCRIPT NAME>.pbs').

Congratulations! You've now successfully created and submitted a Molecular
Dynamics Simulation!
Depending on your simulation size, duration and hardware the simulation runtime
will vary greatly. If you entered in your email in 'Script Options' you should now
receive an email when your simulation starts or ends.
Once you receive the completion email refer to the next tab 'Analysis'.
"""


Analysis_Instructions = """MDS Analysis:
This section outline the basics of using the MDS analysis component of MDSGAT. Please
note that this is not an in depth discussion on how to interpret any results but
instead a guide on how to generate them.
To begin your analysis you will need to utilise your file transfer program of choice
again, except this time you will be coping the 'Analysis' folder to anywhere on your PC.
This may take some time depending on the size and length of your simulation as these files
can grow to multiple gigabytes in size.

Now select the 'Analyse MDS' button on the main page of this program. Since you likely only
have one completed simulation we will stick with the 'Single MDS' option. 'Comparative MDS'
is very similar but will allow you to plot two  simulations together and compare
where they differ. Note 'Comparative MDS' is intended for comparison of the SAME structure
under different environmental circumstances (be it temperature, pressure, time, ect.) and
will likely not operate as intended otherwise!

First start by pressing the 'Select File' button and navigating to the 'Analysis' folder
you copied from your HPC system earlier. Note, feel free to rename this folder to something
more recognisable if desired. The checkboxes to the right of the 'Select File' button should
begin to be checked in as each of the simulation files is recognised, if any of these check
boxes are still empty please ensure that your analysis folder contains all the expected files
(PROD.xtc, PROD.gro and NPT.gro). After all the check boxes to the right are ticked, enter an
Entry Name; this will appear above any plots generated.

Next select the analysis methods you with to perform, be wary more analyses will take longer to
calculate, especially Principle Component Analysis (PCA). Other than PCA a number of common 
MDS analysis methods are present such as Root Mean Square Deviation (RMSD), Root Mean 
Square Fluctuation (RMSF) and Radius of Gyration (RoG).
Once all desired analyses are selected press the 'Analyse Results' button. Again depending on
the size and length of your simulation this can take a long time.
After analysis is complete you should be presented with a series of plots, take some time to
familiarise yourself with the controls at the bottom of the plots for additional options such as
image saving.

Congratulations! You have now successfully created, ran and analysed a Molecular Dynamics 
Simulation!"""