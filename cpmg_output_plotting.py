import matplotlib.pyplot as plt
import math


"""Display Label"""
Residue=True
Temperature=True
spectrometer_frequency=True
Atom_Coherence=False
font_size=8

"""For pdb plotting"""
pdb_file=''
startaa=''

outlier_removed_percent=1.1

write_cs_b_only_file=True

plot_cpmg_fits=False
plot_csb=True
plot_csb_on_pdb=False
show_values_above_std=True

cval_file='full.dat'
cs_file='full.res'

def display_toggle(label_list):
    display_list=[]
    display=label_list[0].split()
    if Residue is True:
        display_list.append(display[0])
    if Atom_Coherence is True:
        display_list.append(display[1])
    if spectrometer_frequency is True:
        display_list.append(display[2])
    if Temperature is True:
        display_list.append(display[3])
    return display_list

def plot_cpmg_fit():
    cpfrq_list=[]
    experimental_value_list=[]
    expected_value_list=[]
    error_list=[]
    label_list=[]
    unexplained_variance_list=[]
    total_variance_list=[]
    counter=0
    plot_counter_rows=-1
    plot_counter_columns=0
    with open(cval_file) as output_file:
        fig,axs=plt.subplots(4,4)
        for lines in output_file:
            if lines.split() == []:
                continue
            if lines.split()[0] == '#':
                continue
            counter+=1
            label=' '.join(lines.split()[0:5])
            if counter == 1:
                label_list.append(label)
            else:
                if label not in label_list:
                    plot_counter_rows+=1
                    if plot_counter_rows == 4:
                        plot_counter_columns+=1
                        plot_counter_rows=0
                    if plot_counter_columns == 4:
                        fig.tight_layout()
                        plt.show()
                        fig,axs=plt.subplots(4,4)
                        plot_counter_rows=0
                        plot_counter_columns=0
                    for exp_values,calc_values,error_values in zip(experimental_value_list,expected_value_list,error_list):
                        average=sum(expected_value_list)/len(expected_value_list)
                        squares_sum=((exp_values-calc_values)**2)
                        total_variance=math.sqrt((average-exp_values)**2)
                        unexplained_variance_list.append(squares_sum)
                        total_variance_list.append(total_variance)
                    display=display_toggle(label_list)
                    unexplained_variance=sum(unexplained_variance_list)
                    total_variation=sum(total_variance_list)
                    R2=1-(unexplained_variance/total_variation)
                    axs[plot_counter_rows,plot_counter_columns].plot(cpfrq_list,experimental_value_list)
                    axs[plot_counter_rows,plot_counter_columns].plot(cpfrq_list,expected_value_list)
                    axs[plot_counter_rows,plot_counter_columns].set_title(f'{" ".join(display)} R2: {"{:.2f}".format(R2)}' )
                    cpfrq_list.clear()
                    experimental_value_list.clear()
                    error_list.clear()
                    expected_value_list.clear()
                    label_list.clear()
                    total_variance_list.clear()
                    unexplained_variance_list.clear()
            label_list.append(label)
            cpfrq=float(lines.split()[6])
            experimental_value=float(lines.split()[7])
            error=float(lines.split()[8])
            calculated_value=float(lines.split()[9])
            cpfrq_list.append(cpfrq)
            experimental_value_list.append(experimental_value)
            error_list.append(error)
            expected_value_list.append(calculated_value)
        for exp_values,calc_values,error_values in zip(experimental_value_list,expected_value_list,error_list):
            average=sum(expected_value_list)/len(expected_value_list)
            squares_sum=((exp_values-calc_values)**2)
            total_variance=math.sqrt((average-exp_values)**2)
            unexplained_variance_list.append(squares_sum)
            total_variance_list.append(total_variance)
        if plot_counter_columns == 4 and plot_counter_rows == 4:
            fig.tight_layout()
            plt.show()
            fig,axs=plt.subplots(4,4)
            plot_counter_rows=0
            plot_counter_columns=0
        elif plot_counter_rows == 4:
            plot_counter_columns+=1
            plot_counter_rows=0
        else:
            plot_counter_rows+=1
        display=display_toggle(label_list)
        unexplained_variance=sum(unexplained_variance_list)
        total_variation=sum(total_variance_list)
        R2=1-(unexplained_variance/total_variation)
        axs[plot_counter_rows,plot_counter_columns].plot(cpfrq_list,experimental_value_list)
        axs[plot_counter_rows,plot_counter_columns].plot(cpfrq_list,expected_value_list)
        axs[plot_counter_rows,plot_counter_columns].set_title(f'{" ".join(display)} R2: {"{:.2f}".format(R2)}' )
    fig.tight_layout()
    plt.show()

def obtain_csb():
    with open(cs_file) as output_file:
        only_cs_b=[]
        for lines in output_file:
            if lines.split() == []:
                continue
            if lines.split()[0] == 'CS0_B:':
                only_cs_b.append(lines.strip())
        if write_cs_b_only_file is True:
            with open('cs_b_only.txt','w') as cs_b_file:
                for entries in only_cs_b:
                    cs_b_file.write(entries.strip().split()[4]+'\n')
        return only_cs_b

def average_and_std(average_list):
    standard_deviation_list=[]
    sum_average=sum(average_list)/len(average_list)
    for values in average_list:
        deviation=((float(values)-sum_average)**2)+((float(values)-sum_average)**2)
        standard_deviation_list.append(deviation)
    standard_deviation=math.sqrt(sum(standard_deviation_list)/len(standard_deviation_list))
    std_up=sum_average+standard_deviation
    std_down=sum_average-standard_deviation
    outliers_removed_average_list=[]
    outliers_removed_standard_deviation_list=[]
    for averages in average_list:
        if averages < (std_up*outlier_removed_percent) and averages > (std_down*outlier_removed_percent):
            outliers_removed_average_list.append(averages)
    outliers_removed_sum_average=sum(outliers_removed_average_list)/len(outliers_removed_average_list)
    for new_averages in outliers_removed_average_list:
        new_deviation=((float(new_averages)-outliers_removed_sum_average)**2)+((float(new_averages)-outliers_removed_sum_average)**2)
        outliers_removed_standard_deviation_list.append(new_deviation)
    outliers_removed_standard_deviation=math.sqrt(sum(outliers_removed_standard_deviation_list)/len(outliers_removed_standard_deviation_list))
    outliers_removed_std_up=outliers_removed_sum_average+outliers_removed_standard_deviation
    return outliers_removed_sum_average, outliers_removed_std_up

def csb_plot():
    cs_b=obtain_csb()
    amino_acid=[]
    cs=[]
    error=[]
    for lines in cs_b:
        amino_acid.append(lines.split()[1])
        cs.append(float(lines.split()[4]))
        error.append(float(lines.split()[5]))
    x_axis=[]
    y_axis=[]
    error_bars=[]
    for x_values,y_values,error_values in zip(amino_acid,cs,error):
        if y_values < 0 or y_values == -0.0:
            y_values=0.0
            error_values=0.0
        if error_values > (max(cs)*2):
            y_values=0.0
            error_values=0.0
        x_axis.append(x_values)
        y_axis.append(y_values)
        error_bars.append(error_values)
    sum_average,std_up=average_and_std(y_axis)
    if show_values_above_std is True:
        print('Res','CS-B','Error')
        for label,values,err in zip (x_axis,y_axis,error_bars):
            if values > std_up:
                print(label,values,err)
    plt.plot(x_axis,[sum_average]*len(x_axis),color='r')
    plt.plot(x_axis,[std_up]*len(x_axis),color='g')
    plt.bar(x_axis,y_axis,yerr=error_bars)
    plt.show()

def pymol_csb():
    csb_only=[]
    cs_b=obtain_csb()
    pymol.finish_launching()
    mol=pdb_file[0:-4]
    for lines in csb_only:
        csb_only.append(lines.strip().split()[4])
    obj=cmd.get_object_list(mol)
    cmd.alter(mol,"b=-1.0")
    counter=int(startaa)
    bfacts=[]
    for line in csb_only:
        bfact=float(line)
        bfacts.append(bfact)
        cmd.alter("%s and resi %s and n. CA"%(mol,counter), "b=%s"%bfact)
        counter=counter+1
        cmd.cartoon("automatic",mol)
        cmd.spectrum("b","grey blue red", "%s and n. CA " %mol)
        cmd.recolor()

def main():
    if plot_cpmg_fits is True:
        plot_cpmg_fit()
    if plot_csb is True:
        csb_plot()
    if plot_csb_on_pdb is True:
        pymol_csb()

main()
