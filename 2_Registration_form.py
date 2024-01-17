import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av
from Home import Face_rec

st.set_page_config(page_title='Registration Form',layout='wide')

st.subheader('Registration Form')

## init registration form
registration_form = Face_rec.RegistrationForm()


# collect person name and role
# from
person_name = st.text_input(label='Name',placeholder='First & Last Name')
role = st.selectbox(label='select your Role',options=('Students',
                                                      'Teacher'))

#collect facial embedding
def video_callback_func(frame):
    img = frame.to_ndarray(format='bgr24') 
    reg_img, embedding = registration_form.get_embedding(img)
    # two step process
    #1st step save data in local computer txt
    if embedding is not None:
        with open('face_embedding.txt',mode='ab') as f:
            np.savetxt(f,embedding)



    return av.VideoFrame.from_ndarray(reg_img,format='bgr24')

webrtc_streamer(key='registrtion',video_frame_callback=video_callback_func)

#save the data in radis


if st.button('Submit'):
    return_val = registration_form.save_data_in_redis_db(person_name,role)
    if return_val == True:
        st.success("{person_name} registered sucessfully")
    elif return_val == 'name_false':
        st.error('Please enter name: Name cannot be empty or spaces')
    elif return_val == 'file_face':
        st.error('face_embedding.txt is not found. Please refresh the page and exicute again')