import ipfshttpclient
import os
import random
from fpdf import FPDF
from cryptography.fernet import Fernet

# Generate or load encryption key
def load_or_generate_key():
    key_file = "encryption_key.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
        return key

# Generate a PDF from customer text file
def create_pdf_from_text(text_file, pdf_path, target_size_kb):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    with open(text_file, "r") as file:
        content = file.read()
    
    while True:
        pdf.multi_cell(0, 10, content)
        pdf.output(pdf_path)
        if os.path.getsize(pdf_path) >= target_size_kb * 1024:
            break

# Encrypt PDF
def encrypt_pdf(file_path, encrypted_file_path, key):
    cipher = Fernet(key)
    with open(file_path, "rb") as f:
        encrypted_data = cipher.encrypt(f.read())
    with open(encrypted_file_path, "wb") as f:
        f.write(encrypted_data)
    os.remove(file_path)  # Delete original PDF

# Upload encrypted PDF to IPFS
def upload_to_ipfs(file_path):
    client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001")  # Updated connection
    res = client.add(file_path)
    os.remove(file_path)  # Clean up local copy
    return res["Hash"]

if __name__ == "__main__":
    key = load_or_generate_key()
    input_dir = "C:\\Users\\WINDOWS\\Documents\\CSS400_GDPR-RBC\\cust-info"
    output_dir = "C:\\Users\\WINDOWS\\Documents\\CSS400_GDPR-RBC\\cust-pdf"
    os.makedirs(output_dir, exist_ok=True)
    
    customer_files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
    customer_files = customer_files[:2000]  # Limit to first 2000 customers
    
    for i, filename in enumerate(customer_files):
        text_file = os.path.join(input_dir, filename)
        target_size_kb = random.choice([10, 20, 50, 75, 100])
        pdf_filename = f"customer_{i+1}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        create_pdf_from_text(text_file, pdf_path, target_size_kb)
        encrypted_pdf_path = pdf_path.replace(".pdf", "_enc.pdf")
        encrypt_pdf(pdf_path, encrypted_pdf_path, key)
        
        ipfs_hash = upload_to_ipfs(encrypted_pdf_path)
        print(f"Encrypted PDF uploaded to IPFS with CID: {ipfs_hash}")
