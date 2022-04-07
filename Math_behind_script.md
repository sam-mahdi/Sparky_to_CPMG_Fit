Math Behind Experiment:

CPMG is run by using a time constant (time_t2) and increasing the number of CPMG cycles (ncyc or ncyc_cp). Both values within procpar file

The ncyc is converted to cpmg frequency by taking the time inverse and multiplying it by the ncyc

```
cpmg_frequency=(1/time_t2)*ncyc
```

The next step is to calculate Reff, this is done by multiplying the inverse time by the negative natural log of your peak instensity at a particular cpmg frequency divided by the peak intensity when no CPMG pulse is applied (i.e. the reference signal intensity). If exchange is occuring, then the CPMG frequency between the lowest and highest frequcy should differ by quite a bit. Thus the Rex value is the difference between the lowest and highest CPMG frequency.

```
Reff= (1/time_t2)*-ln(I(cpmg_frequency)/I0) where I(cpmg_frequency) is the peak intensity for a particular CPMG frequency, and I0 is the reference signal intensity)
Rex=Reff(lowest_cpmg_frequency)-Reff(highest_cpmg_frequency) 
```

Duplicate CPMG frequencies are run to obtain errors. This is the natural variation in peak intensity (e.g. noise). The error is calculated by first determining a baseline ("noise") error. This is done by getting the relative error of the duplicates first, which is just the average of your duplicates dividied by the standard deviation, then comparing that to a standard error. You then take the max of the 2 errors, and use that to calculate the error for each cpmg frequency, for each residue.
The final value at the duplicate frequency is the average of the duplicate values. 

```
relative_error=average_duplicates/standard_deviation_duplicates

reference_global_eror=0.04

#if relative error is higher than global error, then the relative error is used. Otherwise the global error is used for the below

peak_error=absolute_value(Reff*error)

```

If multiple duplicate frequencies are run, then you should have 2 relative errors. You may average these to one, or compare both to the global error. 

EXAMPLE SET:

```
Peak Intensities for each CPMG frequency
0.00	1.02E+08 #reference intensity
25.00	9.46E+07
50.00	9.44E+07
50.00	9.52E+07
75.00	9.45E+07
100.00	9.52E+07
150.00	9.52E+07
200.00	9.48E+07
300.00	9.44E+07
400.00	9.50E+07
500.00	9.50E+07
500.00	9.55E+07
600.00	9.46E+07
700.00	9.52E+07
800.00	9.52E+07
900.00	9.48E+07
1000.00	9.58E+07

Peak Intensities converted to Reff 
0.00	0
25.00	1.803960821
50.00	1.859507583
50.00	1.65381022
75.00	1.838332356
100.00	1.645932482
150.00	1.664317733
200.00	1.766998094
300.00	1.862155748
400.00	1.698497682
500.00	1.706392004
500.00	1.580381026
600.00	1.798677085
700.00	1.664317733
800.00	1.66169044
900.00	1.761722163
1000.00	1.501945488
Rex	0.302015333

Note duplicates at 50 and 500. For example below, only 50 will be shown, but both errors should be calculated and used. 

Average: 1.756658901
Standard_deviation: 0.14545
relative_error: 0.082799228
global_error: 0.04
new_value_for_50: 1.756658901 #note it is the same as the average

Errors
25	0.149366563
50	0.14545
75	0.152212499
100	0.136281938
150	0.137804223
200	0.146306077
300	0.154185058
400	0.140634296
500	0.136071134
600	0.148929073
700	0.137804223
800	0.137586685
900	0.145869234
1000	0.124359926
```




