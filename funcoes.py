import customtkinter as ctk
import qrcode
import os
from tkinter import messagebox

# Caminho de destino fixo conforme seu ambiente
DIRETORIO_DESTINO = r'C:\Users\Sistema-C3\OneDrive\Área de Trabalho\Área de Trabalho\chatbot\QR'

class JanelaQRCode(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Ferramenta QR Code")
        self.geometry("450x450")
        
        # Garante que a janela abra na frente
        self.attributes("-topmost", True)
        self.grab_set() # Foca a interação apenas nesta janela

        self.label_titulo = ctk.CTkLabel(self, text="Gerador de QR Code", font=("Roboto", 20, "bold"))
        self.label_titulo.pack(pady=20)

        self.entry_url = ctk.CTkEntry(self, placeholder_text="Cole o link (URL) aqui...", width=350, height=35)
        self.entry_url.pack(pady=10)

        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome do arquivo (sem extensão)", width=350, height=35)
        self.entry_nome.pack(pady=10)

        self.btn_gerar = ctk.CTkButton(
            self, 
            text="GERAR E SALVAR", 
            width=200, 
            height=50,
            font=("Roboto", 14, "bold"),
            command=self.acao_gerar
        )
        self.btn_gerar.pack(pady=30)

    def acao_gerar(self):
        url = self.entry_url.get()
        nome = self.entry_nome.get()
        
        if not url or not nome:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        try:
            os.makedirs(DIRETORIO_DESTINO, exist_ok=True)
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            caminho_completo = os.path.join(DIRETORIO_DESTINO, f"{nome}.png")
            
            img.save(caminho_completo)
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{caminho_completo}")
            self.destroy() # Fecha a janelinha após o sucesso
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")