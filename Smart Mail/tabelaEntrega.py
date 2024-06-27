import tkinter as tk
from tkinter import ttk
import sqlite3

class TabelaEntrega:
    def __init__(self):
        self.janela = tk.Tk()
        self.criar_tabela_entregas() 
        self.tela_cadastro()

    def tela_cadastro(self):
        self.janela.geometry("800x600")
        self.janela.title("Tabela de Entrega")

        
        self.tree = ttk.Treeview(self.janela, columns=("ID", "Morador", "Data Entrega", "Data Retirada", "Tamanho Armário", "Status", "Armário"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Morador", text="Morador")
        self.tree.heading("Data Entrega", text="Data Entrega")
        self.tree.heading("Data Retirada", text="Data Retirada")
        self.tree.heading("Tamanho Armário", text="Tamanho Armário")
        self.tree.heading("Status", text="Status")  
        self.tree.heading("Armário", text="Armário")
        self.tree.pack(expand=True, fill='both')


    def criar_tabela_entregas(self):
        conn = sqlite3.connect('meubanco.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Tabela_de_Entregas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    morador_id INTEGER NULL,
                    data_entrega DATETIME NULL,
                    data_retirada DATETIME NULL,
                    codigo_gerado TEXT NULL,
                    status TEXT NULL,
                    armario_id INTEGER NULL,
                    FOREIGN KEY (morador_id) REFERENCES Cadastro(id),
                    FOREIGN KEY (armario_id) REFERENCES Armario(id)
                )
            """)
            conn.commit()
            print("Tabela de entregas criada com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela de entregas: {e}")
        finally:
            conn.close()

    def buscar_entregas(self):
        conn = sqlite3.connect('meubanco.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT e.id, m.nome, e.data_entrega, e.data_retirada, a.descricao, e.status, a.status
                FROM Tabela_de_Entregas e
                JOIN Cadastro m ON e.morador_id = m.id
                LEFT JOIN Armario a ON e.armario_id = a.id
            """)
            entregas = cursor.fetchall()
            return entregas
        except sqlite3.Error as e:
            print(f"Erro ao buscar entregas: {e}")
            return []
        finally:
            conn.close()

    def atualizar_lista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
      
        entregas = self.buscar_entregas()
        if entregas:
            for entrega in entregas:
                self.tree.insert("", tk.END, values=entrega)
        else:
            self.tree.insert("", tk.END, values=("Nenhuma entrega encontrada",))

if __name__ == "__main__":
    app = TabelaEntrega()
    app.janela.mainloop()


 
    

