
from app.Social_media_handler.twitter import Twitter
from app.Social_media_handler.linkedin import Linkedin
# from app.AI.ama_ai_google import main as ai_text_generator
from app.AI.ama_ai_aws import main as ai_text_generator

twitter_obj = Twitter()
linkedin_obj = Linkedin()


class Sm_handler:
    def __init__(self) -> None:
        self.sm = {
            "twitter": twitter_obj.entry_point,
            "linkedin": linkedin_obj.entry_point
        }

    def entry_point(self, method: str | list, image_path: list, context: str):
        print('hi')
        if isinstance(method, str):
            method = [method]
        print('hi')

        return_value = []
        print('hi')

        for meth in method:
            while True:
                text = ai_text_generator(meth, context)
                print(meth, text)
                if meth != 'twitter':
                    break

                if len(text) < 280:
                    break
            print('hi')

            response = self.sm[meth](image_path, text)
            response['method'] = meth
            response['generated_text'] = text
            return_value.append(response)
        print('hi')

        return return_value


if __name__ == "__main__":
    sm_obj = Sm_handler()
    value = sm_obj.entry_point(['twitter', 'linkedin'], [], "aws udpate, new feature url: adex.ltd")
    print(value)
