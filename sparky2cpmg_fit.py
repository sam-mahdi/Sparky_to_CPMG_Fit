import math
import re
import os
import shutil


"""Adjustable Parameters"""

peak_lists=['RING_CPMG_v0.list','RING_CPMG_v25.list','RING_CPMG_v50a.list','RING_CPMG_v50b.list','RING_CPMG_v75.list','RING_CPMG_v100.list','RING_CPMG_v150.list','RING_CPMG_v200.list','RING_CPMG_v300.list','RING_CPMG_v400.list','RING_CPMG_v500a.list','RING_CPMG_v500b.list','RING_CPMG_v600.list','RING_CPMG_v700.list','RING_CPMG_v800.list','RING_CPMG_v900.list','RING_CPMG_v1000.list']
time_value=0.04
error_min=0.04
time_zero='RING_CPMG_v0.list'
list_of_CPMG_frequencies=['0','25','50','50','75','100','150','200','300','400','500','500','600','700','800','900','1000']
duplicate_frequencies=['50','500']
temperature='25'
spectrometer_frequency='500'
labeling='N15'
identifier='Thomas'
quantum_type='S'
directory_pathway='data/all'
font_size=8
selective_group_file='selective_groups.txt'
outlier_removed_percent=1.1
rex_reff_plot_xaxis_label_fontsize=6

generate_plots=False
generate_excel_output_file=False
selective_groups=False
recommended_peaks=True
only_show_good_reff_and_rex=True
plot_rex_reff=False
generate_excel__rex_reff_plot_file=True

axis_labels_flag=True
plot_size=(12,12)
x_axis_fontsize=12
y_axis_fontsize=14
x_ticker_fontsize=10
y_ticker_fontsize=10
x_ticker_interval=200
y_ticker_interval=1

custom_plot_flag=True

"""SCRIPT START"""


def create_peaklist():
    """Creates the peaklist to be used to organize peak height list"""
    list_of_peaks=[]
    with open(time_zero) as peaklist_file:
        for lines in peaklist_file:
            if lines.split() == []:
                continue
            if lines.split()[0] == 'Assignment':
                continue
            label=lines.split()[0]
            list_of_peaks.append(label)
    return list_of_peaks

def organize_peak_heights():
    """Create a list of lists of peakheights compiled from each peaklist"""
    temp_peak_height_list=[]
    peak_height_list=[]
    for peaks in list_of_peaks:
        for peaklists in peak_lists:
            with open(peaklists) as peaklist_file:
                for lines in peaklist_file:
                    if lines.split() == []:
                        continue
                    if lines.split()[0] == 'Assignment':
                        continue
                    label=lines.split()[0]
                    peak_heights=lines.split()[3]
                    if peaks == label:
                        temp_peak_height_list.append(peak_heights)
                        break
        peak_height_list.append([' '.join(temp_peak_height_list)])
        temp_peak_height_list.clear()
    return peak_height_list



def create_rex():
    """Generate Rex value from peak heights"""
    counter=0
    first_value=0
    temp_rex=[]
    rex=[]
    for lines in peak_height_list:
        skip_flag=False
        for next_line in lines:
            for heights in next_line.split():
                counter+=1
                if counter == 1:
                    first_value+=float(heights)
                    if first_value < 0:
                        first_value = 1
                if float(heights) < 0:
                    heights = 1
                exchange_formula=-(1/time_value)*math.log(float(heights)/first_value)
                if float(heights) < 0:
                    exchange_formula=0
                temp_rex.append(str(exchange_formula))
        if skip_flag is True:
            rex.append([' '.join(['1']*len(list_of_CPMG_frequencies))])
        else:    
            rex.append([' '.join(temp_rex)])
        temp_rex.clear()
        counter=0
        first_value=0
    return rex


def create_errors():
    """error values are created by comparing the relative error (which is just the average/standard deviation of duplicate freq runs) with a user standard value. The relative errors are added for multiple duplicate frequencies.
    These are then added to the rex value"""
    temp_rex_error_list=[]
    rex_error_list=[]
    rel_error_for_plotting=[]
    for values in rex:
        for lines in values:
            dup_list=[]
            for duplicates in duplicate_frequencies:
                dup_index=[i for i, x in enumerate(list_of_CPMG_frequencies) if x == duplicates]
                duplicate_1_index=dup_index[0]
                duplicate_2_index=dup_index[1]
                average=(float(lines.split()[duplicate_1_index])+float(lines.split()[duplicate_2_index]))/2
                standard_deviation=math.sqrt((((float(lines.split()[duplicate_1_index])-average)**2)+((float(lines.split()[duplicate_2_index])-average)**2))/2)
                rel_error=standard_deviation/average
                dup_list.append(rel_error)
            avg_rel_error=sum(dup_list)/len(dup_list)
            if avg_rel_error < error_min:
                error=error_min
            else:
                error=avg_rel_error
            for rex_values in lines.split():
                rex_error=abs(float(rex_values)*error)
                temp_rex_error_list.append(str(rex_error))
        rel_error_for_plotting.append(error)
        rex_error_list.append([' '.join(temp_rex_error_list)])
        temp_rex_error_list.clear()
    return rex_error_list,rel_error_for_plotting



def duplicate_rex_combined():
    """The rex values from the repeated frequencies are combined"""
    new_rex=[]
    for values in rex:
        for lines in values:
            new_list=lines.split()
            counter=-1
            for duplicates in duplicate_frequencies:
                counter+=1
                dup_index=[i for i, x in enumerate(list_of_CPMG_frequencies) if x == duplicates]
                duplicate_1_index=dup_index[0]+counter
                duplicate_2_index=dup_index[1]+counter
                average=(float(lines.split()[duplicate_1_index])+float(lines.split()[duplicate_2_index]))/2
                new_list[duplicate_1_index]=average
                del new_list[duplicate_2_index]
            del new_list[0]
        new_rex.append(new_list)
    return new_rex


def duplicate_errors_combined():
    """The error values from the repeated frequencies are combined"""
    new_errors=[]
    for values in errors:
        for lines in values:
            new_list=lines.split()
            counter=-1
            for duplicates in duplicate_frequencies:
                counter+=1
                dup_index=[i for i, x in enumerate(list_of_CPMG_frequencies) if x == duplicates]
                duplicate_1_index=dup_index[0]+counter
                duplicate_2_index=dup_index[1]+counter
                average=(float(lines.split()[duplicate_1_index])+float(lines.split()[duplicate_2_index]))/2
                new_list[duplicate_1_index]=average
                del new_list[duplicate_2_index]
            del new_list[0]
        new_errors.append(new_list)
    return new_errors


def modify_frequency_list():
    global list_of_CPMG_frequencies
    """Remove 0 frequency, since its not needed in cpmg_fit, and remove duplicates since their values were average)"""
    del list_of_CPMG_frequencies[0]
    for values in list_of_CPMG_frequencies:
        if values in duplicate_frequencies:
            del list_of_CPMG_frequencies[list_of_CPMG_frequencies.index(values)]

def create_cpmg_fit_peaklist_files():
    """Creates CPMG Fit files for each amino acid"""
    if os.path.isdir(working_directory+'/'+directory_pathway) is True:
        shutil.rmtree(working_directory+'/'+directory_pathway)
    os.makedirs(working_directory+'/'+directory_pathway)
    os.chdir(working_directory+'/'+directory_pathway)
    for peaks,rex_values,error_values,rel_error in zip(list_of_peaks,duplicate_rex,duplicate_errors,rel_error_for_plotting):
        with open(peaks+'_'+identifier+'.txt','w') as CPMG_peaklist_files:
            reff="{:.2f}".format([float(i) for i in rex_values][0]-[float(i) for i in rex_values][-1])
            CPMG_peaklist_files.write(f'#{peaks} Rex: {reff} Rel Error: {rel_error}\n')
            for rex_line,error_line,frequency in zip(rex_values,error_values,list_of_CPMG_frequencies):
                CPMG_peaklist_files.write(f'{frequency}\t{rex_line}\t{error_line}\n')
def create_cpmg_fit_input_file():
    """Creates the input file used for CPMG_fit"""
    os.chdir(working_directory)
    with open('cpmg_fit_input.txt','w') as cpmg_input:
        for peaks in list_of_peaks:
            residue=re.search('\d+',peaks)
            cpmg_input.write(f'read {directory_pathway}/{peaks}_{identifier}.txt d {residue.group(0)} {quantum_type} {labeling} {temperature} {spectrometer_frequency} {time_value} @ c\n')
        cpmg_input.write(f'\nset m 3\nset k @ 0 500 u\nset k @ 1 0 f\nset k @ 2 0 f\nset p @ 0 0.98 f\nset p @ 1 0.02 u\nset c @ {labeling} 0 0 0 f\nset c @ {labeling} 1 0 1.0 u\nset c @ {labeling} 2 0 0 f\nset r @ @ @ @ @ @ 10 u g\nwrite > p\n min\nwrite > p\n write full.res p\n write full.dat d\n backup full.bk\n')

"""plotting"""
selective_list=[]

def plot_data():
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.optimize import curve_fit
    plt.rc('font', size=font_size)
    counter=-1
    counter2=0
    counter3=0
    fig,axs=plt.subplots(4,4, figsize=plot_size)
    for rex_values,labels,error_values,data_error in zip(duplicate_rex,list_of_peaks,rel_error_for_plotting,duplicate_errors):
        if selective_group_plot is True:
            label_search=re.search('[A-Z]\d+[A-Z]*\d*-*[A-Z]*\d*',labels)
            if label_search is not None:
                if label_search.group(0) not in selective_list:
                    continue
        counter3+=1
        counter+=1
        if counter3 == 17:
            fig.tight_layout()
            plt.show()
            fig,axs=plt.subplots(4,4,figsize=plot_size)
            counter=0
            counter2=0
            counter3=1
        reff="{:.2f}".format([float(i) for i in rex_values][0]-[float(i) for i in rex_values][-1])
        error_plot=int(error_values*100)
        x_axis=[float(i) for i in list_of_CPMG_frequencies]
        y_axis=[float(i) for i in rex_values]
        error_bars=[float(i) for i in data_error]
        if custom_plot_flag is True:
            #axs[counter,counter2].plot(x_axis,y_axis,linestyle=':',color='blue')
            axs[counter,counter2].plot(x_axis,y_axis,linestyle='',marker='o',color='red')
            axs[counter,counter2].errorbar(x_axis,y_axis,yerr=error_bars,linestyle='')
            axs[counter,counter2].plot(x_axis,np.poly1d(np.polyfit(np.array(x_axis),np.array(y_axis),2))(np.array(x_axis)),color='orange',linestyle='-')

        else:
            axs[counter,counter2].plot(x_axis,y_axis)
        axs[counter,counter2].set_title(f'{labels} Rex: {reff}\u00B1{error_plot}%')
        if custom_plot_flag is True:
            if axis_labels_flag is True:
                axs[counter,counter2].set_xlabel('ν$_{CPMG}$ [HZ]',fontsize=x_axis_fontsize)
                axs[counter,counter2].set_ylabel('R$_{2,eff}$ [$s^{-1}$]',fontsize=y_axis_fontsize)
            axs[counter,counter2].tick_params(axis='x',labelsize=x_ticker_fontsize)
            axs[counter,counter2].tick_params(axis='y',labelsize=y_ticker_fontsize)
            #axs[counter,counter2].set_xticks((np.arange(min(x_axis),max(x_axis),x_ticker_interval)))
            #axs[counter,counter2].set_yticks((np.arange(min(y_axis),max(y_axis),y_ticker_interval)))
        if counter == 3:
            counter=-1
            counter2+=1
    fig.tight_layout()
    plt.show()

def generate_for_excel_plotting():
    import glob
    os.chdir(working_directory+'/'+directory_pathway)
    cpmg_fit_peaklist_files=glob.glob('*.txt')
    with open('excel_file_for_plotting.txt','w') as excel_file:
        for files in cpmg_fit_peaklist_files:
            with open(files) as infile:
                excel_file.write(infile.read())

def selective_generator():
    global selective_list
    if os.path.isdir(working_directory+'/'+directory_pathway) is True:
        shutil.rmtree(working_directory+'/'+directory_pathway)
    os.makedirs(working_directory+'/'+directory_pathway)
    with open(selective_group_file) as file:
        for lines in file:
            if lines.split() == []:
                continue
            selective_list.append(lines.strip())
    os.chdir(working_directory+'/'+directory_pathway)
    for peaks,rex_values,error_values,rel_error in zip(list_of_peaks,duplicate_rex,duplicate_errors,rel_error_for_plotting):
        residue_search=re.search('[A-Z]\d+[A-Z]*\d*-*[A-Z]*\d*',peaks)
        if residue_search.group(0) in selective_list:
            with open(peaks+'_'+identifier+'.txt','w') as CPMG_peaklist_files:
                reff="{:.2f}".format([float(i) for i in rex_values][0]-[float(i) for i in rex_values][-1])
                CPMG_peaklist_files.write(f'#{peaks} Rex: {reff} Rel Error: {rel_error}\n')
                for rex_line,error_line,frequency in zip(rex_values,error_values,list_of_CPMG_frequencies):
                    CPMG_peaklist_files.write(f'{frequency}\t{rex_line}\t{error_line}\n')
    os.chdir(working_directory)
    with open('cpmg_fit_selective_input.txt','w') as cpmg_input:
        for peaks in list_of_peaks:
            residue=re.search('\d+',peaks)
            residue_search=re.search('[A-Z]\d+[A-Z]*\d*-*[A-Z]*\d*',peaks)
            if residue_search.group(0) in selective_list:
                cpmg_input.write(f'read {directory_pathway}/{peaks}_{identifier}.txt d {residue.group(0)} {quantum_type} {labeling} {temperature} {spectrometer_frequency} {time_value} @ c\n')
        cpmg_input.write(f'\nset m 3\nset k @ 0 500 u\nset k @ 1 0 f\nset k @ 2 0 f\nset p @ 0 0.98 f\nset p @ 1 0.02 u\nset c @ {labeling} 0 0 0 f\nset c @ {labeling} 1 0 1.0 u\nset c @ {labeling} 2 0 0 f\nset r @ @ @ @ @ @ 10 u g\nwrite > p\n min\nwrite > p\n write full.res p\n write full.dat d\n backup full.bk\n')


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


def smart_peak_picking():
    filtered_rex=[]
    average_list=[]
    for rex_values in duplicate_rex:
        average_rex=sum([float(i) for i in rex_values])/len(rex_values)
        average_list.append(average_rex)
    outliers_removed_sum_average,outliers_removed_std_up=average_and_std(average_list)
    for rex_values2,peaks in zip(duplicate_rex,list_of_peaks):
        average_rex=sum([float(i) for i in rex_values2])/len(rex_values2)
        if average_rex > outliers_removed_std_up:
            filtered_rex.append(f'{peaks} {average_rex}')
            if only_show_good_reff_and_rex is False:
                print('Good Reff',peaks,average_rex)
    return filtered_rex,average_list,outliers_removed_sum_average,outliers_removed_std_up

def smart_peak_picking_reff():
    filtered_reff_list=[]
    reff_list=[]
    for rex_values in duplicate_rex:
        reff=[float(i) for i in rex_values][0]-[float(i) for i in rex_values][-1]
        reff_list.append(reff)
    outliers_removed_sum_average,outliers_removed_std_up=average_and_std(reff_list)
    for rex_values2,peaks in zip(duplicate_rex,list_of_peaks):
        filtered_reff=[float(i) for i in rex_values2][0]-[float(i) for i in rex_values2][-1]
        if filtered_reff > outliers_removed_std_up:
            filtered_reff_list.append(f'{peaks} {filtered_reff}')
            if only_show_good_reff_and_rex is False:
                print('Good Rex',peaks,filtered_reff)
    return filtered_reff_list,reff_list,outliers_removed_sum_average,outliers_removed_std_up

def plot_rex_reff_bar_graph(rex_list,reff_list,average_rex,rex_std_up,average_reff,reff_std_up):
    import matplotlib.pyplot as plt
    label_list=[]
    for labels in list_of_peaks:
        residue_search=re.search('\d+',labels)
        label_list.append(residue_search.group(0))
    fig,(ax1,ax2) = plt.subplots(1,2)
    ax1.bar(label_list,rex_list,width=0.3)
    ax1.set_title('Reff Plot')
    ax1.plot(label_list,[average_rex]*len(label_list),color='r',label='average')
    ax1.plot(label_list,[rex_std_up]*len(label_list),color='g',label='standard_deviation')
    ax2.bar(label_list,reff_list,width=0.3)
    ax2.plot(label_list,[average_reff]*len(label_list),color='r',label='average')
    ax2.plot(label_list,[reff_std_up]*len(label_list),color='g',label='standard_deviation')
    ax2.set_title('Rex Plot')
    ax1.legend(loc='upper right')
    ax2.legend(loc='upper right')
    ax1.tick_params(axis='x',labelsize=rex_reff_plot_xaxis_label_fontsize)
    ax2.tick_params(axis='x',labelsize=rex_reff_plot_xaxis_label_fontsize)
    plt.show()

def rex_reff_excel_file(rex_list,reff_list,average_rex,rex_std_up,average_reff,reff_std_up):
    with open('rex_reff_plot_output.txt','w') as output_file:
        output_file.write(f'Amino Acid\tReff\tReff Average\tReff Upper Stdev\tAmino Acid\tRex\tRex Average\tRex Upper Stdev\n')
        for labels,rex_values,reff_values,rex_average,std_up_rex,reff_average,std_up_reff in zip(list_of_peaks,rex_list,reff_list,[average_rex]*len(rex_list),[rex_std_up]*len(rex_list),[average_reff]*len(reff_list),[reff_std_up]*len(reff_list)):
            output_file.write(f'{labels}\t{rex_values}\t{rex_average}\t{std_up_rex}\t{labels}\t{reff_values}\t{reff_average}\t{std_up_reff}\n')


working_directory=os.getcwd()
list_of_peaks=create_peaklist()
peak_height_list=organize_peak_heights()
rex=create_rex()
errors,rel_error_for_plotting=create_errors()
duplicate_rex=duplicate_rex_combined()
duplicate_errors=duplicate_errors_combined()
modify_frequency_list()
if recommended_peaks is True:
    filtered_rex,rex_list,average_rex,rex_std_up=smart_peak_picking()
    filtered_reff,reff_list,average_reff,reff_std_up=smart_peak_picking_reff()
    for values in filtered_rex:
        for values2 in filtered_reff:
            if values.split()[0] == values2.split()[0]:
                print(f'Good Reff {values} and Rex {values2}')
    if plot_rex_reff is True:
        plot_rex_reff_bar_graph(rex_list,reff_list,average_rex,rex_std_up,average_reff,reff_std_up)
    if generate_excel__rex_reff_plot_file is True:
        rex_reff_excel_file(rex_list,reff_list,average_rex,rex_std_up,average_reff,reff_std_up)

if selective_groups is True:
    selective_generator()
else:
    create_cpmg_fit_peaklist_files()
    create_cpmg_fit_input_file()

if generate_plots is True:
    plot_data()
if generate_excel_output_file is True:
    generate_for_excel_plotting()
