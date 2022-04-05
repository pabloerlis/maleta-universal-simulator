'''
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
'''
#----------------------------------------------
from tkinter import Tk, filedialog




def choose_directory():
    '''
    Solicita ao usuário que selecione um diretório.
Opção de palavra-chave adicional:
mustexist - determina se a seleção deve ser um diretório existente.
    '''
    directory_root = Tk()
    directory_root.withdraw()
    path_work = filedialog.askdirectory()
    if path_work == '':
        print('path inválido')
        
        return choose_directory()
    else:
        return path_work
#---------------------------------------------------------
'''
cria uma Opencaixa de diálogo e retornam os nomes de arquivos 
selecionados que correspondem aos arquivos existentes.
'''
#print(filedialog.asksaveasfilename())
#---------------------------------------------------------
'''
Crie uma SaveAscaixa de diálogo e retorne um objeto de arquivo aberto no modo somente gravação.
'''
#filedialog.asksaveasfile( modo = "w" , ** opções ) 
filedialog.asksaveasfile (mode = 'w', defaultextension = "")
print(filedialog.asksaveasfile (mode = 'w', defaultextension = "").name)
#-------------------------------------------------------
