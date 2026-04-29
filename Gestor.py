import customtkinter as ctk
import ferramentas
import os, sys
from PIL import Image

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, os.path.basename(relative_path))

class SweeToolsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SweeTools - Central de Ferramentas")
        self.geometry("550x700")
        ctk.set_appearance_mode("system")
        
        try:
            self.iconbitmap(resource_path("ferramentas.ico"))
        except Exception as e:
            print(f"Não foi possível carregar ferramentas.ico: {e}")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both")

        self.frame_menu = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_qr = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_csv = ctk.CTkFrame(self.container, fg_color="transparent")

        self.setup_menu()
        self.setup_qr_screen()
        self.setup_csv_screen()
        self.mostrar_tela(self.frame_menu)

    def mostrar_tela(self, frame):
        for f in [self.frame_menu, self.frame_qr, self.frame_csv]:
            f.pack_forget()
        frame.pack(expand=True, fill="both")
        self.atualizar_labels_destino()

    def atualizar_labels_destino(self):
        m = ferramentas.obter_memorias()
        self.lbl_dest_qr.configure(text=f"Destino atual: {m.get('destino_qr') or 'Não definido'}")
        self.lbl_dest_csv.configure(text=f"Destino atual: {m.get('destino_csv') or 'Não definido'}")

    def setup_menu(self):
        ctk.CTkLabel(self.frame_menu, text="CENTRAL DE COMANDO", font=("Roboto", 26, "bold")).pack(pady=40)

        ctk.CTkButton(self.frame_menu, text="GERADOR DE QR CODE", width=320, height=80,
                      corner_radius=15, font=("Roboto", 16, "bold"),
                      command=lambda: self.mostrar_tela(self.frame_qr)).pack(pady=15)

        ctk.CTkButton(self.frame_menu, text="CONVERSOR CSV -> WORD", 
                      width=320, height=80, corner_radius=15, font=("Roboto", 16, "bold"),
                      fg_color="#2c3e50", hover_color="#1a252f",
                      command=lambda: self.mostrar_tela(self.frame_csv)).pack(pady=15)

    def setup_qr_screen(self):
        ctk.CTkLabel(self.frame_qr, text="GERADOR DE QR CODE", font=("Roboto", 20, "bold")).pack(pady=20)
        self.ent_qr_url = ctk.CTkEntry(self.frame_qr, placeholder_text="Link...", width=350, height=40)
        self.ent_qr_url.pack(pady=5)
        self.ent_qr_nome = ctk.CTkEntry(self.frame_qr, placeholder_text="Nome do arquivo...", width=350, height=40)
        self.ent_qr_nome.pack(pady=5)
        
        self.lbl_dest_qr = ctk.CTkLabel(self.frame_qr, text="", font=("Roboto", 10), text_color="gray")
        self.lbl_dest_qr.pack(pady=(15, 0))
        ctk.CTkButton(self.frame_qr, text="Alterar Pasta de Destino", width=150, height=25, fg_color="#3d3d3d",
                      command=lambda: self.trocar_pasta("destino_qr")).pack(pady=5)
        
        ctk.CTkButton(self.frame_qr, text="GERAR E SALVAR AGORA", width=320, height=80, font=("Roboto", 16, "bold"),
                      command=self.acao_qr).pack(pady=20)
        ctk.CTkButton(self.frame_qr, text="← Voltar", fg_color="transparent", command=lambda: self.mostrar_tela(self.frame_menu)).pack()

    def setup_csv_screen(self):
        ctk.CTkLabel(self.frame_csv, text="CONVERSOR CSV -> WORD", font=("Roboto", 20, "bold")).pack(pady=20)
        self.ent_csv_nome = ctk.CTkEntry(self.frame_csv, placeholder_text="Nome base...", width=350, height=45)
        self.ent_csv_nome.pack(pady=10)
        
        self.lbl_dest_csv = ctk.CTkLabel(self.frame_csv, text="", font=("Roboto", 10), text_color="gray")
        self.lbl_dest_csv.pack(pady=(15, 0))
        ctk.CTkButton(self.frame_csv, text="Alterar Pasta de Destino", width=150, height=25, fg_color="#3d3d3d",
                      command=lambda: self.trocar_pasta("destino_csv")).pack(pady=5)
        
        ctk.CTkButton(self.frame_csv, text="CONVERTER AGORA", width=320, height=80, font=("Roboto", 16, "bold"),
                      fg_color="#27ae60", command=self.acao_csv).pack(pady=20)
        ctk.CTkButton(self.frame_csv, text="← Voltar", fg_color="transparent", command=lambda: self.mostrar_tela(self.frame_menu)).pack()

    def trocar_pasta(self, chave):
        if ferramentas.escolher_nova_pasta(chave):
            self.atualizar_labels_destino()

    def acao_qr(self):
        pasta = ferramentas.obter_memorias().get("destino_qr")
        if ferramentas.processar_qr(self.ent_qr_url.get(), self.ent_qr_nome.get(), pasta):
            self.ent_qr_url.delete(0, 'end')
            self.ent_qr_nome.delete(0, 'end')
        else: self.mostrar_tela(self.frame_menu)

    def acao_csv(self):
        pasta = ferramentas.obter_memorias().get("destino_csv")
        if ferramentas.processar_csv_para_word(self.ent_csv_nome.get(), pasta):
            self.ent_csv_nome.delete(0, 'end')
        else: self.mostrar_tela(self.frame_menu)

if __name__ == "__main__":
    SweeToolsApp().mainloop()
