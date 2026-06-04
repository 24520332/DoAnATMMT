import customtkinter as ctk
from tkinter import messagebox, filedialog
import random

# Thiết lập giao diện theo phong cách hiện đại
ctk.set_appearance_mode("System")  # Tự động theo Windows (Dark/Light)
ctk.set_default_color_theme("blue") # Bộ theme gốc

# --- CẤU HÌNH MÀU SẮC ĐỒNG BỘ (BẢNG MÀU PREMIUM) ---
COLOR_PRIMARY = "#10b981"      # Màu xanh Mint chủ đạo cho nút Mã hóa / Giải mã
COLOR_PRIMARY_HOVER = "#059669"# Màu khi di chuột vào nút chính
COLOR_SECONDARY = "#4b5563"    # Màu xám tro cho các nút tính năng phụ (File, Reset, Matrix)
COLOR_SECONDARY_HOVER = "#374151"
COLOR_BG_CARD = ("#f3f4f6", "#1e293b") # Màu nền cho các khung chứa (Light/Dark)
COLOR_TEXTBOX_BG = ("#ffffff", "#0f172a") # Màu nền ô nhập liệu

# ==========================================
# 1. THUẬT TOÁN & LOGIC PLAYFAIR (5X5 & 6X6)
# ==========================================
def generate_playfair_matrix(key, size=5):
    if size == 5:
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        key_clean = "".join([c.upper() for c in key if c.isalpha()]).replace('J', 'I')
    else:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        key_clean = "".join([c.upper() for c in key if c.isalnum()])
        
    combined = key_clean + alphabet
    final_key = []
    for char in combined:
        if char not in final_key:
            final_key.append(char)
    return [final_key[i:i+size] for i in range(0, size*size, size)]

def prepare_playfair_text(text, size=5, is_plaintext=True):
    if size == 5:
        text = "".join([c.upper() for c in text if c.isalpha()]).replace('J', 'I')
    else:
        text = "".join([c.upper() for c in text if c.isalnum()])
        
    if not is_plaintext or not text:
        return text
    
    optimized = ""
    i = 0
    while i < len(text):
        optimized += text[i]
        if i + 1 < len(text):
            if text[i] == text[i+1]:
                optimized += 'X'
            else:
                optimized += text[i+1]
                i += 1
        i += 1
    if len(optimized) % 2 != 0:
        optimized += 'X'
    return optimized

def find_position(matrix, char, size=5):
    for r in range(size):
        for c in range(size):
            if matrix[r][c] == char:
                return r, c
    return 0, 0

def process_playfair(text, key, size=5, encrypt=True):
    try:
        matrix = generate_playfair_matrix(key, size)
        prepared = prepare_playfair_text(text, size, encrypt)
        if not prepared: return ""
        result = ""
        d = 1 if encrypt else -1
        
        for i in range(0, len(prepared), 2):
            r1, c1 = find_position(matrix, prepared[i], size)
            r2, c2 = find_position(matrix, prepared[i+1], size)
            
            if r1 == r2:
                result += matrix[r1][(c1 + d) % size] + matrix[r2][(c2 + d) % size]
            elif c1 == c2:
                result += matrix[(r1 + d) % size][c1] + matrix[(r2 + d) % size][c2]
            else:
                result += matrix[r1][c2] + matrix[r2][c1]
        return result
    except Exception as e:
        return f"Lỗi: {str(e)}"

# ==========================================
# 2. THUẬT TOÁN & LOGIC RSA
# ==========================================
def gcd(a, b):
    while b: a, b = b, a % b
    return a

def mod_inverse(e, phi):
    t, newt = 0, 1
    r, newr = phi, e
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        raise ValueError(f"Không tìm được modular inverse: gcd(e={e}, phi={phi}) ≠ 1. Chọn e khác!")
    if t < 0: t += phi      
    return t

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def generate_prime_keys():
    primes = [
        1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 
        2003, 2011, 2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081,
        3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079
    ]
    p = random.choice(primes)
    q = random.choice(primes)
    while p == q:
        q = random.choice(primes)
    return p, q

def rsa_encrypt_text(plaintext, e, n):
    cipher_list = [str(pow(ord(char), e, n)) for char in plaintext]
    return "-".join(cipher_list)

def rsa_decrypt_text(ciphertext, d, n):
    try:
        blocks = ciphertext.strip().split("-")
        plain_chars = [chr(pow(int(num), d, n)) for num in blocks if num]
        return "".join(plain_chars)
    except Exception:
        return "Lỗi: Chuỗi số mã hóa RSA không hợp lệ hoặc sai thông số Khóa!"

# ==========================================
# 3. GIAO DIỆN ĐA GIẢI THUẬT CAO CẤP V5
# ==========================================
class HarmoniousCryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Hệ Thống Mã Hóa Bảo Mật - CRYPTOGRAPHY WORKSPACE")
        self.geometry("900x680")
        self.resizable(False, False)
        
        # Tiêu đề ứng dụng tối giản thanh lịch
        self.title_lbl = ctk.CTkLabel(self, text="DỰ ÁN MÃ HÓA BẢO MẬT", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
        self.title_lbl.pack(pady=(20, 10))
        
        # Thiết lập thanh Tabs phẳng (Flat UI)
        self.tabview = ctk.CTkTabview(self, width=860, height=580)
        self.tabview.pack(padx=20, pady=5)
        
        self.tab_pf = self.tabview.add("Mã hóa Playfair")
        self.tab_rsa = self.tabview.add("Mã hóa RSA")
        
        self.setup_playfair_ui()
        self.setup_rsa_ui()
        
    # --- GIAO DIỆN TAB PLAYFAIR ---
    def setup_playfair_ui(self):
        main_pf_frame = ctk.CTkFrame(self.tab_pf, fg_color="transparent")
        main_pf_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_frame = ctk.CTkFrame(main_pf_frame, fg_color="transparent", width=460)
        left_frame.pack(side="left", fill="both", expand=True)
        
        self.right_frame = ctk.CTkFrame(main_pf_frame, width=340, fg_color=COLOR_BG_CARD, corner_radius=12)
        self.right_frame.pack(side="right", fill="both", padx=(15, 0))
        
        # Khung chọn Kích thước
        size_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        size_frame.pack(anchor="w", padx=10, pady=(0, 10))
        ctk.CTkLabel(size_frame, text="Kích thước Ma Trận:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w")
        
        self.pf_size_var = ctk.StringVar(value="5x5")
        self.radio_5x5 = ctk.CTkRadioButton(size_frame, text="5 x 5 (Chữ)", variable=self.pf_size_var, value="5x5", command=self.on_matrix_size_change, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER)
        self.radio_5x5.grid(row=0, column=1, padx=20)
        self.radio_6x6 = ctk.CTkRadioButton(size_frame, text="6 x 6 (Chữ + Số)", variable=self.pf_size_var, value="6x6", command=self.on_matrix_size_change, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER)
        self.radio_6x6.grid(row=0, column=2, padx=10)

        # Khung nhập Khóa
        ctk.CTkLabel(left_frame, text="Nhập Khóa (Key):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10)
        key_action_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        key_action_frame.pack(fill="x", padx=10, pady=5)
        self.pf_key = ctk.CTkEntry(key_action_frame, width=280, height=32, fg_color=COLOR_TEXTBOX_BG)
        self.pf_key.insert(0, "CNTT")
        self.pf_key.grid(row=0, column=0, sticky="w")
        
        self.btn_update_matrix = ctk.CTkButton(key_action_frame, text="🔄 Đổi & Hiện Ma Trận", width=140, height=32, fg_color=COLOR_SECONDARY, hover_color=COLOR_SECONDARY_HOVER, font=ctk.CTkFont(weight="bold"), text_color="white")
        self.btn_update_matrix.grid(row=0, column=1, padx=15)
        self.btn_update_matrix.configure(command=self.update_pf_matrix_display)
        
        # Khung Văn bản đầu vào
        file_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        file_frame.pack(anchor="w", padx=10, pady=(10, 2))
        ctk.CTkLabel(file_frame, text="Văn Bản Đầu Vào:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(file_frame, text="📁 Chọn File .txt", width=100, height=20, fg_color=COLOR_SECONDARY, hover_color=COLOR_SECONDARY_HOVER, command=lambda: self.load_file(self.pf_input)).grid(row=0, column=1, padx=20)
        
        self.pf_input = ctk.CTkTextbox(left_frame, width=440, height=100, corner_radius=8, border_width=1, wrap="word", fg_color=COLOR_TEXTBOX_BG)
        self.pf_input.pack(padx=10, pady=5)
        
        # Khung nút bấm hành động (ĐỒNG BỘ MÀU CHỦ ĐẠO)
        btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="🔒 Mã Hóa", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=ctk.CTkFont(weight="bold"), width=150, height=38, text_color="white", command=self.run_pf_encrypt).grid(row=0, column=0, padx=15)
        ctk.CTkButton(btn_frame, text="  Giải Mã", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=ctk.CTkFont(weight="bold"), width=150, height=38, text_color="white", command=self.run_pf_decrypt).grid(row=0, column=1, padx=15)
        
        # Khung Kết quả đầu ra
        file_out_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        file_out_frame.pack(anchor="w", padx=10, pady=(10, 2))
        ctk.CTkLabel(file_out_frame, text="Kết Quả Đầu Ra:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(file_out_frame, text="💾 Lưu File .txt", width=100, height=20, fg_color=COLOR_SECONDARY, hover_color=COLOR_SECONDARY_HOVER, command=lambda: self.save_file(self.pf_output)).grid(row=0, column=1, padx=20)
        
        self.pf_output = ctk.CTkTextbox(left_frame, width=440, height=100, corner_radius=8, border_width=1, fg_color=COLOR_TEXTBOX_BG, wrap="word")
        self.pf_output.pack(padx=10, pady=5)
        
        self.matrix_grid_frame = None
        self.update_pf_matrix_display()

    def on_matrix_size_change(self):
        self.update_pf_matrix_display()

    def update_pf_matrix_display(self):
        if self.matrix_grid_frame is not None:
            self.matrix_grid_frame.destroy()
            
        size = 5 if self.pf_size_var.get() == "5x5" else 6
        key = self.pf_key.get()
        matrix = generate_playfair_matrix(key, size)
        
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(self.right_frame, text=f"MA TRẬN PLAYFAIR {size}x{size}", font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI")).pack(pady=15)
        self.matrix_grid_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.matrix_grid_frame.pack(padx=15, pady=5, expand=True)
        
        box_size = 44 if size == 5 else 38
        
        for r in range(size):
            for c in range(size):
                lbl = ctk.CTkLabel(self.matrix_grid_frame, text=matrix[r][c], width=box_size, height=box_size, corner_radius=6, fg_color=("#ffffff", "#0f172a"), font=ctk.CTkFont(size=14, weight="bold"))
                lbl.grid(row=r, column=c, padx=3, pady=3)

    def run_pf_encrypt(self):
        size = 5 if self.pf_size_var.get() == "5x5" else 6
        res = process_playfair(self.pf_input.get("1.0", "end-1c"), self.pf_key.get(), size, True)
        self.pf_output.delete("1.0", "end")
        self.pf_output.insert("1.0", res)

    def run_pf_decrypt(self):
        size = 5 if self.pf_size_var.get() == "5x5" else 6
        res = process_playfair(self.pf_input.get("1.0", "end-1c"), self.pf_key.get(), size, False)
        self.pf_output.delete("1.0", "end")
        self.pf_output.insert("1.0", res)

    # --- GIAO DIỆN TAB RSA ---
    def setup_rsa_ui(self):
        config_frame = ctk.CTkFrame(self.tab_rsa, fg_color=COLOR_BG_CARD, corner_radius=12)
        config_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(config_frame, text="⚙️ CẤU HÌNH SỐ NGUYÊN TỐ", font=ctk.CTkFont(weight="bold", size=13)).grid(row=0, column=0, columnspan=2, padx=15, pady=8, sticky="w")
        
        ctk.CTkLabel(config_frame, text="Số p:").grid(row=1, column=0, padx=(25,5), pady=8)
        self.rsa_p = ctk.CTkEntry(config_frame, width=90, fg_color=COLOR_TEXTBOX_BG)
        self.rsa_p.insert(0, "1031")
        self.rsa_p.grid(row=1, column=1, padx=5, pady=8)
        
        ctk.CTkLabel(config_frame, text="Số q:").grid(row=1, column=2, padx=15, pady=8)
        self.rsa_q = ctk.CTkEntry(config_frame, width=80, fg_color=COLOR_TEXTBOX_BG)
        self.rsa_q.insert(0, "1039")
        self.rsa_q.grid(row=1, column=3, padx=5, pady=8)
        
        self.btn_auto_key = ctk.CTkButton(config_frame, text="✨ Sinh Khóa Tự Động", fg_color=COLOR_SECONDARY, hover_color=COLOR_SECONDARY_HOVER, font=ctk.CTkFont(weight="bold"), width=180, command=self.auto_generate_rsa_inputs)
        self.btn_auto_key.grid(row=1, column=4, padx=50, pady=8)
        
        # Khung văn bản đầu vào RSA
        input_file_frame = ctk.CTkFrame(self.tab_rsa, fg_color="transparent")
        input_file_frame.pack(anchor="w", padx=15, pady=(5,0))
        ctk.CTkLabel(input_file_frame, text="Nhập Văn Bản Cần Xử Lý:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0)
        ctk.CTkButton(input_file_frame, text="📁 Chọn File .txt", width=100, height=18, fg_color=COLOR_SECONDARY, hover_color=COLOR_SECONDARY_HOVER, command=lambda: self.load_file(self.rsa_input)).grid(row=0, column=1, padx=20)
        
        self.rsa_input = ctk.CTkTextbox(self.tab_rsa, width=810, height=100, corner_radius=8, border_width=1, wrap="word", fg_color=COLOR_TEXTBOX_BG)
        self.rsa_input.pack(padx=15, pady=5)
        
        # Hai nút hành động chính (ĐỒNG BỘ MÀU CHỦ ĐẠO MINT)
        action_frame = ctk.CTkFrame(self.tab_rsa, fg_color="transparent")
        action_frame.pack(pady=10)
        ctk.CTkButton(action_frame, text="🔒 Mã Hóa Văn Bản", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=ctk.CTkFont(weight="bold"), width=220, height=38, command=self.run_rsa_encrypt).grid(row=0, column=0, padx=25)
        ctk.CTkButton(action_frame, text="  Giải Mã Chuỗi Số", fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=ctk.CTkFont(weight="bold"), width=220, height=38, command=self.run_rsa_decrypt).grid(row=0, column=1, padx=25)
        
        # Kết quả đầu ra RSA
        out_file_frame = ctk.CTkFrame(self.tab_rsa, fg_color="transparent")
        out_file_frame.pack(anchor="w", padx=15, pady=(5,0))
        ctk.CTkLabel(out_file_frame, text="Kết Quả Đầu Ra & Nhật Ký Hệ Thống:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0)
        ctk.CTkButton(out_file_frame, text="💾 Lưu Kết Quả", width=100, height=18, fg_color=COLOR_SECONDARY, hover_color=COLOR_SECONDARY_HOVER, command=lambda: self.save_file(self.rsa_output)).grid(row=0, column=1, padx=20)
        
        self.rsa_output = ctk.CTkTextbox(self.tab_rsa, width=810, height=180, corner_radius=8, border_width=1, fg_color=COLOR_TEXTBOX_BG, font=ctk.CTkFont(family="Consolas", size=12), wrap="word")
        self.rsa_output.pack(padx=15, pady=5)

    def auto_generate_rsa_inputs(self):
        p, q = generate_prime_keys()
        self.rsa_p.delete(0, "end")
        self.rsa_p.insert(0, str(p))
        self.rsa_q.delete(0, "end")
        self.rsa_q.insert(0, str(q))

    def get_rsa_keys(self):
        try:
            p = int(self.rsa_p.get())
            q = int(self.rsa_q.get())
        except ValueError:
            raise ValueError("Vui lòng nhập giá trị số nguyên hợp lệ!")
        if p == q:
            raise ValueError("p và q phải khác nhau!")
        if not is_prime(p) or not is_prime(q):
            raise ValueError("Cả p và q buộc phải là số nguyên tố!")
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 3
        while e < phi:
            if gcd(e, phi) == 1: break
            e += 2
        if e >= phi:
            raise ValueError("Không tìm được giá trị e hợp lệ. Chọn p, q lớn hơn!")
        d = mod_inverse(e, phi)
        if d is None:
            raise ValueError("Lỗi tính toán khóa riêng. Thử lại với p, q khác!")
        return e, d, n, phi

    def run_rsa_encrypt(self):
        try:
            e, d, n, phi = self.get_rsa_keys()
            plaintext = self.rsa_input.get("1.0", "end-1c").strip()
            if not plaintext: return
            
            cipher_text = rsa_encrypt_text(plaintext, e, n)
            
            log = f"--- THÔNG SỐ KHÓA RSA PHIÊN NÀY ---\n"
            log += f"• Modulus n = {n} | Phi(n) = {phi}\n"
            log += f"• Public Key (e, n)  = ({e}, {n})\n"
            log += f"• Private Key (d, n) = ({d}, {n})\n"
            log += f"--------------------------------------------------\n"
            log += f"🔒 CHUỖI SỐ MÃ HÓA ĐẦU RA:\n{cipher_text}"
            
            self.rsa_output.delete("1.0", "end")
            self.rsa_output.insert("1.0", log)
        except Exception as ex:
            messagebox.showerror("Lỗi RSA", str(ex))

    def run_rsa_decrypt(self):
        try:
            e, d, n, phi = self.get_rsa_keys()
            raw_input = self.rsa_input.get("1.0", "end-1c").strip()
            
            if "🔒 CHUỖI SỐ MÃ HÓA ĐẦU RA:\n" in raw_input:
                ciphertext = raw_input.split("🔒 CHUỖI SỐ MÃ HÓA ĐẦU RA:\n")[-1].strip()
            else:
                ciphertext = raw_input
                
            if not ciphertext: return
            
            plain_text = rsa_decrypt_text(ciphertext, d, n)
            
            log = f"--- GIẢI MÃ RSA THÀNH CÔNG ---\n"
            log += f"🔓 VĂN BẢN GỐC KHÔI PHỤC ĐƯỢC:\n{plain_text}"
            
            self.rsa_output.delete("1.0", "end")
            self.rsa_output.insert("1.0", log)
        except Exception as ex:
            messagebox.showerror("Lỗi RSA", str(ex))

    # --- ĐỌC/GHI FILE VĂN BẢN ---
    def load_file(self, textbox_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            textbox_widget.delete("1.0", "end")
            textbox_widget.insert("1.0", content)

    def save_file(self, textbox_widget):
        content = textbox_widget.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showwarning("Cảnh báo", "Không có nội dung để xuất file!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Thành công", "Đã lưu file thành công!")

if __name__ == "__main__":
    app = HarmoniousCryptoApp()
    app.mainloop()