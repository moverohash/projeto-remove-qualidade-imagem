from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limitar o upload para 16 MB

# Certifique-se de que a pasta de uploads existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def resize_image(image, max_size=(4000, 4000)):
    """Redimensiona a imagem para caber no tamanho máximo e retorna a imagem redimensionada."""
    image.thumbnail(max_size, resample=Image.LANCZOS)
    return image

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('images')
        image_paths = []

        for file in files:
            if file and file.filename:
                image = Image.open(file)
                resized_image = resize_image(image)

                # Salva a imagem redimensionada
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                resized_image.save(image_path)
                print(f"Imagem salva em: {image_path}")  # Adicione esta linha para depuração
                image_paths.append(image_path)

        return render_template('index.html', image_paths=image_paths)

    return render_template('index.html', image_paths=[])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

