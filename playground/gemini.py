import os
from dotenv import load_dotenv

import pathlib
import textwrap

import google.generativeai as genai


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL")
print(GOOGLE_MODEL)
print(GOOGLE_API_KEY)
print('--------------------------------------------')
genai.configure(api_key=GOOGLE_API_KEY, transport='rest')
print('--------------------------------------------')

# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)

model = genai.GenerativeModel(GOOGLE_MODEL)
print('--------------------------------------------')

prompt = """You are an SEO specialist for Adex International, a Nepal-based cloud solution provider. As an SEO, your job is to post on different social handles for Adex, with a specialization in Twitter. You need to upload pictures and generate posts based on the context of the picture provided.
                                                context: fun, hiking, place: nagarkot, refreshing

                                                absolute rule:
                                                1. Text must be under 280 characters, including hashtags, spaces, and new lines.
                                                2. generate text should absolutly have less tehn 280 characters including hastags, spaces, new lines and all.
                                                3. Provide only content without any unnccessary text and without any url(exception for url if its in the context)
                                                4. Just the text
                                                5. Provide content in such way that i can directly copy paste and good to go, don't provide any options. just the caption. without any unnccessary text and without any url(exception for url if its in the context)

                                                Guidelines for Twitter posts:
                                                Use relevant hashtags for visibility.
                                                Post at optimal times for your audience.
                                                Engage with your followers.
                                                Include visuals in your posts.
                                                Keep messages clear and concise.
                                                Use polls to boost engagement.
                                                Promote your tweets.
                                                Track performance and adjust accordingly.
                                                Best practices:

                                                Be concise (tweets have a maximum length of 280 characters).
                                                Stay on top of trending topics and events.
                                                Utilize Twitter's features for displaying information and correspondence.

                                                Just provide content without any unnecesary text without any urls
"""
response = model.generate_content(prompt)
print('--------------------------------------------')

print(response)
