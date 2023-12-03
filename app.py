# Python In-built packages
from pathlib import Path


#https://www.youtube.com/watch?v=UaHRkS7d8Ks
#https://www.youtube.com/watch?v=LmNMLhMRZKE&t=6s
# External packages
import streamlit as st
import PIL 
import os
import io
# Local Modules
import settings
import helper
from github import Github

#g=Github("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")
#g = Github("omar.19761116@gmail.com","ocima@2021")
g=Github(st.secrets["db_username"])
repo = g.get_repo("omar-Fouad/Laitier")
message = "Commit Message"
branch = "main"
def push_image(path,commit_message,content,branch,update=False):
    if update:
        contents = repo.get_contents(path, ref=branch.name)
        repo.update_file(contents.path, commit_message, content, branch, sha=contents.sha)
    else:
        repo.create_file(path, commit_message, content, branch)
# Setting page layout
st.set_page_config(
    page_title="Laitier_detection",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
#st.title("Object Detection using YOLOv8")

# Sidebar
#st.sidebar.header("ML Model Config")

# Model Options
model_type = 'Detection' #st.sidebar.radio("Select Task", ['Detection', 'Segmentation'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100
col11, col12 = st.sidebar.columns(2)#[1,1])

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

# st.sidebar.header("Image/Video Config")
# source_radio = st.sidebar.radio(
    # "Select Source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if settings.IMAGE == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                #filename = default_image_path.split("/")[len(default_image_path.split("/"))-1]
                #filename=os.path.splitext(default_image_path)[-1] == '.jpg'
                #print(Path(default_image_path).stem)
                #print(filename)
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                #print(boxes)
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")
            with col11:        
              if st.button('save good'):
 
                temp=source_img.name
                
                print(temp)#(Path(filename).stem)
                filename='datasets/good/'+temp
                
                #newsize = (400, 300)
                
                
                #uploaded_image = uploaded_image.resize(newsize)
                uploaded_image.save(filename)
                img_byte_arr = io.BytesIO()
                uploaded_image.save(img_byte_arr, format='png')
                img_byte_arr = img_byte_arr.getvalue()
                temp1="image: " +temp+ "is uploaded to good folder"
                push_image(filename,temp1,img_byte_arr,branch='main',update=False)  
                try:
                    temp1="image: " +temp+ "is uploaded to good folder" 
                    st.write(temp1)
                except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")
            with col12:        
              if st.button('save bad'):
                temp=source_img.name
                print(temp)#(Path(filename).stem)
                filename='datasets/bad/'+temp
                uploaded_image.save(filename)
                img_byte_arr = io.BytesIO()
                uploaded_image.save(img_byte_arr, format='png')
                img_byte_arr = img_byte_arr.getvalue()
                temp1="image: " +temp+ "is uploaded to bad folder"
                push_image(filename,temp1,img_byte_arr,branch='main',update=False)  
                
                try:
                    temp1="image: " +temp+ "is uploaded to bad folder" 
                    st.write(temp1)
                except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")                    
# elif source_radio == settings.VIDEO:
    # helper.play_stored_video(confidence, model)

# elif source_radio == settings.WEBCAM:
    # helper.play_webcam(confidence, model)

# elif source_radio == settings.RTSP:
    # helper.play_rtsp_stream(confidence, model)

# elif source_radio == settings.YOUTUBE:
    # helper.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type!")
