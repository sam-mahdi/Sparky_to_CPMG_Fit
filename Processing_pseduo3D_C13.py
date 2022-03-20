import re
import glob
import os


"""script will go through any directory with .fid extension [ONLY FOR C13 NON FORBIDDEN CPMG DATA], read procpar data, generate ncyc and cpmg frequency files, generate fid.com, and open up NMRDraw. The user can then phase the data, zero fill, add baseline corrections, etc.
This will generate an nmr_ft.com file, that the program will then use to create a nmr_ft_ps3d.com, that is run to create the res_ps3d directory containing the processed pseduo3D data. A .dat and .ft2 file are made since .dat is used for
sparky and other processing, and .ft2 is used for pine. NOTE, since each data set must be phased and processed individually, the script will stop and ask for user input after every dataset (i.e. just click enter to move on to the next dataset)"""


def generate_frequences(file):
    """Reads procpar to extract ncyc and t2 values"""
    counter=0
    t2_counter=0
    for lines in file:
        search=re.search('ncyc(_cp*)\s+',lines) #searches propcar for ncyc or ncyc_cp
        search_t2=re.search('time_T2\s+',lines) #searches for time_t2
        if counter == 1: #the counters exist because the line that will match ncyc or time_T2 search doesn't contain the data we want. It is in fact the line below it. So counter=1 means the line below the searched item.
            counter+=1
            ncync_max=lines.split()[0] #first value in line, contains number of ncyc
            ncync_list=lines.split()[1:] #the rest of the ncyc values in line (excludes first value)
        if t2_counter == 1:
            t2_counter+=1
            t2=float(lines.split()[1]) #T2 values
        if search is not None:
            counter+=1
        if search_t2 is not None:
            t2_counter+=1
    return ncync_max,ncync_list,t2

def generate_reference_files(ncync_max,ncync_list,t2):
    """calculates cmpg frequency values from ncyc values"""
    cpmg_frq=[]
    for entries in ncync_list: #loop through ncyc and calculates cpmg_frequency
        new_ncync_value=float(entries)*(1/t2) # ncyc_value * (1/T2_value) ncyc value multiplied by inverse time_T2
        cpmg_frq.append(new_ncync_value)
    return cpmg_frq

def write_frequency_files(ncync_max,ncync_list,t2,cpmg_frq):
    """writes ncyc.list and cpmg.list files"""
        with open('ncyc.list','w') as ncyc_file,open('nucpmg.list','w') as cpmg_frq_file: #writes an ncyc.list file which is purely used as reference (Dmitry likes to have it), and a nucpmg.list file which is uploaded to varian -pseudo3D, in column format cause that's what Dmitry likes
            for values in ncync_list:
                ncyc_file.write(str(values)+'\n')
            ncyc_file.write('Time_T2 value:'+str(t2))
            for values2 in cpmg_frq:
                cpmg_frq_file.write(str(values2)+'\n')


def generate_fid_dot_com(file,cpmg_frq,ncync_max):
    """generate fid.com, basically replaces varian -pseudo3D command, opens up NMRDraw for phasing and baseline corrections"""
    np_flag=False
    ni_flag=False
    sw_flag=False
    sw1_flag=False
    sfrq_flag=False
    dfrq_flag=False
    for lines in file: #loops through procpar lines. Pretty self explanatory, searches for parameters, if found flag is turned on, parameter extracted then turned off (again, this is because line with data is below line with search)
        np_line=re.search('^np\s+',lines)
        ni_line=re.search('^ni\s+',lines)
        sw_line=re.search('^sw\s+',lines)
        sw1_line=re.search('^sw1\s+',lines)
        sfrq_line=re.search('^sfrq\s+',lines)
        dfrq_line=re.search('^dfrq\s+',lines)
        if np_flag is True:
            np_flag=False
            np=float(lines.split()[1])
        if np_line is not None:
            np_flag=True
        if ni_flag is True:
            ni_flag=False
            ni=float(lines.split()[1])
        if ni_line is not None:
            ni_flag=True
        if sw_flag is True:
            sw_flag=False
            sw=float(lines.split()[1])
        if sw_line is not None:
            sw_flag=True
        if sw1_flag is True:
            sw1_flag=False
            sw1=float(lines.split()[1])
        if sw1_line is not None:
            sw1_flag=True
        if sfrq_flag is True:
            sfrq_flag=False
            sfrq=float(lines.split()[1])
        if sfrq_line is not None:
            sfrq_flag=True
        if dfrq_flag is True:
            dfrq_flag=False
            dfrq=float(lines.split()[1])
        if dfrq_line is not None:
            dfrq_flag=True

    with open('fid_test.txt','w') as fid: #above extracts parameters, here we write them into file
        fid.write('#!/bin/csh\n')
        fid.write(f'set tauList = ({" ".join(str(x) for x in cpmg_frq)})\n\n')
        fid.write('var2pipe -verb -in ./fid \\')
        fid.write('\n-noaswap\t\\\n')
        fid.write(f'-xN\t\t{int(np)}\t-yN\t\t{ncync_max}\t-zN\t\t{int(ni*2)}\t\\\n')
        fid.write(f'-xT\t\t{int(np/2)}\t-yT\t\t{ncync_max}\t-zT\t\t{int(ni)}\t\\\n')
        fid.write(f'-xMODE\t\tComplex\t-yMODE\t\tReal\t-zMODE\t\tComplex\t\\\n')
        fid.write(f'-xSW\t\t{"%.1f" % sw} -ySW\t\t{ncync_max}\t-zSW\t\t{"%.2f" % sw1} \\\n')
        fid.write(f'-xOBS\t\t{"%.3f" % sfrq}\t-yOBS\t\t1.000\t-zOBS\t\t{"%.3f" % dfrq}\t\\\n')
        fid.write(f'-xCAR\t\t0.677\t-yCAR\t\t0.000\t-zCAR\t\t19.978\t\\\n')
        fid.write(f'-xLAB\t\t1H\t-yLAB\t\tTAU\t-zLAB\t\tC13\t\\\n')
        fid.write(f'-ndim\t\t3\t-aq2D\t\tComplex\t\t\t\t\\\n')
        fid.write(f'| nmrPipe -fn MULT -c 3.12500e+01 \\\n')
        fid.write(f'| nmrPipe -fn TP -exch -noord -nohdr \\\n')
        fid.write(f'| nmrPipe -fn ZTP -exch -noord \\\n')
        fid.write(f'| nmrPipe -fn TP -exch -noord -nohdr \\\n')
        fid.write(f'| pipe2xyz -x -out ./data/test%03d.fid -ov\n\n')
        fid.write(f'sortPlanes.com -in ./data/test%03d.fid -out ./data/test%03d.fid -tau $tauList -title\n\n')
        fid.write(f'nmrDraw -process -in data/test%03d.fid -fid data/test%03d.fid\n\nsleep 5')

def generate_nmr_ft_ps3d_dot_com():
    """When phasing and corrections are done in NMRDraw, this results in nmr_ft.com, but this is not the file we want. It contains extra info, and is missing some info required for psudo3D generation.
    Thus, here we extract the useful stuff from nmr_ft.com, and generate a new file with that useful info and added stuff required for pseduo3D."""
    write_flag=False
    with open('nmr_ft.com') as file,open('nmr_ft_ps3d.com','w') as ps3d_file:
        for lines in file:
            if re.search('xyz2pipe',lines) is not None:
                write_flag=True
            if re.search('pipe2xyz',lines) is not None:
                ps3d_file.write('| pipe2xyz -out res_ps3d/ft2d%03d.dat -x -ov\n\n')
                break
            if write_flag is True:
                ps3d_file.write(lines)
        ps3d_file.write('xyz2pipe -in res_ps3d/ft2d%03d.dat > res_ps3d/full_pseudo3d.dat\n')
        ps3d_file.write('xyz2pipe -in res_ps3d/ft2d%03d.dat > res_ps3d/full_pseudo3d.ft2\n')





current_directory=os.getcwd() #gets the current directory

procpar_file='procpar' #procpar file
all_cpmg_file=glob.glob('*.fid') #finds all the names of the .fid files that contain data
for cpmg_file in all_cpmg_file: #loop through all the .fid files
    os.chdir(current_directory+'/'+cpmg_file) #changes directory to fid file directory
    np_flag=False
    with open(procpar_file) as file: #opens procpar file
        ncync_max,ncync_list,t2=generate_frequences(file)
        cpmg_frq=generate_reference_files(ncync_max,ncync_list,t2)
        write_frequency_files(ncync_max,ncync_list,t2,cpmg_frq)
    with open(procpar_file) as file:
        generate_fid_dot_com(file,cpmg_frq,ncync_max)
        os.system('chmod u+x fid.com')
        os.system('./fid.com')
    stop_for_next_analysis=input('Click enter for next folder:  ')
    generate_nmr_ft_ps3d_dot_com()
    os.system('chmod u+x nmr_ft_ps3d.com')
    os.system('./nmr_ft_ps3d.com')
