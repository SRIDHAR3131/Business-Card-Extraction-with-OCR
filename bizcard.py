
import streamlit as st
import mysql.connector  #databse connection MySQL
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import easyocr
import cv2
import re    #text processing
import pandas as pd
import sqlalchemy as sa
import numpy as np
import time  #spinner

#page congiguration
st.set_page_config(page_title= "BizCardX",
                   page_icon= 'random',
                   layout= "wide",)
st.markdown("<h1 style='text-align: center; color: white;'>BizCardX</h1>", unsafe_allow_html=True)

#=========hide the streamlit main and footer
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

#application background
def app_bg():
    st.markdown(f""" <style>.stApp {{
                        background: url("https://cdn.wallpapersafari.com/7/90/BFUQb1.jpg");
                        background-size: cover}}
                     </style>""",unsafe_allow_html=True)
app_bg()

#============================================DATA BASE CONNECTION=======================================================
mydb = mysql.connector.connect(
  host="<your_host>",
  user="<your_user>",
  password="<your_password>",
 database="<your_database>"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE card_data ("
                 "id INT AUTO_INCREMENT PRIMARY KEY,"
                 "name VARCHAR(255),"
                 "designation VARCHAR(255),"
                 "company VARCHAR(255),"
                 "contact VARCHAR(255),"
                 "email VARCHAR(255),"
                 "website VARCHAR(255),"
                 "address VARCHAR(255),"
                 "city VARCHAR(255),"
                 "state VARCHAR(255),"
                 "pincode VARCHAR(255),"
                 "image LONGBLOB )")

navigation,text_process=st.columns([1.2,4.55])
with navigation:

    selected = option_menu('Mani Menu', ['Home',"Image to Text","Database"],
                       icons=["house",'file-earmark-font','gear'],default_index=0)#cloud-check##

with text_process:
    if selected == 'Home':
        left,right=st.columns(2)
        with right:
            url = requests.get("https://assets5.lottiefiles.com/private_files/lf30_euijmy98.json")
            url_json = dict()
            if url.status_code == 200:
                url_json = url.json()
            else:
                print("Error in URL")
            st_lottie(url_json,
                      reverse=False,
                      height=True,
                      width=True,
                      speed=3,
                      loop=True,
                      quality='high'
                      )
            st.write('### TECHNOLOGIES USED')
            st.write('##### *:red[Python]  *:red[Streamlit] *:red[EasyOCR]  *:red[OpenCV]  *:red[MySQL]')
            st.write(
                "To Learn more about easyOCR [press here](https://pypi.org/project/easyocr/) ")


            with left:
                st.markdown("### Welcome to the Business Card Application!")
                st.markdown('###### Bizcard is a Python application designed to extract information from business cards. It utilizes various technologies such as :blue[Streamlit, Streamlit_lottie, Python, EasyOCR , RegEx function, OpenCV, and MySQL] database to achieve this functionality.')
                st.write('The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')
                st.write("Click on the ****:red[Image to text]**** option to start exploring the Bizcard extraction.")

    # ===================================text extraction process====================================================

    if selected=='Image to Text':
        file,text = st.columns([3,2.5])
        with file:
            uploaded_file = st.file_uploader("Choose an image of a business card", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
#=====================original image=============================
                nparr = np.frombuffer(file_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                st.image(image,channels='BGR' ,use_column_width=True)

#===================text extraction bounding image============================
                if st.button('TEXT BOUNDING'):
                    with st.spinner('Detecting text...'):
                        time.sleep(1)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    # Apply threshold to create a binary image
                    new, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                    # Find contours in the binary image
                    contours,new = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    # Iterate through each contour and draw it with a different color
                    for i in contours:
                        # Get the bounding rectangle coordinates
                        x, y, w, h = cv2.boundingRect(i)
                        # Change the text color to green (BGR format)
                        color = (0, 255, 0)
                        # Draw a rectangle around the contour with the specified color
                        new=cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                    st.write('Compare the images')
                    st.image(new,use_column_width=True)
                    st.info('Image might be inaccurate detection of text', icon='ℹ️')
        #=======================creating tab option for view the extracted text ========================
        with text:
            left,right=st.tabs([' Undefined text extraction',' Pre-defined text extraction'])
            with left:
                st.markdown('###### *Here you can view an undefined text extraction Using :red[easyOCR]* and this is advanced tool for random text extraction.')
                st.write('Please note: It will accept all image and further update will available soon!')
                if st.button('RANDOM EXTRACTION'):
                    with st.spinner('Extracting text...'):
                        reader = easyocr.Reader(['en'])
                        results = reader.readtext(image)
                        for i in results:
                            st.write(i[1])

            with right:
                st.markdown("###### *Press below extract button to view structered text format & upload to database Using :blue[easyOCR] & :blue[python regular expression]*")
                st.write('Please note: This tab only for *:blue[business card image]* alone it will not accept random image')
                if st.button('EXTRACT & UPLOAD'):
                    with st.spinner('Extracting text...'):
                        reader=easyocr.Reader(['en'])
                        results = reader.readtext(image)
                        card_info = [i[1] for i in results]
                        demilater = ' '
                        card = demilater.join(card_info)  #convert to string
                        replacement = [
                            (";", ""),
                            (',', ''),
                            ("WWW ", "www."),
                            ("www ", "www."),
                            ('www', 'www.'),
                            ('www.', 'www'),
                            ('wwW', 'www'),
                            ('wWW', 'www'),
                            ('.com', 'com'),
                            ('com', '.com'),

                        ]
                        for old, new in replacement:
                            card = card.replace(old, new)

                        # ----------------------Phone------------------------------------
                        ph_pattern = r"\+*\d{2,3}-\d{3}-\d{4}"
                        ph = re.findall(ph_pattern, card)
                        Phone = ''
                        for num in ph:
                            Phone = Phone + ' ' + num
                            card = card.replace(num, '')

                        # ------------------Mail id--------------------------------------------
                        mail_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}\b"
                        mail = re.findall(mail_pattern, card)
                        Email_id = ''
                        for ids in mail:
                            Email_id = Email_id + ids
                            card = card.replace(ids, '')

                        # ---------------------------Website----------------------------------
                        url_pattern = r"www\.[A-Za-z0-9]+\.[A-Za-z]{2,3}"
                        url = re.findall(url_pattern, card)
                        URL = ''
                        for web in url:
                            URL = URL + web
                            card = card.replace(web, '')

                        # ------------------------pincode-------------------------------------------
                        pin_pattern = r'\d+'
                        match = re.findall(pin_pattern, card)
                        Pincode = ''
                        for code in match:
                            if len(code) == 6 or len(code) == 7:
                                Pincode = Pincode + code
                                card = card.replace(code, '')

                        # ---------------name ,designation, company name-------------------------------
                        name_pattern = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'
                        name_data = []  # empty list
                        for i in card_info:
                            if re.findall(name_pattern, i):
                                if i not in 'WWW':
                                    name_data.append(i)
                                    card = card.replace(i, '')
                        name = name_data[0]
                        designation = name_data[1]

                        if len(name_data) == 3:
                            company = name_data[2]
                        else:
                            company = name_data[2] + ' ' + name_data[3]
                        card = card.replace(name, '')
                        card = card.replace(designation, '')
                        #city,state,address
                        new = card.split()
                        if new[4] == 'St':
                            city = new[2]
                        else:
                            city = new[3]
                        # state
                        if new[4] == 'St':
                            state = new[3]
                        else:
                            state = new[4]
                        # address
                        if new[4] == 'St':
                            s = new[2]
                            s1 = new[4]
                            new[2] = s1
                            new[4] = s  # swapping the St variable
                            Address = new[0:3]
                            Address = ' '.join(Address)  # list to string
                        else:
                            Address = new[0:3]
                            Address = ' '.join(Address)  # list to string
                        st.write('')
                        st.write('###### :red[Name]         :', name)
                        st.write('###### :red[Designation]  :', designation)
                        st.write('###### :red[Company name] :', company)
                        st.write('###### :red[Contact]      :', Phone)
                        st.write('###### :red[Email id]     :', Email_id)
                        st.write('###### :red[URL]          :', URL)
                        st.write('###### :red[Address]      :', Address)
                        st.write('###### :red[City]         :', city)
                        st.write('###### :red[State]        :', state)
                        st.write('###### :red[Pincode]      :', Pincode)

                        #====================insert into database=================================
                        sql = "INSERT INTO card_data (name,designation,company,contact,email,website,address,city,state,pincode,image) " \
                                                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        val = (name,designation,company,Phone,Email_id,URL,Address,city,state,Pincode,file_bytes)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        st.success('Text extracted & successfully uploaded to database', icon="☑️")



#======================================database navigaton===============================================================
    if selected=='Database':
        with st.spinner('Connecting...'):
            time.sleep(1)
        with navigation:
            option = option_menu(None, ['Image data', "Update data", "Delete data"],
                                 icons=["image", "pencil-fill", 'exclamation-diamond'], default_index=0)
        mycursor.execute("SELECT * FROM card_data")
        myresult = mycursor.fetchall()
        #convert into dataframe using pandas
        df=pd.DataFrame(myresult,columns=['id','name','designation','company','contact','email','website','address','city','state','pincode','image'])
        df.set_index('id', drop=True, inplace=True)
        st.write(df)

        # showing the image for selected name and designation
        if option=='Image data':
            left, right = st.columns([2, 2.5])
            with left:
                mycursor.execute("SELECT name,designation FROM card_data")
                rows = mycursor.fetchall()
                row_name = [row[0] for row in rows]   #using list comprehension for loop through where the name and designation
                row_designation = [row[1] for row in rows]
                # Display the selection box
                selection_name = st.selectbox("Select name", row_name)     #selection box for avoiding the user input
                selection_designation = st.selectbox("Select designation", row_designation)
                if st.button('Show Image'):
                    with right:
                        sql = "SELECT image FROM card_data WHERE name = %s AND designation = %s"
                        mycursor.execute(sql, (selection_name, selection_designation))
                        result = mycursor.fetchone()
                            # Check if image data exists
                        if result is not None:
                                # Retrieve the image data from the result
                            image_data = result[0]
                            # Create a file-like object from the image data
                            nparr = np.frombuffer(image_data, np.uint8)
                            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                            st.image(image, channels="BGR", use_column_width=True)
                        if result is None:
                            st.error("Image not found for the given name and designation.")
        #update data in database for selected name and designation
        elif option=='Update data':
            name,new_name=st.columns(2)
            with name:
                # Get the available row IDs from the database
                mycursor.execute("SELECT name,designation FROM card_data")
                rows = mycursor.fetchall()
                row_name = [row[0] for row in rows]
                row_designation = [row[1] for row in rows]

                # Display the selection box
                selection_name = st.selectbox("Select name to update", row_name)
                selection_designation = st.selectbox("Select designation to update", row_designation)
            with new_name:
                # Get the column names from the table
                mycursor.execute("SHOW COLUMNS FROM card_data")
                columns = mycursor.fetchall()
                column_names = [i[0] for i in columns if i[0] not in ['id', 'image','name','designation']]

                # Display the selection box for column name
                selection = st.selectbox("Select specific column to update", column_names)
                new_data = st.text_input(f"Enter the new {selection}")

                # Define the SQL query to update the selected rows
                sql = f"UPDATE card_data SET {selection} = %s WHERE name = %s AND designation = %s"

                # Execute the query with the new values
                if st.button("Update"):
                    mycursor.execute(sql, (new_data, selection_name, selection_designation))
                    # Commit the changes to the database
                    mydb.commit()
                    st.success("updated successfully",icon="👆")


        #===delete data for selected name and dsignation===
        else:
            left,right=st.columns([2,2.5])
            with left:
                mycursor.execute("SELECT name,designation FROM card_data")
                rows = mycursor.fetchall()    #collecting all the data
                row_name = [row[0] for row in rows]
                row_designation = [row[1] for row in rows]
            # Display the selection box
                selection_name = st.selectbox("Select name to delete", row_name)
            with right:
                selection_designation = st.selectbox("Select designation to delete", row_designation)
            with left:
                if st.button('DELETE'):
                    sql = "DELETE FROM card_data WHERE name = %s AND designation = %s"
                # Execute the query with the values as a tuple
                    mycursor.execute(sql, (selection_name, selection_designation))
                    mydb.commit()
                    st.success('Deleted successfully',icon='✅')

            st.write('')
            st.markdown('### Result')
            st.write('To provide a user-friendly interface, Bizcard utilizes Streamlit, a Python framework for building interactive web applications. Users can upload business card images through the Streamlit interface, and the application will process the images, extract the information, and display it on the screen. The application also provides options to view, update, and analyze the extracted data directly from the database.')
            st.info('The detected text on image might be inaccurate. Still application under development fixing bugs.There is lot to explore on easyOCR and openCV',icon='ℹ️')

