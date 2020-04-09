#!/usr/bin/python3 
import sys
cmd=    sys.argv[0]
infile= sys.argv[1]
try:
    outfile=sys.argv[2]
except:
    outfile=infile[:-4] + "html"

with open(infile,"r") as fp:
    text = "[" + fp.readline()
    for line in fp:
        text = text + "," + line

text = text + "]"

# Convert the text to json and extract the stats
import json
jdata = []
jdata = json.loads(text) # convert text to JSON
#jdata = entry["samples"] # removes outer parts so we have a list of snapshot dictionaries

# - - - - - Start nchart functions
chartnum = 10
next_graph_need_stacking = 0

def nchart_start(file, title):
        ''' Head of the HTML webpage'''
        file.write('<html>' + '\n')
        file.write('<head>' + '\n')
        file.write('\t<title>' + title + '</title>\n')
        file.write('\t<script type="text/javascript" src="https://www.google.com/jsapi"></script>\n')
        file.write('\t<script type="text/javascript">\n')
        file.write('\tgoogle.load("visualization", "1.1", {packages:["corechart"]});\n')
        file.write('\tgoogle.setOnLoadCallback(setupCharts);\n')
        file.write('\tfunction setupCharts() {\n')
        file.write('\tvar chart = null;\n')
    
def nchart_bubble_top(file, columnnames):
        ''' Before the graph data with 3D data '''
        file.write('\tvar data_' + str(chartnum) +  ' = google.visualization.arrayToDataTable([\n')
        file.write("[" + columnnames  + "]\n")
    
def nchart_column_top(file, columnnames):
        ''' Before the graph data with multiple columns of data '''
        file.write('\tvar data_' + str(chartnum) +  ' = google.visualization.arrayToDataTable([\n')
        file.write("[" + columnnames  + "]\n")

def nchart_line_top(file, columnnames):
        ''' Before the graph data with datetime + multiple columns of data '''
        file.write('\tvar data_' + str(chartnum) +  ' = google.visualization.arrayToDataTable([\n')
        file.write("[{type: 'datetime', label: 'Datetime'}," + columnnames  + "]\n")
    
def nchart_bubble_bot(file, graphtitle):
        ''' After the JavaSctipt bubble graph data is output, the data is terminated and the bubble graph options set'''
        global chartnum
        file.write('\t]);\n')
        file.write('\tvar options_'+ str(chartnum) + ' = {\n')
        file.write('\t\tchartArea: {left: "5%", width: "85%", top: "10%", height: "80%"},\n')
        file.write('\t\ttitle: "' + graphtitle + '",\n')
        file.write('\t\thAxis: { title:"CPU seconds in Total"},\n')
        file.write('\t\tvAxis: { title:"Character I/O in Total"},\n')
        file.write('\t\tsizeAxis: {maxSize: 200},\n')
        file.write('\t\tbubble: {textStyle: {fontSize: 15}}\n')
        file.write('\t};\n')
        file.write('\tdocument.getElementById("draw_'+ str(chartnum) + '").addEventListener("click", function() {\n')
        file.write('\tif (chart && chart.clearChart) chart.clearChart();\n')
        file.write('\tchart = new google.visualization.BubbleChart(document.getElementById("chart_master"));\n')
        file.write('\tchart.draw( data_'+ str(chartnum) + ', options_'+ str(chartnum) + ');\n')
        file.write('\t});\n')
        chartnum += 1
    
def nchart_line_bot(file, graphtitle):
        ''' After the JavaSctipt line graph data is output, the data is terminated and the graph options set'''
        global next_graph_need_stacking
        global chartnum 
        file.write('\t]);\n')
        file.write('\tvar options_'+ str(chartnum) + ' = {\n')
        file.write('\t\tchartArea: {left: "5%", width: "85%", top: "10%", height: "80%"},\n')
        file.write('\t\ttitle: "' + graphtitle + '",\n')
        file.write('\t\tfocusTarget: "category",\n')
        file.write('\t\thAxis: { gridlines: { color: "lightgrey", count: 30 } },\n')
        file.write('\t\tvAxis: { gridlines: { color: "lightgrey", count: 11 } },\n')
        file.write('\t\texplorer: { actions: ["dragToZoom", "rightClickToReset"],\n')
        file.write('\t\taxis: "horizontal", keepInBounds: true, maxZoomIn: 20.0 },\n')
        if next_graph_need_stacking:
            file.write('\t\tisStacked:  1\n')
            next_graph_need_stacking = 0
        else:
            file.write('\t\tisStacked:  0\n')
        file.write('\t};\n')
        file.write('\tdocument.getElementById("draw_'+ str(chartnum) + '").addEventListener("click", function() {\n')
        file.write('\tif (chart && chart.clearChart) chart.clearChart();\n')
        file.write('\tchart = new google.visualization.AreaChart(document.getElementById("chart_master"));\n')
        file.write('\tchart.draw( data_'+ str(chartnum) + ', options_'+ str(chartnum) + ');\n')
        file.write('\t});\n')
        chartnum += 1
    
def nchart_column_bot(file, graphtitle):
        ''' After the JavaSctipt line graph data is output, the data is terminated & the graph options set'''
        global next_graph_need_stacking
        global chartnum 
        file.write('\t]);\n')
        file.write('\tvar options_'+ str(chartnum) + ' = {\n')
        file.write('\t\tchartArea: {left: "5%", width: "85%", top: "10%", height: "80%"},\n')
        file.write('\t\ttitle: "' + graphtitle + '",\n')
        file.write('\t\tfocusTarget: "category",\n')
        file.write('\t\thAxis: { gridlines: { color: "lightgrey", count: 30 } },\n')
        file.write('\t\tvAxis: { gridlines: { color: "lightgrey", count: 11 } },\n')
        file.write('\t};\n')
        file.write('\tdocument.getElementById("draw_'+ str(chartnum) + '").addEventListener("click", function() {\n')
        file.write('\tif (chart && chart.clearChart) chart.clearChart();\n')
        file.write('\tchart = new google.visualization.ColumnChart(document.getElementById("chart_master"));\n')
        file.write('\tchart.draw( data_'+ str(chartnum) + ', options_'+ str(chartnum) + ');\n')
        file.write('\t});\n')
        chartnum += 1
    
def nchart_end(file, name, config, buttons, summary):
        ''' Generic version using named arguments for 1 to 10 buttons for Server graphs - Finish off the web page '''
        file.write('\t}\n')
        file.write(config)
        file.write('\t</script>\n')
        file.write('\t</head>\n')
        file.write('\t<body bgcolor="#EEEEFF">\n')
        file.write('\t<b>Server: ' + name + ': </b>\n')
        file.write('<button onclick="config()"><b>Configuration</b></button>\n')
        # - - - loop through the buttons and change colours
        colour='black' 
        for num,name in enumerate(buttons, start=10):
           if(name == 'TotalCPU'):
               colour='red'
           if(name == 'Memory'):
               colour='blue'
           if(name == 'TotalDiskRW'):
               colour='brown'
           if(name == 'TotalNet-Bytes'):
               colour='purple'
           file.write('\t<button id="draw_' + str(num) + '" style="color:' + colour + '"><b>'+ name + '</b></button>\n')
        file.write('\t<div id="chart_master" style="width:100%; height:85%;">\n')
        file.write('\t<h2 style="color:blue">Click on a Graph button above, to display that graph</h2>\n')
        file.write('\t</div><br>\n')
        file.write('<table><tr><td>')
        for i,entry in enumerate(summary, start=1):
            file.write("<li>" + entry + "\n")
            if((i % 4) == 0): file.write("<td>\n")
        file.write('</table>\n')
        file.write('Author: Nigel Griffiths @mr_nmon generated by njmon + njmonchart    To Zoom = Left-click and drag. To Reset = Right-click.\n')
        file.write('</body>\n')
        file.write('</html>\n')

# convert ISO date like 2017-08-21T20:12:30 to google date+time 2017,04,21,20,12,30
def googledate(date):
        d = date[0:4] + "," +  str(int(date[5:7]) -1) + "," + date[8:10] + "," + date[11:13] + "," + date[14:16] + "," + date[17:19]
        return d
# - - - - - The nchart function End
# - - - - - The nchart function End
# - - - - - The nchart function End

# These are flags used as function arguments
stacked=1
unstacked=0

def graphit(web,column_names,data,title,button,stack_state):
    global next_graph_need_stacking
    nchart_line_top(web, column_names)
    web.write(data)    
    next_graph_need_stacking = stack_state
    nchart_line_bot(web, title)
    buttonlist.append(button)
 
def bubbleit(web,column_names,data,title,button):
    nchart_bubble_top(web, column_names)
    web.write(data)    
    nchart_bubble_bot(web, title)
    buttonlist.append(button)
 
def columnit(web,column_names,data,title,button):
    nchart_column_top(web, column_names)
    web.write(data)    
    nchart_column_bot(web, title)
    buttonlist.append(button)
 
# ----- MAIN SCRIPT PREPARE DATA -

serial_no = "Unknown"
try:
    serial_no = jdata[0]["identity"]["serial-number"]
except:
    pass
try:
    serial_no = jdata[0]["identity"]["serial_number"]
except:
    pass

# initialise some useful content
buttonlist = []
details=""
try:
    details = details + ' Server=' + jdata[0]['identity']['model']
except:
    try:
        details = details + ' Server=' + jdata[0]['lscpu']['architecture']
    except:
        pass

details = details + ' Serial=' + serial_no

try: 
    details = details + ' OS=%s'%(jdata[0]['os_release']['pretty_name'])
except:
    pass

hostname = jdata[0]['identity']['hostname'] 

tcpu_data=""
rq_data=""
ps_data=""
fe_data = ""
mem_data = ""
pg_data = ""
pa_data = ""
dtrw_data = ""
dtt_data = ""
nio_data = ""
np_data = ""
ipc_data = ""
ni_data = ""
di_data = ""
oc_data = ""
pc_data = ""
gpfs_bytes_data = ""
gpfs_ops_data = ""

#patching line to fix gpfs_total_found not defined error
gpfs_total_found = False

try:
    x = jdata[0]['cpu_total']['user']
    cpu_total_found = True
except:
    cpu_total_found = False

try:
    x = jdata[0]['cpu_counters']['procs_running']
    cpu_counters_found = True
except:
    cpu_counters_found = False

try:
    x = jdata[0]['cpus']
    cpus_or_stat = "cpus"
except:
    cpus_or_stat = "stat"

# - - - Work around "disk" or "disks"
try:
    x = jdata[0]["disks"]
    disk_or_disks = "disks"
except:
    disk_or_disks = "disk"

# loop

for i,s in enumerate(jdata):
    if( i == 0 ):
        continue
    if cpu_total_found: 
        tcpu_data += ",['Date(%s)', %f, %f, %f, %f, %f, %f, %f, %f, %f, %f]\n" %(googledate(s['timestamp']['datetime']),
            s['cpu_total']['user'], 
            s['cpu_total']['sys'], 
            s['cpu_total']['nice'], 
            s['cpu_total']['idle'], 
            s['cpu_total']['iowait'], 
            s['cpu_total']['hardirq'], 
            s['cpu_total']['softirq'], 
            s['cpu_total']['steal'], 
            s['cpu_total']['guest'], 
            s['cpu_total']['guestnice']) 

    if cpu_counters_found:
        fe_data += ",['Date(%s)', %.1f]\n" %(googledate(s['timestamp']['datetime']),
                s['stat_counters']['processes_forks'])

        rq_data += ",['Date(%s)', %d, %d]\n" %(googledate(s['timestamp']['datetime']),
                s['stat_counters']['procs_running'], s['stat_counters']['procs_blocked'])

        ps_data += ",['Date(%s)', %d]\n" %(googledate(s['timestamp']['datetime']), s['stat_counters']['ctxt'])

    mem_data += ",['Date(%s)', %.1f,%.1f, %.1f,%.1f, %.1f,%.1f, %.1f,%.1f]\n" %(googledate(s['timestamp']['datetime']),
                s['proc_meminfo']['MemTotal']//1024.0,
                s['proc_meminfo']['MemFree']/1024.0, 
                #s['proc_meminfo']['MemAvailable']/1024.0, Not available with kernel < 3.14
		0,
                s['proc_meminfo']['Buffers']/1024.0, 
                s['proc_meminfo']['Cached']/1024.0,
                s['proc_meminfo']['Active']/1024.0, 
                s['proc_meminfo']['Inactive']/1024.0,
                s['proc_meminfo']['Active_file']/1024.0 )

    pg_data += ",['Date(%s)', %d, %d]\n" %(googledate(s['timestamp']['datetime']),
            s['proc_meminfo']['SwapTotal']/1024/1024,
            s['proc_meminfo']['SwapFree']/1024/1024)

    pa_data += ",['Date(%s)', %.1f,%.1f, %.1f,%.1f]\n" %(googledate(s['timestamp']['datetime']),
                s['proc_vmstat']['pgpgin'],
                s['proc_vmstat']['pgpgout'],
                s['proc_vmstat']['pswpin'],
                s['proc_vmstat']['pswpout'])

    try:
        rq = s['stat_counters']['procs_running']
        bq = s['stat_counters']['procs_blocked']
    except:
        rq = -1
        bq = -1
    rq_data += ",['Date(%s)', %d, %d]\n" %(googledate(s['timestamp']['datetime']),rq,bq)

# - - - Disks
    read_kbps=0.0
    write_kbps=0.0
    for disk in s[disk_or_disks].keys():
            read_kbps  = read_kbps  + s[disk_or_disks][disk]["rkb"]
            write_kbps = write_kbps + s[disk_or_disks][disk]["wkb"]
    dtrw_data += ",['Date(%s)', %.1f, %.1f]\n" %(googledate(s['timestamp']['datetime']), read_kbps, -write_kbps)

    xfers=0
    for disk in s[disk_or_disks].keys():
        xfers += s[disk_or_disks][disk]["xfers"]
    dtt_data += ",['Date(%s)', %.1f]\n" %(googledate(s['timestamp']['datetime']), xfers)

# - - - Networks
    ibytes=0
    obytes=0
    for net in s["networks"].keys():
        ibytes   = ibytes   + s["networks"][net]["ibytes"]
        obytes   = obytes   + s["networks"][net]["obytes"]
    nio_data += ",['Date(%s)', %.1f, %.1f]\n" %(googledate(s['timestamp']['datetime']), ibytes, -obytes)

    ipackets=0.0
    opackets=0.0
    for net in s["networks"].keys():
        ipackets = ipackets + s["networks"][net]["ipackets"]
        opackets = opackets + s["networks"][net]["opackets"]
    np_data += ",['Date(%s)', %.1f, %.1f]\n" %(googledate(s['timestamp']['datetime']), ipackets,-opackets)

# - - - GPFS = Spectrum Scale total I/ Stats
    try:
        gpfs_total = s["gpfs_io_total"]['readbytes']
        gpfs_total_found = True
    except:
        gpfs_total_found = False
    if(gpfs_total_found):
        gpfs_bytes_data += ",['Date(%s)', %d, %d]\n" %(googledate(s['timestamp']['datetime']),
            s['gpfs_io_total']['readbytes'],
            - s['gpfs_io_total']['writebytes'])

        gpfs_ops_data += ",['Date(%s)', %d,%d, %d,%d, %d,%d]\n" %(googledate(s['timestamp']['datetime']),
            s['gpfs_io_total']['open'],
            s['gpfs_io_total']['close'],
            s['gpfs_io_total']['reads'],
            s['gpfs_io_total']['writes'],
            s['gpfs_io_total']['directorylookup'],
            s['gpfs_io_total']['inodeupdate'])

# - - - Top 20 Processes
# not implimented yet


# - - - CPU USE
cpuuse={}   # start with empty dictionary
samples = 0
for sam in jdata:
        samples = samples + 1
        for cpuname in sam[cpus_or_stat].keys():
            if cpuname[0:9] == "cpu_total":
                continue
            if cpuname[0:3] == "cpu":
                entry=sam[cpus_or_stat][cpuname]
                cpu_percent =entry['user'] + entry['sys']
                if (cpu_percent != 0.0):
                    try:    # update the current entry
                        cpuuse[cpuname] += cpu_percent
                    except: # no current entry so add one
                        cpuuse.update( {cpuname: cpu_percent} )

def sort_cpu(d):
    return int(d[3:])

cpuuse_header = "'CPU','Average Percent'"
cpuuse_data = ""
for cpu in sorted(cpuuse, key=sort_cpu):
    cpuuse_data += ",['%s', %.1f]\n" %(str(cpu), float(cpuuse[cpu])/float(samples))

# - - - Top 20 Disks
tdisk={}   # start with empty dictionary
for sam in jdata:
        for disk in sam[disk_or_disks]:
            entry=sam[disk_or_disks][disk]
            bytes=entry['rkb']+entry['wkb']
            if (bytes != 0):
                #print("disk=%s total bytes=%.1f"%(disk,bytes))
                try:    # update the current entry
                    tdisk[entry[disk]] += bytes
                except: # no current entry so add one
                    tdisk.update( {disk: bytes} )

def sort_dkey(d):
        return tdisk[d]

topdisks = []
for i,disk in enumerate(sorted(tdisk, key=sort_dkey, reverse=True)):
    d=tdisk[disk]
    #print("disk=%s total bytes=%.1f"%(disk,bytes))
    topdisks.append(disk)
    if(i >= 20 ): # Only graph the top 20
        break
#print(topdisks)

td_header = ""
for disk in topdisks:
    td_header += "'" + disk + "',"
td_header = td_header[:-1]

td_data = ""
for sam in jdata:
    td_data += ",['Date(%s)'" %(googledate(sam['timestamp']['datetime']))
    for item in topdisks:
        bytes = sam[disk_or_disks][item]['rkb'] + sam[disk_or_disks][item]['wkb']
        td_data += ", %.1f" %(bytes)
    td_data += "]\n"
# print(td_header)
# print(td_data)

# ----- add config box 
def configdump(section,string):
    newstr = ''
    thing=jdata[0][section]
    for label in thing:
        if len(str(thing[label])) >1:
            newstr = newstr + "%20s = %s<br>\\\n"%(label,str(thing[label]))
    return string + newstr

config_str = '\nfunction config() {\n' + '    var myWindow = window.open("", "MsgWindow", "width=1024, height=800");\n' + \
          '    myWindow.document.write("<h2>Configuration data <br>Use PageDown or Scroll bar (if available)</h2><br>\\\n'
config_str = configdump("identity",config_str)
config_str = configdump("timestamp",config_str)
config_str = configdump("os_release",config_str)
config_str = configdump("proc_version",config_str)
config_str = configdump("lscpu",config_str)
config_str = config_str + '");\n}\n\n'

# ----- MAIN SCRIPT CREAT WEB FILE -
web = open(outfile,"w")        # Open the output file
nchart_start(web, 'Hostname:%s' + hostname)


if cpu_total_found:
    graphit(web, "'User','System','Nice','Idle','IOwait','hardirq','softirq','steal','guest','guestnice'", tcpu_data,  'Total CPU Util (stacked)' + details, "Totalcpu",stacked)
# - - - CPU not idle or Wait
# Example: "cpu19": { "user": 60.209, "nice": 0.000, "sys": 39.773, "idle": 0.000, "iowait": 0.000, "hardirq": 0.000, "softirq": 0.000, "steal": 0.000, "guest": 0.000, "guestnice": 0.000 },

cpustr = ""
for proc in jdata[0][cpus_or_stat].keys():
    cpustr = cpustr + "'" + proc + "',"
cpustr = cpustr[:-1]
nchart_line_top(web, cpustr)
for i,s in enumerate(jdata):
    if i == 0:
        continue
    web.write(",['Date(%s)' " %(googledate(s['timestamp']['datetime'])))
    for proc in s[cpus_or_stat].keys():
        try:
            web.write(",%.1f" %(s[cpus_or_stat][proc]["user"] + 
                                s[cpus_or_stat][proc]["nice"] + 
                                s[cpus_or_stat][proc]["sys"] + 
                                s[cpus_or_stat][proc]["hardirq"] + 
                                s[cpus_or_stat][proc]["softirq"] + 
                                s[cpus_or_stat][proc]["steal"] + 
                                s[cpus_or_stat][proc]["guest"] + 
                                s[cpus_or_stat][proc]["guestnice"] ))
        except:
            web.write(",%.1f" %( 0.0))
    web.write("]\n")
nchart_line_bot(web, 'CPU busy (usr+nice+sys+irq+steel+guest)' + details)
buttonlist.append("CPU-Busy")

# - - - MHz
mhzstr = ""
for proc in jdata[0]["cpuinfo"].keys():
    mhzstr = mhzstr + "'" + proc + "',"
mhzstr = mhzstr[:-1]
nchart_line_top(web, mhzstr)
for i,s in enumerate(jdata):
    if i == 0:
        continue
    web.write(",['Date(%s)' " %(googledate(s['timestamp']['datetime'])))
    for proc in s["cpuinfo"].keys():
        try:
            web.write(",%.1f" %( s["cpuinfo"][proc]["mhz_clock"] ))
        except:
            web.write(",%.1f" %( 0.12345))
    web.write("]\n")
nchart_line_bot(web, 'CPU MHz' + details)
buttonlist.append("MHz")

columnit(web, cpuuse_header, cpuuse_data,  'CPU Use by CPU core thread' + details, "CPUuse")
graphit(web, td_header, td_data,  'Top Disks (mbps)' + details, "TopDisks",unstacked)
if cpu_counters_found:
    graphit(web, "'Run Queue','Blocked'", rq_data,  'CPU Run/Blocked Queue' + details, "RunQueue",unstacked)
    graphit(web, "'Process Switch (ctxt)'", ps_data,  'Process Switches' + details, "pSwitch",unstacked)
    graphit(web, "'Fork'", fe_data,  'Systems Calls fork()' + details, "Forks",unstacked)
graphit(web, "'MemTotal_mb','MemFree_mb','MemAvailable_mb','Buffers_mb','Cached_mb','Active_mb','Inactive_mb','Active_file_mb'", mem_data, 'Memory MB' + details, "Memory",unstacked)
graphit(web, "'Size', 'Free'", pg_data,  'Paging Space in MB' + details, "PageSpace",unstacked)
graphit(web, "'PgpgIn', 'PgpgOut', 'PgSwapIn','PgSwapOut'", pa_data,  'Paging page (in & out) + Swap (in & out)' + details, "Paging",unstacked)
graphit(web, "'Read KB','Write KB'", dtrw_data,  'Total Read & Write KB' + details, "TotalDiskRW",unstacked)
graphit(web, "'Transfers'", dtt_data, 'Total Transfers' + details, "TotalDiskXters",unstacked)

# - - - Disks
dstr = ""
for device in jdata[0][disk_or_disks].keys():
    dstr = dstr + "'" + device + "',"
dstr = dstr[:-1]
nchart_line_top(web, dstr)
for i,s in enumerate(jdata):
    if i == 0:
        continue
    web.write(",['Date(%s)' " %(googledate(s['timestamp']['datetime'])))
    for device in s[disk_or_disks].keys():
        try:
            web.write(",%.1f" %( s[disk_or_disks][device]["busy"] ))
        except:
            web.write(",%.1f" %( s[disk_or_disks][device]["time"] ))
    web.write("]\n")
nchart_line_bot(web, 'Disk Busy' + details)
buttonlist.append("Disk-Busy")

dstr = ""
for device in jdata[0][disk_or_disks].keys():
    dstr = dstr + "'" + device + "+read','" + device + "-write',"
dstr = dstr[:-1]
nchart_line_top(web, dstr)
for i,s in enumerate(jdata):
    if i == 0:
        continue
    web.write(",['Date(%s)' " %(googledate(s['timestamp']['datetime'])))
    for device in s[disk_or_disks].keys():
        web.write(",%.1f,%.1f" %(
                 s[disk_or_disks][device]["rkb"],
                -s[disk_or_disks][device]["wkb"]))
    web.write("]\n")
nchart_line_bot(web, 'Disks KB/s' + details)
buttonlist.append("Disk-KB")

dstr = ""
for device in jdata[0][disk_or_disks].keys():
    dstr = dstr + "'" + device + "+read','" + device + "-write',"
dstr = dstr[:-1]
nchart_line_top(web, dstr)
for i,s in enumerate(jdata):
    if i == 0:
        continue
    web.write(",['Date(%s)' " %(googledate(s['timestamp']['datetime'])))
    for device in s[disk_or_disks].keys():
        web.write(",%.1f,%.1f " %(
                 s[disk_or_disks][device]["reads"],
                -s[disk_or_disks][device]["writes"]))
    web.write("]\n")
nchart_line_bot(web, 'Disk Op/s' + details)
buttonlist.append("Disk-Ops")

# - - - Adapters
# not implimented

fsstr = ""
for fs in jdata[0]["filesystems"].keys():
    fsstr = fsstr + "'" + fs + "',"
fsstr = fsstr[:-1]
nchart_line_top(web, fsstr)
for i,s in enumerate(jdata):
    web.write(",['Date(%s)' " %(googledate(s['timestamp']['datetime'])))
    for fs in s["filesystems"].keys():
        web.write(", %.1f" %( s["filesystems"][fs]["fs_full_percent"]))
    web.write("]\n")
nchart_line_bot(web, 'File Systems Full percent' + details)
buttonlist.append("JFS")

graphit(web, "'Incoming', 'Outgoing'", nio_data,  'Network Bytes/s' + details, "TotalNet-Bytes",unstacked)
graphit(web, "'Incoming', 'Outgoing'", np_data,  'Network Packets/s' + details, "TotalNet-Xfer",unstacked)

netstr = ""
for device in jdata[0]["networks"].keys():
    netstr = netstr + "'" + device + "+in','" + str(device) + "-out',"
netstr = netstr[:-1]
nchart_line_top(web, netstr)
for i,s in enumerate(jdata):
    if i == 0:
        continue
    web.write(",['Date(%s)' " %(googledate(s['timestamp']['datetime'])))
    for device in s["networks"].keys():
        web.write(",%.1f,%.1f" %(
             s["networks"][device]["ibytes"],
            -s["networks"][device]["obytes"]))
    web.write("]\n")
nchart_line_bot(web, 'Network MB/s' + details)
buttonlist.append("Net-MB")

netstr = ""
for device in jdata[0]["networks"].keys():
    netstr = netstr + "'" + device + "+in','" + str(device) + "-out',"
netstr = netstr[:-1]
nchart_line_top(web, netstr)
for i,s in enumerate(jdata):
    if i == 0:
        continue
    web.write(",['Date(%s)' " %(googledate(s['timestamp']['datetime'])))
    for device in s["networks"].keys():
        web.write(",%.1f,%.1f " %(
             s["networks"][device]["ipackets"],
            -s["networks"][device]["opackets"]))
    web.write("]\n")
nchart_line_bot(web, 'Network packets/s' + details)
buttonlist.append("Net-packets")

if(gpfs_total_found):
    graphit(web, "'+Read', '-Write'", gpfs_bytes_data,  'Spectrum Scale (GPFS) Bytes/s' + details, "GPFS-Bytes",unstacked)
    graphit(web, "'Open', 'Close', 'Reads', 'Writes', 'Directory-Lookup', 'InodeUpdate'", gpfs_ops_data,  'Spectrum Scale (GPFS) Op/s' + details, "GPFS-Ops",unstacked)


# - - - GPFS = Spectrum Scale filesystem Stats
if(gpfs_total_found):
    gpfs_fs = ""
    gpfs_fsnames = []
    for fs in jdata[0]["gpfs_filesystems"].keys():
        gpfs_fs = gpfs_fs + "'" + str(fs) + "+read','" + str(fs) + "-write',"
        gpfs_fsnames.append(fs)
    gpfs_fs = gpfs_fs[:-1]
    nchart_line_top(web, gpfs_fs)
    for i,s in enumerate(jdata):
        if i == 0:
            continue
        web.write(",['Date(%s)' " %(googledate(s['timestamp']['datetime'])))
        for fs in gpfs_fsnames:
            try:
                web.write(",%.1f,%.1f " %(
                    s["gpfs_filesystems"][fs]["readbytes"],
                   -s["gpfs_filesystems"][fs]["writebytes"]))
            except:
                web.write(",-0.0,-0.0 ")
        web.write("]\n")
    nchart_line_bot(web, 'Spectrum Scale (GPFS) bytes/s' + details)
    buttonlist.append("GPFS-FS-bytes")

    gpfs_fs = ""
    for fs in jdata[0]["gpfs_filesystems"].keys():
        gpfs_fs = gpfs_fs + "'" + str(fs) + "',"
    gpfs_fs = gpfs_fs[:-1]
    nchart_line_top(web, gpfs_fs)
    for i,s in enumerate(jdata):
        if i == 0:
            continue
        web.write(",['Date(%s)' " %(googledate(s['timestamp']['datetime'])))
        for fs in gpfs_fsnames:
            try:
                web.write(",%d " %(
                 s["gpfs_filesystems"][fs]["open"] +
                 s["gpfs_filesystems"][fs]["close"] +
                 s["gpfs_filesystems"][fs]["reads"] +
                 s["gpfs_filesystems"][fs]["writes"] +
                 s["gpfs_filesystems"][fs]["directorylookup"] +
                 s["gpfs_filesystems"][fs]["inodeupdate"] ))
            except:
                web.write(",-0.0 ")
        web.write("]\n")
    nchart_line_bot(web, 'Spectrum Scale (GPFS) Op/s' + details)
    buttonlist.append("GPFS-FS-Ops")

#web.write(config_button_str)
summary = [
"Hostname:" + jdata[0]["identity"]["hostname"],
"Command: " + jdata[0]["identity"]["njmon_command"],
"njmon:" + jdata[0]["identity"]["njmon_version"],
"njmonchart: For Linux Version 30",
"User:" + jdata[0]["identity"]["username"],
"DateTime:" + jdata[0]["timestamp"]["datetime"],
"UTC:" + jdata[0]["timestamp"]["UTC"],
"Snapshots:" + str(len(jdata)),
"Seconds:" + str(jdata[0]["timestamp"]["snapshot_seconds"]),
"Architecture:" + jdata[0]["lscpu"]["architecture"],
"Model:" + jdata[0]["lscpu"]["model"],
"SerialNo:" + str(serial_no), 
"OS: Linux" + jdata[0]["os_release"]["pretty_name"] ]

nchart_end(web, hostname,config_str, buttonlist, summary)
web.close()

# The End
