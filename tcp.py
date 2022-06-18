import logging

logging.basicConfig(level=logging.INFO, format=' - %(message)s')
FSDictionary = {
    'CLOSED': {'APP_PASSIVE_OPEN': 'LISTEN',
               'APP_ACTIVE_OPEN': 'SYN_SENT'},

    'LISTEN': {'RCV_SYN': 'SYN_RCVD',
               'APP_SEND': 'SYN_SENT',
               'APP_CLOSE': 'CLOSED'},

    'SYN_RCVD': {'APP_CLOSE': 'FIN_WAIT_1',
                 'RCV_ACK': 'ESTABLISHED'},

    'SYN_SENT': {
        'RCV_SYN': 'SYN_RCVD',
        'RCV_SYN_ACK': 'ESTABLISHED',
        'APP_CLOSE': 'CLOSED'},

    'ESTABLISHED': {'APP_CLOSE': 'FIN_WAIT_1',
                    'RCV_FIN': 'CLOSE_WAIT'},
    'FIN_WAIT_1': {'RCV_FIN': 'CLOSING',
                   'RCV_FIN_ACK': 'TIME_WAIT',
                   'RCV_ACK': 'FIN_WAIT_2'},

    'CLOSING': {'RCV_ACK': 'TIME_WAIT'},
    'FIN_WAIT_2': {'RCV_FIN': 'TIME_WAIT'},
    'TIME_WAIT': {'APP_TIMEOUT': 'CLOSED'},
    'CLOSE_WAIT': {'APP_CLOSE': 'LAST_ACK'},
    'LAST_ACK': {'RCV_ACK': 'CLOSED'}

}


def traverse_TCP_states(events):
    state = "CLOSED"
    for fs in events:
        try:
            state = FSDictionary[state][fs]
            logging.info(state)
        except TypeError or KeyError:
            return 'ERROR'
    return state


stateCode1 = ['APP_PASSIVE_OPEN', 'RCV_SYN', 'RCV_ACK', 'APP_CLOSE']
stateCode2 = ['APP_ACTIVE_OPEN', 'RCV_SYN', 'APP_CLOSE', 'RCV_FIN', 'RCV_ACK', 'APP_TIMEOUT']
stateCode3 = ['APP_ACTIVE_OPEN', 'RCV_SYN', 'APP_CLOSE', 'RCV_FIN', 'RCV_ACK', 'APP_TIMEOUT']
r = traverse_TCP_states(stateCode3)
print(r)
