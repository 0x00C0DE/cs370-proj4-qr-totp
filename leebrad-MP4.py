#Braden Lee
import argparse
import array
import base64
import hashlib
import hmac
import math
import os
import sys
import time
from urllib.parse import quote

SECRET_FILE = "totp_secret.txt"
QR_FILE = "uri_qrcode.svg"


def get_base_path():
	return os.path.dirname(os.path.abspath(__file__))


def get_secret_file_path():
	return os.path.join(get_base_path(), SECRET_FILE)


def get_qr_file_path():
	return os.path.join(get_base_path(), QR_FILE)


def generate_secret():
	# Generate a 160-bit secret, which matches the size commonly used for TOTP.
	return base64.b32encode(os.urandom(20)).decode("utf-8").rstrip("=")


def save_secret(secret):
	with open(get_secret_file_path(), "w", encoding="ascii") as secret_file:
		secret_file.write(secret)


def load_secret():
	secret_path = get_secret_file_path()
	if not os.path.exists(secret_path):
		print("[ERROR]")
		print("No enrolled secret found. Run --generate-qr first.")
		print("[ERROR]")
		sys.exit(1)

	with open(secret_path, "r", encoding="ascii") as secret_file:
		return secret_file.read().strip()


def decode_secret(secret):
	padding = (-len(secret)) % 8
	return base64.b32decode(secret + ("=" * padding), casefold=True)


def build_otpauth_url(issuer, username, user_email, secret):
	label = quote(f"{issuer}:{user_email}")
	issuer_param = quote(issuer)
	return (
		f"otpauth://totp/{label}?secret={secret}"
		f"&issuer={issuer_param}&username={quote(username)}"
	)


def create_qrcode(issuer, username, user_email):
	import pyqrcode

	secret = generate_secret()
	save_secret(secret)

	url = build_otpauth_url(issuer, username, user_email, secret)
	url_qrcode = pyqrcode.create(url)
	url_qrcode.svg(get_qr_file_path(), scale=8)

	print("QR code saved to:", get_qr_file_path())
	print("Username:", username)
	print("Email:", user_email)
	print("Issuer:", issuer)
	return


def create_otp():
	c_timer = math.floor(time.time())
	steps_thirty = 30
	time_counter = int(c_timer / steps_thirty)

	t_c = time_counter
	byte_arr = array.array("B")
	for i in reversed(range(0, 8)):
		byte_arr.insert(0, t_c & 0b11111111)
		t_c >>= 8

	time_bytes = byte_arr
	secret = decode_secret(load_secret())
	qr_otp = hmac.new(secret, time_bytes, hashlib.sha1).hexdigest()

	bitstring = bin(int(qr_otp, 16))
	last_4_bits = bitstring[-4:]
	qr_offset = int(last_4_bits, 2)
	binary_otp = int(qr_otp[(qr_offset * 2):((qr_offset * 2) + 8)], 16) & 0b01111111111111111111111111111111

	dig_6 = str(binary_otp)[-6:]
	print("dig_6 is: ", dig_6)
	return


def parse_args():
	parser = argparse.ArgumentParser(
		description="Generate a TOTP QR enrollment and matching one-time passwords."
	)
	parser.add_argument(
		"--generate-qr",
		action="store_true",
		help="Generate a QR code with a fresh random secret.",
	)
	parser.add_argument(
		"--get-otp",
		action="store_true",
		help="Generate the current OTP from the saved secret.",
	)
	parser.add_argument(
		"--issuer",
		help="Issuer name shown in authenticator apps. Required with --generate-qr.",
	)
	parser.add_argument(
		"--username",
		help="Username associated with the QR enrollment. Required with --generate-qr.",
	)
	parser.add_argument(
		"--email",
		help="Email associated with the QR enrollment. Required with --generate-qr.",
	)

	args = parser.parse_args()

	if args.generate_qr == args.get_otp:
		parser.error("choose exactly one of --generate-qr or --get-otp")

	if args.generate_qr:
		missing_args = []
		if not args.issuer:
			missing_args.append("--issuer")
		if not args.username:
			missing_args.append("--username")
		if not args.email:
			missing_args.append("--email")
		if missing_args:
			parser.error("--generate-qr requires " + ", ".join(missing_args))

	return args


def main():
	args = parse_args()

	if args.generate_qr:
		create_qrcode(args.issuer, args.username, args.email)

	if args.get_otp:
		create_otp()

	print("done")


if __name__ == "__main__":
	main()
