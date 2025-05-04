import customtkinter as ctk
from tkinter import filedialog
import fitz  # PyMuPDF
import re
import os
from collections import defaultdict
def read_pdf_to_txt(pdf_path):
    doc = fitz.open(pdf_path)
    record_list = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        lines = text.splitlines()
        matches = re.findall(r'(Line# \d+\s+\d+)', text)
        for match in matches:
            line_number = int(re.findall(r'Line# (\d+)\s+\d+', match)[0])
            if len(record_list) == 0:
                record_list.append([line_number,match])
            elif line_number - 1 == record_list[-1][0] or line_number == record_list[-1][0]:
                record_list.append([line_number, match])
            else:
                break
    record_list2 = []
    for line in record_list:
        message_id = re.findall(r'Line# \d+\s+(\d+)', line[1])[0]
        if message_id != "628":
            record_list2.append(line[1].replace("\n", " "))
    for line in record_list:
        message_id = re.findall(r'Line# \d+\s+(\d+)', line[1])[0]
        if message_id == "628":
            record_list2.append(line[1].replace("\n", " "))

    grouped = defaultdict(list)
    for line in record_list2:
        match = line.strip().split()
        if len(match) == 3:
            line_label, number, message_id = match
            grouped[message_id].append(f"Line# {number}")
    file = open("./generated_txts/"+pdf_path.split("/")[-1][:-4] + ".txt", "w")
    file.truncate()
    file.close
    file = open("./generated_txts/"+pdf_path.split("/")[-1][:-4] + ".txt", "a")
    for message_id in grouped.keys():
        file.write("\n")
        file.write(f"{message_id}\n")
        for line_num in grouped[message_id]:
            file.write(f"{line_num}\n")
    file.close
    return "./generated_txts/"+pdf_path.split("/")[-1][:-4] + ".txt"

class PDFApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF Line Extractor")
        self.geometry("600x250")

        self.pdf_path = ""

        self.label = ctk.CTkLabel(self, text="Select a PDF file")
        self.label.pack(pady=10)

        self.select_button = ctk.CTkButton(self, text="Browse PDF", command=self.browse_file)
        self.select_button.pack(pady=5)

        # Textbox to display selected path
        self.path_entry = ctk.CTkEntry(self, width=500)
        self.path_entry.pack(pady=5)

        # Frame to hold run and exit buttons side by side
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.run_button = ctk.CTkButton(self.button_frame, text="Run", command=self.run_process, state="disabled")
        self.run_button.pack(side="left", padx=10)

        self.exit_button = ctk.CTkButton(self.button_frame, text="Exit", command=self.quit)
        self.exit_button.pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

    def browse_file(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            self.label.configure(text=f"Selected: {os.path.basename(self.pdf_path)}")
            self.path_entry.delete(0, ctk.END)
            self.path_entry.insert(0, self.pdf_path)
            self.run_button.configure(state="normal")

    def run_process(self):
        output_path = read_pdf_to_txt(self.pdf_path)
        self.status_label.configure(text=f"Saved to:\n{output_path}")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = PDFApp()
    app.mainloop()



