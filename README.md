# Sparky_to_CPMG_Fit
Converts SPARKY peaklist files to CPMG_Fit format

Modify adjustable parameters. 

1. peak_lists- This parameter is a list of strings containing all the peaklist files. ***Must be in order of increasing CPMG frequency***
The files must be strings (surrounded by quotation marks), and closed by brackets. I.E. ['file1.txt', 'file2.txt']
2. time_value- This is the t_value from the procpar file [float input]
3. error_min- The lowest possible error. Any relative error value that is below this, will be set to this value by default [float input]
4. time_zero- This is the very first spectra in the CPMG sequence, standard NHSQC [string input]
5. list_of_CPMG_frequencies- This is a list of the CPMG frequences. Like the peaklists, must be a list of strings (so closed by brackets, surrounded by quotations) I.E. ['0','25']
6. duplicate_frequences-The frequences that are duplicated. These will be used for errors, same format as peak_lists [list of strings]
7. temperature- Define temperature in C [string input]
8. spectrometer_frequency- The spectrometer frequency the experiments were run at [string input]
9. labeling- What atoms is the CPMG experiment on [stirng input]
10. identifier- The output files will be labeled per the labels in the peaklists. You may add an extra label via here [string input]
11. quantum_type- The type of CPMG experiment, this is for CPMG_Fit (e.g. single-quantum is S, double-quantum is D, etc.) [string input]
12. directory_pathway= The pathway your CPMG_Fit files will be created [string input]
13. font_size- The font size for the plot labels [intger input]
14. selective_group_file- If you wish to only generate CPMG_Fit files for specific residues, you may define them in a text file, with one column labeling the amino acid type, and residue number [string input]
I.E.
```
G34
Q55
A66
```
generate_plots (if set to True)- The program will generate sets of 16 plots for you to visualize the Reff plot to choice which amino acids you want to selectively run CPMG_Fit on. It will also display Rex and relative error %. If False, the program will not generate plots. 

generate_excel_output_file (if set to True)- The program will generate an output file containing the CPMG_Fit output files in a vertical column that can easily be plotted in excel (in case the user wishes to plot the Reff themselves)

selective_groups (if set to True)- The program will read a selective group file to only generate CPMG_Fit files for the amino acids specified in the file. 

***Recommended usage***
1. Change paremters to fit your experimental setup
2. Set generate_plots to True and selective_groups to False, set directory_pathway to 'data/all'
3. Check plots of all peaks, and pick the ones that appear to have good Rex
4. Create a txt file specifying these amino acids, then set selective_groups to True, set directory_pathway to 'data/selective' run program again
5. You now have CPMG_Fit files for all your amino acids, and the ones you selectively want to run
