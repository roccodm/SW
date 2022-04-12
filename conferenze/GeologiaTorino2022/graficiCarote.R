library(ggplot2)
#library(ggpmisc) 

library(ggpubr)

setwd("/home/pi/lavori/Federico/per3carote/")

ds1cm<-read.csv(file="carote_1cm.csv",sep=";",dec=",")
ds03cm<-read.csv(file="carote_0.3cm.csv",sep=";",dec=",")

for (i in 2:length(ds1cm)){
    fieldname<-colnames(ds1cm[i])
    print(fieldname)
    mytable<-data.frame(y=as.vector(ds1cm[1]),x=as.vector(ds1cm[i]))  
    mytable2<-data.frame(y=as.vector(ds03cm[1]),x=as.vector(ds03cm[i]))  
    pl<-ggplot(NULL)+
      geom_line(aes(x=mytable[,1],y=mytable[,2]),col="darkblue")+
      geom_line(aes(x=mytable2[,1],y=mytable2[,2]),col="darkorange")+
      coord_flip()+
      scale_x_reverse()+
      scale_y_continuous(position = "right")+
      labs(x = "Depth (cm)", y = fieldname)
    
    mytable[,2]<-round(mytable[,2],digits=2)
    mytable2[,2]<-round(mytable2[,2],digits=2)
    
    colnames(mytable)<-c("Depth (cm)", fieldname)
    colnames(mytable2)<-c("Depth (cm)", fieldname)
    
    tab<-ggtexttable(mytable,rows=NULL,theme = ttheme(base_size = 8))
    tab <- tab %>%
      tab_add_title(text = "1 cm", face = "bold", size=10)
    tab2<-ggtexttable(mytable2,rows=NULL,theme = ttheme(base_size = 8))
    tab2 <- tab2 %>%
      tab_add_title(text = "0.3 cm", face = "bold", size=10)

    plt<-ggarrange(pl,tab2,tab,nrow=1,ncol=3, align="h",widths=c(5,1.5,1.5))
    
    fname=paste(fieldname,"png",sep=".")
    print(fname)
    png(filename="pippo.png", width=1200, height=1000)
    pl
    dev.off()
}
warnings()

dev.off()
