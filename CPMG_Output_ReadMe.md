Plots output files from CPMG_Fit

***Parameters***

1. plot_cpmg_fit (if True) - Plots the calculated CPMG_Fit and the experimental data and calculates the R2 (16 amino acids at a time). 
  a) Residue (if True)- Displays the residue number on the plot title
  b) Temperature (if True)- Display the temperature the experiment was run at
  c) Spectrometer_frequency (if True)- Displays the spectrometer frequency 
  d) Atom_Coherence (if True)- Displays Quantum Coherence type
  e) fontsize- font size for plot label
 
2. plot_csb (if True) - Generates a plot of the CS_B for each amino acid (with averages and upper standard deviation)
  a) outlier_removed_percent - The standard deviation will exclude amino acids that are outside a particular value in its average and standard deviation calculation (default is 10%, to change to say 20%, you'd do 1.2). 
  b) show_values_above_std (if True) - Displays CS_B values that are outside the upper standard deviation (and their errors)
 
3. write_cs_b_only_file (if True) - Generates a text file with only the CS_B values in a column (for pymol b factor plotting)

4. plot_csb_on_pdb (if True) - B factor plots the CS_B values
  a) pdb_file - The pdb file to use
  b) startaa- Start of the amino acid in the CPMG_Output file
