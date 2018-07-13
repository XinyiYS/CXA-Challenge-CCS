import os
import numpy as np
import pandas as pd
import sys
from multiprocessing import Process, Queue
import json

def add( a,b):
	return a+b


def voice_handler_init(function_queue):
	c = 0
	while(True):
		if c>=100:
			break
		if c % 7 ==0:
			to_put = [add,c,c+1]
			function_queue.put(to_put)
		c+=1
	return

def perform(fcn,*args):
	return fcn( *args)


def main():
	
	function_queue = Queue()
	p = Process(target=voice_handler_init, args=(function_queue,))
	p.start()
	while True:
		a =  (function_queue.get())    # prints "[42, None, 'hello']"
		fcn = a[0]
		args = a[1:]
		print(perform(fcn,*args))

	p.join()


if __name__ == '__main__':
	main()





