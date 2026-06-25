from flask import Flask, render_template, request, redirect, url_for, send_file
import pymysql
from fpdf import FPDF
from datetime import datetime
import io
import re

# 1. INISIALISASI APLIKASI FLASK
app = Flask(__name__)

# 2. KONFIGURASI KONEKSI DATABASE MYSQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rps_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)


# 3. CLASS STRUKTUR CETAKAN DOKUMEN PDF
class RPS_PDF(FPDF):
    def header(self):
        # Desain Kop Surat Resmi STMIK Mardira Indonesia
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 5, 'STMIK MARDIRA INDONESIA', ln=True, align='C')
        self.set_font('Helvetica', '', 8)
        self.cell(0, 4, 'JL. SOEKARNO-HATTA NO. 211 BANDUNG', ln=True, align='C')
        self.cell(0, 4, 'Telp: 022-5233429 email: info@stmik-mi.ac.id', ln=True, align='C')
        
        self.ln(5)
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 5, 'RENCANA PEMBELAJARAN SEMESTER (RPS)', ln=True, align='C')
        
        self.ln(2)
        self.set_line_width(0.6)
        y_garis = self.get_y()
        self.line(10, y_garis, 200, y_garis)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_line_width(0.2)
        self.line(10, 282, 200, 282)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Halaman {self.page_no()} dari {{nb}}', align='R')
        self.set_x(10)
        self.cell(0, 10, 'STMIK Mardira Indonesia - Jurusan Teknik Informatika S1', align='L')


# 4. ROUTING / MANAGEMENT ALUR APLIKASI WEB
@app.route('/')
def index():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM detail_mata_kuliah WHERE id = 1")
            mk_info = cursor.fetchone()
            
            cursor.execute("SELECT * FROM sesi_rps ORDER BY CAST(no_sesi AS UNSIGNED) ASC")
            sesi_list = cursor.fetchall()
    finally:
        connection.close()
    return render_template('index.html', mk=mk_info, data=sesi_list)


@app.route('/update_mk', methods=['POST'])
def update_mk():
    nama_mk = request.form.get('nama_mk', '')
    semester = request.form.get('semester', '')
    tgl_raw = request.form.get('tgl_penyusunan', '')

    if not tgl_raw:
        tgl_formatted = ""
        tgl_db_raw = None
    else:
        tgl_db_raw = tgl_raw
        try:
            date_obj = datetime.strptime(tgl_raw, '%Y-%m-%d')
            tgl_formatted = date_obj.strftime('%d-%m-%Y')
        except ValueError:
            tgl_formatted = tgl_raw

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """UPDATE detail_mata_kuliah 
                     SET nama_mk=%s, semester=%s, tgl_penyusunan=%s, tgl_raw=%s 
                     WHERE id=1"""
            cursor.execute(sql, (nama_mk, semester, tgl_formatted, tgl_db_raw))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('index'))


@app.route('/add_sesi', methods=['POST'])
def add_sesi():
    no_sesi = request.form['no_sesi']
    tgl_sesi_raw = request.form.get('tgl_sesi', '')
    sub_cp_mk = request.form['sub_cp_mk']
    sub_pokok_bahasan = request.form['sub_pokok_bahasan']
    
    if tgl_sesi_raw:
        try:
            date_obj = datetime.strptime(tgl_sesi_raw, '%Y-%m-%d')
            tgl_sesi = date_obj.strftime('%d-%m-%Y')
        except ValueError:
            tgl_sesi = tgl_sesi_raw
    else:
        tgl_sesi = ""

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO sesi_rps (no_sesi, tgl_sesi, sub_cp_mk, sub_pokok_bahasan) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (no_sesi, tgl_sesi, sub_cp_mk, sub_pokok_bahasan))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('index'))


@app.route('/delete_sesi/<int:id>')
def delete_sesi(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sesi_rps WHERE id = %s", (id,))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('index'))


@app.route('/reset_all')
def reset_all():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE detail_mata_kuliah SET nama_mk='', semester='', tgl_penyusunan='', tgl_raw=NULL WHERE id=1")
            cursor.execute("TRUNCATE TABLE sesi_rps")
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('index'))


@app.route('/download_pdf')
def download_pdf():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM detail_mata_kuliah WHERE id = 1")
            mk = cursor.fetchone()
            cursor.execute("SELECT * FROM sesi_rps ORDER BY CAST(no_sesi AS UNSIGNED) ASC")
            items = cursor.fetchall()
    finally:
        connection.close()

    pdf = RPS_PDF(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- RENDER TABEL IDENTITAS ATAS DOKUMEN ---
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(245, 245, 245)
    pdf.set_line_width(0.2)
    
    pdf.cell(40, 7, ' Mata Kuliah', border=1, fill=True)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(150, 7, f" {mk['nama_mk'] if mk else ''}", border=1, ln=True)
    
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(40, 7, ' Semester', border=1, fill=True)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(150, 7, f" {mk['semester'] if mk else ''}", border=1, ln=True)
    
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(40, 7, ' Tgl Penyusunan', border=1, fill=True)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(150, 7, f" {mk['tgl_penyusunan'] if mk else ''}", border=1, ln=True)
    
    pdf.ln(6)

    # --- RENDER HEADER TABEL DENGAN KOLOM TERPISAH ---
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(230, 230, 230)
    
    w_sesi = 15
    w_tgl = 25
    w_cp = 75
    w_mat = 75
    
    pdf.cell(w_sesi, 8, 'Sesi', 1, 0, 'C', True)
    pdf.cell(w_tgl, 8, 'Tanggal', 1, 0, 'C', True)
    pdf.cell(w_cp, 8, 'Sub-CP-MK', 1, 0, 'C', True)
    pdf.cell(w_mat, 8, 'Sub-Pokok Bahasan / Materi', 1, 0, 'C', True)
    pdf.ln()

    # --- RENDER BARIS TABEL DINAMIS ---
    pdf.set_font('Helvetica', '', 9)
    
    for item in items:
        lines_cp = pdf.multi_cell(w_cp, 5, item['sub_cp_mk'], split_only=True)
        lines_mat = pdf.multi_cell(w_mat, 5, item['sub_pokok_bahasan'], split_only=True)
        
        max_lines = max(len(lines_cp), len(lines_mat), 1) 
        row_h = (max_lines * 5) + 4  
        
        if pdf.get_y() + row_h > 270:
            pdf.add_page()
            pdf.set_font('Helvetica', 'B', 9)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(w_sesi, 8, 'Sesi', 1, 0, 'C', True)
            pdf.cell(w_tgl, 8, 'Tanggal', 1, 0, 'C', True)
            pdf.cell(w_cp, 8, 'Sub-CP-MK', 1, 0, 'C', True)
            pdf.cell(w_mat, 8, 'Sub-Pokok Bahasan / Materi', 1, 0, 'C', True)
            pdf.ln()
            pdf.set_font('Helvetica', '', 9)

        x_start = pdf.get_x()
        y_start = pdf.get_y()
        
        # Kolom 1: Sesi
        pdf.set_xy(x_start, y_start + 2)
        pdf.cell(w_sesi, 5, str(item['no_sesi']), 0, 0, 'C')
        
        # Kolom 2: Tanggal Terpisah
        pdf.set_xy(x_start + w_sesi, y_start + 2)
        pdf.cell(w_tgl, 5, str(item['tgl_sesi']), 0, 0, 'C')
        
        # Kolom 3: Sub-CP-MK
        pdf.set_xy(x_start + w_sesi + w_tgl, y_start + 2)
        pdf.multi_cell(w_cp, 5, item['sub_cp_mk'], 0, 'L')
        
        # Kolom 4: Pokok Bahasan
        pdf.set_xy(x_start + w_sesi + w_tgl + w_cp, y_start + 2)
        pdf.multi_cell(w_mat, 5, item['sub_pokok_bahasan'], 0, 'L')
        
        # Grid Garis Pembungkus Seluruh Kolom
        pdf.set_xy(x_start, y_start)
        pdf.cell(w_sesi, row_h, '', 1)
        pdf.cell(w_tgl, row_h, '', 1)
        pdf.cell(w_cp, row_h, '', 1)
        pdf.cell(w_mat, row_h, '', 1)
        
        pdf.set_xy(x_start, y_start + row_h)

    # --- PENAMAAN FILE OUTPUT SESUAI NAMA MATA KULIAH ---
    nama_matkul = mk['nama_mk'] if mk and mk['nama_mk'] else "Mata_Kuliah"
    filename_clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', nama_matkul.strip())
    download_name = f"RPS_{filename_clean}.pdf"

    # --- PERBAIKAN OUTPUT BERDASARKAN PARAMETER DETEKSI STRING/BYTES ---
    pdf_string = pdf.output(dest='S') # Memaksa output menjadi raw string ('S')
    
    pdf_output = io.BytesIO()
    # Mengonversi string murni FPDF ke format bytes menggunakan encoding latin-1 agar aman bagi PDF
    pdf_output.write(pdf_string.encode('latin-1')) 
    pdf_output.seek(0)
    
    return send_file(pdf_output, mimetype='application/pdf', as_attachment=False, download_name=download_name)


if __name__ == '__main__':
    app.run(debug=True)