from paddleocr import PaddleOCR
from PIL import Image
import os
import numpy as np
import pandas as pd
import uuid
import xml.etree.ElementTree as ET

def generate_unique_filename():
    unique_id = str(uuid.uuid4())
    return f"image_{unique_id}.jpg"

def ImgtoOcr(folder_path):
    ocr = PaddleOCR(lang='en')

    data = []

    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path).convert("RGB")
        image_name = os.path.basename(image_path)

        # Read XML file and get bounding box coordinates
        xml_file_path = os.path.join(folder_path, filename.replace(".png", ".xml"))
        tree = ET.parse("./xml/frame.xml")
        root = tree.getroot()
        xmin = int(root.find(".//xmin").text)
        ymin = int(root.find(".//ymin").text)
        xmax = int(root.find(".//xmax").text)
        ymax = int(root.find(".//ymax").text)

        # Crop the image based on bounding box coordinates
        cropped_image = image.crop((xmin, ymin, xmax, ymax))

        result = ocr.ocr(np.array(cropped_image))

        text_data = ""
        for line in result[0]:
            text = line[1][0]
            coordinates = line[0]
            text_data += f"{text} (Coordinates: {coordinates}), "

        data.append({'Image Name': image_name, 'Extracted Text': text_data})

    df = pd.DataFrame(data)
    excel_file_path = 'TextDoc/ocr_results_with_coordinates.xlsx'
    df.to_excel(excel_file_path, index=False)

    print(f"OCR results with coordinates saved to Excel file: {excel_file_path}")

folder_path = 'Images'
ImgtoOcr(folder_path)