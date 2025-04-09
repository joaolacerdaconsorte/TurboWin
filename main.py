import customtkinter as ctk
from tkinter import messagebox
import psutil, os, shutil, ctypes, time, platform, subprocess
import sys

# Função para carregar o ícone corretamente no executável
def recurso_caminho(relativo):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relativo)

# Configuração da interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("TurboWin - Otimizador de Desempenho 🚀")
app.geometry("600x550")

# Ícone compatível com o .exe
app.iconbitmap(recurso_caminho("assets/icone.ico"))

status_var = ctk.StringVar(value="Pronto.")

# Funções
def progresso(valor, mensagem):
    progress.set(valor)
    status_var.set(mensagem)
    app.update_idletasks()
    time.sleep(0.5)

def liberar_memoria():
    progresso(20, "🧠 Liberando memória...")
    encerrados = 0
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            if proc.info['memory_info'].rss > 100 * 1024 * 1024 and "python" not in proc.info['name'].lower():
                proc.terminate()
                encerrados += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    messagebox.showinfo("Memória", f"{encerrados} processos encerrados.")

def limpar_temporarios():
    progresso(50, "🧹 Limpando arquivos temporários...")
    paths = [os.getenv('TEMP'), os.getenv('TMP'), r'C:\Windows\Temp']
    removidos = 0
    for path in paths:
        try:
            for file in os.listdir(path):
                full = os.path.join(path, file)
                if os.path.isfile(full) or os.path.islink(full):
                    os.unlink(full)
                    removidos += 1
                elif os.path.isdir(full):
                    shutil.rmtree(full, ignore_errors=True)
                    removidos += 1
        except:
            continue
    messagebox.showinfo("Limpeza", f"{removidos} arquivos removidos!")

def boost_performance():
    progresso(80, "🚀 Aplicando boost de performance...")
    try:
        SPI_SETANIMATION = 0x0049
        class ANIMATIONINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("iMinAnimate", ctypes.c_int)]
        ai = ANIMATIONINFO()
        ai.cbSize = ctypes.sizeof(ANIMATIONINFO)
        ai.iMinAnimate = 0
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETANIMATION, ai.cbSize, ctypes.byref(ai), 0)
        messagebox.showinfo("Boost", "Boost aplicado! Animações desativadas.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao aplicar boost: {e}")

def limpar_downloads():
    pasta = os.path.expanduser("~\\Downloads")
    count = 0
    for file in os.listdir(pasta):
        try:
            full = os.path.join(pasta, file)
            if os.path.isfile(full):
                os.remove(full)
                count += 1
            elif os.path.isdir(full):
                shutil.rmtree(full)
                count += 1
        except:
            continue
    messagebox.showinfo("Downloads", f"{count} arquivos apagados da pasta Downloads!")

def info_sistema():
    info = f"Sistema: {platform.system()} {platform.release()}\n"
    info += f"CPU: {platform.processor()}\n"
    info += f"RAM Total: {round(psutil.virtual_memory().total / (1024**3), 2)} GB\n"
    info += f"Uso de Disco: {psutil.disk_usage('/').percent}%\n"
    info += f"Tempo ligado: {round(psutil.boot_time())}"
    messagebox.showinfo("Info do Sistema", info)

def reiniciar_explorer():
    try:
        subprocess.run("taskkill /f /im explorer.exe", shell=True)
        time.sleep(1)
        subprocess.run("start explorer", shell=True)
        messagebox.showinfo("Explorer", "Windows Explorer reiniciado!")
    except:
        messagebox.showerror("Erro", "Não foi possível reiniciar o Explorer.")

def modo_turbo():
    progresso(10, "🔧 Iniciando Modo Turbo...")
    liberar_memoria()
    limpar_temporarios()
    boost_performance()
    limpar_downloads()
    progresso(100, "✅ Tudo pronto!")
    messagebox.showinfo("TurboWin", "Seu PC foi otimizado com sucesso! 🚀")

# Layout
ctk.CTkLabel(app, text="TurboWin", font=("Helvetica", 28, "bold"), text_color="#98c379").pack(pady=10)
ctk.CTkLabel(app, text="Otimize seu Windows com um clique!", font=("Helvetica", 15)).pack(pady=5)

ctk.CTkButton(app, text="🧠 Liberar Memória", command=liberar_memoria, fg_color="#61afef", width=320).pack(pady=7)
ctk.CTkButton(app, text="🧹 Limpar Temporários", command=limpar_temporarios, fg_color="#98c379", width=320).pack(pady=7)
ctk.CTkButton(app, text="📁 Limpar Downloads", command=limpar_downloads, fg_color="#e5c07b", width=320).pack(pady=7)
ctk.CTkButton(app, text="🚀 Boost Performance", command=boost_performance, fg_color="#e06c75", width=320).pack(pady=7)
ctk.CTkButton(app, text="💻 Info do Sistema", command=info_sistema, fg_color="#56b6c2", width=320).pack(pady=7)
ctk.CTkButton(app, text="🔄 Reiniciar Explorer", command=reiniciar_explorer, fg_color="#c678dd", width=320).pack(pady=7)
ctk.CTkButton(app, text="🔥 MODO TURBO", command=modo_turbo, fg_color="#be5046", hover_color="#a8463a", width=340, height=45, font=("Helvetica", 14, "bold")).pack(pady=15)

progress = ctk.CTkProgressBar(app, width=400)
progress.set(0)
progress.pack(pady=10)

ctk.CTkLabel(app, textvariable=status_var).pack()

app.mainloop()
