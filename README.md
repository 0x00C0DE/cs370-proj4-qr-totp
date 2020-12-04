# cs370-proj4-qr-totp
CS370 project 4

Braden Lee
Oregon State University

This program is intended to mimic the well known "Google Authenticator". This program generates a qr code intended to be read by qr scanners. This program also has the ability to generate the exact 6 digit totp that GA uses's in their algorithm. 

INSTRUCTIONS
---------------
how to set up virtual environment in current directory

1. python3 -m venv env
2. source env/bin/activate

need to install pyqrcode to generate qr

1. pip install pyqrcode

to execute

1. python3 qrcode_bl.py --generate-qr
2. python3 qrcode_bl.py --get-otp

to leave virtual environment

1. deactive
---------------
