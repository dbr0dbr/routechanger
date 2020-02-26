#!/usr/bin/env python3
import time
import os
import logging
from config import first, second, log

cmd = 'systemctl status routechanger | grep "Active: active (running)"'
serviceRun = list(os.popen(cmd))

logging.basicConfig(
    filename=log,
    level=logging.WARN,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

def test_inet(test_hosts):
    """
    Тестирует подключения, принимает массив тестируемых IP.
    Добавляет в массив значений провайдера наименьшее из значений потерь 
    протестированных через него IP
    """
    first_values, second_values = [], []
    fpingCmd = 'fping -q -s -c 10 -i 1 -p 20 ' + ' '.join(test_hosts) + ' 2>&1'
    fpingRespone = list(os.popen(fpingCmd))
    for line in fpingRespone:
        if not line.rstrip(): continue
        ip = line.rstrip().split()[0]
        if ip in test_hosts:
            value = int(line.split()[4].split('/')[2].split('%')[0])
            if ip in first.test_hosts:
                first_values.append(value)
                if value != 0: 
                    logging.info(first.name + ':' + line.rstrip())
            elif ip in second.test_hosts:
                second_values.append(value)
                if value != 0:
                    logging.info(second.name + ':' + line.rstrip())
    first.add_value(min(first_values))
    second.add_value(min(second_values))

def logging_status(log_comment):
    first.log_status(log_comment)
    second.log_status(log_comment)

while True:
    test_inet(first.test_hosts + second.test_hosts)
    if first.is_bad() and first.is_default() and not second.is_bad():
        second.set_default()
        logging_status(first.name + ' is down, swich to ' + second.name)
    elif first.can_resume() and not first.is_default():
        first.set_default()
        logging_status(first.name + ' ok, resume to ' + first.name)
    elif first.is_bad() and second.is_bad():
        if first.last == 0 and second.last == 100 and not first.is_default():
            first.set_default()
            logging_status('all is bad, swich to ' + first.name)
        elif second.last == 0 and first.last == 100 and not second.is_default():
            second.set_default()
            logging_status('all is bad, swich to ' + first.name)
        elif sum(first.ping_list) < sum(second.ping_list) and not first.is_default():
            first.set_default()
            logging_status('all is bad, swich to ' + first.name)
        elif sum(first.ping_list) > sum(second.ping_list) and not second.is_default():
            second.set_default()
            logging_status('all is bad, swich to ' + second.name)
    time.sleep(30) 
