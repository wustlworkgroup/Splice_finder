import numpy as np
import os
import argparse


parser = argparse.ArgumentParser(description="Select gene splice area and generate labels.")
parser.add_argument("input_seq", type=str, help="gene exons file path")
parser.add_argument("Out_path", type=str, help="Output directory for generated files")
args = parser.parse_args()

def encode(seq):
    encoded_seq = np.zeros(1600,int)
    for j in range(400):
        if seq[j] == 'A' or seq[j] == 'a':
            encoded_seq[j*4] = 1
            encoded_seq[j*4+1] = 0
            encoded_seq[j*4+2] = 0
            encoded_seq[j*4+3] = 0

        elif seq[j] == 'C' or seq[j] == 'c':
            encoded_seq[j*4] = 0
            encoded_seq[j*4+1] = 1
            encoded_seq[j*4+2] = 0
            encoded_seq[j*4+3] = 0

        elif seq[j] == 'G' or seq[j] == 'g':
            encoded_seq[j*4] = 0
            encoded_seq[j*4+1] = 0
            encoded_seq[j*4+2] = 1
            encoded_seq[j*4+3] = 0

        elif seq[j] == 'T' or seq[j] == 't':
            encoded_seq[j*4] = 0
            encoded_seq[j*4+1] = 0
            encoded_seq[j*4+2] = 0
            encoded_seq[j*4+3] = 1

        else:
            encoded_seq[j*4] = 0
            encoded_seq[j*4+1] = 0
            encoded_seq[j*4+2] = 0
            encoded_seq[j*4+3] = 0

    return encoded_seq

        
       



def main():
    
    i = 0
  
    input_path=args.input_seq 
    output=args.Out_path
    output_file=os.path.join(output,'encoded_seq')

    encoded_f = open(output_file, 'w')
           
    seq_file = open(input_path,'r')


    for line in seq_file:
        seq = line
        encoded_seq = encode(seq)
        for base in encoded_seq:
            encoded_f.write(str(base))
            encoded_f.write("   ")
        encoded_f.write("\n")

        i=i+1
        print(i)
    seq_file.close()



    encoded_f.close()

if __name__ =='__main__':
    main()
