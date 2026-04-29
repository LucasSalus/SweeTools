import customtkinter as ctk
import qrcode
import os
from tkinter import messagebox


class JanelaQRCode(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Ferramenta QR Code")
        self.geometry("450x450")
        
        self.attributes("-topmost", True)
        self.grab_set()

        self.label_titulo = ctk.CTkLabel(self, text="Gerador de QR Code", font=("Roboto", 20, "bold"))
        self.label_titulo.pack(pady=20)

        self.entry_url = ctk.CTkEntry(self, placeholder_text="Cole o link (URL) aqui...", width=350, height=35)
        self.entry_url.pack(pady=10)

        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome do arquivo (sem extensão)", width=350, height=35)
        self.entry_nome.pack(pady=10)

        self.lbl_info_pasta = ctk.CTkLabel(self, text="", font=("Roboto", 10), text_color="gray")
        self.lbl_info_pasta.pack(pady=5)
        self.atualizar_label_pasta()

        self.btn_alterar_dest = ctk.CTkButton(
            self, text="Alterar Pasta", width=120, height=25, 
            fg_color="#3d3d3d", command=self.trocar_pasta_janela
        )
        self.btn_alterar_dest.pack(pady=5)
        
        self.btn_gerar = ctk.CTkButton(
            self, 
            text="GERAR E SALVAR", 
            width=200, 
            height=50,
            font=("Roboto", 14, "bold"),
            command=self.acao_gerar
        )
        self.btn_gerar.pack(pady=30)

    def atualizar_label_pasta(self):
        m = ferramentas.obter_memorias()
        pasta = m.get("destino_qr") or "Pasta não definida no menu principal"
        self.lbl_info_pasta.configure(text=f"Destino atual: {pasta}")

    def trocar_pasta_janela(self):
        if ferramentas.escolher_nova_pasta("destino_qr"):
            self.atualizar_label_pasta()

    def acao_gerar(self):
        url = self.entry_url.get()
        nome = self.entry_nome.get()

        pasta_destino = ferramentas.obter_memorias().get("destino_qr")
        
        
        if not pasta_destino or pasta_destino == "Não definido":
            messagebox.showwarning("Atenção", "Selecione a pasta de destino no menu principal primeiro.")
            return

        if not url or not nome:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        if ferramentas.processar_qr(url, nome, pasta_destino):
            self.destroy()
