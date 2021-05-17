#!/usr/bin/python3
import sys, argparse, pprint, re
import os.path
import warnings as w
import mariadb as mdb
from os import path

print("Start parsing file")
pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser( description = "parse db file" )
parser.add_argument( 'file', metavar='file name path',  help="give a file path to parse")
args = parser.parse_args()
args.file = os.path.abspath(args.file)

db_user_passwd = 'martosh';

# Connect to MariaDB Platform
try:
    conn = mdb.connect(
        user="martosh",
        password=db_user_passwd,
        host="127.0.0.1",
        port=3306,
        database="mindata"

    )

except mdb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

###################
def main():
###################
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

    parsed_data = {};

    for sdata in split_data:
        sdata = re.sub( '#', '', sdata );
        sdata = re.sub( r'\n+?', '\n', sdata );
        if not sdata or len(sdata) < 3:
            continue;
        m = re.findall( r'\d{4}\/\d{2}\/\d{2}', sdata )
        thought_date = '';
        if m:
            thought_date = m[0];
            #remove date from sdata
            sdata = re.sub( r'\d{4}\/\d{2}\/\d{2}', '', sdata );

        p = re.compile( r'важно', re.I );

        prio = 0;

        if p.search( sdata):
            prio = 1;
            sdata = re.sub( r'Важно', '', sdata, flags=re.I);
        
        #print(f'show me split data[{sdata}] for date[{thought_date}]');
        parsed_data = { "data": sdata, 'time': thought_date, 'prio': prio };
        insert_data( **parsed_data ); 


###################
def open_file(file):
###################
    print(f"about to read file[{file}]")
    with open( file, 'r' ) as f:
       data = f.read();
    return data

###################
def insert_data(data, time, prio):
    print(f"start insert_data with params data[{data}] time[{time}] pri[{prio}]");
    input();
###################
    #insert data from dict

main()
