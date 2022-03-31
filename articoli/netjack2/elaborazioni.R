library(ggplot2)
library(ggpubr)
# Ping test
ping<-read.csv("/home/pi/lavori/lucchetti/delfi/articolo_netjack2/dataset_ping.csv",sep=";",dec=",")

ping_graph<-ggplot(ping,aes(x=test,y=ping_mean)) +
   geom_point()+
   geom_point(aes(y=ping_min), shape=1)+
   geom_point(aes(y=ping_max), shape=1)+
   geom_errorbar(aes(ymin=ping_mean-ping_std/2, ymax=ping_mean+ping_std/2),width=.15,
                 position=position_dodge(0.05)) +
   labs (x="",y="Round trip time (ms)")+
   scale_y_continuous(breaks = seq(0, 12, by = 1))
   #ggtitle("Ping flood tests")

ping_graph

library(jsonlite)

files=c(
  "/home/pi/lavori/lucchetti/delfi/articolo_netjack2/test_ridracoli/test_land.log",
  "/home/pi/lavori/lucchetti/delfi/articolo_netjack2/test_ridracoli/test1.log",
  "/home/pi/lavori/lucchetti/delfi/articolo_netjack2/test_ridracoli/test4.log"
)


tcp_long<-data.frame()
udp_long<-data.frame()

i=1
for (myfile in files){
  mydata<-read_json(myfile, simplifyDataFrame = TRUE)
  for (element in mydata[["tcp_long_100"]][["intervals"]][["streams"]])
  {
    tcp_long<-rbind(tcp_long,(cbind(t=i, mb=100,as.data.frame(element))))
  }
  for (element in mydata[["tcp_long_300"]][["intervals"]][["streams"]])
  {
    tcp_long<-rbind(tcp_long,(cbind(t=i, mb=300,as.data.frame(element))))
  }
  for (element in mydata[["udp_long_100"]][["intervals"]][["streams"]])
  {
    udp_long<-rbind(udp_long,(cbind(t=i, mb=100,as.data.frame(element))))
  }
  for (element in mydata[["udp_long_300"]][["intervals"]][["streams"]])
  {
    udp_long<-rbind(udp_long,(cbind(t=i, mb=300,as.data.frame(element))))
  }
  
  i=i+1
}
tcp=data.frame(t=as.factor(tcp_long$t), Mbps=as.factor(tcp_long$mb) , v=as.integer(tcp_long$bits_per_second/2^20))
ggplot(tcp, aes(x=t, y=v, fill=Mbps)) + 
  geom_boxplot() +
  labs (x="Test",y="Mbps",fill="Test type (Mbps)")+
  ggtitle("TCP Summary report")  

stream=subset(tcp,Mbps==100)
stream$x=1:nrow(stream)
stream=rbind(stream,cbind(subset(tcp,Mbps==300),x=1:nrow(stream)))


g_a<-ggplot(rbind(stream[1:30,],stream[91:120,]), aes(x=x, y=v, color=Mbps)) + 
  geom_line() +
  labs (x="seconds",y="Mbps",fill="Test type (Mbps)")+
  ggtitle("Land test")+ theme(legend.position = "none")  
g_b<-ggplot(rbind(stream[31:60,],stream[121:150,]), aes(x=x-30, y=v, color=Mbps)) + 
  geom_line() +
  labs (x="seconds",y="Mbps",fill="Test type (Mbps)")+
  ggtitle("Test 1")+ theme(legend.position = "none")  
g_c<-ggplot(rbind(stream[61:90,],stream[151:180,]), aes(x=x-60, y=v, color=Mbps)) + 
  geom_line() +
  labs (x="seconds",y="Mbps",color="Test type")+
  ggtitle("Test 2")  
tests<-ggarrange(g_a,g_b,g_c, ncol=3, nrow=1)
tests
#udp=data.frame(t=as.factor(udp_long$t), Mbps=as.factor(udp_long$mb) , v=as.integer(udp_long$bits_per_second/2^20))
#ggplot(udp, aes(x=t, y=v, fill=Mbps)) + 
#  geom_boxplot() +
#  labs (x="Test",y="Mbps",fill="Test type (Mbps)")+
#  ggtitle("UDP Summary report")+
#  ylim(80,100)

g_cpu=vector('list', 4)
g_mem=vector('list', 4)
g_net=vector('list', 4)
id=1

for (elab in c("1ch_96kSps","2ch_96kSps","1ch_192kSps","2ch_192kSps")){
   report=read.csv(paste("/home/pi/lavori/lucchetti/delfi/articolo_netjack2/",elab,sep=""),sep=";",dec=".")
   data<-report[1:240,]
   cpu_data<-data.frame()
   cpu_data<-rbind(cpu_data,data.frame(t="jackd %cpu",x=1:240,y=data$top_cpu/4))
   cpu_data<-rbind(cpu_data,data.frame(t="%cpu usr",x=1:240,y=data$cpu_usr))
   cpu_data<-rbind(cpu_data,data.frame(t="%cpu soft",x=1:240,y=data$cpu_soft))
   cpu_data<-rbind(cpu_data,data.frame(t="%cpu sys",x=1:240,y=data$cpu_sys))
   cpu_data<-rbind(cpu_data,data.frame(t="%cpu irq",x=1:240,y=data$cpu_irq))
   cpu_data<-rbind(cpu_data,data.frame(t="%cpu iowait",x=1:240,y=data$cpu_iowait))
   g_cpu[[id]]<-local({
      id <- id
      p<-ggplot(cpu_data, aes(x=x ,y=y, color=t))+
         labs (x="Time (x10 sec)",y="Cpu usage (%)",color="Value")+
         geom_line()+
         ggtitle(elab)+
         scale_y_continuous(limits=c(0,6))
      if (id<4) {p<-p+ theme(legend.position = "none") }
      if (id>1) {p<-p+ labs (y="")}
      print(p)
   })     

   mem_total<-max(data$mem_total)
   mem_data<-data.frame()
   mem_data<-rbind(mem_data,data.frame(t="mem used",x=1:240,y=data$mem_used/1024))
   mem_data<-rbind(mem_data,data.frame(t="mem free",x=1:240,y=data$mem_free/1024))
   mem_data<-rbind(mem_data,data.frame(t="mem shared",x=1:240,y=data$mem_shared/1024))
   mem_data<-rbind(mem_data,data.frame(t="mem buffered",x=1:240,y=data$mem_buff/1024))
   g_mem[[id]]<-local({
     id <- id
     p<-ggplot(mem_data, aes(x=x ,y=y, color=t))+
       labs (x="Time (x10 sec)",y="RAM usage (MB)",color="Value")+
       geom_line()+
       ggtitle(elab)
     if (id<4) {p<-p+ theme(legend.position = "none") }
     if (id>1) {p<-p+ labs (y="")}
     print(p)
   })     

   eth_data<-data.frame()
   tx=array()
   for (i in 2:nrow(data)){
      tx[i-1]=(data$net_tx_ok[i]-data$net_tx_ok[i-1])  
   }
   rx=array()
   for (i in 2:nrow(data)){
      rx[i-1]=(data$net_rx_ok[i]-data$net_rx_ok[i-1])  
   }

   eth_data<-rbind(eth_data,data.frame(t="tx",x=1:239,y=tx))
   eth_data<-rbind(eth_data,data.frame(t="rx",x=1:239,y=rx))
   g_net[[id]]<-local({
     id <- id
     p<-ggplot(eth_data, aes(x=x ,y=y, color=t))+
       labs (x="Time (x10 sec)",y="Network usage (kbps)",color="Value")+
       geom_line()+
       ggtitle(elab)+
       scale_y_continuous(limits=c(2000,20000))
     if (id<4) {p<-p+ theme(legend.position = "none") }
     if (id>1) {p<-p+ labs (y="")}
     print(p)
   })     
   print(id)
   id=id+1
}

gr<-ggarrange(g_cpu[[1]],g_cpu[[2]],g_cpu[[3]], g_cpu[[4]], ncol=4, nrow=1, widths=c(4,4,4,5.72))
gr

gr<-ggarrange(g_mem[[1]],g_mem[[2]],g_mem[[3]], g_mem[[4]], ncol=4, nrow=1, widths=c(4,4,4,5.72))
gr

gr<-ggarrange(g_net[[1]],g_net[[2]],g_net[[3]], g_net[[4]], ncol=4, nrow=1, widths=c(4,4,4,4.7))
gr



