import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import re # Thư viện Regular Expressions

# --- PHẦN XỬ LÝ CHÍNH SỬ DỤNG REGEX ---

def xu_ly_cau_hoi_chinh_xac(noi_dung):
    """
    Hàm xử lý logic chính sử dụng Regular Expressions để phân tách câu hỏi và đáp án.
    """
    # 1. Làm sạch nội dung: Xóa các ký tự thừa, nhiều khoảng trắng, v.v.
    noi_dung = re.sub(r'\s{2,}', ' ', noi_dung)
    noi_dung = noi_dung.replace('\n', ' ').strip()
    
    # 2. Định nghĩa mẫu Regex để tìm kiếm các khối câu hỏi
    # Mẫu này tìm kiếm:
    # (Số thứ tự + dấu chấm/ký tự) + (Nội dung câu hỏi cho đến khi gặp "Đáp án:")
    # (Phần Đáp án: ... cho đến khi gặp câu hỏi tiếp theo)
    
    # Mẫu tìm kiếm cho TẤT CẢ các loại câu hỏi (A, B, C) và câu hỏi trắc nghiệm
    # Mẫu này sẽ tách dựa trên đánh số: 1. hoặc 2. ... hoặc B/ hoặc C/
    pattern = re.compile(
        r'(?P<index>[A-Z]/|\d+\.?)'  # Bắt đầu bằng đánh số (1., 2., B/, C/)
        r'(.*?)(?=(?P<next_index>[A-Z]/|\d+\.?|$))', # Lấy nội dung cho đến câu tiếp theo
        re.DOTALL
    )
    
    processed_data = []
    
    # Bắt đầu xử lý từng khối
    matches = list(pattern.finditer(noi_dung))
    
    if not matches:
        return "Không tìm thấy cấu trúc câu hỏi nào (thiếu đánh số 1., 2., B/, C/).", 0

    for match in matches:
        block_text = match.group(0).strip()
        index = match.group('index').strip()
        
        if index.endswith('/'): # Bỏ qua các tiêu đề như B/, C/, D/
            processed_data.append(f"--- PHẦN {index} ---")
            continue

        # Tách biệt Câu hỏi và Đáp án
        parts = re.split(r'答案[：:]', block_text, maxsplit=1)
        
        question_text = parts[0].strip()
        answer_text = parts[1].strip() if len(parts) > 1 else "Không có đáp án"
        
        # Làm sạch câu hỏi
        question_text = re.sub(r'^' + re.escape(index), '', question_text).strip()
        
        # Thử tách lựa chọn (A., B., C., D.) trong câu hỏi
        options_match = re.search(r'([A-D]\.\s.*?)答案', block_text, re.DOTALL)
        options_text = ""
        
        if options_match:
            # Nếu có lựa chọn (là câu trắc nghiệm), tách lựa chọn ra
            options_text = options_match.group(1).strip()
            # Bỏ phần lựa chọn khỏi câu hỏi chính
            question_text = question_text.replace(options_text, '').strip()

        # Thêm vào kết quả
        processed_data.append({
            "index": index,
            "question": question_text,
            "options": options_text,
            "answer": answer_text
        })

    # 3. Định dạng lại kết quả cho người dùng xem
    output_string = "--- DỮ LIỆU ĐÃ PHÂN TÁCH CHÍNH XÁC ---\n\n"
    so_cau_duoc_xu_ly = 0
    
    for item in processed_data:
        if isinstance(item, str): # Là các tiêu đề (B/, C/)
            output_string += f"{item}\n"
            continue
            
        so_cau_duoc_xu_ly += 1
        output_string += f"[{item['index']}]\n"
        output_string += f"Câu hỏi: {item['question']}\n"
        if item['options']:
            output_string += f"Các lựa chọn:\n{item['options']}\n"
        output_string += f"Đáp án: {item['answer']}\n"
    
        
    return output_string, so_cau_duoc_xu_ly

# --- GIAO DIỆN TKINTER (Giữ nguyên cấu trúc, chỉ thay đổi hàm xử lý) ---

def button_click():
    noi_dung = input_text.get(1.0, tk.END)
    if not noi_dung.strip():
        messagebox.showwarning("Cảnh Báo", "Vui lòng dán nội dung câu hỏi vào ô.")
        return
        
    # Gọi hàm xử lý chính xác
    ket_qua_xu_ly, so_cau = xu_ly_cau_hoi_chinh_xac(noi_dung)

    # Hiển thị kết quả xử lý
    messagebox.showinfo(
        "Xử Lý Hoàn Tất", 
        f"Đã phân tách thành công {so_cau} khối câu hỏi."
    )
    
    # Cập nhật kết quả vào ô output
    output_text.delete(1.0, tk.END) # Xóa nội dung cũ
    output_text.insert(tk.END, ket_qua_xu_ly) # Chèn nội dung mới
    

def tao_giao_dien():
    """Tạo cửa sổ và các thành phần giao diện."""
    
    window = tk.Tk()
    window.title("Công Cụ Tách Câu Hỏi Trắc Nghiệm (Dùng Regex)")
    window.geometry("900x700")

    # Global variables
    global input_text, output_text

    # --- Phần 1: Ô nhập liệu (Input) ---
    tk.Label(window, text="1. Dán toàn bộ danh sách câu hỏi vào đây (Gồm cả 'Đáp án:...' và 'A. B. C. D.'):", 
             font=('Arial', 10, 'bold')).pack(pady=5, anchor='w', padx=10)

    input_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=18, font=('Arial', 10))
    input_text.pack(pady=5, padx=10, fill=tk.X)
    
    # --- Phần 2: Nút Xử lý ---
    tk.Button(window, text="2. XỬ LÝ VÀ PHÂN TÁCH DỮ LIỆU >>", command=button_click, 
              bg="#007bff", fg="white", font=('Arial', 12, 'bold')).pack(pady=10)

    # --- Phần 3: Ô kết quả (Output) ---
    tk.Label(window, text="3. Kết quả đã phân tách (Kiểm tra xem câu hỏi và đáp án có đúng chưa):", 
             font=('Arial', 10, 'bold')).pack(pady=5, anchor='w', padx=10)

    output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=15, font=('Arial', 10))
    output_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    window.mainloop()

# Chạy chương trình
if __name__ == "__main__":
    tao_giao_dien()