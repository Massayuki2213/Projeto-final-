import tkinter as tk
from tkinter import messagebox, Listbox
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

        tk.Label(frame_search, text="Buscar (ID ou Nome):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search = tk.Entry(frame_search)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)
        self.entry_search.bind('<KeyRelease>', self.update_suggestions)

        btn_search = tk.Button(frame_search, text="Buscar Contato", command=self.search_contact)
        btn_search.grid(row=1, columnspan=2, pady=10)

        self.listbox_suggestions = Listbox(frame_search)
        self.listbox_suggestions.grid(row=2, columnspan=2, padx=5, pady=5)
        self.listbox_suggestions.bind('<<ListboxSelect>>', self.fill_search_entry)

        # Frame para remover contato
        frame_remove = tk.Frame(self.root)
        frame_remove.pack(pady=10)

        tk.Label(frame_remove, text="Remover (ID ou Nome):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_remove = tk.Entry(frame_remove)
        self.entry_remove.grid(row=0, column=1, padx=5, pady=5)

        btn_remove = tk.Button(frame_remove, text="Remover Contato", command=self.remove_contact)
        btn_remove.grid(row=1, columnspan=2, pady=10)

        # Frame para listar todos os contatos
        frame_list = tk.Frame(self.root)
        frame_list.pack(pady=10)

        btn_list = tk.Button(frame_list, text="Listar Todos os Contatos", command=self.list_contacts)
        btn_list.grid(row=0, columnspan=2, pady=10)

        self.text_contacts = tk.Text(frame_list, width=50, height=10)
        self.text_contacts.grid(row=1, columnspan=2, pady=5)

    def add_contact(self):
        name = self.entry_name.get()
        number = self.entry_number.get()
        if name and number:
            try:
                self.db.insert(name, number)
                messagebox.showinfo("Sucesso", f"Contato {name} adicionado com sucesso!")
                self.entry_name.delete(0, tk.END)
                self.entry_number.delete(0, tk.END)
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Por favor, insira o nome e o número.")

    def search_contact(self):
        search_term = self.entry_search.get().strip()
        if search_term:
            try:
                contact_id = int(search_term)
                contact = self.db.search_by_id(contact_id)
                
                if contact:
                    messagebox.showinfo("Resultado da Busca", f"ID: {contact['id']}, Nome: {contact['name']}, Telefone: {contact['number']}")
                else:
                    messagebox.showinfo("Resultado da Busca", f"Contato com ID {contact_id} não encontrado.")
            except ValueError:
                results = self.db.search_by_name(search_term)
                if results:
                    self.text_contacts.delete(1.0, tk.END)
                    for contact in results:
                        self.text_contacts.insert(tk.END, f"ID: {contact['id']}, Nome: {contact['name']}, Telefone: {contact['number']}\n")
                else:
                    messagebox.showinfo("Resultado da Busca", f"Contato {search_term} não encontrado.")
        else:
            messagebox.showerror("Erro", "Por favor, insira o ID ou o nome para buscar.")
        if not results:
            self.listbox_suggestions.delete(0, tk.END) 

    def update_suggestions(self, event):
        prefix = self.entry_search.get().strip()
        suggestions = self.db.search_suggestions(prefix)
        self.listbox_suggestions.delete(0, tk.END)
        for contact in suggestions:
                        self.listbox_suggestions.insert(tk.END, f"{contact['name']} (ID: {contact['id']})")

    def fill_search_entry(self, event):
        selected = self.listbox_suggestions.curselection()
        if selected:
            name_with_id = self.listbox_suggestions.get(selected[0])
            name = name_with_id.split(' (ID:')[0]
            self.entry_search.delete(0, tk.END)
            self.entry_search.insert(0, name)
            self.listbox_suggestions.delete(0, tk.END)

    def remove_contact(self):
        search_term = self.entry_remove.get().strip()
        if search_term:
            try:    
                contact_id = int(search_term)
                self.db.delete_by_id(contact_id)
                messagebox.showinfo("Sucesso", f"Contato com ID {contact_id} removido com sucesso!")
            except ValueError:
                self.db.delete_by_name(search_term)
                messagebox.showinfo("Sucesso", f"Contato {search_term} removido com sucesso!")
            self.entry_remove.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Por favor, insira o ID ou o nome para remover.")

    def list_contacts(self):
        contacts = self.db.list_contacts()
        self.text_contacts.delete(1.0, tk.END)
        if contacts:
            for contact in contacts:
                # Verifica se o contato tem o campo 'id'
                contact_id = contact.get('id', 'N/A')
                self.text_contacts.insert(tk.END, f"ID: {contact_id}, Nome: {contact['name']}, Telefone: {contact['number']}\n")
        else:
            self.text_contacts.insert(tk.END, "Nenhum contato encontrado.\n")

def main():
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

