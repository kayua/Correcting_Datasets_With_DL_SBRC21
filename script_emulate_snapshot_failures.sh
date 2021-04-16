#!/bin/bash

INPUT_FILE="0"
OUTPUT_FILE="0"
PROB="undef" # failure prob: must be expressed between [0,100]
SEED=1

while getopts hi:o:r:p: option; do
        case "${option}" in
                h)
                        echo "`basename $0`: emulates failure probability in a snapshot file";
                        echo "";
                        echo "     output is a snapshot file in the same format";
                        echo "";
                        echo "`basename $0`: args";
                        echo "  -i      input file";
                        echo "  -o      output file";
                        echo "  -r      random number generator seed";
                        echo "  -p      failure probability -  must be expressed between [0,100]";
                        echo "";
                        exit 0;
                        ;;
                i) INPUT_FILE=${OPTARG};;
                o) OUTPUT_FILE=${OPTARG};;
                r) SEED=${OPTARG};;
                p) PROB=${OPTARG};;
        esac;
done

if [ $INPUT_FILE = "0" ]; then
  echo "-i : Input file must be specified";
  exit 1;
fi;

if [ $OUTPUT_FILE = "0" ]; then
  echo "-o : Output file must be specified";
  exit 1;
fi;

if [ $PROB = "undef" ]; then
  echo "-p : Failure probability must be specified";
  exit 1;
fi;

# file format:
#window #time_min #IP:port #peerId #monitorId #monitor

# input random number generator seed
RANDOM=$SEED

DEBUG_FILE=${OUTPUT_FILE}.debug;

#cleanup
rm -f $DEBUG_FILE;
rm -f $OUTPUT_FILE;

# keep stats of number of peers within window, number of failed
curr_window=-1
count_peers=0;
count_failed=0;

echo "debug file is ${DEBUG_FILE}";
echo "output file is ${OUTPUT_FILE}";

while read line; do
	set -- $line;
	window=$1;

	failure=$((RANDOM%101));

	if [ $curr_window -ne $window ]; then
		if [ $curr_window -ne -1 ]; then
			echo "stat: window $curr_window: peers $count_peers failed $count_failed" >> ${DEBUG_FILE};
		fi;
		curr_window=$window;
		count_peers=0;
		count_failed=0;
	fi;

	let count_peers=count_peers+1;

	if [ $PROB -lt $failure  ]; then
		echo $line >> ${OUTPUT_FILE};
	else
		echo "peer $4 failed at window $1: $failure" >> ${DEBUG_FILE};
		let count_failed=count_failed+1;
	fi
done < <(tail -n+2 ${INPUT_FILE})
