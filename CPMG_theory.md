***Info below is from this paper. Must read: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2717354/***

Proteins can often accomadate multiple conformations. They may rapidly switch between these conformations. It's important to understand, the "time" it takes to switch to these conformations may vary. For example, if the rate of exchange is slow, then you will see 2 distinct peaks in your spectra, corresponding to a particular amino acid. These 2 peaks, represent the 2 different conformations the protein adopts. However, if the rate of exchange is faster (i.e. in the us-ms timescale), then you will not observe 2 peaks. Instead what will happen is the peak will simply broaden or weaken (sometimes disappear completely. It is often assumed peaks that do not show up in your spectra, are due to us-ms timescale motion).

A CPMG experiment is a series of 180 degree pulses (refocusing pulses).

Imagine an amino acid that exists in 2 states (2 conformations), and is slowly exchanging between 2 states. In other words, you see 2 peaks in your spectrum for this singular amino acid. If you apply a 90 degree pulse to it, both states will shift to the x-axis. If you then allow them to relax (i.e. precess), they will then precess at their own distinct frequency. After a certain time, you apply a 180 degree pulse. You then allow the 2 states to relax again with the same time as before. They should both arrive back at the same place they started (i.e. x-axis). 

A similar analogy is 2 runners on a race track. These 2 runners run at their own distinct speeds (5mph/10mph). The first "relaxation time" is the gun going off, and them starting the race. Say, you let them run at this speed for 5 minutes (5mph goes 0.4miles, 10mph runs 0.8 miles).  The 180 degree pulse is then telling the racers, now turn around, and run back to the starting line. You let them run at the same speed, again for 5 minutes. The races will arrive back at the start line, at the same time. 

This results in 2 distince peaks. 

Now imagine an amino acid that exists in 2 states, but is exchanging between them on a us-ms timescale. In other words, you only see 1 peak in your spectrum, that has broadened due to this exchange. As before, if you apply a 90 degree pulse to it, both states will shift to the x-axis. If you then allow them to relax (i.e. precess), they will then precess at their own distinct frequency. However, this time, that frequency is not constant throughout the entire time. It is now exchanging rapidly between the 2 states. After a certain time, you apply a 180 degree pulse. You then allow the 2 states to relax again with the same time as before. They again, will not precess at the same frequency, this frequency will constantly be exchanging. Thus, at the end of the experiment, the 2 states will not arrive back to the same place. Thus, you will get line broadening. 

A similar analogy is the 2 runners on a race track. Same scenario as before. Except now, the speed is not a constant 5mph/10mph, since their speeds will be exchange with one another. The first runner might run 5mph the first 2.5min, then 10mph the next 2.5min. But after the 180 degree pulse they might run 5mph the first minute, then 10mph the next, and back to 5mph the next, etc. Thus, during the first relaxation the first runner will be going on average 7.5mph (0.625 miles), and after the 180 degree pulse during the 2nd relaxation they will run an average of 7mph (0.58 miles). Thus, runner 1 will not end up back at the start line, and will be short 0.04 miles. The same will be true of runner 2. 


Now if you wished to minimize this problem (not arriving back at the starting point), you could simply shorten the time of the race. Instead of running for 5 minutes, 180, then 5 minutes (i.e. total 10 minutes). Just do 1min, 180, 1min. But...then you wouldn't get much of a race in just 2 minutes. Instead what you can do is keep the total time the same, but increase the number of 180s. In other words, 2min 180 2min 180 2min 180 2min 180 2min 180 2min. What results, is as you increase the number of these 180s, you get the races closer and closer to the finish line.

This is the philosophy behind CPMG. As you increase the frequency of the 180 degree pulses, your 2 states will refocus better and better. Thus, we can now see there is a dependency, a correlation, to the rate of exchange between the 2 states, the frequency of the CPMG pulses, and the intensity of the peak. Therefore, by varying the frequncy of these CPMG pulses, you can get varying peak intensities, and from them, derive the rate of exchange between the 2 states. 

The "ncyc" value, is exactly that. The "n" nyumber of "cyc" cycles (of 180 degree pulses), within a particular constant time frame (time_t2). The more cycles (the more 180 degre pulses), the more intense the peak. These are converted to what's known as CPMG frequency (the frequency of CPMG pulses, same meaning, different value). As the CPMG frequency increases, the intensity of the peak increases. The Reff value that is then calculated, is the inverse of these intensity values. In other words, the higher the frequency, the lower the Reff value. ***This is of course only true for amino acids undergoing exchange on a us-ms timescale***. If the peak is not undergoing exchange on this time scale, there is no dependency on peak intensity and the 180 degree pulses (look above at when 2 states exchange slower), and thus the Reff value will not change throughout the experiment, and you will result in a flat line. 

If Reff is plotted against the CPMG frequency, a slope is generated (for those that have exchange on us-ms). Thus, the correlation between intensity and CPMG frequency is demonstrated. Reff is correlated to the exchange between the 2 states, in addition to the population of the 2 states, and the difference between the chemical shifts of the 2 states. Thus, all these values can be derived through a non linear fitting of the Reff_CPMG curve. 

```
Reff=PaPb/Ke
where Pa and Pb are the populations of the 2 states
Ke is the rate of exchange between the 2 states
```


