import datetime
import tkinter as tk
import sqlite3
from tkinter import messagebox
from datetime import datetime
import time
import secrets

class Telinha:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.geometry("460x540")
        self.janela.title("Telinha")
        self.tela_inicial()
        self.janela.mainloop()

    def tela_inicial(self):
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)

        botao_retirar = tk.Button(frame_botoes, text="Retirar", width=10, height=2, command=self.abrir_tela_retirar)
        botao_retirar.grid(row=0, column=0, padx=5)

        botao_entregar = tk.Button(frame_botoes, text="Entregar", width=10, height=2, command=self.abrir_tela_login_entregar)
        botao_entregar.grid(row=0, column=1, padx=5)

    def abrir_tela_login_entregar(self):
        self.janela.withdraw()
        self.tela_login = tk.Toplevel(self.janela)
        self.tela_login.geometry("360x150")
        self.tela_login.title("Tela de Login")
        self.tela_login.protocol("WM_DELETE_WINDOW", self.voltar_para_tela_inicial)

        self.tela_entregar(self.tela_login)

    def tela_entregar(self, tela):
        entregador = tk.Frame(tela)
        entregador.pack(pady=10)

        userEntregador_label = tk.Label(entregador, text="Digite sua Senha:")
        userEntregador_label.grid(row=0, column=0, pady=5, sticky="w")
        self.userEntregador_entry = tk.Entry(entregador, width=25, show="*")
        self.userEntregador_entry.grid(row=0, column=1, pady=5, sticky="w")

        def verificar_senha_entregador():
            senha = self.userEntregador_entry.get()
            conn = sqlite3.connect('meubanco.db')
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM Cadastro_Entregador WHERE senha1 = ?", (senha,))
                entregador = cursor.fetchone()
                if entregador:
                    self.selecionar_armario()
                else:
                    messagebox.showerror("Erro", "Senha incorreta.")
            except sqlite3.Error as e:
                print(f"Erro ao verificar senha do entregador: {e}")
            finally:
                conn.close()

        botao_entregar = tk.Button(entregador, text="Entrar", width=10, height=2, command=verificar_senha_entregador)
        botao_entregar.grid(row=0, column=2, padx=5)

    def selecionar_armario(self):
        self.tela_login.destroy()
        self.tela_armario = tk.Toplevel(self.janela)
        self.tela_armario.geometry("600x400")
        self.tela_armario.title("Selecionar Armário")
        self.tela_armario.protocol("WM_DELETE_WINDOW", self.voltar_para_tela_inicial)

        dados_morador = tk.Frame(self.tela_armario)
        dados_morador.pack(pady=10)

        self.armario_selecionado = tk.StringVar(value="Nenhum")

        armario_p = tk.Radiobutton(dados_morador, text="PEQUENO", variable=self.armario_selecionado, value="Pequeno")
        armario_p.grid(row=0, column=1, padx=5)

        armario_m = tk.Radiobutton(dados_morador, text="MÉDIO", variable=self.armario_selecionado, value="Médio")
        armario_m.grid(row=0, column=2, padx=5)

        selecione = tk.Button(dados_morador, text="Confirmar", width=15, height=2, command=self.confirmar_armario)
        selecione.grid(row=2, column=2, padx=5)

    def confirmar_armario(self):
        tamanho_selecionado = self.armario_selecionado.get()
        descricao_codigo = None

        if tamanho_selecionado == "Pequeno":
            descricao_codigo = "1"
        elif tamanho_selecionado == "Médio":
            descricao_codigo = "2"

        if descricao_codigo:
            conn = sqlite3.connect('meubanco.db')
            cursor = conn.cursor()

            try:
                
                cursor.execute("""
                    SELECT 1, 2 FROM Tabela_de_Entregas 
                    WHERE armario_id = ? AND status = 'A retirar'
                """, (descricao_codigo,))
                armario_ocupado = cursor.fetchone()

                if armario_ocupado:
                    # mensagem q fala se o armario ta ocupado
                    print(f"O armário {descricao_codigo} já está sendo usado.")
                    
                    return

                
                cursor.execute("SELECT descricao FROM Armario WHERE descricao = ?", (descricao_codigo, ))
                resultado = cursor.fetchone()

                if resultado:
                    armario_descricao = resultado[0]
                    self.abrir_tela_busca_morador(armario_descricao, descricao_codigo)
                else:
                    messagebox.showerror("Erro", "Armário não encontrado.")
            except sqlite3.Error as e:
                print(f"Erro ao buscar armário: {e}")
                messagebox.showerror("Erro", f"Erro ao buscar armário: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Erro", "Tamanho inválido.")



    def abrir_tela_busca_morador(self, armario_descricao, descricao_codigo):
        self.tela_armario.destroy()
        self.tela_busca_morador = tk.Toplevel(self.janela)
        self.tela_busca_morador.geometry("530x150")
        self.tela_busca_morador.title("Buscar Morador")
        self.tela_busca_morador.protocol("WM_DELETE_WINDOW", self.voltar_para_tela_inicial)

        busca_morador = tk.Frame(self.tela_busca_morador)
        busca_morador.pack(pady=10)

        tk.Label(busca_morador, text="Buscar Morador: ").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.criterio_entry = tk.Entry(busca_morador, width=40)
        self.criterio_entry.grid(row=0, column=1, padx=5, pady=5)

        botao_buscar = tk.Button(busca_morador, text="Buscar", command=lambda: self.buscar_morador_por_criterio(armario_descricao, descricao_codigo))
        botao_buscar.grid(row=0, column=2, padx=5, pady=5)

    def buscar_morador_por_criterio(self, armario_descricao, descricao_codigo):
        criterio = self.criterio_entry.get()

        conn = sqlite3.connect('meubanco.db')
        cursor = conn.cursor()
        try:
            query = """
                SELECT  nome, sobrenome, N_ap, telefone 
                FROM Cadastro 
                WHERE nome = ? OR sobrenome = ? OR telefone = ? OR N_ap = ?
            """

            cursor.execute(query, (criterio, criterio, criterio, criterio))
            moradores_encontrados = cursor.fetchall()

            if not moradores_encontrados:
                print(f"Nenhum morador encontrado '{criterio}'.")
            else:
                for morador in moradores_encontrados:
                    print("Nome:", morador[0])
                    print("Sobrenome:", morador[1])
                    print("Nº Apartamento:", morador[2])
                    print("Telefone:", morador[3])


                codigo_entrega = self.finalizar_processo(armario_descricao)

                self.inserir_entrega(morador, descricao_codigo, codigo_entrega)
                self.abrir_janela_finalizado(armario_descricao)

        except sqlite3.Error as e:
            print(f"Erro ao buscar morador: {e}")
        finally:
            conn.close()

    def abrir_janela_finalizado(self, armario_descricao):
        print(f"Armário a ser aberto: {armario_descricao}")

        
        self.tela_busca_morador.destroy()
        self.tela_finalizado = tk.Toplevel(self.janela)
        self.tela_finalizado.geometry("600x400")
        self.tela_finalizado.title("Finalizado")
        self.tela_finalizado.protocol("WM_DELETE_WINDOW", self.voltar_para_tela_inicial)

        finalizado_entrega = tk.Frame(self.tela_finalizado)
        finalizado_entrega.pack(pady=10)

        texto_finalizado = tk.Label(finalizado_entrega,)
        texto_finalizado.grid(row=0, column=0, pady=5)

        finalize = tk.Button(finalizado_entrega, text="Finalizado", command=self.voltar_para_tela_inicial)
        finalize.grid(row=1, column=0, pady=10)

    def finalizar_processo(self, armario_descricao):
        self.abrir_janela_finalizado(armario_descricao)



        #codigo aleatorio

        codigo_entrega = secrets.choice(range(10000, 100000))
        print(f"Código de Entrega Gerado: {codigo_entrega}")

        return codigo_entrega

    def inserir_entrega(self, morador, descricao_codigo, codigo_entrega):
        conn = None
        cursor = None

        for attempt in range(5):
            try:
                conn = sqlite3.connect('meubanco.db')
                cursor = conn.cursor()



               
                data_DAentrega = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    INSERT INTO Tabela_de_Entregas (morador_id, data_entrega, codigo_gerado, status, armario_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (morador[0], data_DAentrega, codigo_entrega, 'A retirar', descricao_codigo))
                conn.commit()
                print(f"Entrega para {morador[0]} {morador[1]} no armário {descricao_codigo}.")
                break
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    print(" tentando novamente ")
                    time.sleep(1)
                else:
                    print(f"Erro ao inserir entrega: {e}")
                    break
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        else:
            print("Não foi possível acessar o banco de dados")


    def voltar_para_tela_inicial(self):
        if hasattr(self, 'tela_finalizado') and self.tela_finalizado.winfo_exists():
            self.tela_finalizado.destroy()
        self.janela.deiconify()

    def abrir_tela_retirar(self):
        self.janela.withdraw()
        self.tela_retirar = tk.Toplevel(self.janela)
        self.tela_retirar.geometry("560x350")
        self.tela_retirar.title("Tela Retirar Encomenda")
        self.tela_retirar.protocol("WM_DELETE_WINDOW", self.voltar_para_tela_inicial)

        morador_retira = tk.Frame(self.tela_retirar)
        morador_retira.pack(pady=10)

        usermorador_retira_label = tk.Label(morador_retira, text="Digite seu codigo:")
        usermorador_retira_label.grid(row=0, column=0, pady=5, sticky="w")
        self.usermorador_retira_entry = tk.Entry(morador_retira, width=25, show="*")
        self.usermorador_retira_entry.grid(row=0, column=1, pady=5, sticky="w")

        botao_confirmar = tk.Button(morador_retira, text="Confirmar", command=self.verificar_codigo)
        botao_confirmar.grid(row=1, column=3, pady=5)

  

    def verificar_codigo(self):
        codigo_digitado = self.usermorador_retira_entry.get()
        
        conn = sqlite3.connect('meubanco.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT codigo_gerado FROM Tabela_de_Entregas WHERE codigo_gerado = ?", (codigo_digitado,))
            resultado = cursor.fetchone()
            if resultado:
                cursor.execute("SELECT morador_id, armario_id FROM Tabela_de_Entregas WHERE codigo_gerado = ?", (codigo_digitado,))
                entrega = cursor.fetchone()
                if entrega:
                    morador_id, armario_id = entrega
                    print(f"Código {codigo_digitado} encontrado no armário {armario_id}")
                    
                    self.abrir_tela_retirado(armario_id, codigo_digitado)  
                else:
                    messagebox.showerror("Erro", "Dados não encontrados.")
            else:
                messagebox.showerror("Erro", "Código incorreto.")
                    
        except sqlite3.Error as e:
            print(f"Erro ao verificar código: {e}")
        finally:
            conn.close()

    def abrir_tela_retirado(self, armario_id, codigo_entrega):
        self.atualizar_entrega(codigo_entrega)
        self.tela_retirar.destroy()
        self.tela_retirado = tk.Toplevel(self.janela)
        self.tela_retirado.geometry("560x350")
        self.tela_retirado.title("Tela Retirado Encomenda")
        self.tela_retirado.protocol("WM_DELETE_WINDOW", self.voltar_para_tela_inicial)

        encomenda_entregue = tk.Frame(self.tela_retirado)
        encomenda_entregue.pack(pady=10)

        texto = tk.Label(self.tela_retirado, text=f"Retira sua encomenda no armário {armario_id}", width=40)
        texto.pack(padx=10, pady=10)

        botao_abrir = tk.Button(encomenda_entregue, text="Abrir", command=self.tela_inicial_recomeçar)
        botao_abrir.grid(row=5, column=6, pady=5)


    def atualizar_entrega(self, codigo_entrega):
        conn = sqlite3.connect('meubanco.db')
        cursor = conn.cursor()
        try:
            
            data_saida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("UPDATE Tabela_de_Entregas SET data_retirada = ?, status = ? WHERE codigo_gerado = ?", (data_saida, "entregue", codigo_entrega))
            conn.commit()
            print(f"Entrega com código {codigo_entrega} atualizada com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao atualizar entrega: {e}")
        finally:
            conn.close()



    def tela_inicial_recomeçar(self):
        if hasattr(self, 'tela_retirado') and self.tela_retirado.winfo_exists():
            self.tela_retirado.destroy()
        self.janela.deiconify()







if __name__ == "__main__":
    app = Telinha()
