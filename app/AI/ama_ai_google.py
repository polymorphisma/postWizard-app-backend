import os
from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL")


promts = {
        "twitter": """You are an SEO specialist for Adex International, a Nepal-based cloud solution provider. As an SEO, your job is to post on different social handles for Adex, with a specialization in Twitter. You need to generate a caption using following context and rules.
                                                context: {}

                                                absolute rule:
                                                Text must be under 280 characters, including hashtags, spaces, and new lines.
                                                generate text should absolutly have less tehn 280 characters including hastags, spaces, new lines and all.
                                                Provide only content without any unnccessary text and without any url(exception for url if its in the context)

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

                                                Just provide content without any unnecesary text without any urls""",

        "linkedin": """You are an SEO specialist for Adex International, a Nepal-based cloud solution provider. As an SEO, your job is to post on different social handles for Adex, with a specialization in LINKEDIN. You need to generate a caption using following context and rules. you will be posting it so don't include any thing just porivde content only.
                                                context: {}

                                                absolute rule:
                                                Provide only content which can be directly posted to linkedin without editing
                                                without any unnccessary text and without any url(exception for url if its in the context)


                                                Guidelines for linkedin posts:
                                                Use relevant hashtags for visibility.
                                                Start with a compelling top line header.
                                                Use Emojis for Bullet Points
                                                Replace traditional bullet points with emojis for visual appeal.
                                                Structure the post with bullet points or numbered lists to break up text and make it easily digestible.
                                                Keep in mind the 1300-character limit; posts longer than a certain length will include a 'see more' button.
                                                Post without a link first, then edit to add the link, or include the link in the first comment to maintain engagement.
                                                Use external links sparingly to ensure your posts maintain reach and engagement.
                                                Focus on one specific topic per post to keep content concise and engaging.
                                                Track how your posts perform and adjust your strategy accordingly.
                                                Encourage interaction by asking questions or prompting comments.
                                                Ensure all posts are professional and align with Adex International's brand voice.
                                                Just provide content without any unnecesary text without any urls"""
}


def main(method, context):
    print(method, context)
    print("---------------------------------------------")
    genai.configure(api_key=GOOGLE_API_KEY, transport='rest')
    model = genai.GenerativeModel(GOOGLE_MODEL)
    text = promts[method].format(context)
    print(text)
    print('-----------------------------------------------------------')
    response = model.generate_content(text)
    return response.text


if __name__ == "__main__":
    value = main('linkedin', 'hiking, fun, sports, place: nagarkot')
    print(value)
