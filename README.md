# MDSGAT_Public
The Molecular Dynamics Script Generator and Analysis Tool (MDSGAT) is a Molecular Dynamics Simulation (MDS) assistance tool that brings the ability to both configure and analyse MDS projects on the users local machine.


# Capability
Currently the MDSGAT Program is designed to be used with the GROMACS simulation environment and is configured for use with organic macromolecules (proteins). Although the default configurations are all available to the user and as such may be possible to use under various circumstances.

# Script Generator
As mentioned above the MDSGAT program develops scripts for use with the GROMACS simulation suite and formats this script in the form of a PBS job submission script for use with HPC systems, this being said generating a script to run locally is as simple and removing the PBS arguments at the top of the generated script.

# Analysis
MDSGAT utilises both MDAnalysis and MDTraj libraries for its analysis methods and is expandable using such libraries. Currently implemented methods are: RMSD, RMSF, Radii of gyration, PCA and SASA but is currently under review for expansion.

# Purpose of MDSGAT
MDSGAT was developed out of the frustration of requiring external services/hosts to have a good, simple MDS experience without any uneccessary overcomplicated or repetitive configuration and as such the current and future purpose of MDSGAT is to empower a broader range of experts with certain locally owned and ran MDS tools.
