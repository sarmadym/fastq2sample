#!/opt/python/bin/python2.7
import sys
import getopt
import os
import os.path
import re
import fnmatch 
def usage():
   print "use: sample2fastq -p pathtolookforfastqs"

def main(argv):
	"""
   	multi-line comment
   	"""
   	try:
   		path = os.getcwd()
		opts, args = getopt.getopt(argv,"hp:",["help","path="])
		for opt, arg in opts:
			if opt in ("-h","--help"):
				usage()
				sys.exit()
			elif opt in ("-p","--path="):
				path= arg
		source = "".join(args)

	except getopt.GetoptError:
   		usage()
   		sys.exit(2)
   	print ("Looking for fastq files in "+path)
   # includ file extensions
   	includes = ['*.fastq', '*.fastq.gz','*.fq','*.fq.gz']
   	includes = r'|'.join([fnmatch.translate(x) for x in includes])
   	for root, dirs, files in os.walk(path):
         print files
         files = [os.path.join(root, f) for f in files]
   		#files = [f for f in files if not re.match(excludes, f)]
         files = [f for f in files if re.match(includes, f)]

   	for fname in files:
   		print fname


if __name__ == "__main__":
   sys.exit(main(sys.argv[1:]))
