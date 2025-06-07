import tkinter as tk
from tkinter import ttk, messagebox
import math

class HammingSimulator:    
    def __init__(self):
        # ana pencere
        self.root = tk.Tk()
        self.root.title("Hamming SEC-DED Simülatörü")
        self.root.geometry("1400x700") 
        
        # deeğişkenler
        self.data_size = tk.IntVar(value=8)  # varsayılan 8 bit
        self.original_data = ""              # kullanıcının girdiği orijinal veri
        self.hamming_code = []               # üretilen Hamming kodu
        self.corrupted_code = []             # hata oluşturulmuş kod
        self.bit_buttons = []                 # bit butonları listesi
        self.changed_bits_count = 0         # Değiştirilen bit sayısı
        
        self.create_gui()
    
    def create_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Hamming SEC-DED Simülatörü", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # input alanı
        self.create_input_section(main_frame)
        
        # hamming kodunun gösterildiği section
        self.create_code_display_section(main_frame)
        
        # hata kontrolu
        self.create_error_check_section(main_frame)
    
    def create_input_section(self, parent):
        input_frame = ttk.LabelFrame(parent, padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # veri boyutu seçimi
        size_frame = ttk.Frame(input_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame, text="Veri Boyutu:").pack(side=tk.LEFT, padx=5)
        
        # sadece 8, 16, 32 bit seçenekleri
        for size in [8, 16, 32]:
            ttk.Radiobutton(size_frame, text=f"{size} bit", variable=self.data_size, value=size).pack(side=tk.LEFT, padx=5)
        
        # binary veri girişi
        data_frame = ttk.Frame(input_frame)
        data_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(data_frame, text="Binary Veri:").pack(side=tk.LEFT, padx=5)
        self.data_entry = ttk.Entry(data_frame, width=35, font=('Courier', 10))
        self.data_entry.pack(side=tk.LEFT, padx=5)
        
        # kod üretme butonu
        generate_btn = ttk.Button(data_frame, text="Hamming Kodu Üret", command=self.generate_hamming_code)
        generate_btn.pack(side=tk.LEFT, padx=10)
    
    def create_code_display_section(self, parent):
        self.code_frame = ttk.LabelFrame(parent, text="2. Hamming Kodu (Hata oluşturmak için bitlere tıklayın)", padding="10")
        self.code_frame.pack(fill=tk.X, pady=5)
        
        info_label = ttk.Label(self.code_frame, text="Yeşil: Parite Bitleri | Mavi: Veri Bitleri | Sarı: Toplam Parite | Kırmızı: Hatalı Bit", font=('Arial', 9))
        info_label.pack(pady=5)
    
    def create_error_check_section(self, parent):
        check_frame = ttk.LabelFrame(parent, text="3. Hata Tespiti ve Düzeltme", padding="10")
        check_frame.pack(fill=tk.X, pady=5)
        
        # kontrol butonu
        check_btn = ttk.Button(check_frame, text="Hata Kontrolü Yap", command=self.check_errors)
        check_btn.pack(pady=10)
        
        # sonuç alanı
        self.syndrome_label = ttk.Label(check_frame, text="Syndrome: -", font=('Courier', 11))
        self.syndrome_label.pack(pady=5)
        
        self.result_label = ttk.Label(check_frame, text="Durum: Kod üretilmedi", font=('Arial', 12, 'bold'))
        self.result_label.pack(pady=5)
        
        self.corrected_data_label = ttk.Label(check_frame, text="Düzeltilmiş Veri: -", font=('Courier', 11))
        self.corrected_data_label.pack(pady=5)
    
    def generate_hamming_code(self):
        # kullanıcıdan inputu al
        user_input = self.data_entry.get().strip()
        selected_size = self.data_size.get()
        
        # giriş kontrolü
        if not self.validate_input(user_input, selected_size):
            return
        
        self.original_data = user_input
        
        self.calculate_hamming_code()
        
        self.corrupted_code = self.hamming_code.copy()
        
        self.changed_bits_count = 0
        
        self.display_hamming_code()
        
        self.update_status("Hamming kodu üretildi. Hata oluşturmak için bitlere tıklayabilirsiniz.")
    
    def validate_input(self, user_input, selected_size):
        # boş girdi kontrolü
        if not user_input:
            messagebox.showerror("Hata", "Lütfen binary veri girin!")
            return False
        
        # Sadece 0 ve 1 kontrolü
        if not all(bit in '01' for bit in user_input):
            messagebox.showerror("Hata", "Sadece 0 ve 1 karakterleri kullanın!")
            return False
        
        # sadece seçilen bit sayısı kadar kabul et
        if len(user_input) != selected_size:
            messagebox.showerror("Hata", f"Tam olarak {selected_size} bit girmelisiniz!\nGirilen: {len(user_input)} bit")
            return False
        
        return True
    
    def calculate_hamming_code(self):
        data_bits = len(self.original_data)
        
        # parite bit sayısını hesaplıyor (2**k >= m + k + 1)
        parity_bits = 1
        while (2 ** parity_bits) < (data_bits + parity_bits + 1):
            parity_bits += 1
        
        total_bits = data_bits + parity_bits
        
        # kodu oluşturur önce sıfırlar eklenir
        code = []
        for _ in range(total_bits + 1):
            code.append(0)        

        # veri bitlerini yerleştir (parite pozisyonları hariç)
        data_index = 0
        for i in range(1, total_bits + 1):
            if not self.is_power_of_2(i):    # parite pozisyonu değilse
                if data_index < data_bits:
                    code[i] = int(self.original_data[data_index])
                    data_index += 1
        
        # parite bitlerini hesapla
        for i in range(parity_bits):
            parity_pos = 2 ** i
            parity_value = 0
            
            #parite bitinin kontrol ettiği pozisyonları bulur
            for j in range(1, total_bits + 1):
                if (j >> i) & 1:  
                    parity_value ^= code[j] # pythonda bu xor ataması olarak kullanılır.
            
            code[parity_pos] = parity_value
        
        # Toplam parite bitini hesapla (çift bit hata tespiti için)
        total_parity = 0
        for i in range(1, total_bits + 1):
            total_parity ^= code[i]
        
        # Hamming kodunu kaydet (0. index toplam parite)
        self.hamming_code = [total_parity] + code[1:]
    
    def is_power_of_2(self, n):
        return n > 0 and (n & (n - 1)) == 0
    
    def display_hamming_code(self):
        # önceki butonları tamamen temizle
        for widget in self.code_frame.winfo_children():
            widget.destroy()
        self.bit_buttons.clear()
        
        # Yeni açıklama ekle
        info_label = ttk.Label(self.code_frame, text="Yeşil: Parite Bitleri | Mavi: Veri Bitleri | Sarı: Toplam Parite | Kırmızı: Hatalı Bit", font=('Arial', 9))
        info_label.pack(pady=5)
        
        # kaydırılabilir frame oluşturur
        canvas = tk.Canvas(self.code_frame, height=150)
        scrollbar = ttk.Scrollbar(self.code_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        
        # bit butonlarını oluştur
        total_bits = len(self.hamming_code)
        
        for i in range(total_bits):
            if i == 0:
                # Toplam parite biti (0. index)
                label = "Toplam\nParite"
                color = "#FFD700"
            else:
                pos = i
                if self.is_power_of_2(pos):
                    # parite biti
                    label = f"P{pos}"
                    color = "#90EE90"   # yeşişl
                else:
                    # Veri biti
                    label = f"D{pos}"
                    color = "#ADD8E6"  #mavi
            
            # bit butonu oluştur
            btn = tk.Button(scrollable_frame, text=str(self.corrupted_code[i]), width=3, height=2, font=('Courier', 10, 'bold'), bg=color, command=lambda idx=i: self.flip_bit(idx))
            btn.grid(row=0, column=i, padx=1, pady=1) 
            
            # pozisyon etiketi
            lbl = ttk.Label(scrollable_frame, text=label, font=('Arial', 7))
            lbl.grid(row=1, column=i, padx=1) 
            
            self.bit_buttons.append(btn)
        
        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")
    
    def flip_bit(self, index):
        if not self.hamming_code:
            return
        
        # şu anki bitin durumunu kontrol et
        is_currently_changed = (self.corrupted_code[index] != self.hamming_code[index])
        
        if is_currently_changed:
            # Bit zaten değiştirilmişse, geri al
            self.corrupted_code[index] = self.hamming_code[index]
            self.changed_bits_count -= 1
            
            # orijinal renge döndürür
            if index == 0:
                self.bit_buttons[index].config(bg="#FFD700")  
            elif self.is_power_of_2(index):
                self.bit_buttons[index].config(bg="#90EE90")  
            else:
                self.bit_buttons[index].config(bg="#ADD8E6")  
            
            self.update_status("Bit geri alındı. Hata kontrolü yapın.")
        else:
            # bit değiştirilmek isteniyor
            if self.changed_bits_count >= 2:
                return
            
            # biti değiştir
            self.corrupted_code[index] = 1 - self.corrupted_code[index]
            self.changed_bits_count += 1
            
            # kırmızı renge çevir (hatalı bit)
            self.bit_buttons[index].config(bg="#FF6347")
            
            self.update_status(f"Bit değiştirildi ({self.changed_bits_count}/2). Hata kontrolü yapın.")
        
        # buton görünümünü güncelle
        self.bit_buttons[index].config(text=str(self.corrupted_code[index]))
        
        # canvas scroll alanını güncelle
        canvas = None
        for widget in self.code_frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                canvas = widget
                break
        if canvas:
            canvas.configure(scrollregion=canvas.bbox("all"))
    
    def check_errors(self):
        if not self.corrupted_code:
            messagebox.showerror("Hata", "Önce Hamming kodu üretin!")
            return
        
        # koddan toplam parite ve veri kısmını ayır
        received_total_parity = self.corrupted_code[0]
        received_code = self.corrupted_code[1:]
        
        # syndrome hesapla
        syndrome = self.calculate_syndrome(received_code)
        
        # mevcut toplam pariteyi hesapla
        current_total_parity = 0
        for bit in received_code:
            current_total_parity ^= bit
        
        # sonuçları göster
        self.syndrome_label.config(text=f"Syndrome: {syndrome} (Binary: {bin(syndrome)})")
        
        # hata tespiti ve düzeltme
        self.detect_and_correct_errors(syndrome, current_total_parity, 
                                     received_total_parity, received_code)
    
    def calculate_syndrome(self, code):
        code_length = len(code)
        parity_bits = math.ceil(math.log2(code_length + 1))
        syndrome = 0
        
        for i in range(parity_bits):
            parity_pos = 2 ** i
            parity_value = 0
            
            for j in range(1, code_length + 1):
                if (j >> i) & 1:
                    parity_value ^= code[j - 1] 
            
            if parity_value != 0:
                syndrome += parity_pos
        
        return syndrome
    
    def detect_and_correct_errors(self, syndrome, current_total_parity, received_total_parity, received_code):

        if syndrome == 0:
            if current_total_parity == received_total_parity: # no error
                self.result_label.config(text="✓ Hata tespit edilmedi", foreground="green")
                self.show_corrected_data(received_code)
            else:
                self.result_label.config(text="✓ Toplam parite bitinde hata (düzeltildi)", 
                                       foreground="orange")
                self.corrupted_code[0] = current_total_parity
                self.bit_buttons[0].config(text=str(current_total_parity), bg="#FFD700")
                self.show_corrected_data(received_code)
        else:
            if current_total_parity != received_total_parity: # single error
                error_pos = syndrome
                if 1 <= error_pos <= len(received_code):
                    self.result_label.config(text=f"✓ single error corrected (Pozisyon: {error_pos})", 
                                           foreground="blue")
                    
                    # single error correcting
                    corrected_code = received_code.copy()
                    corrected_code[error_pos - 1] = 1 - corrected_code[error_pos - 1]
                    
                    # GUI'yi güncelle bit rengini düzelt
                    if error_pos < len(self.bit_buttons):
                        original_color = "#FFD700" if error_pos == 0 else ("#90EE90" if self.is_power_of_2(error_pos) else "#ADD8E6")
                        self.bit_buttons[error_pos].config(text=str(corrected_code[error_pos - 1]), bg=original_color)
                    
                    self.show_corrected_data(corrected_code)
                else:
                    self.result_label.config(text="✗ Geçersiz hata pozisyonu", foreground="red")
            else:
                # double error 
                self.result_label.config(text="✗ double error detecting (düzeltilemez)", foreground="red")
    
    def show_corrected_data(self, corrected_code):
        # veri bitlerini çıkar
        data_bits = []
        for i in range(1, len(corrected_code) + 1):
            if not self.is_power_of_2(i):
                data_bits.append(str(corrected_code[i - 1]))
        
        corrected_data = "".join(data_bits)
        self.corrected_data_label.config(text=f"Düzeltilmiş Veri: {corrected_data}")
    
    def update_status(self, message):
        self.result_label.config(text=f"Durum: {message}", foreground="black")
        self.syndrome_label.config(text="Syndrome: -")
        self.corrected_data_label.config(text="Düzeltilmiş Veri: -")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HammingSimulator()
    app.run()