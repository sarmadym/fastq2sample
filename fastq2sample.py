#!/opt/python/bin/python2.7
import sys
import getopt
import os
import ntpath
import re
import fnmatch


class Pair(object):
    def __init__(self, p1, p2):
        self.pe1 = p1
        self.pe2 = p2

    @staticmethod
    def find_pair(pair_array, pair):
        """Returns index of pair in pair_array (returns -1 when pair is not in pair_array)"""
        print "Looking for: ["+ pair.pe1 + ", " +pair.pe2 +"]"

        for current_pair in pair_array:
            print "current_pair: [" + current_pair.pe1 + ", " + current_pair.pe2 +"]"
            current_pair_pe1_root = current_pair.pe1[:current_pair.pe1.find("_pe1")]
            current_pair_pe2_root = current_pair.pe2[:current_pair.pe2.find("_pe2")]
            pair_pe1_root = pair.pe1[:pair.pe2.find("_pe1")]
            pair_pe2_root = pair.pe2[:pair.pe2.find("_pe2")]

            if (current_pair_pe1_root != "MISSING"  and current_pair_pe1_root == pair_pe1_root ) or \
                    ( current_pair_pe2_root != "MISSING" and current_pair_pe2_root == pair_pe2_root):
                return pair_array.index(current_pair)
            elif (current_pair_pe1_root != "MISSING"  and current_pair_pe2_root != "MISSING") and \
                    (current_pair_pe2_root == pair_pe1_root or current_pair_pe1_root == pair_pe2_root):
                return pair_array.index(current_pair)

        print "No Match! returning -1"
        return -1 # no match


class Sample(object):
    def __init__(self, sampleLabel):
        self.label = sampleLabel
        self.seq_array = [] # This list stores pairs of paths to paired end fastq files.

    def add_pair(self, p1, p2):
        self.seq_array.append(Pair(p1, p2))

    @staticmethod
    def find_sample(sample_array, label):
        """Returns index of the sample object in sample_array by comparing sample labels with label
        (returns -1 when sample_object is not in sample_array).
        """

        for sample in sample_array:
            if sample.label == label:
                return sample_array.index(sample)

        return -1 # no match



def usage():
    print "use: sample2fastq -p path-to-look-for-fastqs"

def sample_name(path):
    filename = ntpath.basename(path)
    sample_label = filename.partition('_')
    return sample_label[0]


def main(argv):

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
        include_files = [f for f in files if re.match(includes, f)]

    for file_path in include_files:

        print ""
        print "matched " + file_path

        sample_label = sample_name(file_path)
        print "Sample label found " + sample_label
        pair_to_add = Pair('MISSING','MISSING')


        current_sample = Sample(sample_label)
        pair_seen = 1

        if file_path.find('pe_1') >= 0 :
            current_sample.add_pair(file_path, 'MISSING')
            pair_to_add.pe1 = file_path
            pair_to_add.pe2 = 'MISSING'

        elif file_path.find('pe_2') >= 0 :
            current_sample.add_pair('MISSING',file_path)
            pair_to_add.pe2 = file_path
            pair_to_add.pe1 = 'MISSING'
            pair_seen = 2

        s_index= Sample.find_sample(samples, sample_label)
        if s_index < 0: #  This is a new sample, a new object has to be added
            samples.append(current_sample)
            print "New sample"+ current_sample.label + " added"
        else: # This sample has been already seen, we just need to add fastq pairs
            list_sample = samples[s_index]
            print "Sample "+sample_label +" is already in the list at position "+ str(s_index)

            p_index= Pair.find_pair(list_sample.seq_array, pair_to_add)
            if p_index < 0:
                list_sample.add_pair(pair_to_add.pe1,pair_to_add.pe2)
            else:
                if pair_seen == 1:
                    if list_sample.seq_array[p_index].pe1 == 'MISSING':
                        list_sample.seq_array[p_index].pe1 == pair_to_add.pe1
                    else:
                        print "WARNING: This sample has "+ \
                              list_sample.seq_array[p_index].pe1 +\
                              " as value for paired end 1.It is going to be replaced with " + \
                              pair_to_add.pe1
                        list_sample.seq_array[p_index].pe1 == pair_to_add.pe1

                if pair_seen == 2:
                    if list_sample.seq_array[p_index].pe2 == 'MISSING':
                        list_sample.seq_array[p_index].pe2 == pair_to_add.pe2

                    else:
                        print "WARNING: This sample has "+ \
                              list_sample.seq_array[p_index].pe2 +\
                              " as value for paired end 2.It is going to be replaced with " + \
                              pair_to_add.pe1
                        list_sample.seq_array[p_index].pe2 == pair_to_add.pe2
    print "DONE! LISTING WHAT WE FOUND NOW:"
    for s in samples:
        print s.label +":"
        for pair in s.seq_array:
            print "   Pair1:"+pair.pe1
            print "   Pair2:"+pair.pe2




if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
