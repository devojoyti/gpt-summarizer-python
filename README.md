# GPT-Summarizer
### Lightweight library to summarize long texts using GPT models

GPT-Summarizer provides the capability of summarizing very large text corpus exceeding the token limit of normal GPT models. Of course, you can use it to summarize shorter texts as well. 

## Installation
- Clone this repo
- `python setup.py install` inside the cloned folder
- Done !

## Usage
```sh
>>> from gptsummarizer import summarizer
>>> generator = summarizer.Summarizer(key="put_your_openai_key_here")
>>> summary = generator.getSummary(text="Hello! How are you?")
>>> summary
Two people are exchanging greetings and inquiring about each others wellbeing.
```

## 💪 Power Usage

Setting the GPT model to use for summarization. Currently supports two GPT engines, `text-davinci-003` and `gpt-3.5-turbo`. If no engine is specified, it defaults to `text-davinci-003`
```sh
>>> summary = generator.getSummary(text="Hello! How are you?", engine="gpt-3.5-turbo")
```

Setting other model parameters like `temperature`, `max_tokens` are optional, and can be done similarly. 
```sh
>>> generator.getSummary(text="Hello! How are you?", 
                         engine="text-davinci-003", 
                         temperature=0.3, 
                         max_tokens=600, 
                         top_p=1, 
                         frequency_penalty=0, 
                         presence_penalty=1)
```

For more information on how to fine-tune these parameters, follow [OpenAI documentation](https://platform.openai.com/docs/api-reference/completions/create).

## License

MIT
