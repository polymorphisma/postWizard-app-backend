import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

# Twitter API credentials
consumer_key = os.getenv("twitter_consumer_key")
consumer_secret = os.getenv("twitter_consumer_secret")
access_token = os.getenv("twitter_access_token")
access_token_secret = os.getenv("twitter_access_token_secret")



class Twitter:
    def __init__(self) -> None:
        pass

    def auth_handler(self):
        # Initialize Tweepy API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        client = tweepy.Client(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
        )

        return api, client

    def entry_point(self, image_paths, text):

        if isinstance(image_paths, str):
            image_paths = [image_paths]

        # Check if the number of images is within Twitter's limit (max 4 images)
        if len(image_paths) > 4:
            return {"success": False, "message": "Twitter allows a maximum of 4 images per tweet."}

        tweet_text = text
        api, client = self.auth_handler()

        try:
            media_ids = []
            for image_path in image_paths:
                # Upload each image and collect the media IDs
                media = api.media_upload(filename=image_path)
                media_ids.append(media.media_id_string)

            # Create the tweet with the uploaded media
            response = client.create_tweet(
                text=tweet_text,
                media_ids=media_ids
            )

            tweet_url = f"https://twitter.com/user/status/{response.data['id']}"
            return {"success": True, "message": tweet_url}
        except Exception as e:
            print("An error occurred:", e)
            return {"success": False, "message": f"An error occurred: {e}"}
