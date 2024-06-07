import os
import send2trash
import tkinter as tk
from tkinter import messagebox, ttk
import platform
import psutil
import threading

try:
    import psutil_sensors
except ImportError:
    psutil_sensors = None

def limpar_cache():
    if messagebox.askyesno("Confirmação", "Tem certeza de que deseja limpar o cache? Essa ação não pode ser desfeita."):
        progress_window = tk.Toplevel(root)
        progress_window.title("Limpando Cache")
        progress_window.configure(bg="white")
        progress_window.geometry("300x100")
        progress_window.resizable(False, False)

        progress_label = tk.Label(progress_window, text="Limpando...", bg="white", font=('Helvetica', 14))
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=200, mode="indeterminate")
        progress_bar.pack(pady=5)

        progress_thread = threading.Thread(target=limpar_cache_thread, args=(progress_bar,))
        progress_thread.start()

def limpar_cache_thread(progress_bar):
    diretorios = [
        os.path.join(os.getenv("LOCALAPPDATA"), "Temp"),
        os.path.join(os.getenv("AppData"), "Mozilla\\Firefox\\Profiles"),
        os.path.join(os.getenv("AppData"), "Google\\Chrome\\User Data"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft\\Windows\\INetCache"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft\\Windows\\Caches"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft\\Edge\\User Data"),
        os.path.join(os.getenv("AppData"), "discord\\Cache"),
        os.path.join(os.getenv("AppData"), "Opera Software\\Opera GX Stable\\Cache"),
        os.path.join(os.getenv("AppData"), "BraveSoftware\\Brave-Browser\\User Data\\Cache"),
        os.path.join(os.getenv("AppData"), "Roblox\\Versions\\version-...\\Local Storage"),
        # Adicione mais diretórios aqui conforme necessário
    ]
    
    for diretorio in diretorios:
        for raiz, _, arquivos in os.walk(diretorio):
            for arquivo in arquivos:
                try:
                    send2trash.send2trash(os.path.join(raiz, arquivo))
                except Exception as e:
                    print(f"Erro ao excluir {os.path.join(raiz, arquivo)}: {e}")
                    continue
    messagebox.showinfo("Cache Limpo", "Cache limpo com sucesso!")

def informacoes_do_sistema():
    sistema = platform.system()
    release = platform.release()
    arquitetura = platform.machine()
    processador = platform.processor()
    nome_do_computador = platform.node()
    versao_do_python = platform.python_version()
    memoria_total = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    memoria_disponivel = round(psutil.virtual_memory().available / (1024 ** 3), 2)
    memoria_usada = round(psutil.virtual_memory().used / (1024 ** 3), 2)
    porcentagem_cpu = psutil.cpu_percent()
    porcentagem_memoria = psutil.virtual_memory().percent
    disco_total = round(psutil.disk_usage('/').total / (1024 ** 3), 2)
    disco_disponivel = round(psutil.disk_usage('/').free / (1024 ** 3), 2)
    disco_usado = round(psutil.disk_usage('/').used / (1024 ** 3), 2)
    ip = get_ip_address()
    ipv4 = get_ipv4_address()
    temperatura_cpu = get_cpu_temperature()
    temperatura_gpu = get_gpu_temperature()
    # Adicione mais informações conforme necessário

    info_window = tk.Toplevel(root)
    info_window.title("Informações do Sistema")
    info_window.configure(bg="white")

    info_label = tk.Label(info_window, text=f"""
    Sistema Operacional: {sistema} {release}
    Arquitetura: {arquitetura}
    Processador: {processador}
    Nome do Computador: {nome_do_computador}
    Versão do Python: {versao_do_python}
    Memória Total: {memoria_total} GB
    Memória Disponível: {memoria_disponivel} GB
    Memória Usada: {memoria_usada} GB
    Porcentagem de Uso de CPU: {porcentagem_cpu}%
    Porcentagem de Uso de Memória: {porcentagem_memoria}%
    Disco Total: {disco_total} GB
    Disco Disponível: {disco_disponivel} GB
    Disco Usado: {disco_usado} GB
    IP: {ip}
    IPv4: {ipv4}
    Temperatura da CPU: {temperatura_cpu}°C
    Temperatura da GPU: {temperatura_gpu}°C
    """, bg="white", fg="black")
    info_label.pack()

def get_ip_address():
    import socket
    return socket.gethostbyname(socket.gethostname())

def get_ipv4_address():
    import socket
    return socket.gethostbyname_ex(socket.gethostname())[-1]

def get_cpu_temperature():
    if psutil_sensors:
        sensors = psutil_sensors.sensors_temperatures()
        if 'coretemp' in sensors:
            for entry in sensors['coretemp']:
                if entry.label == 'Package id 0':
                    return entry.current
    return "N/A"

def get_gpu_temperature():
    if psutil_sensors:
        sensors = psutil_sensors.sensors_temperatures()
        if 'amdgpu' in sensors:
            for entry in sensors['amdgpu']:
                if entry.label == 'edge':
                    return entry.current
        if 'nouveau' in sensors:
            for entry in sensors['nouveau']:
                if entry.label == 'GPU':
                    return entry.current
    return "N/A"

root = tk.Tk()
root.title("Utilitário de Limpeza e Informações do Sistema")
root.configure(bg="white")

style = ttk.Style()
style.configure('TButton', foreground='black', background='lightblue', font=('Helvetica', 12))

title_label = tk.Label(root, text="Made by: Vexy", bg="white", fg="red", font=('Helvetica', 16, 'bold'))
title_label.pack(pady=10)

cache_button = ttk.Button(root, text="Limpar Cache", command=limpar_cache)
cache_button.pack(pady=10)

info_button = ttk.Button(root, text="Informações do Sistema", command=informacoes_do_sistema)
info_button.pack(pady=10)

root.mainloop()