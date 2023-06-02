from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение загруженных пользователем изображений
        image1 = request.files['image1']
        image2 = request.files['image2']

        # Загрузка изображений с помощью библиотеки Pillow
        img1 = Image.open(image1)
        img2 = Image.open(image2)

        # Преобразование изображений в массивы NumPy
        arr1 = np.array(img1)
        arr2 = np.array(img2)

        # Получение значения уровня смешения от 0 до 1
        alpha = float(request.form['alpha'])

        # Смешивание изображений
        blended = alpha * arr1 + (1 - alpha) * arr2
        blended = blended.astype(np.uint8)

        # Сохранение результата смешивания в новое изображение
        result = Image.fromarray(blended)
        result.save('static/result.jpg')

        # Генерация графиков распределения цветов
        color_distribution1 = get_color_distribution(arr1)
        color_distribution2 = get_color_distribution(arr2)
        color_distribution_result = get_color_distribution(blended)

        # Отображение шаблона HTML с результатами
        return render_template('result.html',
                               color_distribution1=color_distribution1,
                               color_distribution2=color_distribution2,
                               color_distribution_result=color_distribution_result)

    return render_template('index.html')


def get_color_distribution(image_array):
    # Получение распределения цветов в изображении
    r, g, b = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2]
    r_hist = np.histogram(r, bins=256, range=(0, 255))[0]
    g_hist = np.histogram(g, bins=256, range=(0, 255))[0]
    b_hist = np.histogram(b, bins=256, range=(0, 255))[0]
    return r_hist, g_hist, b_hist


if __name__ == '__main__':
    app.run(debug=True)



@app.route('/resized_images', methods=['GET'])
def show_resized_images():
    scale_factor = float(request.args.get('scale_factor', 1.0))
    image_files = request.files.getlist('image')

    resized_images = []

    for image_file in image_files:
        image_path = 'static/uploaded_image.jpg'
        image_file.save(image_path)

        original_image = Image.open(image_path)
        original_width, original_height = original_image.size
        new_original_width = int(original_width / scale_factor)
        new_original_height = int(original_height / scale_factor)

        resized_original_image = original_image.resize((new_original_width, new_original_height))

        resized_original_image_path = 'image1.jpg'
        resized_original_image.save(resized_original_image_path)

        resized_images.append(resized_original_image_path)

    return render_template('resized_images.html', scale_factor=scale_factor, resized_images=resized_images)