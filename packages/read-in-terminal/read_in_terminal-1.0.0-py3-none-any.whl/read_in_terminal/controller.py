import subprocess, os, pyttsx3
from read_in_terminal import utils as util


engine = pyttsx3.init()
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "terminal_log.txt")

os.makedirs(LOG_DIR, exist_ok=True)

def run_command_and_log(command):
    # Executa um comando no terminal e salva no log, usando subprocess
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        log.write(f"\n> {' '.join(command)}\n")  # Salva o comando digitado

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, errors="replace")
            output = result.stdout + result.stderr
        except Exception as e:
            output = f"Erro ao executar o comando: {e}"

        log.write(output + "\n")
        return output

def read_terminal_history(command):
    #Le o comando salvo no arquivo de historico, executa comandos e fala o conteúdo
    output = run_command_and_log(command)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as file:
            history = file.read()
            print(history)
            util.keyPressed()
            util.speak(history)
            return history
    else:
        history = "Nenhum histórico encontrado."
        print(history)
        util.speak(history)
        return history

def run_python_script(script_name):
    # Executa um arquivo Python no terminal e retorna sua saida, ou o erro
    current_directory = os.getcwd()
    script_path = os.path.join(current_directory, script_name)
    util.keyPressed()
    
    if not os.path.exists(script_path):
        error_msg = f"Erro: O arquivo '{script_name}' não foi encontrado no diretório '{current_directory}'"
        print(error_msg)
        util.speak(error_msg)
        return error_msg

    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )
    
    # Se for 0 a saida foi bem sucedida
    if result.returncode == 0:
        output = result.stdout.strip()
        print("Saída do script: \n", output)
        util.speak(output)
        return output
    else:
        error_msg = f"Erro ao executar o script:\n{result.stderr.strip()}"
        print(error_msg)
        util.speak(error_msg)
        return error_msg