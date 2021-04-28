#!/usr/bin/python3
import sys, argparse, pprint, re
import os.path
import warnings as w
from os import path

print("Start parsing file")
pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser( description = "parse db file" )
parser.add_argument( 'file', metavar='file name path',  help="give a file path to parse")
args = parser.parse_args()
args.file = os.path.abspath(args.file)


def main():
    if path.exists( args.file ) and path.getsize(args.file) > 1 :
        print("file exists " + args.file)
        #read file
    else:
        raise OSError(f"file[{args.file}] is missing")

    data = open_file(args.file);

    #a bit cleaning
    data = re.sub( r"#+?\s+", '####\n', data )
    data = re.sub( r"\s+#", '\n', data )
    split_data =[];
    split_data = data.split( sep='###' );

    for sdata in split_data:
        sdata = re.sub( '#', '', sdata );
        sdata = re.sub( r'\n+?', '\n', sdata );
        if not sdata or len(sdata) < 3:
            continue;
        m = re.search( r'\d{4}\/\d{2}\/\d{2}', sdata )
        t_date = '';
        if m:
            t_date = m.group

        print(f'show me split data[{sdata}] for date[{t_date}]');
    


def open_file(file):
    print(f"about to read file[{file}]")
    with open( file, 'r' ) as f:
       data = f.read();
    return data

main()
