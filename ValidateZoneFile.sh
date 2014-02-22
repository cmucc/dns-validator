#!/bin/bash

# for prefix definitions see http://cr.yp.to/djbdns/tinydns-data.html

ZONEFILE="$1"

IGNORE_PREFIX="(#|@|Z|:|'|&)"

validate_name() {
	if [[ $1 =~ " " ]]; then
		errmsg="cannot have spaces in hostname"
		return 1
	fi
	for word in $(echo $1 | tr '.' ' '); do
		if ! [[ $word =~ [a-zA-Z0-9]+ ]]; then
			errmsg="hostname \"$1\" contains invalid character"
			return 1
		fi
	done
}

validate_ipbyte() {
	[ $1 -ge 0 ] && [ $1 -le 255 ]
	if [ $? -ne 0 ]; then
		errmsg="number in ip address must be between 0~255"
		return 1
	fi
}

validate_ipaddr() {
	if [[ "$1" =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
		b1=${BASH_REMATCH[1]}
		b2=${BASH_REMATCH[2]}
		b3=${BASH_REMATCH[3]}
		b4=${BASH_REMATCH[4]}
		validate_ipbyte $b1 \
			&& validate_ipbyte $b2 \
			&& validate_ipbyte $b3 \
			&& validate_ipbyte $b4
		return $?
	else
		errmsg="incorrect ip address: $1"
		return 1
	fi
}

validate_integer() {
	if [[ ! $1 =~ ^[0-9]+$ ]]; then
		errmsg="incorrect integer: $1"
		return 1
	fi
}

lineno=0
cat $ZONEFILE | while read line; do
	lineno=$((lineno+1))
	first_char="${line:0:1}"
	if [[ ! "${first_char}" || "$first_char" =~ $IGNORE_PREFIX ]]; then
		continue;
	fi

	raw_record_line="${line:1}"
	record_name=
	record_maps_to=
	# strip comments
	raw_record_line=$(echo "$line" | sed 's/[ \t][ \t]*#.*$//g')

	case "$first_char" in
		"C" )
			#echo -n "Validating CNAME record "
			record_name=$(cut -d ':' -f 1 <<< "$raw_record_line")
			record_maps_to=$(cut -d ':' -f 2 <<< "$raw_record_line")
			number=$(cut -d ':' -f 3 <<< "$raw_record_line")
			if [ -z "$number" ]; then number=0; fi
			validate_name "$record_name" && validate_name "$record_maps_to" \
				&& validate_integer "$number"
			;;
		"+" )
			#echo -n "Validating ip alias "
			record_name=$(cut -d ':' -f 1 <<< "$raw_record_line")
			record_maps_to=$(cut -d ':' -f 2 <<< "$raw_record_line")
			number=$(cut -d ':' -f 3 <<< "$raw_record_line")
			if [ -z "$number" ]; then number=0; fi
			validate_name "$record_name" && validate_ipaddr "$record_maps_to" \
				&& validate_integer "$number"
			;;
		*) echo "Unknown prefix $first_char for $line"
			false
			;;
	esac
	if [ $? -ne 0 ]; then
		echo "error: line $lineno: $errmsg"
	fi
done
