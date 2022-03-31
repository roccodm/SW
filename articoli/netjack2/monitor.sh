echo "cpu_usr;cpu_nice;cpu_sys;cpu_iowait;cpu_irq;cpu_soft;cpu_steal;cpu_guest;cpu_gnice;cpu_idle;net_rx_ok;net_rx_err;net_rx_drp;net_rx_ovr;net_tx_ok;net_tx_err;net_tx_drp;net_tx_ovr;net_flag;mem_total;mem_used;mem_free;mem_shared;mem_buff;mem_av;top_pr;top_ni;top_virt;top_res;top_shr;top_cpu;top_mem"
while test 1
do

cpustat=`mpstat |grep "all"|sed s/','/'.'/g`
cpu_usr=`echo $cpustat | cut -f3 -d" "`
cpu_nice=`echo $cpustat | cut -f4 -d" "`
cpu_sys=`echo $cpustat | cut -f5 -d" "`
cpu_iowait=`echo $cpustat | cut -f6 -d" "`
cpu_irq=`echo $cpustat | cut -f7 -d" "`
cpu_soft=`echo $cpustat | cut -f8 -d" "`
cpu_steal=`echo $cpustat | cut -f9 -d" "`
cpu_guest=`echo $cpustat | cut -f10 -d" "`
cpu_gnice=`echo $cpustat | cut -f11 -d" "`
cpu_idle=`echo $cpustat | cut -f12 -d" "`




net=`netstat -i |grep eth0`
net_rx_ok=`echo $net|cut -f3 -d" "`
net_rx_err=`echo $net|cut -f4 -d" "`
net_rx_drp=`echo $net|cut -f5 -d" "`
net_rx_ovr=`echo $net|cut -f6 -d" "`
net_tx_ok=`echo $net|cut -f7 -d" "`
net_tx_err=`echo $net|cut -f8 -d" "`
net_tx_drp=`echo $net|cut -f9 -d" "`
net_tx_ovr=`echo $net|cut -f10 -d" "`
net_flag=`echo $net|cut -f11 -d" "`

mem=`free | grep "Mem"`
mem_total=`echo $mem|cut -f2 -d" "`
mem_used=`echo $mem|cut -f3 -d" "`
mem_free=`echo $mem|cut -f4 -d" "`
mem_shared=`echo $mem|cut -f5 -d" "`
mem_buff=`echo $mem|cut -f6 -d" "`
mem_av=`echo $mem|cut -f7 -d" "`

top=`top -b -n 1 |grep jackd|sed s/","/"."/g`

top_pr=`echo $top|cut -f3 -d" "`
top_ni=`echo $top|cut -f4 -d" "`
top_virt=`echo $top|cut -f5 -d" "`
top_res=`echo $top|cut -f6 -d" "`
top_shr=`echo $top|cut -f7 -d" "`
top_cpu=`echo $top|cut -f9 -d" "`
top_mem=`echo $top|cut -f10 -d" "`



echo "$cpu_usr;$cpu_nice;$cpu_sys;$cpu_iowait;$cpu_irq;$cpu_soft;$cpu_steal;$cpu_guest;$cpu_gnice;$cpu_idle;$net_rx_ok;$net_rx_err;$net_rx_drp;$net_rx_ovr;$net_tx_ok;$net_tx_err;$net_tx_drp;$net_tx_ovr;$net_flag;$mem_total;$mem_used;$mem_free;$mem_shared;$mem_buff;$mem_av;$top_pr;$top_ni;$top_virt;$top_res;$top_shr;$top_cpu;$top_mem"
sleep 10s
done
