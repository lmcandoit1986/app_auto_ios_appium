#!/usr/bin/python
# -*- coding: utf-8 -*-
import _thread
from subprocess import Popen, PIPE, STDOUT
import os
import time


class Summery(object):
    '''
    都是Byte 字节
    bit 位， 1Byte = 8bit
    '''
    Log_Show_Lev = 5

    SWITCH_MEM = False
    SWITCH_CPU = False
    SWITCH_NET = False
    SWITCH_FPS = False

    Mem_list = []
    Fps_list = []
    Cpu_list = []
    Net_list = []
    FPS_last_list = []

    WAIT_TIME = 3  # 等待时间最小2秒

    Max = True

    get_meminfo = '/Users/liming/Library/Android/sdk/platform-tools/adb shell dumpsys meminfo {0}'
    get_cpu = '/Users/liming/Library/Android/sdk/platform-tools/adb shell dumpsys cpuinfo | grep {0}'
    get_net = '/Users/liming/Library/Android/sdk/platform-tools/adb shell cat /proc/{0}/net/dev'
    get_Cpu_All = '/Users/liming/Library/Android/sdk/platform-tools/adb shell cat /proc/stat |grep cpu'
    get_Cpu_Pid = '/Users/liming/Library/Android/sdk/platform-tools/adb shell cat /proc/{0}/stat'
    top = "/Users/liming/Library/Android/sdk/platform-tools/adb -s {0} shell top -s 6 -n 1 -b |grep {1}"
    ps = '/Users/liming/Library/Android/sdk/platform-tools/adb shell ps |find "{0}"'
    reset_fps = '/Users/liming/Library/Android/sdk/platform-tools/adb shell dumpsys gfxinfo {0} reset'
    get_fps = "/Users/liming/Library/Android/sdk/platform-tools/adb shell dumpsys gfxinfo {0} framestats | grep -A 120 'Flags'"

    def setSWITCH_MEM(self, BOOL):
        self.SWITCH_MEM = BOOL

    def setSWITCH_CPU(self, BOOL):
        self.SWITCH_CPU = BOOL

    def setSWITCH_NET(self, BOOL):
        self.SWITCH_NET = BOOL

    def setSWITCH_FPS(self, BOOL):
        self.SWITCH_FPS = BOOL

    def Top(self, devicesID, PackageName):
        # 200 * 5 =1000s /60 = 16分
        self.ProcessItem = Popen(self.top.format(devicesID, PackageName), stdout=PIPE, stderr=STDOUT, shell=True)
        while self.ProcessItem.poll() is None:
            lines = self.ProcessItem.stdout.readline().decode("utf-8").strip().replace('\\n', '')
            self.Log(lines, 4)
            if devicesID == '1dcb290a':
                if PackageName in lines:
                    # if lines.endswith(PackageName)
                    self.Log(lines, 4)
                    PT_data = lines.split()
                    if PT_data[11] == PackageName:
                        self.Log("PK:{4},pid:{0},RES:{1},SHR:{2},CPU（%）:{3}".format(PT_data[0], PT_data[5], PT_data[6],
                                                                                    PT_data[8], PT_data[11]), 2)
                        return PT_data[0]
            else:
                if PackageName in lines:
                    # if lines.endswith(PackageName)
                    self.Log(lines, 4)
                    PT_data = lines.split()
                    if PT_data[11] == PackageName:
                        self.Log("PK:{4},pid:{0},RES:{1},SHR:{2},CPU（%）:{3}".format(PT_data[0], PT_data[5], PT_data[6],
                                                                                    PT_data[8], PT_data[11]), 2)
                        return PT_data[0]

    def Get_Pid(self, PackageName):
        Res = os.popen(self.ps.format(PackageName)).read()

    def FPS(self, Package):
        Res = []
        res = os.popen(self.get_fps.format(Package)).read()
        self.FPSreset(Package)
        if res.count("QueueBufferDuration") == 2:
            i = 0
            for lines in res.splitlines():
                if lines.strip().__contains__('QueueBufferDuration'):
                    i += 1
                if i == 2:
                    if not lines.strip().__contains__('Flags'):
                        if lines.strip().__contains__('PROFILEDATA'):
                            break
                        self.Log(lines.strip(), 2)
                        line = lines.strip().split(',')
                        Res.append((int(line[13]) - int(line[1])) / 1000000)
        else:
            for lines in res.splitlines():
                if not lines.strip().__contains__('Flags'):
                    if lines.strip().__contains__('PROFILEDATA'):
                        break
                    self.Log(lines.strip(), 2)
                    line = lines.strip().split(',')
                    Res.append((int(line[13]) - int(line[1])) / 1000000)
        self.Log(Res, 1)
        return Res

    def FPSreset(self, Package):
        # print self.reset_fps.format(Package)
        os.popen(self.reset_fps.format(Package))

    def setMax(self, result):
        self.Log('set MAX', 4)
        self.Max = result

    def getMax(self):
        self.Log('get MAX', 4)
        return self.Max

    def Mem(self, pid):
        return os.popen(self.get_meminfo.format(pid)).read()

    def CPU(self, pid):
        return os.popen(self.get_cpu.format(pid)).read()

    def CPU_file_all(self):
        return os.popen(self.get_Cpu_All).read()

    def Log(self, printContent, Lev):
        if self.Log_Show_Lev >= Lev:
            print(time.ctime() + ":{0}".format(printContent))

    def CPU_file_pid(self, pid):
        return os.popen(self.get_Cpu_Pid.format(pid)).read()

    def Net(self, pid):
        return os.popen(self.get_net.format(pid)).read()

    def Deal_Net(self, Con):
        print("Net:" + Con)
        if Con:
            for line in Con.splitlines():
                self.Log(line, 4)
                if line.__contains__('wlan0'):
                    self.Log("Receive:{0},Transmit:{1}".format(str(int(line.split()[1]) / 1024),
                                                               str(int(line.split()[9]) / 1024)), 2)  # 单位KB
                    return round(int(line.split()[1]) / 1024 + int(line.split()[9]) / 1024, 2)
        else:
            return 0

    def Deal_Mem(self, Con):
        Res = {}
        print("Mem:" + Con)
        if Con:
            for line in Con.splitlines():
                if line.__contains__('TOTAL') and not line.__contains__('TOTAL SWAP PSS'):
                    print(line)
                    self.Log(
                        "PSS Total:{0},Private Dirty:{1}".format(int(line.split()[1]) / 1024,
                                                                 int(line.split()[2]) / 1024),
                        2)
                    Res['pss'] = round(int(line.split()[1]) / 1024, 2)
                    Res['PrivateDirty'] = round(int(line.split()[2]) / 1024, 2)
                    return Res

        Res['pss'] = 0
        Res['PrivateDirty'] = 0
        return Res

    def Deal_CPU(self, Con, PackageName):
        for line in Con.splitlines():
            if line.__contains__(PackageName):
                Result = line.strip().split()
                self.Log('all:{0},user:{1},kernel:{2}'.format(Result[0], Result[2], Result[5]), 2)
                return Result[0]

    def Deal_Cpu_All(self, Con):
        lines = Con.splitlines()[0].split()
        j = 0
        for i in range(len(lines) - 1):
            j += int(lines[i + 1])
        self.Log('all cpu:{}'.format(j), 2)
        return j

    def Deal_Cpu_Pid(self, Con):
        print("cpu:" + Con)
        if Con:
            lines = Con.splitlines()[0].split()
            j = int(lines[13]) + int(lines[14]) + int(lines[15]) + int(lines[16])
            self.Log('pid cpu:{}'.format(j), 2)
            return j
        else:
            return 0

    def Cpurate(self, Pid, Start_Cpu_All, Start_Cpu_Pid):
        cpu_begin = Start_Cpu_All
        cpu_begin_pid = Start_Cpu_Pid
        Res = {}
        for i in range(1):
            cpu_end = self.Deal_Cpu_All(self.CPU_file_all())
            cpu_end_pid = self.Deal_Cpu_Pid(self.CPU_file_pid(Pid))
            cpurate = round(100 * (cpu_end_pid - cpu_begin_pid) / (cpu_end - cpu_begin), 2)
            # print cpurate
            # cpu_begin,cpu_begin_pid=cpu_end,cpu_end_pid
            # time.sleep(5)
        Res['rate'] = cpurate
        Res['all'] = cpu_end
        Res['pid'] = cpu_end_pid
        return Res

    def UseNet(self, Start, pid_target):
        Res = {}
        End = self.Deal_Net(self.Net(pid_target))
        if End:
            Res['Use'] = round(End - Start, 2)
            Res['end'] = round(End, 2)
            return Res
        else:
            Res['Use'] = 0
            Res['end'] = 0
            return Res

    def Check_fps(self):
        for i in range(len(self.Fps_list)):
            j = i
            begin = 0
            restart = True
            while restart:
                if j >= len(self.Fps_list):
                    print('time:{0}'.format(begin))
                    break
                else:
                    begin += self.Fps_list[j]
                    j += 1
                    if begin > 1000:
                        restart = False
                        print('fps:{0}'.format(j - i))
                        self.FPS_last_list.append(j - i)

    def Monitor(self, Deviceid, Package):
        if self.getMax():
            pid_target = self.Top(Deviceid, Package)
            print("pid:" + pid_target)
            if self.SWITCH_CPU:
                Start_Cpu_All = self.Deal_Cpu_All(self.CPU_file_all())
                Start_CPU_Pid = self.Deal_Cpu_Pid(self.CPU_file_pid(pid_target))
            if self.SWITCH_NET:
                Start_Net = self.Deal_Net(self.Net(pid_target))
            if self.SWITCH_FPS:
                self.FPSreset(Package)
            time.sleep(self.WAIT_TIME - 2)
        while self.getMax():
            StrLog = ''
            if self.SWITCH_CPU:
                Res = self.Cpurate(pid_target, Start_Cpu_All, Start_CPU_Pid)
                self.Log(Res, 2);
                Start_Cpu_All, Start_CPU_Pid = Res['all'], Res['pid']
                StrLog += 'CpuRate:{0},'.format(Res['rate'])
                self.Cpu_list.append(Res['rate'])
                print(self.Cpu_list)
            if self.SWITCH_NET:
                ResNet = self.UseNet(Start_Net, pid_target)
                Start_Net = ResNet['end']
                self.Log(ResNet, 2);
                StrLog += 'Net:{0},'.format(ResNet['Use'])
                self.Net_list.append(ResNet['Use'])
                print(self.Net_list)
            if self.SWITCH_MEM:
                ResMem = self.Deal_Mem(self.Mem(pid_target))
                self.Log(ResMem, 2);
                StrLog += 'PSS:{0},PrivateDirty:{1}'.format(ResMem['pss'], ResMem['PrivateDirty'])
                self.Mem_list.append(ResMem['pss'])
                print(self.Mem_list)
            if self.SWITCH_FPS:
                self.Fps_list += self.FPS(Package)

            self.Log(StrLog, 1)
            time.sleep(self.WAIT_TIME - 2)

    def MonitorFPS(self, Package):
        self.FPSreset(Package)
        while self.getMax():
            time.sleep(1.5)
            if self.SWITCH_FPS:
                self.Fps_list += self.FPS(Package)

    def saveResult(self, path, data):
        save = open(path, 'a')
        save.write(data + '\n')
        save.close()


class AutoCase(object):

    def RunCase(self, cmd, deviceID, PackageName, Path, Mem=False, CPU=False, FPS=False, Net=False):
        self.ProcessCMD = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
        # Entry = Summery()
        # Entry.setSWITCH_CPU(CPU)
        # Entry.setSWITCH_FPS(FPS)
        # Entry.setSWITCH_MEM(Mem)
        # Entry.setSWITCH_NET(Net)
        PTDATA = []
        CaseName = ''
        while self.ProcessCMD.poll() is None:
            Results = self.ProcessCMD.stdout.readline().decode("utf-8").strip().replace('\\n', '')
            print(Results)
            if 'INSTRUMENTATION_STATUS: test=' in Results:
                CaseName = Results.strip().split('=')[1]
                print('CaseName:{0}'.format(CaseName))
            if 'INSTRUMENTATION_STATUS_CODE: 5' in Results:
                Entry = Summery()
                Entry.setSWITCH_CPU(CPU)
                Entry.setSWITCH_FPS(FPS)
                Entry.setSWITCH_MEM(Mem)
                Entry.setSWITCH_NET(Net)
                _thread.start_new_thread(Entry.Monitor, (deviceID, PackageName), )
            if 'INSTRUMENTATION_STATUS_CODE: 6' in Results:
                Entry.setMax(False)
                if FPS:
                    Entry.Check_fps()
                itemDict = {}
                itemDict['Case'] = CaseName
                itemDict['Mem'] = Entry.Mem_list
                itemDict['CPU'] = Entry.Cpu_list
                itemDict['Net'] = Entry.Net_list
                itemDict['FPS'] = Entry.FPS_last_list
                # Entry.saveResult(Path, str(itemDict))
                PTDATA.append(itemDict)
                # Entry.saveResult(Path, CaseName)
                # Entry.saveResult(Path, 'Mem:{}'.format(Entry.Mem_list))
                # Entry.saveResult(Path, 'CPU:{}'.format(Entry.Cpu_list))
                # Entry.saveResult(Path, 'Net:{}'.format(Entry.Net_list))
                # Entry.saveResult(Path, 'FPS:{}'.format(Entry.FPS_last_list))
        # if FPS:
        #     Entry.Check_fps()
        # Entry.saveResult(Path, cmd)
        # Entry.saveResult(Path, 'Mem:{}'.format(Entry.Mem_list))
        # Entry.saveResult(Path, 'CPU:{}'.format(Entry.Cpu_list))
        # Entry.saveResult(Path, 'Net:{}'.format(Entry.Net_list))
        # Entry.saveResult(Path, 'FPS:{}'.format(Entry.FPS_last_list))
        Entry.saveResult(Path, str(PTDATA))


if __name__ == "__main__":
    ResultPath = './result.log'
    cmd = '/Users/liming/Library/Android/sdk/platform-tools/adb -s B2NGAC6850506946 shell am instrument -w -r   -e debug false -e class \'com.hnrmb.Cases.SumCase#Bank_BankCheck\' com.hnrmb.test/androidx.test.runner.AndroidJUnitRunner'
    Auto = AutoCase()
    Auto.RunCase(cmd=cmd, deviceID='B2NGAC6850506946', PackageName='com.hnrmb.salary', Path=ResultPath, Mem=True,
                 CPU=True, FPS=True, Net=True)
