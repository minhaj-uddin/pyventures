import os
import qrcode

url_dict = {
    "Google": "https://www.google.com",
    "GitHub": "https://www.github.com",
    "OpenAI": "https://www.openai.com",
    "Python": "https://www.python.org",
    "Microsoft": "https://www.microsoft.com"
}

output_dir = "qr-codes"
os.makedirs(output_dir, exist_ok=True)

for name, url in url_dict.items():
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    
    filename = f"{name}_QR.png"
    image = qr.make_image(fill_color='black', back_color='white')
    image.save(os.path.join(output_dir, filename))
    print(f"QR code for {name} saved as {filename}")
