import time

stream = None

def write(msg):
    if stream:
        stream.write(msg)
        stream.flush()

def wait(msg, condition):
    num_dots = 0
    max_num_dots = 12
    while not condition():
        msg_with_dots = msg + "." * num_dots + " " * (max_num_dots - num_dots) + "\r"
        write(msg_with_dots)
        num_dots += 1
        if num_dots > max_num_dots:
            num_dots = 0

        time.sleep(0.5)

def clear():
    if stream:
        stream.write(" "*127 + "\r")
