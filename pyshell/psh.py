import os

def psh_exit(args):
    print("Good Bye!")
    return 0


def psh_cd(args):
    os.chdir(os.path.expanduser(args[1]))   
    print(os.path.abspath(os.path.curdir))
    return 1


def psh_execute(args):    
    #ignore empty lines
    if (args == []):
        return 1
    # check if command is a builtin, i.e. cd and exit

    if(args[0] in builtins):
        return builtins[args[0]](args)
        
    # fork the current process
    # the child will get pid 0    
    pid = os.fork()
    if pid == 0:
        # execute the command in the child
        os.execvp(args[0], args)
    else:
        # parent waits until child exits
        while True:
            wpid, status = os.waitpid(pid, 0)
            if os.WIFSIGNALED(status) or os.WIFEXITED(status):
                break
    return 1


def psh_loop():
    status=1
    while(status):
        # read input
        print("> ",end='')
        line = input()
        # tokenize
        args = line.split()
        # execute
        status = psh_execute(args)
    return status

builtins={'cd': psh_cd, 'exit': psh_exit}

if __name__ == '__main__':
    psh_loop()
    exit(0)

