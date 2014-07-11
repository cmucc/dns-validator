#!/bin/bash

# for prefix definitions see http://cr.yp.to/djbdns/tinydns-data.html

ZONEFILE=/Users/sroaj/Desktop/DB.club.cc.cmu.edu

IGNORE_PREFIX="(#|@|Z|:|'|&)"

PING_TIMEOUT=3

control_c()
{
  exit 1
}
trap control_c SIGINT

while read line; do
	first_char="${line:0:1}"
	if [[ ! "${first_char}" || "$first_char" =~ $IGNORE_PREFIX ]]; then
		continue;
	fi

	raw_record_line="${line:1}"
	record_name=
	record_maps_to=

	case "$first_char" in
	    "C" )
				#echo -n "Validating CNAME record "
				record_name=$(cut -d ':' -f 1 <<< "$raw_record_line")
				record_maps_to=$(cut -d ':' -f 2 <<< "$raw_record_line")
	        : ;;
	    "+" )
				#echo -n "Validating ip alias "
				record_name=$(cut -d ':' -f 1 <<< "$raw_record_line")
				record_maps_to=$(cut -d ':' -f 2 <<< "$raw_record_line")
	        : ;;
	    *) echo "Unknown prefix $first_char for $line"  ;;
	esac

##-------------------- mapping test using dig

	echo "Testing mapping of $record_name --> $record_maps_to."

	dig_output=$(dig +short "$record_name")

	while read -r dig_output_line; do
		if [[ "$dig_output_line" == "$record_maps_to" ]]; then

			# reverse lookup
			dig_output=$(dig +short "$record_name")
			if [ "x$dig_output" = "x" ]; then
				echo "+!+ Reverse lookup failed for $record_maps_to"
			fi
			dig_validated=true
		else 
			dig_validated=false
			break;
		fi
	done <<< "$dig_output"

	if [ ! $dig_validated ]; then 
		echo "dig output:"
		echo "$dig_output"
		echo "+!+ No dig record matches $record_maps_to"
		# read -p "Press [Enter] key to continue..." </dev/tty
	fi

	unset dig_validated
	unset dig_output_line
	unset dig_output

##-------------------- ping test

	#echo "Testing ping of $record_name with timeout of $PING_TIMEOUT"

	ping -c 3 -t $PING_TIMEOUT $record_name >> /dev/null

	if [ $? -ne 0 ]; then
		echo "+!+ Unable to ping $record_name";
		#read -p "Press [Enter] key to continue..." </dev/tty;
	fi

done < $ZONEFILE