#!/usr/bin/python

import os ;import sys ;  import numpy as np ; import datetime as dt ; from dateutil import tz ; 
import matplotlib.pyplot as plt; #import seaborn as sns ;


main='/home/vkvalappil/Data/' ; date=str(sys.argv[1]) ; l_idx_s=0 ; l_idx_e=30 ;
output=main+'oppModel/output/vis_plots/' +str(l_idx_s)+'_'+str(l_idx_e)+'hour/'+date+'/'
if not os.path.exists(output)   :
    os.makedirs(output)

modFile=main+'oppModel/output/visibility_'+date+'.csv' ; lstFile=main+'modelWRF/scripts/master_uae.csv'

lst_f=np.genfromtxt(lstFile,delimiter=',',dtype='S')
mod_data=np.genfromtxt(modFile,delimiter=',',dtype='S') ;  

for ii in range(0,lst_f.shape[0]):
    tid=lst_f[ii,0] ; locNme=lst_f[ii,-1]  ; 
    g_req_data=mod_data[np.where(mod_data[:,0]==tid)[0],:]    
 
    f_date=g_req_data[:,3][::24] ; date_1=dt.datetime.strptime(f_date[0],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
    date_2=dt.datetime.strptime(f_date[1],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d') ; 
    date_3=dt.datetime.strptime(f_date[2],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d');
    
    rs_file_1='/home/vkvalappil/Data/metarData/_data_mr/'+date_1[0:4]+'/'+date_1[0:6]+'/'+locNme+'_'+date_1+'.csv'
    rs_file_2='/home/vkvalappil/Data/metarData/_data_mr/'+date_2[0:4]+'/'+date_2[0:6]+'/'+locNme+'_'+date_2+'.csv'
    rs_file_3='/home/vkvalappil/Data/metarData/_data_mr/'+date_3[0:4]+'/'+date_3[0:6]+'/'+locNme+'_'+date_3+'.csv' 
    
    rs_data_1=np.genfromtxt(rs_file_1,delimiter=',',dtype='S')
    rs_data_2=np.genfromtxt(rs_file_2,delimiter=',',dtype='S')
    rs_data_3=np.genfromtxt(rs_file_3,delimiter=',',dtype='S')
    
    rs_data=np.concatenate([rs_data_1[1:,:],rs_data_2[1:,:],rs_data_3[1:,:]],axis=0)    
    
    from_zone = tz.gettz('Asia/Dubai') ; to_zone = tz.gettz('UTC') ;
    date_list=np.array([(dt.datetime.strptime(x,'%Y-%m-%d %H:%M:%S')).replace(tzinfo=from_zone).astimezone(to_zone).strftime('%Y-%m-%d %H:%M') for x in g_req_data[:,3]]); 
    rs_req_data=rs_data[np.where(np.in1d(rs_data[:,1],date_list))[0],:]    
     
    
##################################################Temperature ##########################################################################################    
    outFile=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'_visibility_'+locNme+date
    data_1=g_req_data[l_idx_s:l_idx_e,5].astype(float) ;  
    data_2=g_req_data[l_idx_s:l_idx_e,6].astype(float) ;  
    data_3=g_req_data[l_idx_s:l_idx_e,7].astype(float) ;  
    data_4=g_req_data[l_idx_s:l_idx_e,8].astype(float) ;  
    obs=np.round(rs_req_data[l_idx_s:l_idx_e,12].astype(float)*1.6)
    
    
    fig=plt.figure(figsize=(14,6),dpi=50,frameon=True); ax = fig.add_subplot(111,axisbg='white')
    #sns.set(style='ticks') ;   
    
    pos_1  = np.arange(0,len(data_1),1) ;  ax.hold(True); wdh=4
    
    
    ax.plot(pos_1,data_1,'blue',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='wrf vis upp')

    ax.plot(pos_1,data_2,'red',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='red',markeredgecolor='red',label='wrf vis ruc')

    ax.plot(pos_1,data_3,'green',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='green',markeredgecolor='green',label='wrf vis fsl')

    ax.plot(pos_1,data_4,'orange',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='orange',markeredgecolor='orange',label='wrf vis avg(upp,ruc)')


    ax.plot(pos_1,obs,'black',linestyle='-',linewidth=wdh,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='black',markeredgecolor='black',label='OBS')


    ax.xaxis.set_ticks_position('bottom')  ; ax.yaxis.set_ticks_position('left') ;

    ax.spines['bottom'].set_color('black') ; ax.spines['right'].set_color('black') ;
    ax.spines['top'].set_color('black')    ; ax.spines['left'].set_color('black') ;     
 
 

    ax.set_yticks(np.arange(0,14,2.0))


    ax.set_xticks(pos_1[::2]) ; xTickMarks=date_list[l_idx_s:l_idx_e][::2]
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=90, fontsize=6,family='sans-serif')
   

    ax.tick_params(axis='x', colors='black',labelsize=18) ; ax.tick_params(axis='y', colors='black',labelsize=18)

    #ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)
    ax.set_ylabel('Visibility (Km) ',color='black',fontsize=14) ;  
    ax.set_xlabel('Date ',color='black',fontsize=14) ;  

    #Get artists and labels for legend and chose which ones to display
    handles, labels = ax.get_legend_handles_labels()
    display = (0,1,2,3,4)

    #Create custom artists
    simArtist = plt.Line2D((0,1),(0,0), color='blue', marker='o', linestyle='')
    anyArtist = plt.Line2D((0,1),(0,0), color='k')

    #Create legend from custom artist/label lists
    leg=ax.legend([handle for i,handle in enumerate(handles) if i in display]+[simArtist,anyArtist],
          [label for i,label in enumerate(labels) if i in display],loc=1,bbox_to_anchor=(-0.01, 0.2, 1., .102),frameon=1,fontsize=10)

    frame = leg.get_frame() ; frame.set_facecolor('white')
#################################################################################################################

    titl='Metar & model Visibility_' + date +'-'+ str(l_idx_s)+'_'+str(l_idx_e)+'hour'
    plt.title(titl,color='black',fontsize=25,y=1.05)
    plt.tight_layout(h_pad=3) ; 
    plt.savefig(outFile);
    plt.close(fig) ; fig.clf(fig)  
    
#######################################################################################################################