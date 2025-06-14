# Importar bibliotecas
import csv
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

################# cores ###############
co0 = "#f0f3f5"  # Preta
co1 = "#feffff"  # Branca
co2 = "#3fb5a3"  # Verde
co3 = "#fc766d"  # Vermelha
co4 = "#403d3d"  # Letra
co5 = "#4a88e8"  # Azul

# Criando janela
janela = Tk()
janela.title("Bloqueador de Sites")
janela.geometry("390x350")
janela.configure(background=co1)
janela.resizable(width=FALSE, height=FALSE)

# Frames
frame_logo = Frame(janela, width=400, height=60, bg=co1, relief="flat")
frame_logo.grid(row=0, column=0, pady=1, padx=0, sticky=NSEW)

frame_corpo = Frame(janela, width=400, height=400, bg=co1, relief="flat")
frame_corpo.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

# Configurando frame logo
imagem = Image.open('icon.png')
imagem = imagem.resize((44, 44))
imagem = ImageTk.PhotoImage(imagem)

l_imagem = Label(frame_logo, height=60, image=imagem)
l_imagem.place(x=20, y=5)

l_logo = Label(frame_logo, text='Bloqueador Sites', height=1, anchor=NE, font=("Ivy 25"), bg=co1, fg=co4)
l_logo.place(x=70, y=10)

l_linha = Label(frame_logo, text='', width=445, height=1, anchor=NW, font=("Ivy 1"), bg=co2)
l_linha.place(x=0, y=57)

#Criando funções -------------------

global iniciar
global websites

iniciar = BooleanVar()

# Função ver sites
def ver_site():
    listbox.delete(0, END)
    try:
        with open('sites.csv', 'r', newline='', encoding='utf-8') as file:
            ler_csv = csv.reader(file)
            for row in ler_csv:
                listbox.insert(END, row[0])
    except FileNotFoundError:
        open('sites.csv', 'w', encoding='utf-8').close()  # Cria o arquivo se não existir

# Função salvar site
def salvar_site(site):
    with open('sites.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([site])
    messagebox.showinfo('Site', 'O site foi adicionado')
    ver_site()

# Função deletar site
def deletar_site(site_para_remover):
    nova_lista = []
    with open('sites.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if site_para_remover.strip() not in row:
                nova_lista.append(row)

    with open('sites.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(nova_lista)

    messagebox.showinfo('Site', f'O site "{site_para_remover}" foi removido com sucesso.')
    ver_site()

# Função botão adicionar
def adicionar_site():
    site = e_site.get().strip()
    if site:
        salvar_site(site)
        e_site.delete(0, END)

# Função botão remover
def remover_site():
    site = listbox.get(ACTIVE)
    if site:
        deletar_site(site)


def desbloquear_site():
    iniciar.set(False)
    messagebox.showinfo('Site', 'Os sites na lista foram Desbloqueados')
    bloqueador_site()

def bloquear_site():
    iniciar.set(True)
    messagebox.showinfo('Site', 'Os sites na lista foram bloqueadas')
    bloqueador_site()


# Função bloqueador site
def bloqueador_site():
    import os

    # Caminho do arquivo hosts no Linux
    local_do_hosts = "/etc/hosts"
    redirecionar = '127.0.0.1'

    websites = []

    # Lendo os sites do CSV
    with open('sites.csv', 'r', encoding='utf-8') as file:
        ler_csv = csv.reader(file)
        for row in ler_csv:
            websites.append(row[0].strip())

    # Verifica se deve bloquear ou desbloquear
    if iniciar.get():  # Se está marcado, BLOQUEAR
        with open(local_do_hosts, 'r+', encoding='utf-8') as file:
            conteudo = file.read()
            for site in websites:
                entrada = f"{redirecionar} {site}"
                if entrada not in conteudo:
                    file.write(f"\n{entrada}")
        
    else:  # Se não está marcado, DESBLOQUEAR
        with open(local_do_hosts, 'r+', encoding='utf-8') as file:
            linhas = file.readlines()
            file.seek(0)
            for linha in linhas:
                if not any(site in linha for site in websites):
                    file.write(linha)
            file.truncate()
        messagebox.showinfo('Bloqueador', 'Sites desbloqueados com sucesso!')





# Configurando frame corpo
l_site = Label(frame_corpo, text='Digite o site que deseja bloquear *', height=1, anchor=NE, font=("Ivy 10 bold"), bg=co1, fg=co4)
l_site.place(x=20, y=20)

e_site = Entry(frame_corpo, width=18, justify='left', font=('', 15), highlightthickness=1, relief=SOLID)
e_site.place(x=23, y=50)

b_adicionar = Button(frame_corpo, command=adicionar_site, text='Adicionar', width=10, height=1, font=("Ivy 10 bold"), relief=RAISED, overrelief=RIDGE, bg=co5, fg=co1)
b_adicionar.place(x=280, y=50)

b_remover = Button(frame_corpo, command=remover_site, text='Remover', width=10, height=1, font=("Ivy 10 bold"), relief=RAISED, overrelief=RIDGE, bg=co2, fg=co1)
b_remover.place(x=280, y=100)

b_desbloquear = Button(frame_corpo, command=desbloquear_site, text='Desbloquear', width=10, height=1, font=("Ivy 10 bold"), relief=RAISED, overrelief=RIDGE, bg=co2, fg=co1)
b_desbloquear.place(x=280, y=150)

b_bloquear = Button(frame_corpo, command=bloquear_site, text='Bloquear', width=10, height=1, font=("Ivy 10 bold"), relief=RAISED, overrelief=RIDGE, bg=co3, fg=co1)
b_bloquear.place(x=280, y=200)

listbox = Listbox(frame_corpo, font=('Arial 9 bold'), width=33, height=10)
listbox.place(x=23, y=100)

# Inicializa a lista com sites do arquivo
ver_site()

# Inicia a interface
janela.mainloop()
