import cv2
import numpy as np
import base64
import openai
import tempfile
import os
from google.cloud import vision_v1
import logging
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import gc
import io

class LivenessDetector:
    def __init__(self, client, openai_api_key):
        self.google_client = client
        openai.api_key = openai_api_key

    def extract_frames(self, video_path):
        """Extract 3 key frames from video: start, middle, and end."""
        frames = []
        try:
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Get start, middle, and end frames
            frame_indices = [0, total_frames//2, total_frames-1]
            
            for frame_idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                if ret:
                    # Resize frame to reduce memory usage and processing time
                    frame = cv2.resize(frame, (640, 480))
                    frames.append(frame)
                    
        finally:
            cap.release()
            gc.collect()
        return frames

    def image_to_base64(self, image):
        """Convert image to base64 string with compression."""
        try:
            # Compress image before encoding
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
            _, buffer = cv2.imencode('.jpg', image, encode_param)
            return base64.b64encode(buffer).decode('utf-8')
        finally:
            del buffer
            gc.collect()

    def analyze_frame_openai(self, frame):
        """Analyze frame using OpenAI's GPT-4 Vision."""
        try:
            base64_image = self.image_to_base64(frame)
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Is this a live person or screen recording? Look for moiré patterns, pixelation, screen bezels. JSON response only with: is_live(True/False), confidence(0-100), gaze_direction."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=50  # Reduced tokens for faster response
            )
            
            return response.choices[0].message['content']
        except Exception as e:
            logging.error(f"Error analyzing frame with OpenAI: {str(e)}")
            return None
        finally:
            del base64_image
            gc.collect()

    def analyze_final_results(self, frame_results):
        """Quick analysis of frame results."""
        try:
            analysis_prompt = f"""Analyze these video frame results for liveness detection:
            {frame_results}
            Return only dictionary, no other text like json, python, or anything else, only dictionary in your response with is_person_live value to be a boolean(True/False):
            {{"is_person_live": True/False, "confidence": 0-100}}"""

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=50
            )
            
            return response.choices[0].message['content']
        except Exception as e:
            logging.error(f"Error in final OpenAI analysis: {str(e)}")
            return None
        finally:
            gc.collect()

    def calculate_landmarks_movement(self, current_landmarks, previous_landmarks):
        try:
            return sum(
                abs(cur_point.position.x - prev_point.position.x) +
                abs(cur_point.position.y - prev_point.position.y)
                for cur_point, prev_point in zip(current_landmarks, previous_landmarks)
            )
        finally:
            gc.collect()

    def calculate_face_movement(self, current_face, previous_face):
        try:
            return abs(current_face[0].x - previous_face[0].x) + abs(current_face[0].y - previous_face[0].y)
        finally:
            gc.collect()

    def calculate_liveness_result(self, eyebrow_movement, nose_movement, lip_movement, face_movement):
        eyebrow_movement_threshold = 15.0
        nose_movement_threshold = 15.0
        lip_movement_threshold = 15.0
        face_movement_threshold = 10.0
        
        return any([
            eyebrow_movement > eyebrow_movement_threshold,
            nose_movement > nose_movement_threshold,
            lip_movement > lip_movement_threshold,
            face_movement > face_movement_threshold
        ])

    def check_google_liveness(self, video_path):
        """Optimized Google Vision API check."""
        try:
            frames = self.extract_frames(video_path)
            if not frames:
                return 'consider'

            previous_landmarks = None
            previous_face = None
            liveness_result_list = []

            # Process frames in parallel
            def process_frame(frame):
                _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
                image = vision_v1.Image(content=buffer.tobytes())
                response = self.google_client.face_detection(image=image)
                return response.face_annotations

            with ThreadPoolExecutor(max_workers=2) as executor:
                face_results = list(executor.map(process_frame, frames))

            for faces in face_results:
                if not faces:
                    continue

                largest_face = max(faces, key=lambda face: 
                    abs((face.bounding_poly.vertices[2].x - face.bounding_poly.vertices[0].x) * 
                        (face.bounding_poly.vertices[2].y - face.bounding_poly.vertices[0].y)))

                current_landmarks = largest_face.landmarks
                current_face = largest_face.bounding_poly.vertices

                if previous_landmarks and previous_face:
                    movements = [
                        self.calculate_landmarks_movement(current_landmarks[:10], previous_landmarks[:10]),  # eyebrows
                        self.calculate_landmarks_movement(current_landmarks[10:20], previous_landmarks[10:20]),  # nose
                        self.calculate_landmarks_movement(current_landmarks[20:28], previous_landmarks[20:28]),  # lips
                        self.calculate_face_movement(current_face, previous_face)  # face
                    ]
                    
                    thresholds = [15.0, 15.0, 15.0, 10.0]  # eyebrow, nose, lip, face thresholds
                    liveness_result = any(m > t for m, t in zip(movements, thresholds))
                    liveness_result_list.append(liveness_result)

                previous_landmarks = current_landmarks
                previous_face = current_face

            return 'clear' if any(liveness_result_list) else 'consider'

        except Exception as e:
            logging.error(f"Error in Google Vision check: {str(e)}")
            return 'consider'
        finally:
            gc.collect()

    def check_openai_liveness(self, video_path):
        """Optimized OpenAI check."""
        try:
            frames = self.extract_frames(video_path)
            if not frames:
                return 'consider'

            # Process frames in parallel
            with ThreadPoolExecutor(max_workers=2) as executor:
                frame_results = list(executor.map(self.analyze_frame_openai, frames))
                frame_results = [r for r in frame_results if r]

            if not frame_results:
                return 'consider'

            final_result = self.analyze_final_results(frame_results)
            print(f'\nFinal AI Analysis: {final_result}\n')
            if not final_result:
                return 'consider'

            try:
                final_analysis = json.loads(final_result)  # Using eval instead of json.loads for speed
                if final_analysis.get('is_person_live', False) and final_analysis.get('confidence', 0) >= 60:
                    return 'clear'
            except:
                pass

            return 'consider'
        finally:
            gc.collect()

    def check_liveness(self, video_bytes):
        """Optimized parallel liveness check."""
        temp_video_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        temp_video_file_path = temp_video_file.name
        
        try:
            # Write video bytes efficiently
            with open(temp_video_file_path, 'wb') as f:
                f.write(video_bytes)
            del video_bytes
            gc.collect()

            # Run checks in parallel with timeout
            with ThreadPoolExecutor(max_workers=2) as executor:
                future_google = executor.submit(self.check_google_liveness, temp_video_file_path)
                future_openai = executor.submit(self.check_openai_liveness, temp_video_file_path)

                # Wait for both results with timeout
                google_result = future_google.result(timeout=8)  # 8 second timeout
                openai_result = future_openai.result(timeout=8)  # 8 second timeout

                print(f'\nMotion tracking Result: {google_result}\nAI Analysis Result: {openai_result}\n')

            return 'clear' if google_result == 'clear' and openai_result == 'clear' else 'consider'

        except Exception as e:
            logging.error(f"Error in liveness check: {str(e)}")
            return 'consider'
        finally:
            if os.path.exists(temp_video_file_path):
                os.remove(temp_video_file_path)
            gc.collect() 