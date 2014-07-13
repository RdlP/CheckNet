# -*- coding: utf-8 -*-

import subprocess
import sys, os
import struct
import time
import platform
import Skype4Py
try:
    import pynotify
except ImportError:
    from win32api import *
    from win32gui import *
    import win32con

class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = { win32con.WM_DESTROY: self.OnDestroy,}

        # Registramos la clase.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = 'PythonTaskbar'
        wc.lpfnWndProc = message_map # Podríamos registrar tamnbién un wndproc.
        classAtom = RegisterClass(wc)

        # Creamos la ventana.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(classAtom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, hinst, None)
        UpdateWindow(self.hwnd)

        # Iconos
        iconPathName = os.path.abspath(os.path.join( sys.path[0], 'ICON.ico' ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, 'Tooltip')

         # Notificación
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20, hicon, 'Balloon Tooltip', msg, 200, title))
        # self.show_balloon(title, msg)
        time.sleep(10)

        # Destrucción
        DestroyWindow(self.hwnd)
        classAtom = UnregisterClass(classAtom, hinst)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminamos.

def showNotifyUnix(title, error):
    n = pynotify.Notification(title,
    error
    )
    n.show()

def showNotifyWindows(title, error):
    w=WindowsBalloonTip(title, error)

def command(Message, Status):
    fail = False
    fails = []
    for host in hosts.keys():
        if hosts[host] == True:
            fail = True
            fails.append(host)
    if fail == True:
        if Status == 'RECEIVED':
            Message.Chat.SendMessage('Hola ' + Message.FromDisplayName.encode("utf-8") + ".\nSoy un programa informático realizado por Ángel Luis para casos en los que la red no funciona. Si tu mensaje es para avisarme de que la red no funciona o el almacenamiento en la nube no funciona, no te preocupes, ya estoy trabajando en ello ;) si por el contrario tu mensaje es para cualquier otra causa entonces déjamela aquí escrita.\n\nSi es un problema relacionado con la red los routers que actualmente están dando problemas son:"+ "\n".join(fails) + "\n\nSi sabes cambiarte de router cambiate a alguno de los siguientes routers que no aparezcan en la lista anterior mientras trabajo en arreglar el problema:\n\nxxx.xxx.xxx.xxx\nyyy.yyyy.yyy.yyyy\nzzz.zzz.zzz.zzz") 

print "Iniciando comprobador de servidores y routers..."
hosts = {"xxx.xxx.xxx.xxx": False, "yyy.yyy.yyy.yyy": False, "zzz.zzz.zzz.zzz": False}
print "Router a comprobar:"
for host in hosts:
    print host
print "Servidores a comprobar:"
servers = ["aaa.aaa.aaa.aaa", "bbb.bbb.bbb.bbb", "ccc.ccc.ccc.ccc"]
for server in servers:
    print server
print "Comprobador de servidores y routers iniciado."
print ""
print "Mantenga esta ventana abierta, aunque puede minimizarla, si se cierra el comprobador de servidores y routers dejará de funcionar"
print ""
print "En cuanto el comprobador encuentre un router o servidor caído le avisará mediante una notificación"

skype = Skype4Py.Skype(); 
skype.OnMessageStatus = command 
skype.Attach();  
while True:
    for host in hosts.keys():
        if platform.system() == "Linux":
            ping = subprocess.Popen(
                ["ping", "-c", "3", host],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
        elif platform.system() == "Windows":
            ping = subprocess.Popen(
                ["ping", "-n", "3", host],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
        else:
            print "Sistema operativo no soportado"
            sys.exit()
        out, error = ping.communicate()
        if platform.system() == "Linux":
            if "agotado" in out:
                hosts[host] = True
                showNotifyWindows("Router Caido","El router " + host + " no responde")
            else:
                hosts[host] = False
        elif platform.system() == "Windows":
            if "agotado" in out:
                hosts[host] = True
                showNotifyWindows("Router Caido","El router " + host + " no responde")
            else:
                hosts[host] = False

    for server in servers:
        if platform.system() == "Linux":
            ping = subprocess.Popen(
                ["ping", "-c", "3", server],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
        elif platform.system() == "Windows":
            ping = subprocess.Popen(
                ["ping", "-n", "3", server],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
        else:
            print "Sistema operativo no soportado"
            sys.exit()
        out, error = ping.communicate()
        if platform.system() == "Linux":
            pass
        elif platform.system() == "Windows":
            if "agotado" in out:
                showNotifyWindows("Servidor Caido", "El servidor " + server + " no responde")
