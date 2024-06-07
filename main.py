import os
import send2trash
import tkinter as tk
from tkinter import messagebox, ttk
import platform
import psutil
import threading
import subprocess
import wmi

def limpar_cache():
    global stop_cleanup
    stop_cleanup = False
    if messagebox.askyesno("Confirmação", "Tem certeza de que deseja limpar o cache do sistema? Essa ação não pode ser desfeita."):
        progress_window = tk.Toplevel(root)
        progress_window.title("Limpando Cache")
        progress_window.configure(bg="white")
        progress_window.geometry("300x100")
        progress_window.resizable(False, False)
        progress_window.protocol("WM_DELETE_WINDOW", stop_cleanup_cleanup)

        progress_label = tk.Label(progress_window, text="Limpando...", bg="white", font=('Helvetica', 14))
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=200, mode="indeterminate")
        progress_bar.pack(pady=5)

        progress_thread = threading.Thread(target=limpar_cache_thread, args=(progress_bar,))
        progress_thread.start()

def stop_cleanup_cleanup():
    global stop_cleanup
    stop_cleanup = True

def limpar_cache_thread(progress_bar):
    global stop_cleanup
    diretorios = [
        os.path.join(os.getenv("LOCALAPPDATA"), "Temp"),  # Pasta Temp local
        os.path.join(os.getenv("AppData"), "Mozilla\\Firefox\\Profiles"),  # Perfis do Firefox
        os.path.join(os.getenv("AppData"), "Google\\Chrome\\User Data"),  # Dados do usuário do Chrome
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft\\Windows\\INetCache"),  # Cache do Internet Explorer
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft\\Windows\\Caches"),  # Cache do sistema Windows
        os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft\\Edge\\User Data"),  # Dados do usuário do Microsoft Edge
        os.path.join(os.getenv("AppData"), "discord\\Cache"),  # Cache do Discord
        os.path.join(os.getenv("AppData"), "Opera Software\\Opera GX Stable\\Cache"),  # Cache do Opera GX
        os.path.join(os.getenv("AppData"), "BraveSoftware\\Brave-Browser\\User Data\\Cache"),  # Cache do Brave Browser
        os.path.join(os.getenv("AppData"), "Roblox\\Versions\\version-...\\Local Storage"),  # Armazenamento local do Roblox
        os.path.join(os.getenv("AppData"), "Microsoft\\Windows\\Explorer\\Recent"),  # Pastas recentes do Windows Explorer
        os.path.join(os.getenv("AppData"), "Microsoft\\Teams\\Cache"),  # Cache do Microsoft Teams
        os.path.join(os.getenv("AppData"), "Microsoft\\Teams\\databases"),  # Bancos de dados do Microsoft Teams
        os.path.join(os.getenv("AppData"), "Microsoft\\Teams\\GPUCache"),  # Cache de GPU do Microsoft Teams
        os.path.join(os.getenv("AppData"), "Microsoft\\Teams\\IndexedDB"),  # Banco de dados indexado do Microsoft Teams
        os.path.join(os.getenv("AppData"), "Microsoft\\Teams\\Local Storage"),  # Armazenamento local do Microsoft Teams
        os.path.join(os.getenv("AppData"), "Microsoft\\Teams\\tmp"),  # Temp do Microsoft Teams
        os.path.join(os.getenv("AppData"), "Steam\\htmlcache"),  # Cache HTML do Steam
        os.path.join(os.getenv("AppData"), "Steam\\config\\htmlcache"),  # Configuração do cache HTML do Steam
        # Adicionar mais no futuro
    ]

    
    for diretorio in diretorios:
        if stop_cleanup:
            break
        for raiz, _, arquivos in os.walk(diretorio):
            if stop_cleanup:
                break
            for arquivo in arquivos:
                try:
                    send2trash.send2trash(os.path.join(raiz, arquivo))
                except Exception as e:
                    print(f"Erro ao excluir {os.path.join(raiz, arquivo)}: {e}")
                    continue
    if not stop_cleanup:
        messagebox.showinfo("Cache Limpo", "Cache limpo com sucesso! Verifique sua lixeira")

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
    if platform.system() == "Windows":
        return get_windows_cpu_temperature()
    else:
        return "N/A"  # Implementação para outros sistemas operacionais

def get_windows_cpu_temperature():
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        cpu_temperature = [sensor.Value for sensor in temperature_infos if "CPU" in sensor.Name]
        if cpu_temperature:
            return f"{cpu_temperature[0]} °C"
        else:
            return "N/A"
    except Exception as e:
        print(f"Erro ao obter a temperatura da CPU: {e}")
        return "N/A"

def get_gpu_temperature():
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