#Braden Lee
import os
import sys
import pyqrcode
import getpass
import random
import base64
import hmac
import string
import hashlib
import time
import math
import struct
import array

# function to generate qr code svg	
def create_qrcode(): 

	#creates user id
	username = 'leebrad'
	user_email = username + "@oregonstate.edu"	
	#print(user_email)


	# static secret to test
	secret = base64.b32encode(bytearray("BIGONEBUYNOWSAVE", "ascii")).decode('utf-8')[:-6]	
	#print(secret)

	#url = 'otpauth://totp/' + '0x00C0DE' + ':' + user_email + '?secret=' + secret + '&issuer=' + '0x00C0DE'
	url = 'otpauth://totp/' + 'smallmediumpizza' + ':' + user_email + '?secret=' + secret + '&issuer=' + 'smallmediumpiza'
	#print(url)

	url_qrcode = pyqrcode.create(url)

	url_qrcode.svg("uri_qrcode.svg", scale="8")

	return


# function to generate totp
def create_otp():
	
	# epoch time
	c_timer = math.floor(time.time())

	# couter variable for 30 seconds
	steps_thirty = 30

	Time_counter = int((c_timer/steps_thirty))

	t_c = Time_counter
	#print("timer counter:", Time_counter)

	# convert time to bytes
	byte_arr = array.array('B')
	for i in reversed(range(0, 8)):
		
		# (AND) with 1111 1111 to leave the last 8 bits
		byte_arr.insert(0, t_c & 0b11111111)
		# perform bit shift by 8 places
		t_c >>= 8

	# Time converted to bytes
	Time_bytes = byte_arr
	#print("Time_bytes: ", Time_bytes)

	# static secret to test to bytes
	secret = bytearray("BIGONEBUYNOWSAVE", "ascii")

	# hmac generation
	qr_otp = hmac.new(secret, Time_bytes, hashlib.sha1).hexdigest()

	# convert to binary and take last 4 bits to use as the offset
	bitstring = bin(int(qr_otp, 16))
	last_4_bits = bitstring[-4:]
	qr_offset = int(last_4_bits, 2)

	# grabs the next 31 bits needed using (AND) with bitmask 01111111 11111111 11111111 11111111
	binary_otp = int(qr_otp[(qr_offset * 2):((qr_offset * 2) + 8)], 16) & 0b01111111111111111111111111111111
	
	# takes the last 6 digits as totp
	dig_6 = str(binary_otp)
	dig_6 = dig_6[-6:]	

	print("dig_6 is: ", dig_6)
	return

if len(sys.argv) == 1:
	print("[ERROR]")
	print("not enough args.lol")
	print("[ERROR]")
else:
	first_arg = sys.argv[1]
	print("first arg is:", first_arg)


if first_arg == '--generate-qr':
	print("in [generate qr]")
	create_qrcode()

if first_arg == "--get-otp":
	print("in [get otp]")
	create_otp()

print("done")
