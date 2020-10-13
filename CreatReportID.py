import re
def CreatID():
    with open(r'./ReportID', 'r') as fp:
        lines = fp.readlines()
        Lowlast_line = lines[-1]
    newlast=str(int(Lowlast_line)+1)+'\n'
    f=open(r'./ReportID','a',encoding='utf-8')
    f.write(newlast)
    return  newlast


def readReportID():
    with open(r'./ReportID', 'r') as fp:
        lines = fp.readlines()
        Lowlast_line = lines[-1]
        test=re.findall(r"\d+\.?\d*", Lowlast_line)
        Lowlast_line=str(test[0])
        return Lowlast_line