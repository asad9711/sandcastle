#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, commands, requests
from argparse import ArgumentParser

print """
   ____             __             __  __   
  / __/__ ____  ___/ /______ ____ / /_/ /__ 
 _\ \/ _ `/ _ \/ _  / __/ _ `(_-</ __/ / -_)
/___/\_,_/_//_/\_,_/\__/\_,_/___/\__/_/\__/ 
                                            
S3 bucket enumeration // release v1.2.4 // ysx

"""
targetStem = ""
inputFile = ""

parser = ArgumentParser()
parser.add_argument("-t", "--target", dest="targetStem",
                    help="Select a target stem name (e.g. 'shopify')", metavar="targetStem", required="True")
parser.add_argument("-f", "--file", dest="inputFile",
                    help="Select a bucket permutation file (default: bucket-names.txt)", default="bucket-names.txt", metavar="inputFile")
parser.add_argument("-o", "--output-file", dest="outputFile",
                    help="File to write the command output", default=None, metavar="outputFile")

args = parser.parse_args()
with open(args.inputFile, 'r') as f:
    bucketNames = [line.strip() for line in f] 
    lineCount = len(bucketNames)

print "[*] Commencing enumeration of '%s', reading %i lines from '%s'." % (args.targetStem, lineCount, f.name)
output_file = None
for name in bucketNames:
	r = requests.head("http://%s%s.s3.amazonaws.com" % (args.targetStem, name))
	if r.status_code != 404:
                # macOS, coming soon: os.system("notify Potential match found! %s%s: %s" % (args.targetStem, name, r.status_code))
		print "[+] Checking potential match: %s%s --> %s" % (args.targetStem, name, r.status_code)
		check = commands.getoutput("/usr/local/bin/aws s3 ls s3://%s%s" % (args.targetStem, name))
		if args.outputFile is not None:
			# will create the file if file not exists
			output_file = open(args.outputFile, 'w')
			output_file.write('Bucket Name --> %s%s' % (args.targetStem, name) + os.linesep)
			output_file.write(check + os.linesep)
		else:
			print check
	else:
		sys.stdout.write('')

print "[*] Enumeration of '%s' buckets complete." % (args.targetStem)
# close the file if its open
if output_file:
	print "[*] Enumeration output written into file %s " % args.outputFile
	output_file.close()
# macOS, coming soon: os.system("notify Enumeration of %s buckets complete." % (args.targetStem))
