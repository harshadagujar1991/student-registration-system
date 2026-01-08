# invoice_generator.py
# Handles PDF invoice generation using fpdf2

from fpdf import FPDF
import os

def generate_invoice(student, payment, department_name="-"):
    """
    Generate a PDF invoice for a student's payment.
    Args:
        student: Student object from SQLAlchemy
        payment: Payment object from SQLAlchemy
        department_name: Optional string for department name
    Returns:
        filename (str): Path to the generated PDF file
    """
    os.makedirs('invoices', exist_ok=True)
    filename = f"invoices/invoice_{student.Student_ID}_{payment.Pay_ID}.pdf"

    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Student Registration Invoice', ln=True, align='C')

    # Body
    pdf.set_font('Arial', '', 12)
    pdf.ln(4)
    pdf.cell(0, 8, f'Student ID: {student.Student_ID}', ln=True)
    pdf.cell(0, 8, f'Name: {student.Name}', ln=True)
    pdf.cell(0, 8, f'Email: {student.Email or "-"}', ln=True)
    pdf.cell(0, 8, f'Department: {department_name}', ln=True)

    pdf.ln(4)
    pdf.cell(0, 8, f'Payment ID: {payment.Pay_ID}', ln=True)
    pdf.cell(0, 8, f'Amount Paid: {payment.Amount}', ln=True)
    pdf.cell(0, 8, f'Status: {payment.Status}', ln=True)
    pdf.cell(0, 8, f'Date: {payment.Date}', ln=True)

    pdf.output(filename)
    return filename
