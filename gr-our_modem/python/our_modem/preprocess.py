#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 fucking_us.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
from collections import deque

class preprocess(gr.sync_block):
    """
    docstring for block preprocess
    """
    def __init__(self, t, fs, input_str):

        self.queue = preprocess.process(input_str, t, fs)
        
        gr.sync_block.__init__(self,
            name="preprocess",
            in_sig=None,
            out_sig=[np.float32, ])


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
        
        noise_duration = 1 # 1 second
        noise_samples = int(noise_duration * fs)
        noise = np.random.normal(loc=0, scale=1, size=0)
        queue = deque(noise)

        preamble = np.full((int(t*fs)), -1)
        queue.extend(preamble)
        
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
    
    
