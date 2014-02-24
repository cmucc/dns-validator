# Tiny-DNS Validator

This is a simple validator for [Tiny-DNS](http://cr.yp.to/djbdns/tinydns.html)
config files. It checks for the following properties:

- Lines begin with '+' is in the format *hostname*:*ipaddr*[:*TTL*].
- Lines begin with 'C' is in the format *hostname*:*hostname*[:*TTL*].
- The file ends with a newline.
- Ignores lines begin with characters in `IGNORE_PREFIX`.

There are two implementations, `ValidateZoneFile.py` and `ValidateZoneFile.sh`.
The python implementation is a lot faster than the bash script implementation
and is more robust, so please use that one whenever possible.
