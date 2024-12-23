import tkinter as tk
from tkinter import messagebox
import sqlite3

def criar_tabela():
    conexao = sqlite3.connect("estoque.db")
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bebidas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        tipo TEXT NOT NULL,
                        marca TEXT NOT NULL,
                        quantidade INTEGER NOT NULL,
                        valor REAL NOT NULL,
                        cod_id TEXT NOT NULL UNIQUE)''')
    conexao.commit()
    conexao.close()

def cadastrar_bebida():
    nome = entry_nome.get()
    tipo = entry_tipo.get()
    marca = entry_marca.get()
    quantidade = entry_quantidade.get()
    valor = entry_valor.get()
    cod_id = entry_cod_id.get()

    if not (nome and tipo and marca and quantidade and valor and cod_id):
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return

    try:
        quantidade = int(quantidade)
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e Valor devem ser numéricos!")
        return

    conexao = sqlite3.connect("estoque.db")
    cursor = conexao.cursor()
    try:
        cursor.execute('''INSERT INTO bebidas (nome, tipo, marca, quantidade, valor, cod_id)
                          VALUES (?, ?, ?, ?, ?, ?)''', (nome, tipo, marca, quantidade, valor, cod_id))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Bebida cadastrada com sucesso!")
        limpar_campos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Código ID já cadastrado!")
    conexao.close()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_tipo.delete(0, tk.END)
    entry_marca.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_valor.delete(0, tk.END)
    entry_cod_id.delete(0, tk.END)

def consultar_estoque():
    conexao = sqlite3.connect("estoque.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM bebidas")
    registros = cursor.fetchall()
    conexao.close()

    janela_consulta = tk.Toplevel(root)
    janela_consulta.title("Consulta de Estoque")

    text = tk.Text(janela_consulta, wrap=tk.WORD, width=80, height=20)
    text.pack(padx=10, pady=10)

    if registros:
        for reg in registros:
            text.insert(tk.END, f"ID: {reg[0]} | Nome: {reg[1]} | Tipo: {reg[2]} | Marca: {reg[3]} | Quantidade: {reg[4]} | Valor: R${reg[5]:.2f} | Cod ID: {reg[6]}\n")
            text.insert(tk.END, "-" * 80 + "\n")
    else:
        text.insert(tk.END, "Nenhum registro encontrado.")

# Configurações da janela principal
root = tk.Tk()
root.title("Cadastro de Bebidas")
root.geometry("600x400")
root.configure(bg="#d3d3d3")

# Título
label_titulo = tk.Label(root, text="Cadastro", font=("Arial", 20, "bold"), bg="#d3d3d3")
label_titulo.pack(pady=10)

# Frame para os campos
frame_campos = tk.Frame(root, bg="#d3d3d3")
frame_campos.pack(pady=20)

# Nome
label_nome = tk.Label(frame_campos, text="Nome", bg="#d3d3d3", font=("Arial", 12))
label_nome.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_nome = tk.Entry(frame_campos, width=25)
entry_nome.grid(row=0, column=1, pady=5)

# Quantidade
label_quantidade = tk.Label(frame_campos, text="Quantidade", bg="#d3d3d3", font=("Arial", 12))
label_quantidade.grid(row=0, column=2, padx=10, pady=5, sticky="e")
entry_quantidade = tk.Entry(frame_campos, width=15)
entry_quantidade.grid(row=0, column=3, pady=5)

# Tipo
label_tipo = tk.Label(frame_campos, text="Tipo", bg="#d3d3d3", font=("Arial", 12))
label_tipo.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_tipo = tk.Entry(frame_campos, width=25)
entry_tipo.grid(row=1, column=1, pady=5)

# Valor
label_valor = tk.Label(frame_campos, text="Valor", bg="#d3d3d3", font=("Arial", 12))
label_valor.grid(row=1, column=2, padx=10, pady=5, sticky="e")
entry_valor = tk.Entry(frame_campos, width=15)
entry_valor.grid(row=1, column=3, pady=5)

# Marca
label_marca = tk.Label(frame_campos, text="Marca", bg="#d3d3d3", font=("Arial", 12))
label_marca.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_marca = tk.Entry(frame_campos, width=25)
entry_marca.grid(row=2, column=1, pady=5)

# Cod ID
label_cod_id = tk.Label(frame_campos, text="Cod ID", bg="#d3d3d3", font=("Arial", 12))
label_cod_id.grid(row=2, column=2, padx=10, pady=5, sticky="e")
entry_cod_id = tk.Entry(frame_campos, width=15)
entry_cod_id.grid(row=2, column=3, pady=5)

# Botão Cadastrar
botao_cadastrar = tk.Button(root, text="Cadastrar", command=cadastrar_bebida, bg="#4d4d4d", fg="white", font=("Arial", 12), width=15)
botao_cadastrar.pack(pady=10)

# Botão Consultar Estoque
botao_consultar = tk.Button(root, text="Consultar Estoque", command=consultar_estoque, bg="#4d4d4d", fg="white", font=("Arial", 12), width=15)
botao_consultar.pack(pady=10)

# Inicialização do banco de dados
criar_tabela()

# Loop principal
root.mainloop()
