 ip=$1
 x=`iperf3 -c $ip | tail -4 | head -2`
 u=`echo $x | cut -d ' ' -f7`
 d=`echo $x | cut -d ' ' -f8`

 echo $u $d
