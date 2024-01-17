import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import Face_rec
import time

st.set_page_config(page_title='Predictions')

st.subheader('Real-Time Attendance System')

# Retrive the data fro Radis Database
with st.spinner('Retriving Data from Redis DB ...'):
    redis_face_db = Face_rec.retrive_data(name='academy:register')
    
    st.dataframe(redis_face_db) 
    
st.success("Data sucessfully retrived from Redis")

#time
waitTime = 30
setTime = time.time()
realtimepred = Face_rec.RealTimePred() # real time prediction class
# Real Time Prediction
# Streamlit webrtc
#callback function

def video_frame_callback(frame):
        global setTime
        img = frame.to_ndarray(format="bgr24")# 3 dimension numpy array
        # operation that you can perform on the array
        pred_img =  realtimepred.face_prediction(img,redis_face_db,
                                             'facial_features',['Name','Role'],thresh=0.5)
        
        timenow = time.time()
        difftime = timenow - setTime
        if difftime>= waitTime:
              realtimepred.saveLogs_redis()
              setTime = time.time()

              print('Save Data to redis database')
        return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="raltimePrediction", video_frame_callback=video_frame_callback)