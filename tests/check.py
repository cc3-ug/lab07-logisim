from subprocess import run
from subprocess import PIPE
from tabulate import tabulate


# executes a shell command
def execute(cmd=[], shell=False, timeout=5):
    return run(cmd, shell=shell, stdout=PIPE, stderr=PIPE, timeout=timeout)


# reads a file
def read(filename):
    f = open(filename, 'r')
    text = f.read()
    f.close()
    return text.strip()


# creates a pretty result report
def create_report(table):
    return tabulate(table, headers=['Exercise', 'Grade', 'Message'])


# checks alu.circ
def check_ALU():
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/ALU.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip()
    expected = read('tests/expected/ALU')
    if output == expected:
        return (100, 'passed', '')
    else:
        return (0, 'failed', '')


# checks lab 7
def lab7_logisim():
    alu_result = check_ALU()
    table = [('1. ALU', *alu_result[0: 2])]
    errors = alu_result[2]
    errors = errors.strip()
    grade = alu_result[0]
    grade = min(round(grade), 100)
    report = create_report(table)
    if errors != '':
        report += '\n\nMore Info:\n\n' + errors
    print(report)
    print('\n=> Score: %d/100' % grade)


if __name__ == '__main__':
    lab7_logisim()
