import MDAnalysis as mda
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from MDAnalysis.analysis import rms, align, pca
from MDAnalysis.analysis.base import (AnalysisBase, AnalysisFromFunction, analysis_class)
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis as HBA
import warnings
import seaborn as sns
import csv
import shutil
import os
#import mdtraj - Disabled for application code due to causing issues during application packaging.



def ExecuteAnalysis(AnalysisList, Files, PlotCount):
    print("Beginning analysis...")

    if os.path.isdir("Temp_Data")!=True:
            os.makedirs('Temp_Data/')

    plotrows = -(-PlotCount // 2)
    if PlotCount>1:
        plotcolumns = 2
    else:
        plotcolumns = 1
    plotnumber = 1
    if "Single" in AnalysisList:
        if len(Files) != 4:
            print("Number of input files is incorrect!")
            print("Analysis is expecting 3 files...")
        else:
            print("Setting up analysis environemnt.\nThis may take some time...")
            start = Files["NPT.gro"]
            end = Files["PROD.gro"]
            traj = Files["PROD.xtc"]
            #MDTtraj = mdtraj.load(traj,top=start)
            MDAuniverse = mda.Universe(start,traj)
            print("Analysis environment successfully setup!")

            if "RMSD" in AnalysisList:
                print("Calculating RMSD, this may take some time...")
                rmsd = rms.RMSD(MDAuniverse, select="name CA")
                rmsd.run(verbose=True)
                print("RMSD calculated! Adding to plots.")
                RMSD_Time = rmsd.times
                RMSD_A = rmsd.results.rmsd[:,2]
                plt.subplot(plotrows,plotcolumns,plotnumber)
                plotnumber+=1
                plt.plot(RMSD_Time,RMSD_A)
                plt.xlabel("Time (ps)")
                plt.ylabel("RMSD ($\AA$)")
                plt.title(Files["Name"] + " RMSD")

            if "RMSF" in AnalysisList:
                print("Calculating RMSF, this may take some time...")
                RMSF_average = align.AverageStructure(MDAuniverse, MDAuniverse, select="protein and name CA", ref_frame=0).run()
                RMSF_ref = RMSF_average.results.universe
                RMSF_aligner = align.AlignTraj(MDAuniverse, RMSF_ref, select="protein and name CA", filename="Temp_Data/aligned_traj.dcd", in_memory=False).run()
                RMSF_u = mda.Universe(start, "Temp_Data/aligned_traj.dcd")
                RMSF_c_alphas = RMSF_u.select_atoms('protein and name CA')
                RMSF = rms.RMSF(RMSF_c_alphas).run()
                print("RMSF calculated! Adding to plots.")
                plt.subplot(plotrows,plotcolumns,plotnumber)
                plotnumber+=1

                plt.scatter(RMSF_c_alphas.resids, RMSF.results.rmsf)
                plt.xlabel("Residue Number")
                plt.ylabel("RMSF ($\AA$)")
                plt.title(Files["Name"] + " RMSF")

            if "RoG" in AnalysisList:
                print("Calculating Radii of Gyration, this may take some time...")
                protein = MDAuniverse.select_atoms('protein')
                rog = AnalysisFromFunction(radgyr, MDAuniverse.trajectory, protein, protein.masses, total_mass=np.sum(protein.masses))
                rog.run()

                plt.subplot(plotrows,plotcolumns,plotnumber)
                plotnumber+=1
                labels = ['all', 'x-axis', 'y-axis', 'z-axis']
                for col, label in zip(rog.results['timeseries'].T, labels):
                    plt.plot(col, label=label)
                print("Radii of Gyration complete! Adding to plots.")
                plt.legend()
                plt.ylabel('Radius of gyration (Å)')
                plt.xlabel('Frame')
                plt.title(Files["Name"] + " Radii of Gyration")

            if "PCA" in AnalysisList:
                print("Performing PCA, this can take a very long time...")
                aligner = align.AlignTraj(MDAuniverse, MDAuniverse, select="backbone", filename="Temp_Data/aligned_traj.dcd", in_memory=False).run()
                u = mda.Universe(start, "Temp_Data/aligned_traj.dcd")
                pc = pca.PCA(u, select="backbone", align=True, mean=None, n_components=None).run()
                backbone = u.select_atoms("backbone")
                n_bb = len(backbone)
                print(f"There are {n_bb} backbone atoms in the analysis")
                print(pc.p_components.shape)
                print(f"PC1: {pc.variance[0]:.5f}")
                for i in range(3):
                    print(f"Cumulated variance: {pc.cumulated_variance[i]:.3f}")

                print("PCA complete! Adding PCA summary to plots.")
                plt.plot(pc.cumulated_variance[:10])
                plt.xlabel('Principal component')
                plt.ylabel('Cumulative variance')
                plt.title(Files["Name"] + " PCA")

                print("Extracting PCA components, this can take some time...")
                transformed = pc.transform(backbone, n_components=3)
                transformed.shape
                df = pd.DataFrame(transformed,
                            columns=['PC{}'.format(i+1) for i in range(3)])
                df['Time (ps)'] = df.index * u.trajectory.dt
                df.head()
                print("Plotting PCA findings...")
                g = sns.PairGrid(df, hue='Time (ps)', palette=sns.color_palette('Oranges_d', n_colors=len(df)))
                g.map(plt.scatter, marker='.')
            
            if "H-Bonds" in  AnalysisList:
                print("Performing H-Bond analysis, this may take some time...")
                hbonds = HBA(MDAuniverse)
                hbonds.hydrogens_sel = hbonds.guess_hydrogens("protein")
                hbonds.acceptors_sel = hbonds.guess_acceptors("protein")

                #water_hydrogens_sel = "resname TIP3 and name H1 H2"
                #water_acceptors_sel = "resname TIP3 and name OH2"

                hbonds.run()

                plt.plot(pc.cumulated_variance[:10])
                plt.xlabel('Principal component')
                plt.ylabel('Cumulative variance')
                plt.title(Files["Name"] + " PCA")

            # See MDTraj Import Comment!
            """
            if "SASA" in AnalysisList:
                print("Performing Solvent Accessable Surface Area (SASA) analysis, this may take some time...")
                sasa = mdtraj.shrake_rupley(MDTtraj)
                total_sasa = sasa.sum(axis=1)

                plt.subplot(plotrows,plotcolumns,plotnumber)
                plotnumber+=1
                print("SASA complete! Adding to plots.")
                plt.plot(MDTtraj.time, total_sasa)
                plt.ylabel('Total SASA (nm)^2')
                plt.xlabel('Time (ps)')
                plt.title(Files["Name"] + " SASA")
            """



    elif "Comparative" in AnalysisList:
        if len(Files) != 8:
            print("Number of input files is incorrect!")
            print("Analysis is expecting 8 files...")
        else:
            print("Setting up analysis environemnt.\nThis may take some time...")
            start1 = Files["NPT1.gro"]
            end1 = Files["PROD1.gro"]
            traj1 = Files["PROD1.xtc"]
            start2 = Files["NPT2.gro"]
            end2 = Files["PROD2.gro"]
            traj2 = Files["PROD2.xtc"]
            MDAuniverse1 = mda.Universe(start1,traj1)
            MDAuniverse2 = mda.Universe(start2,traj2)

            print("Analysis environment successfully setup!")

            if "RMSD" in AnalysisList:
                print("Calculating RMSD, this may take some time...")
                rmsd1 = rms.RMSD(MDAuniverse1, select="name CA")
                rmsd1.run(verbose=True)
                RMSD_Time1 = rmsd1.times
                RMSD_A1 = rmsd1.results.rmsd[:,2]
                rmsd2 = rms.RMSD(MDAuniverse2, select="name CA")
                rmsd2.run(verbose=True)
                RMSD_Time2 = rmsd2.times
                RMSD_A2 = rmsd2.results.rmsd[:,2]
                print("RMSD calculated! Adding to plots.")
                for i in AnalysisList:
                    if i == "RMSD":
                        plt.subplot(plotrows,plotcolumns,plotnumber)
                        plotnumber+=1
                        plt.plot(RMSD_Time1,RMSD_A1)
                        plt.xlabel("Time (ps)")
                        plt.ylabel("RMSD ($\AA$)")
                        plt.title(Files["Name1"] + " RMSD")

                        plt.subplot(plotrows,plotcolumns,plotnumber)
                        plotnumber+=1
                        plt.plot(RMSD_Time2,RMSD_A2)
                        plt.xlabel("Time (ps)")
                        plt.ylabel("RMSD ($\AA$)")
                        plt.title(Files["Name2"] + " RMSD")
                    if i == "Comparative RMSD":
                        plt.subplot(plotrows,plotcolumns,plotnumber)
                        plotnumber+=1
                        plt.plot(RMSD_Time1,RMSD_A1,label=Files["Name1"])
                        plt.plot(RMSD_Time2,RMSD_A2,label=Files["Name2"])
                        plt.xlabel("Time (ps)")
                        plt.ylabel("RMSD ($\AA$)")
                        plt.legend()
                        plt.title(Files["Name1"] + " and " + Files["Name2"] + " RMSD")


            if "RMSF" in AnalysisList:
                print("Calculating RMSF, this may take some time...")
                RMSF_average1 = align.AverageStructure(MDAuniverse1, MDAuniverse1, select="protein and name CA", ref_frame=0).run()
                RMSF_ref1 = RMSF_average1.results.universe
                RMSF_aligner1 = align.AlignTraj(MDAuniverse1, RMSF_ref1, select="protein and name CA", filename="Temp_Data/aligned_traj1.dcd", in_memory=False).run()
                RMSF_u1 = mda.Universe(start1, "Temp_Data/aligned_traj1.dcd")
                RMSF_c_alphas1 = RMSF_u1.select_atoms('protein and name CA')
                RMSF1 = rms.RMSF(RMSF_c_alphas1).run()
                RMSF_average2 = align.AverageStructure(MDAuniverse2, MDAuniverse2, select="protein and name CA", ref_frame=0).run()
                RMSF_ref2 = RMSF_average2.results.universe
                RMSF_aligner2 = align.AlignTraj(MDAuniverse2, RMSF_ref2, select="protein and name CA", filename="Temp_Data/aligned_traj2.dcd", in_memory=False).run()
                RMSF_u2 = mda.Universe(start2, "Temp_Data/aligned_traj2.dcd")
                RMSF_c_alphas2 = RMSF_u2.select_atoms('protein and name CA')
                RMSF2 = rms.RMSF(RMSF_c_alphas2).run()
                print("RMSF calculated! Adding to plots.")
                for i in AnalysisList:
                    if i == "RMSF":
                        plt.subplot(plotrows,plotcolumns,plotnumber)
                        plotnumber+=1
                        plt.plot(RMSF_c_alphas1.resids, RMSF1.results.rmsf)
                        plt.xlabel("Residue Number")
                        plt.ylabel("RMSF ($\AA$)")
                        plt.title(Files["Name1"] + " RMSF")

                        plt.subplot(plotrows,plotcolumns,plotnumber)
                        plotnumber+=1
                        plt.plot(RMSF_c_alphas2.resids, RMSF2.results.rmsf)
                        plt.xlabel("Residue Number")
                        plt.ylabel("RMSF ($\AA$)")
                        plt.title(Files["Name2"] + " RMSF")
                    if i == "Comparative RMSF":
                        plt.subplot(plotrows,plotcolumns,plotnumber)
                        plotnumber+=1
                        plt.plot(RMSF_c_alphas1.resids, RMSF1.results.rmsf,label=Files["Name1"])
                        plt.plot(RMSF_c_alphas2.resids, RMSF2.results.rmsf,label=Files["Name2"])
                        plt.xlabel("Residue Number")
                        plt.ylabel("RMSF ($\AA$)")
                        plt.legend()
                        plt.title(Files["Name1"] + " and " + Files["Name2"] + " RMSF")

            if "RoG" in AnalysisList:
                print("Calculating Radii of Gyration, this may take some time...")
                protein1 = MDAuniverse1.select_atoms('protein')
                rog1 = AnalysisFromFunction(radgyr, MDAuniverse1.trajectory, protein1, protein1.masses, total_mass=np.sum(protein1.masses))
                rog1.run()
                labels1 = ['all', 'x-axis', 'y-axis', 'z-axis']
    
                protein2 = MDAuniverse2.select_atoms('protein')
                rog2 = AnalysisFromFunction(radgyr, MDAuniverse2.trajectory, protein2, protein2.masses, total_mass=np.sum(protein2.masses))
                rog2.run()
                labels2 = ['all', 'x-axis', 'y-axis', 'z-axis']
                for i in AnalysisList:
                    if i == "RoG":
                        plt.subplot(plotrows,plotcolumns,plotnumber)
                        plotnumber+=1
                        for col, label in zip(rog1.results['timeseries'].T, labels1):
                            plt.plot(col, label=label)
                        plt.legend()
                        plt.ylabel('Radius of gyration (Å)')
                        plt.xlabel('Frame')
                        plt.title(Files["Name1"] + " Radii of Gyration")

                        plt.subplot(plotrows,plotcolumns,plotnumber)
                        plotnumber+=1
                        for col, label in zip(rog2.results['timeseries'].T, labels2):
                            plt.plot(col, label=label)
                        print("Radii of Gyration complete! Adding to plots.")
                        plt.legend()
                        plt.ylabel('Radius of gyration (Å)')
                        plt.xlabel('Frame')
                        plt.title(Files["Name2"] + " Radii of Gyration")

                    if i == "Comparative RoG":
                        plt.subplot(plotrows,plotcolumns,plotnumber)
                        plotnumber+=1
                        for col, label in zip(rog1.results['timeseries'].T, labels1):
                            plt.plot(col, label=label)
                        for col, label in zip(rog2.results['timeseries'].T, labels2):
                            plt.plot(col, label=label)
                        plt.legend()
                        plt.ylabel('Radius of gyration (Å)')
                        plt.xlabel('Frame')
                        plt.title(Files["Name1"] + " and " + Files["Name2"] + " Radii of Gyration")
                    

            if "PCA" in AnalysisList:
                print("Performing PCA, this can take a very long time...")
                aligner1 = align.AlignTraj(MDAuniverse1, MDAuniverse1, select="backbone", filename="Temp_Data/aligned_traj1.dcd", in_memory=False).run()
                u1 = mda.Universe(start1, "Temp_Data/aligned_traj1.dcd")
                pc1 = pca.PCA(u1, select="backbone", align=True, mean=None, n_components=None).run()
                backbone1 = u1.select_atoms("backbone")
                n_bb1 = len(backbone)
                print(f"There are {n_bb1} backbone atoms in the analysis")
                print(pc.p_components.shape)
                print(f"PC1: {pc1.variance[0]:.5f}")
                for i in range(3):
                    print(f"Cumulated variance: {pc1.cumulated_variance[i]:.3f}")

                print("PCA complete! Adding PCA summary to plots.")
                plt.subplot(plotrows,plotcolumns,plotnumber)
                plotnumber+=1
                plt.plot(pc1.cumulated_variance[:10])
                plt.xlabel('Principal component')
                plt.ylabel('Cumulative variance')
                plt.title(Files["Name1"] + " PCA")

                print("Extracting PCA components, this can take some time...")
                transformed1 = pc1.transform(backbone1, n_components=3)
                transformed1.shape
                df1 = pd.DataFrame(transformed1,
                            columns1=['PC{}'.format(i+1) for i in range(3)])
                df1['Time (ps)'] = df1.index * u1.trajectory.dt
                df1.head()
                print("Plotting PCA findings...")
                plt.subplot(plotrows,plotcolumns,plotnumber)
                plotnumber+=1
                g1 = sns.PairGrid(df1, hue='Time (ps)', palette=sns.color_palette('Oranges_d', n_colors=len(df1)))
                g1.map(plt.scatter, marker='.')



                aligner2 = align.AlignTraj(MDAuniverse2, MDAuniverse2, select="backbone", filename="Temp_Data/aligned_traj2.dcd", in_memory=False).run()
                u2 = mda.Universe(start2, "Temp_Data/aligned_traj2.dcd")
                pc2 = pca.PCA(u2, select="backbone", align=True, mean=None, n_components=None).run()
                backbone2 = u2.select_atoms("backbone")
                n_bb2 = len(backbone)
                print(f"There are {n_bb2} backbone atoms in the analysis")
                print(pc.p_components.shape)
                print(f"PC2: {pc2.variance[0]:.5f}")
                for i in range(3):
                    print(f"Cumulated variance: {pc2.cumulated_variance[i]:.3f}")

                print("PCA complete! Adding PCA summary to plots.")
                plt.subplot(plotrows,plotcolumns,plotnumber)
                plotnumber+=1
                plt.plot(pc2.cumulated_variance[:10])
                plt.xlabel('Principal component')
                plt.ylabel('Cumulative variance')
                plt.title(Files["Name2"] + " PCA")

                print("Extracting PCA components, this can take some time...")
                transformed2 = pc2.transform(backbone2, n_components=3)
                transformed2.shape
                df2 = pd.DataFrame(transformed2,
                            columns2=['PC{}'.format(i+1) for i in range(3)])
                df2['Time (ps)'] = df2.index * u2.trajectory.dt
                df2.head()
                print("Plotting PCA findings...")
                plt.subplot(plotrows,plotcolumns,plotnumber)
                plotnumber+=1
                g2 = sns.PairGrid(df2, hue='Time (ps)', palette=sns.color_palette('Oranges_d', n_colors=len(df2)))
                g1.map(plt.scatter, marker='.')
            


    plt.show()
    return








def radgyr(atomgroup, masses, total_mass=None):
    # coordinates change for each frame
    coordinates = atomgroup.positions
    center_of_mass = atomgroup.center_of_mass()

    # get squared distance from center
    ri_sq = (coordinates-center_of_mass)**2
    # sum the unweighted positions
    sq = np.sum(ri_sq, axis=1)
    sq_x = np.sum(ri_sq[:,[1,2]], axis=1) # sum over y and z
    sq_y = np.sum(ri_sq[:,[0,2]], axis=1) # sum over x and z
    sq_z = np.sum(ri_sq[:,[0,1]], axis=1) # sum over x and y

    # make into array
    sq_rs = np.array([sq, sq_x, sq_y, sq_z])

    # weight positions
    rog_sq = np.sum(masses*sq_rs, axis=1)/total_mass
    # square root and return
    return np.sqrt(rog_sq)


'''
TestAnalysisList = ["Single", "RMSD"]
TestFileList = {"NPT.gro":"GlyG1_Single_295K_NPT.gro",
                "PROD.gro":"GlyG1_Single_295K_PROD.gro",
                "PROD.xtc":"GlyG1_Single_295K_PROD.xtc"}
TestPlotCount = 1
ExecuteAnalysis(TestAnalysisList, TestFileList, TestPlotCount)
'''