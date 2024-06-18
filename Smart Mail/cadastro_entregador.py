import tkinter as tk
import sqlite3

class CadastroEntregador:
    def __init__(self):
        self.janela = tk.Tk()
        self.criar_tabela() 
        self.tela_cadastro()

    def tela_cadastro(self):
        self.janela.geometry("460x540")
        self.janela.title("Cadastro de Entregador")

        label_nome_completo = tk.Label(self.janela, text="Nome Completo:")
        label_nome_completo.grid(row=0, column=0, pady=5, sticky="w")
        self.entry_nome_completo = tk.Entry(self.janela, width=25)
        self.entry_nome_completo.grid(row=0, column=1, pady=5, columnspan=3, sticky="w")

        cpf_label = tk.Label(self.janela, text="CPF:")
        cpf_label.grid(row=1, column=0, pady=5, sticky="w")
        self.cpf_entry = tk.Entry(self.janela, width=25)
        self.cpf_entry.grid(row=1, column=1, pady=5, sticky="w")

        email_label = tk.Label(self.janela, text="Email:")
        email_label.grid(row=2, column=0, pady=5, sticky="w")
        self.email_entry = tk.Entry(self.janela, width=25)
        self.email_entry.grid(row=2, column=1, pady=5, sticky="w")

        telefone_label = tk.Label(self.janela, text="Telefone:")
        telefone_label.grid(row=3, column=0, pady=5, sticky="w")
        self.telefone_entry = tk.Entry(self.janela, width=25)
        self.telefone_entry.grid(row=3, column=1, pady=5, sticky="w")

        senha1_label = tk.Label(self.janela, text="Cadastre sua Senha:")
        senha1_label.grid(row=4, column=0, pady=5, sticky="w")
        self.senha1_entry = tk.Entry(self.janela, width=25, show="*")
        self.senha1_entry.grid(row=4, column=1, pady=5, sticky="w")

        senha2_label = tk.Label(self.janela, text="Confirme sua Senha:")
        senha2_label.grid(row=5, column=0, pady=5, sticky="w")
        self.senha2_entry = tk.Entry(self.janela, width=25, show="*")
        self.senha2_entry.grid(row=5, column=1, pady=5, sticky="w")

        botao_salvar = tk.Button(self.janela, text="Salvar", command=self.cadastrar)
        botao_salvar.grid(row=6, column=1, columnspan=1, pady=10)


        self.janela.mainloop()

    def criar_tabela(self):
        conn = sqlite3.connect('meubanco.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Cadastro_Entregador (
                    id INTEGER PRIMARY KEY,
                    nome_completo TEXT NOT NULL,
                    cpf INTEGER UNIQUE,
                    email TEXT UNIQUE NOT NULL,
                    telefone INTEGER,
                    senha1 TEXT NOT NULL
                )
            """)
            conn.commit()
            print("Tabela criada com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")
        finally:
            conn.close()


    def cadastrar(self):
        nome_completo_valor = self.entry_nome_completo.get()
        cpf_valor = self.cpf_entry.get()
        email_valor = self.email_entry.get()
        telefone_valor = self.telefone_entry.get()
        senha1_valor = self.senha1_entry.get()
        senha2_valor = self.senha2_entry.get()

        if nome_completo_valor == "" or email_valor == "" or senha1_valor == "" or senha2_valor == "":
            print("Por favor, preencha todos os campos obrigatórios.")
            return

        if senha1_valor != senha2_valor:
            print("As senhas digitadas não correspondem.")
            return

        conn = sqlite3.connect('meubanco.db')
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM Cadastro_Entregador WHERE cpf = ? OR email = ?", (cpf_valor, email_valor))
            if cursor.fetchone() is not None:
                print("CPF ou Email já cadastrado.")
                return

            cursor.execute("""
                INSERT INTO Cadastro_Entregador (nome_completo, cpf, email, telefone, senha1)
                VALUES (?, ?, ?, ?, ?)
            """, (nome_completo_valor, cpf_valor, email_valor, telefone_valor, senha1_valor))
            conn.commit()
            print("Dados cadastrados com sucesso.")

            self.janela.destroy()
        except sqlite3.Error as e:
            print(f"Erro ao cadastrar dados: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    app = CadastroEntregador()

