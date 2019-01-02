#!/system/bin/sh

echo "definition:"
echo "   check period    --- 5min(300sec)"
echo "   check interval  --- 5second"
echo "   check cpu thres --- 80%"
echo "output:"
echo "   value    --- cpu overload(>=80%) time(seconds) in 5min"

check="check"
sleeptime=5
while [ "$check" = "check" ]
do
    index=0
    cpucount=0
    while [ "$index" -lt 60 ]
    do
        a=`busybox top -n 1 |awk '{if($0~"CPU:")print}' |awk  'BEGIN{FS="idle"} {print $1}' |awk  '{print $NF}' |awk  'BEGIN{FS="%"} {print $1}'|awk -F\. '{print $1}'`
        let "index=index+1"
        if [ $a -le 20 ];then
            let "cpucount=cpucount+1"
            echo $index --- $a --- cpucount = $cpucount
        else
            echo $index --- $a
        fi
        sleep $sleeptime
    done
    ((value=$cpucount*sleeptime))
    echo value --- $value
    setprop persist.sys.StbCpuUseRatePeak $value
done

