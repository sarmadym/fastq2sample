#!/opt/python/bin/python2.7
import sys
import getopt
import os
import re
import fnmatch


class Pair:
    def __init__(self, p1, p2):
        self.pe1 = p1
        self.pe2 = p2


class Sample:
    def __init__(self, sampleLabel):
        self.label = sampleLabel
        self.seqArray = [] # This list stores pairs of paths to paired end fastq files.

    def addPair(self, p1, p2):
        self.seqArray.append(Pair(p1, p2))


def usage():
    print "use: sample2fastq -p path-to-look-for-fastqs"


def main(argv):
    """
     multi-line comment
     """
    try:
        path = os.getcwd()
        opts, args = getopt.getopt(argv, "hp:", ["help", "path="])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-p", "--path="):
                path = arg
        source = "".join(args)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    print ("Looking for fastq files in " + path)

    samples = []

    # include file extensions
    includes = ['*.fastq', '*.fastq.gz', '*.fq', '*.fq.gz']
    includes = r'|'.join([fnmatch.translate(x) for x in includes])

    for root, dirs, files in os.walk(path):
        files = [os.path.join(root, f) for f in files]
        incfiles = [f for f in files if re.match(includes, f)]

    for fname in incfiles:
        print "matched files:" + fname


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
