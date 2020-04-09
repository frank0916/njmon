from njmon import app
from flask import render_template, request

import os, fnmatch, re, os.path, datetime

re_host = re.compile('^[^_]*')
re_mnth = re.compile('_(\d{6})\d{2}')
re_date = re.compile('_(\d+)_')
re_time  = re.compile('_(\d+)\.')

home = os.environ['HOME']
log_dir = home + '/njmon/log'
tmp_dir = home + '/njmon/tmp'
html_dir = home + '/njmon/html'
njmon_dir = home + '/njmon/njmon'


def get_logs(pattern):
    return fnmatch.filter(os.listdir(log_dir), pattern)


def get_log_files():
    return get_logs('*.json')


def get_hosts(s):
    return re_host.search(s).group()


def get_months(s):
    return re_mnth.search(s).group(1)


def get_dates(s):
    return re_date.search(s).group(1)


def get_times(s):
    return re_time.search(s).group(1)


def to_date(s):
    day = int(s)
    return datetime.date(day // 10000, day % 10000 // 100, day % 100)


def to_time(y4m2d2, h2m2):
    hhmm = int(h2m2)
    return datetime.datetime.combine(
        to_date(y4m2d2),
        datetime.time(hhmm // 100, hhmm % 100))


def fmt(dt, h):
    dt = dt + datetime.timedelta(hours=h)
    return dt.strftime('%Y%m%d_%H%M')


@app.route('/')
@app.route('/home')
@app.route('/1st')
def index():
    files = get_log_files()
    hosts = map(get_hosts, files)
    hosts = sorted(set(hosts))
    return render_template('1st.html', hosts=hosts)


@app.route('/2nd')
def date():
    host = request.args.get('host')
    files = get_log_files()
    files = filter(lambda x: x.startswith(host), files)
    months = map(get_months, files)
    months = sorted(set(months), reverse=True)
    return render_template('2nd.html', host=host, months=months)


@app.route('/3rd')
def mnth():
    host = request.args.get('host')
    month = request.args.get('month')
    files = get_log_files()
    files = filter(lambda x: x.startswith(host), files)
    days = map(get_dates, files)
    days = filter(lambda x: x.startswith(month), days)
    days = sorted(set(days), reverse=True)
    return render_template('3rd.html', host=host, days=days)


@app.route('/4th')
def time():
    host = request.args.get('host')
    y4m2d2 = request.args.get('day')
    day = to_date(y4m2d2)
    pattern = host + '_' + day.strftime('%Y%m%d') + '_*.json'
    files = get_logs(pattern)
    files = sorted(files)
    times = map(get_times, files)
    return render_template('4th.html', host=host, day=y4m2d2, times=times)


@app.route('/chart')
def chart():
    host = request.args.get('host')
    day = request.args.get('day')
    hhmm = request.args.get('time')
    hours = request.args.get('hours')
    new = request.args.get('new')

    file_name = host + '_' + day + '_' + hhmm + '_' + hours
    path_name = html_dir + '/' + file_name

    if new or not os.path.exists(path_name + '.html'):
        dt = to_time(day, hhmm)
        fw = open(path_name + '.json', '+w')
        hs = int(hours)
        for h in range(hs):
            fn = log_dir + '/' + host + '_' + fmt(dt, h) + '.json'
            if os.path.isfile(fn):
                f = open(fn)
                for line in f:
                    if not line.endswith('}\n'):
                        line = line[:-1]
                    fw.write(line)
                f.close()

        fw.flush()
        fw.close()

        cmd = njmon_dir + '/njmonchart.py '
        cmd = cmd + path_name + '.json '
        cmd = cmd + path_name + '.html'

        if os.system(cmd) != 0:
            return 'Failed to create html file'

    with open(path_name + '.html') as file:
        contents = file.read()

    return contents
