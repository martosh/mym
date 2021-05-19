#!/usr/bin/python3
import sys, argparse, re
import os.path
import warnings as w
#MariaDB driver
import mariadb as mdb
#read dir path
from os import path

##########################################################
# read created file with thoughts or taks and insert it db
##########################################################


parser = argparse.ArgumentParser( description = "parse db file" )
parser.add_argument( 'file', metavar='file name path',  help="give a file path to parse")
args = parser.parse_args()
args.file = os.path.abspath(args.file)
print(f"Start parsing file[{args.file}]")


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
    conn = db_conn('martosh', 'martosh' );
    print( 'here'); 
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

        prio = 0;
        p = re.compile('важно', re.I );

        if p.search( sdata):
            prio = 1;
            sdata = re.sub( r'Важно', '', sdata, flags=re.I);
        
        print(f'show me split data[{sdata}] for date[{thought_date}]');
        parsed_data = { "data": sdata, 'time': thought_date, 'prio': prio };
        insert_data( conn.cursor(), **parsed_data ); 

    conn.commit();
    conn.cursor().close();


###################
def open_file(file):
###################
    print(f"about to read file[{file}]")
    with open( file, 'r' ) as f:
       data = f.read();
    return data

#############################
# Connect to MariaDB Platform
#############################
#must be in file
def db_conn(dbuser, dbpass, dbname='mindata'):
   
    try:
        conn = mdb.connect(
                user=dbuser,
                password=dbpass,
                host="127.0.0.1",
                port=3306,
                database=dbname,
                )

    except mdb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    else:
        print(f"Connected to DB");

    #cursor 
    return conn

###################
def insert_data(cursor, data, time, prio):
###################
    # do some formatting  
    time = re.sub( r'[^\d]', '', time ); 
    data = data.strip();
    data = re.sub( r'\s\s*', ' ', data);

    if not data:
        return;

    if not time:
        time = 0;

    print(f"start insert_data with params data[{data}] time[{time}] pri[{prio}]");
        
    values = ( time, '1200', prio, data );

    query = "INSERT INTO thoughts(create_date, create_time, importance, data) VALUES(%s,%s,%s,%s)";
    cursor.execute( query, values );

    if cursor.lastrowid:
        print( "show me last inserted id ", cursor.lastrowid );
    else:
        print( "insert id not found!");

    #insert data from dict



################
# execution
################
main()
