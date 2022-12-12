import re

regex = '[0-9.-]*\s*sec\s*[0-9.]*\s*[A-Z]?Bytes\s*[0-9.]*\s*[A-Z]?bits/sec\s*[0-9]' \
        '*\s*[0-9.]*\s*[A-Z]?Bytes'
keys = ['Interval', 'Transfer', 'Bitrate', 'Retr', 'Cwnd']

def parse(result):
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

