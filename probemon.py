#!/usr/bin/python

import time
import os
from datetime import datetime
import argparse
import netaddr
import time
import sys
import os
import logging
from scapy.all import *
from pprint import pprint
from logging.handlers import RotatingFileHandler
from send_endpoint import send_endpoint


NAME = 'probemon'
DESCRIPTION = "a command line tool for logging 802.11 probe request frames"
FILTERED_MAC = "f6:2f:ee:2c:c9:6c"
DEBUG = False
ap_id = os.environ['AP_ID']

def build_packet_callback(time_fmt, logger, delimiter, mac_info, ssid, rssi, fm, u):
	def packet_callback(packet):
		
		if not packet.haslayer(Dot11):
			return

		# we are looking for management frames with a probe subtype
		# if neither match we are done here
		if packet.type != 0 or packet.subtype != 0x04:
			return

		# list of output fields
		fields = []

		# determine preferred time format 
		log_time = str(int(time.time()))
		if time_fmt == 'iso':
			log_time = datetime.now().isoformat()

		fields.append(log_time)

		# append the mac address itself
		if fm is not None and fm.lower() != packet.addr2.lower():
			return
		fields.append(packet.addr2)

		# parse mac address and look up the organization from the vendor octets
		if mac_info:
			try:
				parsed_mac = netaddr.EUI(packet.addr2)
				fields.append(parsed_mac.oui.registration().org)
			except netaddr.core.NotRegisteredError, e:
				fields.append('UNKNOWN')

		# include the SSID in the probe frame
		if ssid:
			fields.append(packet.info)
			
		if rssi:
			rssi_val = packet.dBm_AntSignal
			fields.append(str(rssi_val))

		fields = [f.decode('cp1252').encode('utf-8') for f in fields]
		# logger.info(delimiter.join(fields))

		if fm is not None and u and ssid and rssi:
			send_endpoint(fields[0], ap_id, fields[1].lower(), fields[3], fields[2])
	return packet_callback

def main():
	parser = argparse.ArgumentParser(description=DESCRIPTION)
	parser.add_argument('-i', '--interface', help="capture interface")
	parser.add_argument('-t', '--time', default='iso', help="output time format (unix, iso)")
	parser.add_argument('-o', '--output', default='probemon.log', help="logging output location")
	parser.add_argument('-b', '--max-bytes', default=5000000, help="maximum log size in bytes before rotating")
	parser.add_argument('-c', '--max-backups', default=99999, help="maximum number of log files to keep")
	parser.add_argument('-d', '--delimiter', default='\t', help="output field delimiter")
	parser.add_argument('-f', '--mac-info', action='store_true', help="include MAC address manufacturer")
	parser.add_argument('-s', '--ssid', action='store_true', help="include probe SSID in output")
	parser.add_argument('-r', '--rssi', action='store_true', help="include rssi in output")
	parser.add_argument('-D', '--debug', action='store_true', help="enable debug output")
	parser.add_argument('-l', '--log', action='store_true', help="enable scrolling live view of the logfile")
	parser.add_argument('-fm', default=FILTERED_MAC, help="filter specific mac address")
	parser.add_argument('-u', '--upload', action='store_true', help="upload to db")

	args = parser.parse_args()

	if not args.interface:
		print "error: capture interface not given, try --help"
		sys.exit(-1)

	os.system("airmon-ng start {}".format(args.interface))
	time.sleep(15)
	
	DEBUG = args.debug

	# setup our rotating logger
	logger = logging.getLogger(NAME)
	logger.setLevel(logging.INFO)
	handler = RotatingFileHandler(args.output, maxBytes=args.max_bytes, backupCount=args.max_backups)
	logger.addHandler(handler)
	if args.log:
		logger.addHandler(logging.StreamHandler(sys.stdout))
	built_packet_cb = build_packet_callback(args.time, logger, 
		args.delimiter, args.mac_info, args.ssid, args.rssi, args.fm, args.upload)
	sniff(iface="{}mon".format(args.interface), prn=built_packet_cb, store=0)

if __name__ == '__main__':
	main()
