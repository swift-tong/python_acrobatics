#!/system/bin/sh

def_gw=`busybox ip route |grep -i default |grep -i eth0| awk '{print $3}'`
echo "def_gw --- ($def_gw)"
if [ "$def_gw" = "" ]; then
   echo "---default gw not found, exit"
   exit
fi

mac=`busybox arp -a $def_gw |awk -F'at' '{print $2}'|awk '{print $1}'`
echo "mac --- ($mac)"

echo "(old):"
getprop persist.sys.StbUpGatewayMAC
setprop persist.sys.StbUpGatewayMAC $mac
echo "(new):"
getprop persist.sys.StbUpGatewayMAC
