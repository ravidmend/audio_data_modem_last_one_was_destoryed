#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 fucking-us.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
from scipy.signal import find_peaks
from collections import deque

class postprocessor(gr.sync_block):
    """
    docstring for block postprocessor
    """

    def __init__(self, t,fs,sensitivity,timeout):
        self.t = t
        self.fs = fs
        self.sensitivity = sensitivity
        self.timeout = timeout*8 # convert bytes to bits
        self.bits = []
        self.queue = deque([])
        self.did_removed_preamble = False

        self.detection_mode=True
        self.undetected_bits=0


        self.stream_count=0
        self.data=[]

        gr.sync_block.__init__(self,
            name="postprocessor",
            in_sig=[np.float32, ],
            out_sig=None)

    def __del__(self):
        datanp=np.concatenate(self.data)
        np.save('data.npy', datanp)


    def work(self, input_items, output_items):
    
        self.stream_count+=1
        in0 = input_items[0]
        
        self.data.append(in0.copy())
            


        sps = int(self.t*self.fs)

        window = np.full((sps), 1)

        

        if (self.detection_mode==True):
            
            correlation = np.correlate(in0, window, mode='full')
            peaks,_ = find_peaks(correlation,height = self.sensitivity*sps) # 0.07 = 0.1(modulation loss) * factor
            
         
            if len(peaks) != 0:
              
                starting_index = peaks[0]
                #np.save("withpreamble.npy", in0)
                in0 = in0[starting_index:len(in0)]
                #np.save("withoutpreamble.npy", in0)
                self.detection_mode=False

                

        else:
            self.queue.extend(in0)
            bit_time = 3
            while(len(self.queue) > (bit_time * sps)):
                
                dequeued_items = np.array([self.queue.popleft() for _ in range(bit_time * sps)])
                corr_max = max(np.correlate(dequeued_items, window, 'full'))

                if corr_max<1e-3:
                    print('noise')
                    self.undetected_bits = self.undetected_bits +1
                else:
                
                    self.undetected_bits = 0

                if self.timeout == self.undetected_bits:
                    print('timeout detected')
                    self.detection_mode=True
                    self.bits = []
                    self.undetected_bits = 0
                    break


                bit = self.decide_bit(dequeued_items,sps, bit_time)
                self.bits.append(bit)

                if (len(self.bits) == 8): # byte consists of 8 bits
                    output_str = self.bits_to_string(self.bits)
                    print(f"{output_str}")
                    self.bits = []
    

            
        return len(input_items[0])
    

    def decide_bit(self, samples_array,sps, bit_time): 
        filtered_samples_array = postprocessor.noise_smoothing(samples_array,sps)
        binary_arr = (filtered_samples_array>0).astype(int)

        if(sum(binary_arr)>(bit_time/2*sps)): # if more than 50 percent is 1 we choose bit 1
            return 1
        else:
            return 0


    @staticmethod
    def bits_to_string(bits_array):
        output_str = ""
        bytes = [bits_array[i:i+8] for i in range(0,len(bits_array),8)] #break into bytes arrays
        
        for byte in bytes:
            byte_string = "".join(map(str,byte)) # turn array to string
            ch = int(byte_string,2)
            output_str += chr(ch)
        return output_str

        
    

    @staticmethod
    def noise_smoothing(samples_array,sps): 
        window = np.full((sps), 1) / sps
        samples_array = np.convolve(samples_array, window, mode='same')
        return samples_array

