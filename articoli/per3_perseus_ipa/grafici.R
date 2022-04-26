require(ggplot2)
library(ggpubr)
setwd("/home/pi/lavori/emanuela/e14/")
data<-read.csv("Elaborazione14.csv",sep=";",dec=",")
p1<-ggplot(data=data, aes(x=reorder(Elemento,VAR.), y=X1)) +
  geom_bar(stat="identity",fill="#3366ff")+
  labs (x="",y="Factor 1")+
  theme(axis.text.x=element_blank(),text = element_text(size = 46)) 
#theme(axis.text.x = element_text(angle = 90, vjust = .5, hjust=1))
png(filename="graph_f1.png", width=1000, height=500)
p1
dev.off()
p2<-ggplot(data=data, aes(x=reorder(Elemento,VAR.), y=X2)) +
  geom_bar(stat="identity",fill="#ff3333")+
  labs (x="",y="Factor 2")+
  theme(axis.text.x=element_blank(),text = element_text(size = 46)) 
#theme(axis.text.x = element_text(angle = 90, vjust = .5, hjust=1))
png(filename="graph_f2.png", width=1000, height=500)
p2
dev.off()
p3<-ggplot(data=data, aes(x=reorder(Elemento,VAR.), y=X3)) +
  geom_bar(stat="identity",fill="#33aa33")+
  labs (x="",y="Factor 3")+
  theme(text = element_text(size = 46), axis.text.x = element_text(angle = 90, vjust = .5, hjust=1))
#  theme(axis.text.x=element_blank())
png(filename="graph_f3.png", width=1000, height=500)
p3
dev.off()
p4<-ggplot(data=data, aes(x=reorder(Elemento,VAR.), y=X4)) +
  geom_bar(stat="identity",fill="#ff33ff")+
  labs (x="",y="Fattore 4")+
  theme(axis.text.x = element_text(angle = 90, vjust = .5, hjust=1))
  #theme(axis.text.x=element_blank())
png(filename="graph_f4.png", width=1000, height=500)
p4
dev.off()
p5<-ggplot(data=data, aes(x=reorder(Elemento,VAR.), y=X5)) +
  geom_bar(stat="identity",fill="#33aaaa")+
  labs (x="",y="Fattore 5")+
  theme(axis.text.x = element_text(angle = 90, vjust = .5, hjust=1))
png(filename="graph_f5.png", width=1000, height=500)
p5
dev.off()

png(filename="3_fattori.png", width=2000, height=1800)
ggarrange (p1,p2,p3, ncol=1, nrow=3, heights=c(3,3,5))
dev.off()

  data<-read.csv("Elaborazione14_mappa.csv",sep=";",dec=",")

write.table(df,file="f1.xyz",col.names = FALSE, row.names = FALSE, sep=" ")
df<-data.frame(data$long,data$lat,data$X2)
write.table(df,file="f2.xyz",col.names = FALSE, row.names = FALSE, sep=" ")
df<-data.frame(data$long,data$lat,data$X3)
write.table(df,file="f3.xyz",col.names = FALSE, row.names = FALSE, sep=" ")
df<-data.frame(data$long,data$lat,data$X4)
write.table(df,file="f4.xyz",col.names = FALSE, row.names = FALSE, sep=" ")
df<-data.frame(data$long,data$lat,data$X5)
write.table(df,file="f5.xyz",col.names = FALSE, row.names = FALSE, sep=" ")


