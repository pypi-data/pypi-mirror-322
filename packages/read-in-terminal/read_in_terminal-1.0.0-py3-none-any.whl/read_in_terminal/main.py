import sys, subprocess, os
from read_in_terminal import controller as control

args = sys.argv

def main():
    if len(args) < 2:
        print('Erro: Nenhum comando fornecido!')
        sys.exit()
    
    cmd = args[1:]
    
    match cmd[0]:
        case '--pyFile':
            if len(cmd)!=2:
                print('Erro: Insira os argumentos corretamente!')
                sys.exit()
            else:
                control.run_python_script(cmd[1])
        case _:
            control.read_terminal_history(cmd)

if __name__ == "__main__":
    main()
