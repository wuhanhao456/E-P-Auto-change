import configparser,os,sys,psutil,time,GPUtil,subprocess,win32api
config = configparser.ConfigParser()
try:
    config.read('配置文件.ini')
    print("读取ini")
    PerformanceMode = config.get('电源计划切换','性能的GUID')
    EcoMode = config.get('电源计划切换','省电的GUID')
    IdletimeSet = int(config.get('电源计划切换','熄屏后时间'),10)
    CpuUsageP = int(config.get('性能切换条件','CPU使用率大于'),10)
    CpuUsageTimeP = int(config.get('性能切换条件','CPU持续使用时间'),10)
    #GpuUsage = config.get('性能切换条件','GPU使用率')
    CpuUsageE = int(config.get('省电切换条件','CPU使用率小于'),10)
    CpuUsageTimeE = int(config.get('省电切换条件','CPU持续使用时间'),10)
    print("读取完成")
    
except :
    config['电源计划切换'] = {'性能的GUID':'381b4222-f694-41f0-9685-ff5bb260df2e','省电的GUID':'a1841308-3541-4fab-bc81-f71556f20b4a','熄屏后时间':'20'}
    config['性能切换条件'] = {'CPU使用率大于':'50','CPU持续使用时间':'3','GPU使用率(弃用)':'0'}
    config['省电切换条件'] = {'CPU使用率小于':'40','CPU持续使用时间':'50'}
    with open('配置文件.ini', 'w') as configfile:
        config.write(configfile)
        sys.exit()
    print("创建ini完成")
while 1 :
    Idletime = (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
    print("Idletime"+str(Idletime))
    CpuUsage = psutil.cpu_percent(interval=1, percpu=False)
    #GPUtil.useAmdGPUs()
    #gpus = GPUtil.getGPUs()
    if CpuUsage > CpuUsageP or Idletime < IdletimeSet:start_time1  = time.time()
    while CpuUsage > CpuUsageP or Idletime < IdletimeSet:#切换到性能
        Idletime = (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
        CpuUsage = psutil.cpu_percent(interval=1, percpu=False)
        duration2 = 0
        duration1 = time.time() - start_time1
        if duration1 >= CpuUsageTimeP:
            #subprocess.run(['powercfg', '-S', PerformanceMode], stdout=subprocess.PIPE, shell =False)
            subprocess.Popen(['powercfg', '-S', PerformanceMode] , shell=False)
            print("P"+str(duration1))
    if CpuUsage < CpuUsageE:start_time2 = time.time()
    while CpuUsage < CpuUsageE and Idletime > IdletimeSet:#切换到节能
        Idletime = (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
        CpuUsage = psutil.cpu_percent(interval=1, percpu=False)
        duration1 = 0
        duration2 = time.time() - start_time2
        if duration2 >= CpuUsageTimeE:
            #subprocess.run(['powercfg', '-S', EcoMode], stdout=subprocess.PIPE, shell =False)
            subprocess.Popen(['powercfg', '-S', EcoMode] , shell=False)
            print("E"+str(duration2))
    time.sleep(1)
    print(CpuUsage)
    #print("计时"+str(duration1)+"    "+str(duration2))

