import subprocess
import re

server_ip = '192.168.0.105'
regex = '[0-9.-]*\s*sec\s*[0-9.]*\s*[A-Z]?Bytes\s*[0-9.]*\s*[A-Z]?bits/sec\s*[0-9]' \
        '*\s*[0-9.]*\s*[A-Z]?Bytes'
keys = ['Interval', 'Transfer', 'Bitrate', 'Retr', 'Cwnd']

def client(server_ip):
    p = subprocess.Popen(['iperf3', '-c', server_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result, error = p.communicate()
    return result, error

def parser(result):
    iperf_results = []
    parsed_list = re.findall(regex, result)
    for i in parsed_list:
        values = []
        values.append(re.search('[0-9.-]*(?=\s*sec)', i).group())
        values.append(float(re.search('[0-9.]*(?=\s*[A-Z]?Bytes)', i).group()))
        values.append(float(re.search('[0-9.]*(?=\s*[A-Z]?bits/sec)', i).group()))
        values.append(float(re.search('\s[0-9]\s', i).group()))
        values.append(float(re.search('[0-9.]*(?=\s*[A-Z]?Bytes\s*$)', i).group()))
        iperf_results.append(dict(zip(keys, values)))
    return iperf_results

result, error = client(server_ip)
iperf_results = parser(result)
if error:
    print(error)
else:
    for value in iperf_results:
        if value['Transfer'] > 2 and value['Bitrate'] > 20:
            print(value)
