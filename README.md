# Bizcard Card Extracting with OCR
Bizcard Extraction is a Python application built with Streamlit, EasyOCR, OpenCV, regex function, and MySQL database. It allows users to extract information from business cards and store it in a MySQL database for further analysis.
# Homepage
![Home page](https://github.com/SRIDHAR3131/Business-Card-Extracting-with-OCR/assets/68391060/17b3a840-d87a-4b6e-b966-98585321ba2f)
# Undefined text extraction
![Screenshot 2023-05-16 190907](https://github.com/SRIDHAR3131/Business-Card-Extracting-with-OCR/assets/68391060/e6253361-6f0d-4ad6-b2c5-d40e43405f17)
# Text extraction
![Screenshot 2023-05-16 185523](https://github.com/SRIDHAR3131/Business-Card-Extracting-with-OCR/assets/68391060/4e605821-30be-4978-a69d-fe2dc7318446)
# Bounding Text
![Screenshot 2023-05-16 222248](https://github.com/SRIDHAR3131/Business-Card-Extracting-with-OCR/assets/68391060/909d344a-a13d-4320-a5ac-24676eae2c98)
# Database
![Screenshot 2023-05-19 153754](https://github.com/SRIDHAR3131/Business-Card-Extracting-with-OCR/assets/68391060/cd36d280-edba-40b1-afb0-4e8b1ddafca5)
# Features
- Extracts text information from business card images using EasyOCR.
- Utilizes OpenCV for image preprocessing, such as resizing, cropping, and enhancing.
- Uses regular expressions (RegEx) to parse and extract specific fields like name, designation, company, contact details, etc.
- Stores the extracted information in a MySQL database for easy retrieval and analysis.
- Provides a user-friendly interface built with Streamlit to upload images, extract information, and view/update the database.
# Usage
1.Run the Streamlit application:

    streamlit run bizcard.py
2.Access the application in your browser at http://localhost:8501.

3.Upload a business card image to extract the information.
 
4.The application will preprocess the image using OpenCV by resizing, cropping, and enhancing it.

5.The processed image will be passed to EasyOCR for text extraction. Install thisfor latest development of easyOCR
    
    pip install git+https://github.com/JaidedAI/EasyOCR.git

6.The extracted information will be displayed on the screen, and it will be stored in the MySQL database.

7.Use the provided options to view, update, or analyze the extracted data in the database.

# Technologies Used
- Streamlit
- Streamlit_lottie
- Python
- RegEx 
- EasyOCR
- OpenCV
- MySQL

# Acknowledgments
#### Streamlit - For building interactive web applications with ease.
#### EasyOCR - For text extraction from images.
#### OpenCV - For image preprocessing and manipulation.
#### MySQL - For the database management system.
