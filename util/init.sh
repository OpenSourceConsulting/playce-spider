# /etc/spider/init.sh
# Vyatta VM Initial Provisioning Script

IFCFG=`/sbin/ifconfig -a`
ROUTE=`netstat -nr`
VBASH=`vbash --version`
UNAME=`uname -a`

cat > /tmp/init.sh.tmp << EOF
### IFCONFIG
$IFCFG
### ROUTE
$ROUTE
### VBASH
$VBASH
### UNAME
$UNAME
### END
EOF

curl -X POST -H "Content-Type: text/plain" http://spider-controller:5001/vmreg --data-binary @/tmp/init.sh.tmp

rm /tmp/init.sh.tmp

