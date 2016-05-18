import csv

with open('e:/work/issues_write.csv','wb') as w_file:
    writer = csv.writer(w_file)
    str = ['#','项目','跟踪','状态','优先级','主题','优先级(HMI12)','发现版本','提出人员','修正版本','SVN Revision','对策确认版本','责任方(HMI12)','关联No','Car(HMI12)','私有','描述']
    writer.writerow(str)
    item = ['','HMI12','ST Bug','新建','普通','[NGI][Medium][HMI NAF] All the setting options below <Display setting>  no response','P2','2015_SGM_NGI_Release_5.3.4.0','YFVE_Z 张勇','Ver*.***','rev.0000; rev.0000','Ver*.***','NAF','572241','328_YF','否','Test Sequence:']
    writer.writerow(item)
    print 'done'
