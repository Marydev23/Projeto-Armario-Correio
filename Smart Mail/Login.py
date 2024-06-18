import tkinter as tk
import sqlite3

class Login:
    def __init__(self):
        self.janela = tk.Tk()
        self.tela_login()

    def tela_login(self):
        self.janela.geometry("600x400")
        self.janela.title("Tela de Login")

        def verificar_login():
            email = login_usuario.get()
            senha = senha_usuario.get()

            conn = sqlite3.connect('meubanco.db')
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT * FROM Cadastro WHERE email=? AND senha1=?", (email, senha))
                user = cursor.fetchone()
                if user:
                    print("Login correto!")
                else:
                    print("Invalido.")
            except sqlite3.Error as e:
                print(f"Error: {e}")
            finally:
                conn.close()

        def senha():
            print("Esqueci Minha Senha")

        def abrir_cadastro():
            self.janela.destroy()
            Cadastro().janela.mainloop()

        def sair():
            self.janela.destroy()
            print("Saindo...")

        texto = tk.Label(self.janela, text="Fazer Login", font=("Arial", 18))
        texto.pack(padx=10, pady=20)

        login_usuario = tk.Entry(self.janela, font=("Arial", 10))
        login_usuario.pack(padx=10, pady=10)

        senha_usuario = tk.Entry(self.janela, show="*", font=("Arial", 10))
        senha_usuario.pack(padx=10, pady=10)

        esq_senha = tk.Button(self.janela, text="Esqueci Minha Senha", command=senha, font=("Arial", 10))
        esq_senha.pack(padx=10, pady=10)

        cadastro = tk.Button(self.janela, text="Não tenho Cadastro", command=abrir_cadastro, font=("Arial", 10))
        cadastro.pack(padx=10, pady=10)

        botao_login = tk.Button(self.janela, text="Login", command=verificar_login, font=("Arial", 10))
        botao_login.pack(padx=10, pady=10)

        botao_sair = tk.Button(self.janela, text="Sair", command=sair, font=("Arial", 10))
        botao_sair.pack(padx=10, pady=10)


class Cadastro:
    def __init__(self):
        self.janela = tk.Tk()
        self.tela_cadastro()

    def tela_cadastro(self):
        self.janela.geometry("890x640")
        self.janela.title("Tela de Cadastro")
        

        def criar_tabela():
            conn = sqlite3.connect('meubanco.db')
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Cadastro (
                        id INTEGER PRIMARY KEY,
                        nome TEXT NOT NULL,
                        sobrenome TEXT NOT NULL,
                        cpf INTEGER NULL, 
                        email TEXT NOT NULL,
                        telefone INTEGER NULL,
                        cep INTEGER NULL,
                        rua TEXT NULL,
                        N_ap INTEGER NULL,
                        bairro TEXT NULL,
                        numero TEXT NULL,
                        cidade TEXT NULL,
                        estado TEXT NULL,
                        senha1 TEXT NULL
                    )
                """)
                conn.commit()
                print("Criada com sucesso.")
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela: {e}")
            finally:
                conn.close()

        criar_tabela()

        def cadastrar():
            nome_valor = nome_entry.get()
            sobrenome_valor = sobrenome_entry.get()
            cpf_valor = cpf_entry.get()
            email_valor = email_entry.get()
            telefone_valor = telefone_entry.get()
            cep_valor = cep_entry.get()
            rua_valor = rua_entry.get()
            N_ap_valor = N_ap_entry.get()
            numero_valor = numero_entry.get()
            bairro_valor = bairro_entry.get()
            cidade_valor = cidade_entry.get()
            estado_valor = estado_entry.get()
            senha1_valor = senha1_entry.get()
            senha2_valor = senha2_entry.get()

            if nome_valor == "" or sobrenome_valor == "" or email_valor == "" or senha1_valor == "" or senha2_valor == "":
                print("Por favor, preencha todos os campos obrigatórios.")
                return

            if senha1_valor != senha2_valor:
                print("As senhas digitadas não correspondem.")
                return

            conn = sqlite3.connect('meubanco.db')
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    INSERT INTO Cadastro (nome, sobrenome, cpf, email, telefone, cep, rua, N_ap, numero, bairro, cidade, estado, senha1)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (nome_valor, sobrenome_valor, cpf_valor, email_valor, telefone_valor, cep_valor, rua_valor, N_ap_valor, numero_valor, bairro_valor, cidade_valor, estado_valor, senha1_valor))
                conn.commit()
                print("Dados cadastrados com sucesso.")
            except sqlite3.Error as e:
                print(f"Erro ao cadastrar dados: {e}")
            finally:
                conn.close()

            self.janela.destroy()

        def fechar():
            self.janela.destroy()
            print("Saindo...")

        def voltar():
            self.janela.destroy()
            Login().janela.mainloop()

        nome_label = tk.Label(self.janela, text="Nome:")
        nome_label.grid(row=0, column=0, pady=5, sticky="w")
        nome_entry = tk.Entry(self.janela, width=50)
        nome_entry.grid(row=0, column=1, pady=5, sticky="w")

        sobrenome_label = tk.Label(self.janela, text="Sobrenome:")
        sobrenome_label.grid(row=0, column=2, pady=5, sticky="w")
        sobrenome_entry = tk.Entry(self.janela, width=50)
        sobrenome_entry.grid(row=0, column=3, pady=5, sticky="w")

        cpf_label = tk.Label(self.janela, text="CPF:")
        cpf_label.grid(row=1, column=0, pady=5, sticky="w")
        cpf_entry = tk.Entry(self.janela, width=50)
        cpf_entry.grid(row=1, column=1, pady=5, sticky="w")

        email_label = tk.Label(self.janela, text="Email:")
        email_label.grid(row=1, column=2, pady=5, sticky="w")
        email_entry = tk.Entry(self.janela, width=50)
        email_entry.grid(row=1, column=3, pady=5, sticky="w")

        telefone_label = tk.Label(self.janela, text="Telefone:")
        telefone_label.grid(row=2, column=0, pady=5, sticky="w")
        telefone_entry = tk.Entry(self.janela, width=50)
        telefone_entry.grid(row=2, column=1, pady=5, sticky="w")

        cep_label = tk.Label(self.janela, text="CEP:")
        cep_label.grid(row=2, column=2, pady=5, sticky="w")
        cep_entry = tk.Entry(self.janela, width=50)
        cep_entry.grid(row=2, column=3, pady=5, sticky="w")

        rua_label = tk.Label(self.janela, text="Rua:")
        rua_label.grid(row=3, column=0, pady=5, sticky="w")
        rua_entry = tk.Entry(self.janela, width=50)
        rua_entry.grid(row=3, column=1, pady=5, sticky="w")

        bairro_label = tk.Label(self.janela, text="Bairro:")
        bairro_label.grid(row=3, column=2, pady=5, sticky="w")
        bairro_entry = tk.Entry(self.janela, width=50)
        bairro_entry.grid(row=3, column=3, pady=5, sticky="w")

        N_ap_label = tk.Label(self.janela, text="Ap:")
        N_ap_label.grid(row=4, column=0, pady=5, sticky="w")
        N_ap_entry = tk.Entry(self.janela, width=5)
        N_ap_entry.grid(row=4, column=1, pady=5, sticky="w")

        numero_label = tk.Label(self.janela, text="Numero:")
        numero_label.grid(row=4, column=2, pady=5, sticky="w")
        numero_entry = tk.Entry(self.janela, width=5)
        numero_entry.grid(row=4, column=3, pady=5, sticky="w")

        cidade_label = tk.Label(self.janela, text="Cidade:")
        cidade_label.grid(row=5, column=0, pady=5, sticky="w")
        cidade_entry = tk.Entry(self.janela, width=50)
        cidade_entry.grid(row=5, column=1, pady=5, sticky="w")

        estado_label = tk.Label(self.janela, text="Estado:")
        estado_label.grid(row=5, column=2, pady=5, sticky="w")
        estado_entry = tk.Entry(self.janela, width=50)
        estado_entry.grid(row=5, column=3, pady=5, sticky="w")

        senha1_label = tk.Label(self.janela, text="Cadastre sua Senha:")
        senha1_label.grid(row=6, column=0, pady=5, sticky="w")
        senha1_entry = tk.Entry(self.janela, show="*", width=50)
        senha1_entry.grid(row=6, column=1, pady=5, sticky="w")

        senha2_label = tk.Label(self.janela, text="Confirme sua Senha:")
        senha2_label.grid(row=6, column=2, pady=5, sticky="w")
        senha2_entry = tk.Entry(self.janela, show="*", width=50)
        senha2_entry.grid(row=6, column=3, pady=5, sticky="w")

        botao_cadastrar = tk.Button(self.janela, text="Cadastrar", command=cadastrar, font=("Arial", 10))
        botao_cadastrar.grid(row=7, column=1, pady=20, sticky="w")

        botao_voltar = tk.Button(self.janela, text="Voltar", command=voltar, font=("Arial", 10))
        botao_voltar.grid(row=8, column=1, pady=10, sticky="w")

        botao_sair = tk.Button(self.janela, text="Fechar", command=fechar, font=("Arial", 10))
        botao_sair.grid(row=9, column=1, pady=10, sticky="w")

if __name__ == "__main__":
    tela_login = Login()
    tela_login.janela.mainloop()
