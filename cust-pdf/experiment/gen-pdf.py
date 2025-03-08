from fpdf import FPDF
import os

def create_pdf(file_path, text_file_path, target_size_kb, filler_text=""):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Read content from the text file
    with open(text_file_path, "r") as file:
        content = file.read()
    
    pdf.multi_cell(0, 10, content)
    pdf_file_path = file_path
    pdf.output(pdf_file_path)
    
    # Add filler text iteratively to reach the target size
    while os.path.getsize(pdf_file_path) < target_size_kb * 1024:
        pdf.add_page()
        pdf.multi_cell(0, 10, filler_text)
        pdf.output(pdf_file_path)
    
    print(f"Generated: {pdf_file_path} ({os.path.getsize(pdf_file_path) / 1024:.2f} KB)")

# Example Usage
output_dir = "C:\\Users\\WINDOWS\\Documents\\CSS400_GDPR-RBC\\cust-pdf\\experiment"
os.makedirs(output_dir, exist_ok=True)

file_sizes_kb = [100,200,400,800,1600]
filler_text = "\n" + ("This is filler text to increase file size. " * 9)

for i, size in enumerate(file_sizes_kb, start=1):
    text_file_path = os.path.join(output_dir, f"customer_{i}.txt")
    pdf_file_path = os.path.join(output_dir, f"customer_{size}KB.pdf")
    create_pdf(pdf_file_path, text_file_path, size, filler_text)

print("Complete")