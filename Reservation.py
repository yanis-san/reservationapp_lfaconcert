import sqlite3
import qrcode
import streamlit as st
from reportlab.pdfgen import canvas
from PIL import Image
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4


# Créer une connexion à la base de données (création si elle n'existe pas)
conn = sqlite3.connect("tickets.db")
c = conn.cursor()

# Créer la table "clients" si elle n'existe pas déjà
c.execute("""CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                age INTEGER,
                gender TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")
conn.commit()

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img


def generate_pdf(data, image):
    # Générer le QR code
    qr_img = generate_qr_code(data)

    # Redimensionner l'image
    image = image.resize((414, 615))  # Redimensionnez selon vos besoins

    # Redimensionner le QR code
    qr_img = qr_img.resize((414, 414))  # Redimensionnez selon vos besoins

    # Calculer la hauteur totale du PDF en ajoutant la hauteur de l'image et du QR code
    total_height = image.size[1] + qr_img.size[1]

    # Générer le PDF
    pdf_buffer = BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=(image.size[0], total_height))

    # Insérer l'image dans le PDF (en haut)
    pdf_canvas.drawImage(ImageReader(image), x=0, y=qr_img.size[1], width=image.size[0], height=image.size[1])

    # Insérer le QR code dans le PDF (juste après l'image)
    pdf_canvas.drawImage(ImageReader(qr_img), x=0, y=0, width=qr_img.width, height=qr_img.height)

    # Enregistrer le contenu du PDF dans le buffer
    pdf_canvas.save()

    # Récupérer les données du PDF
    pdf_data = pdf_buffer.getvalue()

    return pdf_data

def send_email_with_pdf(pdf_data, email):
    from_addr = "lfaconcert@gmail.com"  # Adresse e-mail de l'expéditeur
    password = "pblyapgnvsphjbzk"  # Mot de passe de l'expéditeur

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = email
    msg["Subject"] = "Votre e-ticket pour le concert"

    # Attachement du PDF
    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(pdf_data)
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename="ticket.pdf")
    msg.attach(attachment)

    # Envoi du e-mail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_addr, password)
    server.send_message(msg)
    server.quit()

def main():
    st.title("Recevez votre e-ticket")

    # Saisie des données du client
    name = st.text_input("Nom complet")
    email = st.text_input("Adresse e-mail")
    phone = st.text_input("Numéro de téléphone")
    age = st.number_input("Âge", min_value=0, max_value=150, step=1)
    gender = st.radio("Sexe", ("Homme", "Femme"))

    if st.button("Générer le ticket"):
        # Vérifier que les informations sont saisies
        if not name or not email or not phone:
            st.warning("Veuillez saisir toutes les informations.")
            return

        # Vérifier l'âge en fonction du genre
        if (gender == "Femme" and age < 19) or (gender == "Homme" and age < 20):
            st.error("Cet événement est strictement réservé aux personnes majeures.")
            return

        # Ajouter le client à la base de données
        c.execute("INSERT INTO clients (name, email, phone, age, gender) VALUES (?, ?, ?, ?, ?)",
                  (name, email, phone, age, gender))
        conn.commit()

        # Récupérer l'ID du client
        client_id = c.lastrowid

        # Récupérer l'heure et la date actuelles
        c.execute("SELECT timestamp FROM clients WHERE id = ?", (client_id,))
        timestamp = c.fetchone()[0]

        # Générer les données du ticket
        ticket_data = f"ID client : {client_id}\nNom : {name}\nEmail : {email}\nNuméro de téléphone : {phone}\nÂge : {age}\nSexe : {gender}\nDate et heure : {timestamp}"

        # Générer le PDF avec le QR code et l'image
        image_path = "ticket.jpg"
        image = Image.open(image_path)
        pdf_data = generate_pdf(ticket_data, image)

        # Envoyer le PDF par e-mail
        send_email_with_pdf(pdf_data, email)

        st.success("Votre e-ticket a été envoyé par e-mail.")


if __name__ == "__main__":
    main()
