key="AIzaSyAjJltVZhW9Y1Aro7yj1X3CkGGcvi3rZ2o"

import google.generativeai as genai

genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("hồ chí minh sinh ngày mấy? ")
print(response.text)