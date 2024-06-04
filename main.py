# main.py

import tkinter as tk
from tkinter import messagebox
from mongo_db import MongoDB

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Telefônica")

        self.db = MongoDB()

        self.create_widgets()

    def create_widgets(self):
        # Frame para adicionar contato
        frame_add = tk.Frame(self.root)
        frame_add.pack(pady=10)

        tk.Label(frame_add, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(frame_add)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_add, text="Número:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_number = tk.Entry(frame_add)
        self.entry_number.grid(row=1, column=1, padx=5, pady=5)

        btn_add = tk.Button(frame_add, text="Adicionar Contato", command=self.add_contact)
        btn_add.grid(row=2, columnspan=2, pady=10)

        # Frame para buscar contato
        frame_search = tk.Frame(self.root)
        frame_search.pack(pady=10)

        tk.Label(frame_search, text="Buscar Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search = tk.Entry(frame_search)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)

        btn_search = tk.Button(frame_search, text="Buscar Contato", command=self.search_contact)
        btn_search.grid(row=1, columnspan=2, pady=10)

        # Frame para remover contato
        frame_remove = tk.Frame(self.root)
        frame_remove.pack(pady=10)

        tk.Label(frame_remove, text="Remover Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_remove = tk.Entry(frame_remove)
        self.entry_remove.grid(row=0, column=1, padx=5, pady=5)

        btn_remove = tk.Button(frame_remove, text="Remover Contato", command=self.remove_contact)
        btn_remove.grid(row=1, columnspan=2, pady=10)

        # Frame para listar todos os contatos
        frame_list = tk.Frame(self.root)
        frame_list.pack(pady=10)

        btn_list = tk.Button(frame_list, text="Listar Todos os Contatos", command=self.list_contacts)
        btn_list.grid(row=0, columnspan=2, pady=10)

        self.text_contacts = tk.Text(frame_list, width=40, height=10)
        self.text_contacts.grid(row=1, columnspan=2, pady=5)

    def add_contact(self):
        name = self.entry_name.get()
        number = self.entry_number.get()
        if name and number:
            self.db.insert(name, number)
            messagebox.showinfo("Sucesso", f"Contato {name} adicionado com sucesso!")
            self.entry_name.delete(0, tk.END)
            self.entry_number.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Por favor, insira o nome e o número.")

    def search_contact(self):
        name = self.entry_search.get()
        if name:
            result = self.db.search(name)
            if result:
                messagebox.showinfo("Resultado da Busca", f"Número de telefone de {name}: {result}")
            else:
                messagebox.showinfo("Resultado da Busca", f"Contato {name} não encontrado.")
            self.entry_search.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Por favor, insira o nome para buscar.")

    def remove_contact(self):
        name = self.entry_remove.get()
        if name:
            self.db.delete(name)
            messagebox.showinfo("Sucesso", f"Contato {name} removido com sucesso!")
            self.entry_remove.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Por favor, insira o nome para remover.")

    def list_contacts(self):
        contacts = self.db.list_contacts()
        self.text_contacts.delete(1.0, tk.END)
        if contacts:
            for key, value in contacts:
                self.text_contacts.insert(tk.END, f"Nome: {key}, Telefone: {value}\n")
        else:
            self.text_contacts.insert(tk.END, "Nenhum contato encontrado.\n")

def main():
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
