import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox
import datetime

# Dados fictícios
usuarios = {
    "admin": "senha123",
    "caixa1": "caixa123",
    "gerente": "gerente123"
}

produtos = {
    "1001": {"nome": "Arroz 5kg", "preco_custo": 18.50, "preco_venda": 25.99, "estoque": 100, "unidade": "kg"},
    "1002": {"nome": "Feijão 1kg", "preco_custo": 7.00, "preco_venda": 9.99, "estoque": 150, "unidade": "kg"},
    "1003": {"nome": "Óleo de Soja 900ml", "preco_custo": 8.00, "preco_venda": 12.50, "estoque": 200, "unidade": "ml"},
    "1004": {"nome": "Açúcar 5kg", "preco_custo": 12.00, "preco_venda": 17.99, "estoque": 120, "unidade": "kg"},
    "1005": {"nome": "Sal 1kg", "preco_custo": 2.50, "preco_venda": 4.50, "estoque": 300, "unidade": "kg"},
    "2001": {"nome": "Leite UHT 1L", "preco_custo": 4.00, "preco_venda": 6.50, "estoque": 250, "unidade": "l"},
    "2002": {"nome": "Café Torrado 500g", "preco_custo": 9.50, "preco_venda": 14.99, "estoque": 180, "unidade": "g"},
    "2003": {"nome": "Manteiga 200g", "preco_custo": 6.00, "preco_venda": 8.90, "estoque": 100, "unidade": "g"},
    "3001": {"nome": "Detergente Líquido 500ml", "preco_custo": 2.00, "preco_venda": 3.75, "estoque": 400, "unidade": "ml"},
    "3002": {"nome": "Papel Higiênico (4 rolos)", "preco_custo": 5.50, "preco_venda": 8.75, "estoque": 350, "unidade": "rolos"}
}

historico_vendas = []

class MinimercadoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Minimercado")
        self.root.geometry("750x650")
        self.usuario_logado = None
        self.carrinho = []
        self.total_venda = 0.0
        self.criar_tela_login()
   
    def criar_tela_login(self):
        self.limpar_janela()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Login", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(frame, text="Usuário").pack()
        self.entry_usuario = tk.Entry(frame)
        self.entry_usuario.pack()

        tk.Label(frame, text="Senha").pack()
        self.entry_senha = tk.Entry(frame, show="*")
        self.entry_senha.pack()

        tk.Button(frame, text="Entrar", command=self.verificar_login).pack(pady=10)
        tk.Button(frame, text="Sair", command=self.fechar_tela_login).pack()
        #pady=10) 

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if usuario in usuarios and usuarios[usuario] == senha:
            self.usuario_logado = usuario
            self.menu_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def fechar_tela_login(self):
        self.root.destroy() 


    def menu_principal(self):
        self.limpar_janela()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Menu Principal", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(frame, text=f"Bem-vindo(a), {self.usuario_logado}").pack(pady=5)

        botoes = [
            ("Ponto de Venda", self.ponto_de_venda),
            ("Cadastrar Produto", self.cadastrar_produto),
            ("Controle de Estoque", self.controle_estoque),
            ("Cadastrar Usuário", self.cadastrar_usuario),
            ("Histórico de Vendas", self.historico),
            ("Sair", self.criar_tela_login)
        ]

        for texto, comando in botoes:
            tk.Button(frame, text=texto, width=30, command=comando).pack(pady=5)

    def limpar_janela(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def cadastrar_usuario(self):
        if self.usuario_logado != "admin":
            messagebox.showerror("Erro", "Apenas o administrador pode cadastrar usuários.")
            return
        self.limpar_janela()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Cadastrar Novo Usuário", font=("Helvetica", 14, "bold")).pack(pady=10)

        tk.Label(frame, text="Usuário:").pack()
        entry_user = tk.Entry(frame)
        entry_user.pack()

        tk.Label(frame, text="Senha:").pack()
        entry_pass = tk.Entry(frame)
        entry_pass.pack()

        def salvar_usuario():
            u = entry_user.get()
            s = entry_pass.get()
            if u in usuarios:
                messagebox.showerror("Erro", "Usuário já existe.")
            else:
                usuarios[u] = s
                messagebox.showinfo("Sucesso", "Usuário cadastrado.")
                self.menu_principal()

        tk.Button(frame, text="Salvar", command=salvar_usuario).pack(pady=10)
        tk.Button(frame, text="Voltar", command=self.menu_principal).pack()

    def cadastrar_produto(self):
        if self.usuario_logado not in ["admin", "gerente"]:
            messagebox.showerror("Erro", "Acesso negado.")
            return
        self.limpar_janela()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Cadastro de Produto", font=("Helvetica", 14, "bold")).pack(pady=10)

        campos = {}
        labels = ["Código", "Nome", "Preço Custo", "Preço Venda", "Estoque"]
        for label in labels:
            tk.Label(frame, text=label).pack()
            campo = tk.Entry(frame)
            campo.pack()
            campos[label.lower().replace(" ", "_")] = campo

        tk.Label(frame, text="Unidade").pack()
        unidade = Combobox(frame, values=["kg", "g", "ml", "l", "un", "rolos"])
        unidade.pack()

        def salvar():
            try:
                codigo = campos["código"].get()
                nome = campos["nome"].get()
                preco_custo = float(campos["preço_custo"].get())
                preco_venda = float(campos["preço_venda"].get())
                estoque = int(campos["estoque"].get())
                uni = unidade.get()
                if codigo in produtos:
                    messagebox.showerror("Erro", "Produto já cadastrado.")
                    return
                produtos[codigo] = {
                    "nome": nome,
                    "preco_custo": preco_custo,
                    "preco_venda": preco_venda,
                    "estoque": estoque,
                    "unidade": uni
                }
                messagebox.showinfo("Sucesso", "Produto cadastrado.")
                self.menu_principal()
            except Exception as e:
                messagebox.showerror("Erro", f"Dados inválidos: {e}")

        tk.Button(frame, text="Salvar Produto", command=salvar).pack(pady=10)
        tk.Button(frame, text="Voltar", command=self.menu_principal).pack()

    def controle_estoque(self):
        if self.usuario_logado not in ["admin", "gerente"]:
            messagebox.showerror("Erro", "Acesso negado.")
            return
        self.limpar_janela()
        tk.Label(self.root, text="Controle de Estoque", font=("Helvetica", 14, "bold")).pack(pady=10)
        tree = ttk.Treeview(self.root, columns=("codigo", "nome", "custo", "venda", "estoque", "unidade"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center")
        for cod, p in produtos.items():
            tree.insert("", tk.END, values=(cod, p["nome"], p["preco_custo"], p["preco_venda"], p["estoque"], p["unidade"]))
        tree.pack(expand=True, fill="both")
        tk.Button(self.root, text="Voltar", command=self.menu_principal).pack(pady=10)

    def ponto_de_venda(self):
        self.limpar_janela()
        self.carrinho = []
        self.total_venda = 0.0

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Ponto de Venda", font=("Helvetica", 14, "bold")).pack(pady=5)

        tk.Label(frame, text="Código do Produto:").pack()
        self.entry_codigo = tk.Entry(frame)
        self.entry_codigo.pack()

        tk.Label(frame, text="Quantidade:").pack()
        self.entry_qtd = tk.Entry(frame)
        self.entry_qtd.pack()

        tk.Button(frame, text="Adicionar ao Carrinho", command=self.adicionar_ao_carrinho).pack(pady=5)

        self.label_total = tk.Label(frame, text="Total: R$ 0.00", font=("Helvetica", 12, "bold"))
        self.label_total.pack(pady=5)

        self.tree_carrinho = ttk.Treeview(self.root, columns=("codigo", "nome", "qtd", "total"), show="headings")
        for col in self.tree_carrinho["columns"]:
            self.tree_carrinho.heading(col, text=col.capitalize())
            self.tree_carrinho.column(col, anchor="center")
        self.tree_carrinho.pack(expand=True, fill="both")

        tk.Button(self.root, text="Finalizar Compra", command=self.finalizar_compra).pack(pady=10)
        tk.Button(self.root, text="Voltar ao Menu", command=self.menu_principal).pack(pady=5)

    def adicionar_ao_carrinho(self):
        codigo = self.entry_codigo.get()
        if codigo not in produtos:
            messagebox.showerror("Erro", "Código inválido.")
            return
        try:
            qtd = int(self.entry_qtd.get())
            if qtd <= 0:
                messagebox.showerror("Erro", "Quantidade inválida.")
                return
            if qtd > produtos[codigo]["estoque"]:
                messagebox.showerror("Erro", "Estoque insuficiente.")
                return
            produtos[codigo]["estoque"] -= qtd
            total_item = produtos[codigo]["preco_venda"] * qtd
            self.total_venda += total_item
            self.carrinho.append({"codigo": codigo, "quantidade": qtd})
            self.tree_carrinho.insert("", tk.END, values=(codigo, produtos[codigo]["nome"], qtd, f"R$ {total_item:.2f}"))
            self.label_total.config(text=f"Total: R$ {self.total_venda:.2f}")
            self.entry_codigo.delete(0, tk.END)
            self.entry_qtd.delete(0, tk.END)
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")

    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showerror("Erro", "Carrinho vazio.")
            return

        pagamento_window = tk.Toplevel(self.root)
        pagamento_window.title("Finalizar Pagamento")
        pagamento_window.geometry("400x400")

        tk.Label(pagamento_window, text=f"Total da Compra: R$ {self.total_venda:.2f}", font=("Helvetica", 14, "bold")).pack(pady=10)

        tk.Label(pagamento_window, text="Forma de Pagamento:").pack()
        formas = ["À Vista", "Cartão de Débito", "Cartão de Crédito", "PIX"]
        forma_pagamento = Combobox(pagamento_window, values=formas)
        forma_pagamento.pack()

        entry_valor_pago = tk.Entry(pagamento_window)
        parcelas_combo = Combobox(pagamento_window)

        def atualizar_pagamento(event=None):
            if forma_pagamento.get() == "À Vista":
                tk.Label(pagamento_window, text="Valor Pago (Cliente):").pack()
                entry_valor_pago.pack()
            elif forma_pagamento.get() == "Cartão de Crédito" and self.total_venda >= 150:
                tk.Label(pagamento_window, text="Parcelar em:").pack()
                parcelas_combo['values'] = ["1x", "2x", "3x"]
                parcelas_combo.pack()

        forma_pagamento.bind("<<ComboboxSelected>>", atualizar_pagamento)

        def confirmar_pagamento():
            forma = forma_pagamento.get()
            if forma == "":
                messagebox.showerror("Erro", "Selecione uma forma de pagamento.")
                return

            if forma == "À Vista":
                try:
                    valor_pago = float(entry_valor_pago.get())
                    if valor_pago < self.total_venda:
                        messagebox.showerror("Erro", "Valor insuficiente.")
                        return
                    troco = valor_pago - self.total_venda
                    messagebox.showinfo("Troco", f"Troco: R$ {troco:.2f}")
                except:
                    messagebox.showerror("Erro", "Valor pago inválido.")
                    return

            if forma == "Cartão de Crédito" and self.total_venda >= 150:
                parcelas = parcelas_combo.get()
                if parcelas == "":
                    parcelas = "1x"
                qtd_parcelas = int(parcelas[0])
                valor_parcela = self.total_venda / qtd_parcelas
                messagebox.showinfo("Parcelamento", f"Pagamento em {qtd_parcelas}x de R$ {valor_parcela:.2f} no Cartão.")

            historico_vendas.append({
                "data": datetime.datetime.now(),
                "itens": self.carrinho.copy(),
                "total": self.total_venda,
                "forma_pagamento": forma
            })

            pagamento_window.destroy()
            self.menu_principal()

        tk.Button(pagamento_window, text="Confirmar Pagamento", command=confirmar_pagamento).pack(pady=20)

    def historico(self):
        if self.usuario_logado not in ["admin", "gerente"]:
            messagebox.showerror("Erro", "Acesso negado.")
            return
        self.limpar_janela()
        tk.Label(self.root, text="Histórico de Vendas", font=("Helvetica", 14, "bold")).pack()
        for venda in historico_vendas:
            data = venda["data"].strftime("%d/%m/%Y %H:%M")
            itens = ", ".join([f"{produtos[i['codigo']]['nome']}({i['quantidade']})" for i in venda["itens"]])
            info = f"{data} | {itens} | Total: R$ {venda['total']:.2f} | {venda['forma_pagamento']}"
            tk.Label(self.root, text=info, anchor="w", justify="left").pack()

        tk.Button(self.root, text="Voltar", command=self.menu_principal).pack(pady=10)

def main():
    root = tk.Tk()
    app = MinimercadoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
