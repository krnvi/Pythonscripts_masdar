#!/usr/bin/python

import numpy as np ; import datetime as dt ; from dateutil import tz ; 
import matplotlib.pyplot as plt; import seaborn as sns ;


main='/home/vkvalappil/Data/' ; date='2017060806'


#gsiFile=main+'modelWRF/ARW/output/GFS_ENKF/gsi_opp/newBe/cv5_newbe_1_MJ/hourly'+date+'_d02.csv'
gsiFile=main+'modelWRF/oppModel/ARW/output/hourly'+date+'_d02.csv'

nogFile=main+'modelWRF_2/ARW/output/no_gsi_0.25/hourly'+date+'_d02.csv'

lstFile=main+'modelWRF/scripts/master_uae.csv'

lst_f=np.genfromtxt(lstFile,delimiter=',',dtype='S')
g_data=np.genfromtxt(gsiFile,delimiter=',',dtype='S') ; ng_data=np.genfromtxt(nogFile,delimiter=',',dtype='S')

for ii in range(0,lst_f.shape[0]) : 
    tid=lst_f[ii,0] ; locNme=lst_f[ii,-1]  ; 
    g_req_data=g_data[np.where(g_data[:,0]==tid)[0],:]    
    ng_req_data=ng_data[np.where(ng_data[:,0]==tid)[0],:]    
 
    f_date=g_req_data[:,3][::24] ; date_1=dt.datetime.strptime(f_date[0],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
    date_2=dt.datetime.strptime(f_date[1],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d') ; 
    date_3=dt.datetime.strptime(f_date[2],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d');
    
    rs_file_1='/home/vkvalappil/Data/metarData/'+date[0:6]+'/'+locNme+'_'+date_1+'.csv'
    rs_file_2='/home/vkvalappil/Data/metarData/'+date[0:6]+'/'+locNme+'_'+date_2+'.csv'
    rs_file_3='/home/vkvalappil/Data/metarData/'+date[0:6]+'/'+locNme+'_'+date_3+'.csv' 
    
    rs_data_1=np.genfromtxt(rs_file_1,delimiter=',',dtype='S')
    rs_data_2=np.genfromtxt(rs_file_2,delimiter=',',dtype='S')
    rs_data_3=np.genfromtxt(rs_file_3,delimiter=',',dtype='S')
    
    rs_data=np.concatenate([rs_data_1[1:,:],rs_data_2[1:,:],rs_data_3[1:,:]],axis=0)    
    
    from_zone = tz.gettz('Asia/Dubai') ; to_zone = tz.gettz('UTC') ;
    date_list=np.array([(dt.datetime.strptime(x,'%Y-%m-%d %H:%M:%S')).replace(tzinfo=from_zone).astimezone(to_zone).strftime('%Y-%m-%d %H:%M') for x in g_req_data[:,3]]); 
    rs_req_data=rs_data[np.where(np.in1d(rs_data[:,1],date_list))[0],:]    
    
##################################################Temperature ##########################################################################################    
    l_idx=48 ; outFile=main+'modelWRF/ARW/output/gsi_plots/temperature_2m_'+locNme+date
    data_1=g_req_data[0:l_idx,5].astype(float) ; data_2=ng_req_data[0:l_idx,5].astype(float) ; obs=rs_req_data[0:l_idx,4].astype(float)
    
    fig=plt.figure(figsize=(14,6),dpi=50); ax = fig.add_subplot(111,axisbg='white')
    sns.set(style='ticks') ; 

    pos_1  = np.arange(0,len(data_1),1) ;  ax.hold(True); wdh=4
    
    
    ax.plot(pos_1,data_1,'blue',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='GSI DA')


    ax.plot(pos_1,data_2,'red',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='red',markeredgecolor='red',label='NO GSI')


    ax.plot(pos_1,obs,'black',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='black',markeredgecolor='black',label='OBS')

    ax.xaxis.set_ticks_position('bottom')  ; ax.yaxis.set_ticks_position('left') ;

    ax.spines['bottom'].set_color('black') ; ax.spines['right'].set_color('black') ;
    ax.spines['top'].set_color('black')    ; ax.spines['left'].set_color('black') ;     
 
 

    ax.set_yticks(np.arange(min(obs)-3,max(obs)+3,3.0))


    ax.set_xticks(pos_1[::4]) ; xTickMarks=date_list[0:l_idx][::4]
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=90, fontsize=6,family='sans-serif')
   

    ax.tick_params(axis='x', colors='black',labelsize=18) ; ax.tick_params(axis='y', colors='black',labelsize=18)

    #ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)
    ax.set_ylabel('Temperature ',color='black',fontsize=14) ;  
    ax.set_xlabel('Date ',color='black',fontsize=14) ;  

    #Get artists and labels for legend and chose which ones to display
    handles, labels = ax.get_legend_handles_labels()
    display = (0,1,2)

    #Create custom artists
    simArtist = plt.Line2D((0,1),(0,0), color='blue', marker='o', linestyle='')
    anyArtist = plt.Line2D((0,1),(0,0), color='k')

    #Create legend from custom artist/label lists
    leg=ax.legend([handle for i,handle in enumerate(handles) if i in display]+[simArtist,anyArtist],
          [label for i,label in enumerate(labels) if i in display],loc=1,bbox_to_anchor=(-0.05, 0.9, 1., .102),frameon=1,fontsize=18)

    frame = leg.get_frame() ; frame.set_facecolor('white')
#################################################################################################################

    #titl='Temperature '
    #plt.title(titl,color='black',fontsize=25,y=1.05)
    plt.tight_layout(h_pad=3) ; 
    plt.savefig(outFile);
    plt.close(fig) ; fig.clf(fig)  
    
##########################################Relative Hum #############################################################    
    
    outFile=main+'modelWRF/ARW/output/gsi_plots/rh_2m_'+locNme+date 
    data_1=g_req_data[0:l_idx,7].astype(float) ; data_2=ng_req_data[0:l_idx,7].astype(float) ; obs=np.round(rs_req_data[0:l_idx,6].astype(float))
    
    fig=plt.figure(figsize=(14,6),dpi=50); ax = fig.add_subplot(111,axisbg='white')
    sns.set(style='ticks') ; 

    pos_1  = np.arange(0,len(data_1),1) ;  ax.hold(True); wdh=4
    
    
    ax.plot(pos_1,data_1,'blue',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='GSI DA')


    ax.plot(pos_1,data_2,'red',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='red',markeredgecolor='red',label='NO GSI')


    ax.plot(pos_1,obs,'black',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='black',markeredgecolor='black',label='OBS')

    ax.xaxis.set_ticks_position('bottom')  ; ax.yaxis.set_ticks_position('left') ;

    ax.spines['bottom'].set_color('black') ; ax.spines['right'].set_color('black') ;
    ax.spines['top'].set_color('black')    ; ax.spines['left'].set_color('black') ;     
 
 
    
    ax.set_yticks(np.arange(0,100,5.0))


    ax.set_xticks(pos_1[::4]) ; xTickMarks=date_list[0:l_idx][::4]
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=90, fontsize=6,family='sans-serif')
   

    ax.tick_params(axis='x', colors='black',labelsize=18) ; ax.tick_params(axis='y', colors='black',labelsize=18)

    #ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)
    ax.set_ylabel('Relative Humidity ',color='black',fontsize=14) ;  
    ax.set_xlabel('Date ',color='black',fontsize=14) ;  

    #Get artists and labels for legend and chose which ones to display
    handles, labels = ax.get_legend_handles_labels()
    display = (0,1,2)

    #Create custom artists
    simArtist = plt.Line2D((0,1),(0,0), color='blue', marker='o', linestyle='')
    anyArtist = plt.Line2D((0,1),(0,0), color='k')

    #Create legend from custom artist/label lists
    leg=ax.legend([handle for i,handle in enumerate(handles) if i in display]+[simArtist,anyArtist],
          [label for i,label in enumerate(labels) if i in display],loc=1,bbox_to_anchor=(-0.05, 0.9, 1., .102),frameon=1,fontsize=18)

    frame = leg.get_frame() ; frame.set_facecolor('white')
#################################################################################################################

    #titl='Temperature '
    #plt.title(titl,color='black',fontsize=25,y=1.05)
    plt.tight_layout(h_pad=3) ; 
    plt.savefig(outFile);
    plt.close(fig) ; fig.clf(fig)  
    
###################################################Dew temp ######################################################    
    outFile=main+'modelWRF/ARW/output/gsi_plots/dewtemp_2m_'+locNme+date 
    data_1=g_req_data[0:l_idx,6].astype(float) ; data_2=ng_req_data[0:l_idx,6].astype(float) ; obs=np.round(rs_req_data[0:l_idx,5].astype(float))
    
    fig=plt.figure(figsize=(14,6),dpi=50); ax = fig.add_subplot(111,axisbg='white')
    sns.set(style='ticks') ; 

    pos_1  = np.arange(0,len(data_1),1) ;  ax.hold(True); wdh=4
    
    
    ax.plot(pos_1,data_1,'blue',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='GSI DA')


    ax.plot(pos_1,data_2,'red',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='red',markeredgecolor='red',label='NO GSI')


    ax.plot(pos_1,obs,'black',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='black',markeredgecolor='black',label='OBS')

    ax.xaxis.set_ticks_position('bottom')  ; ax.yaxis.set_ticks_position('left') ;

    ax.spines['bottom'].set_color('black') ; ax.spines['right'].set_color('black') ;
    ax.spines['top'].set_color('black')    ; ax.spines['left'].set_color('black') ;     
 
 

    ax.set_yticks(np.arange(min(obs)-3,max(obs)+3,3.0))


    ax.set_xticks(pos_1[::4]) ; xTickMarks=date_list[0:l_idx][::4]
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=90, fontsize=6,family='sans-serif')
   

    ax.tick_params(axis='x', colors='black',labelsize=18) ; ax.tick_params(axis='y', colors='black',labelsize=18)

    #ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)
    ax.set_ylabel('Dew point Temperature ',color='black',fontsize=14) ;  
    ax.set_xlabel('Date ',color='black',fontsize=14) ;  

    #Get artists and labels for legend and chose which ones to display
    handles, labels = ax.get_legend_handles_labels()
    display = (0,1,2)

    #Create custom artists
    simArtist = plt.Line2D((0,1),(0,0), color='blue', marker='o', linestyle='')
    anyArtist = plt.Line2D((0,1),(0,0), color='k')

    #Create legend from custom artist/label lists
    leg=ax.legend([handle for i,handle in enumerate(handles) if i in display]+[simArtist,anyArtist],
          [label for i,label in enumerate(labels) if i in display],loc=1,bbox_to_anchor=(-0.05, 0.9, 1., .102),frameon=1,fontsize=18)

    frame = leg.get_frame() ; frame.set_facecolor('white')
#################################################################################################################

    #titl='Temperature '
    #plt.title(titl,color='black',fontsize=25,y=1.05)
    plt.tight_layout(h_pad=3) ; 
    plt.savefig(outFile);
    plt.close(fig) ; fig.clf(fig)      
#################################################################################################################

############################################### Mix ratio #######################################################    
    outFile=main+'modelWRF/ARW/output/gsi_plots/mixr_2m_'+locNme+date
    data_1=g_req_data[0:l_idx,10].astype(float) ; data_2=ng_req_data[0:l_idx,10].astype(float) ; obs=rs_req_data[0:l_idx,11].astype(float) 
    
    fig=plt.figure(figsize=(14,6),dpi=50); ax = fig.add_subplot(111,axisbg='white')
    sns.set(style='ticks') ; 

    pos_1  = np.arange(0,len(data_1),1) ;  ax.hold(True); wdh=4
    
    
    ax.plot(pos_1,data_1,'blue',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='GSI DA')


    ax.plot(pos_1,data_2,'red',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='red',markeredgecolor='red',label='NO GSI')


    ax.plot(pos_1,obs,'black',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='black',markeredgecolor='black',label='OBS')

    ax.xaxis.set_ticks_position('bottom')  ; ax.yaxis.set_ticks_position('left') ;

    ax.spines['bottom'].set_color('black') ; ax.spines['right'].set_color('black') ;
    ax.spines['top'].set_color('black')    ; ax.spines['left'].set_color('black') ;     
 
  
    scl_mx=np.array([max(data_1),max(data_2),max(obs)]).max()
    scl_mn=np.array([min(data_1),min(data_2),min(obs)]).min()
    stp=(scl_mx-scl_mn)/len(pos_1)

#    stp_1=data_1[0] ;  stp_2=data_1[1] ;stp=np.round(np.abs(stp_1-stp_2),5)
    ax.set_yticks(np.arange(scl_mn-stp,scl_mx+stp,stp))


    ax.set_xticks(pos_1[::4]) ; xTickMarks=date_list[0:l_idx][::4]
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=90, fontsize=6,family='sans-serif')
   

    ax.tick_params(axis='x', colors='black',labelsize=18) ; ax.tick_params(axis='y', colors='black',labelsize=18)

    #ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)
    ax.set_ylabel('Mixing Ratio ',color='black',fontsize=14) ;  
    ax.set_xlabel('Date ',color='black',fontsize=14) ;  

    #Get artists and labels for legend and chose which ones to display
    handles, labels = ax.get_legend_handles_labels()
    display = (0,1,2)

    #Create custom artists
    simArtist = plt.Line2D((0,1),(0,0), color='blue', marker='o', linestyle='')
    anyArtist = plt.Line2D((0,1),(0,0), color='k')

    #Create legend from custom artist/label lists
    leg=ax.legend([handle for i,handle in enumerate(handles) if i in display]+[simArtist,anyArtist],
          [label for i,label in enumerate(labels) if i in display],loc=1,bbox_to_anchor=(-0.05, 0.9, 1., .102),frameon=1,fontsize=18)

    frame = leg.get_frame() ; frame.set_facecolor('white')
#################################################################################################################

    #titl='Temperature '
    #plt.title(titl,color='black',fontsize=25,y=1.05)
    plt.tight_layout(h_pad=3) ; 
    plt.savefig(outFile);
    plt.close(fig) ; fig.clf(fig)  
    #del ng_req_data,g_req_data,rs_req_data,rs_data ;
#################################################################################################################



    