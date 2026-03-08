#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 fucking_us.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
import base64
from gnuradio import gr
from collections import deque

class preprocess(gr.sync_block):
    """
    docstring for block preprocess
    """
    def __init__(self, t, fs, input_str):

        file_packet = self.create_file_packet(input_str)

        self.queue = preprocess.process(file_packet, t, fs)
        
        gr.sync_block.__init__(self,
            name="preprocess",
            in_sig=None,
            out_sig=[np.float32, ])


    def create_file_packet(self, filepath):
        # packet structure is: filename length : file name : file content
        filepath_length = str(len(filepath))
        filepath_length = filepath_length.zfill(3) # length+suffix can be up to 260 (3 chars)
        with open(filepath, 'rb') as file:
            bin_data = file.read()
            encoded_data = base64.b64encode(bin_data)
            encoded_file_content = encoded_data.decode('utf-8')
           
        packet = filepath_length + filepath + encoded_file_content
        print(packet)
        return packet

    def work(self, input_items, output_items):
        out = output_items[0] 
        
        if len(self.queue) < len(output_items[0]):
            self.queue.extend(np.zeros((len(output_items[0])-len(self.queue))))
            
        dequeued_items = np.array([self.queue.popleft() for _ in range(len(output_items[0]))])
        dequeued_items = dequeued_items.astype(np.float32)

        out[:] = dequeued_items
        
        return len(output_items[0])
    
    @staticmethod
    def process(input_str, t, fs):
        binary_string = preprocess.string_to_binary(input_str)

        preamble = np.full((int(t*fs)), 1)
        queue = deque(preamble)
        
        for bit in binary_string:
            bit_samples = preprocess.bit_to_samples(bit, t, fs)
            queue.extend(bit_samples)
            
        return queue
    
    @staticmethod
    def bit_to_samples(bit, t, fs):
        
        if bit == 0:
            output = np.concatenate((np.full((int(t*fs)), 1), np.full((int(2*t*fs)), -1))) 
        else:
            output = np.concatenate((np.full((int(2*t*fs)), 1), np.full((int(t*fs)), -1))) 
        return output
            
        
    
    @staticmethod
    def string_to_binary(input_str):
        binary_chars = [format(ord(char), '08b') for char in input_str] # list such that each element is the char in binary
        binary_string = [int(bit) for binary_str in binary_chars for bit in binary_str] # bits of all string
        return binary_string
    
    
