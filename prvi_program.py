from flask import Flask, render_template, request, flash, redirect, url_for, Response
from flask_mail import Mail, Message
from datetime import date
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey123")  # koristimo env var za Render

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME")  # ovo dodaj


mail = Mail(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if not name or not email or not message:
            flash("Please fill in all required fields!", "error")
            return redirect(url_for('contact'))

        msg = Message(
        subject=f"New Booking from {name}",
        recipients=[app.config['MAIL_USERNAME']],  # primaš na svoj mail
        reply_to=email,
        body=f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:\n{message}"
        )

        try:
            mail.send(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

        return redirect(url_for('contact'))

    return render_template("contact.html")

@app.route("/sitemap.xml", methods=['GET'])
def sitemap():
    pages = [
        url_for('home', _external=True),
        url_for('about', _external=True),
        url_for('contact', _external=True)
    ]

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in pages:
        sitemap_xml += "  <url>\n"
        sitemap_xml += f"    <loc>{page}</loc>\n"
        sitemap_xml += f"    <lastmod>{date.today()}</lastmod>\n"
        sitemap_xml += "    <priority>0.8</priority>\n"
        sitemap_xml += "  </url>\n"

    sitemap_xml += "</urlset>\n"

    return Response(sitemap_xml, mimetype='application/xml')


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)