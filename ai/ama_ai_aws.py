import boto3
import os
from dotenv import load_dotenv
from langchain.llms.bedrock import Bedrock
import json

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
AWS_REGION = os.getenv("AWS_REGION")
LLM_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"
# LLM_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"


class BedrockLLM:
    @staticmethod
    def get_bedrock_client():
        """
            This function will return the bedrock client.
        """
        bedrock_client = boto3.client(
            'bedrock',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN
        )

        return bedrock_client

    @staticmethod
    def get_bedrock_runtime_client():
        """
        This function will return the bedrock runtime client.
        """
        bedrock_runtime_client = boto3.client(
            'bedrock-runtime',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN
        )
        return bedrock_runtime_client

    @staticmethod
    def get_bedrock_llm(
            model_id: str = LLM_MODEL,
            max_tokens_to_sample: int = 300,
            temperature: float = 0.0,
            top_k: int = 250,
            top_p: int = 1
            ):
        """
        This function will take multiple arguments and return llm

        input args: model_id, maximum token to sample, temprature, top k and top p value.

        output: return bedrock llm
        """
        params = {
            "max_tokens_to_sample": max_tokens_to_sample,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p
        }

        bedrock_llm = Bedrock(
            model_id=model_id,
            client=BedrockLLM.get_bedrock_runtime_client(),
            model_kwargs=params,
        )

        return bedrock_llm


bedrock_client = BedrockLLM.get_bedrock_client()

promts = {
        "twitter": """You are an SEO specialist for Adex International, a Nepal-based cloud solution provider. As an SEO, your job is to post on different social handles for Adex, with a specialization in Twitter. You need to upload pictures and generate posts based on the context of the picture provided.
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

        "linkedin": """You are an SEO specialist for Adex International, a Nepal-based cloud solution provider. As an SEO, your job is to post on different social handles for Adex, with a specialization in LINKEDIN. You need to upload pictures and generate posts based on the context of the picture provided. you will be posting it so don't include any thing just porivde content only.
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

    bedrock_runtime = BedrockLLM.get_bedrock_runtime_client()

    body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": promts[method].format(context)
                            } 
                        ]
                    }
                ]
            }
        )
    modelId = LLM_MODEL
    accept = 'application/json'
    contentType = 'application/json'
    response = bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    answer = response_body["content"][0]["text"]

    return answer


if __name__ == "__main__":
    value = main('linkedin', 'hiking, fun, sports, place: nagarkot')
