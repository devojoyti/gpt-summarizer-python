import tiktoken
import openai
from .gptmodels import GPTModel


class Summarizer:
    TOKEN_LIMIT_TEXT_DAVINCI_003 = 4085
    TOKEN_LIMIT_GPT_35_TURBO = 4085
    TOKEN_LIMIT = 0
    API_KEY = ""

    def __init__(self, key) -> None:
        self.API_KEY = key

    def getSummary(
        self,
        text,
        engine=None,
        temperature=None,
        max_tokens=None,
        top_p=None,
        frequency_penalty=None,
        presence_penalty=None,
    ):
        openai.api_key = self.API_KEY

        # Setting default values if not supplied
        if temperature is None:
            temperature = 0.3
        if max_tokens is None:
            max_tokens = 600
        if top_p is None:
            top_p = 1
        if frequency_penalty is None:
            frequency_penalty = 0
        if presence_penalty is None:
            presence_penalty = 1

        # Will be used to determine token limit
        encoding = None

        # Setting value for engine & token limit
        match engine:
            case "text-davinci-003":
                engine = GPTModel.text_davinci_003
                self.TOKEN_LIMIT = self.TOKEN_LIMIT_TEXT_DAVINCI_003
                encoding = tiktoken.encoding_for_model("text-davinci-003")

            case "gpt-3.5-turbo":
                engine = GPTModel.gpt_35_turbo
                self.TOKEN_LIMIT = self.TOKEN_LIMIT_GPT_35_TURBO
                encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            case _:
                # Default value for now
                engine = GPTModel.text_davinci_003
                self.TOKEN_LIMIT = self.TOKEN_LIMIT_TEXT_DAVINCI_003
                encoding = tiktoken.encoding_for_model("text-davinci-003")

        # Get the length of the current text token
        tokens = encoding.encode(text)
        number_of_tokens = len(tokens)

        output_token_requested = max(max_tokens, number_of_tokens // 4)

        # If the current text input is lesser than the token limit of the model, go forward with summarization
        if number_of_tokens + output_token_requested < self.TOKEN_LIMIT:
            summary = self.__getGPTSummary(
                text,
                engine,
                temperature,
                output_token_requested,
                top_p,
                frequency_penalty,
                presence_penalty,
            )

            return summary

        else:
            # We need to shorten the text, while preserving all the details.
            max_token_batch = 3 * (self.TOKEN_LIMIT // 4)
            summary = ""
            ptr = 0
            done = False
            curr_chunk = 0
            while not done:
                # If we have reached at token end, finish after this operation
                if ptr + max_token_batch >= len(tokens):
                    done = True
                    curr_chunk = len(tokens)

                else:
                    curr_chunk = ptr + max_token_batch

                curr_tokens = tokens[ptr:curr_chunk]
                # Keeping a buffer of 100 tokens so that no loss of info takes place
                ptr = curr_chunk - 100

                # Transfer back to normal text
                curr_text = encoding.decode(curr_tokens)

                interim_summary = self.__getGPTSummary(
                    curr_text,
                    engine,
                    temperature,
                    output_token_requested,
                    top_p,
                    frequency_penalty,
                    presence_penalty,
                )
                summary += " " + interim_summary

            return summary

    def __getGPTSummary(
        self,
        text,
        engine,
        temperature,
        max_tokens,
        top_p,
        frequency_penalty,
        presence_penalty,
    ):
        if engine == GPTModel.text_davinci_003:
            return self.__getDaVinci003Summary(
                text,
                temperature,
                max_tokens,
                top_p,
                frequency_penalty,
                presence_penalty,
            )

        elif engine == GPTModel.gpt_35_turbo:
            return self.__getGPT35TurboSummary(
                text,
                temperature,
                max_tokens,
                top_p,
                frequency_penalty,
                presence_penalty,
            )

    def __getDaVinci003Summary(
        self,
        text,
        temperature,
        max_tokens,
        top_p,
        frequency_penalty,
        presence_penalty,
    ):
        summary_prompt = "Summarize the following text: "

        text = summary_prompt + text

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )

        return response["choices"][0]["text"].strip()

    def __getGPT35TurboSummary(
        self,
        text,
        temperature,
        max_tokens,
        top_p,
        frequency_penalty,
        presence_penalty,
    ):
        summary_prompt = "Summarize the following text: "

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": summary_prompt},
                {"role": "user", "content": text},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )

        return response["choices"][0]["message"]["content"].strip()
