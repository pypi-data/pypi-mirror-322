# doprompt-py
DoPrompt is a python package to parse and execute dotprompt files - a [filetype created by Google](https://firebase.google.com/docs/genkit/dotprompt) to store prompts outside of the code itself.

This library exists to create vendor independent tooling for a better way to store and interact with prompts. 

Please check out the visual studio code extension to easily play around with your prompts without ripping them out of your code.

## Example

1. Install doprompt
```bash
pip install doprompt
```

2. Create a `chatbot.prompt` file
```
---
model: openai/gpt-4o
config:
  temperature: 0.9
input:
  schema:
    userQuestion: string
---
{{role "system"}}
You are a helpful AI assistant that really loves to talk about food. Try to work
food items into all of your conversations.
{{role "user"}}
{{userQuestion}}
```

3. Execute the prompt
You can use our completion API to automatically dispatch the prompt to the right vendor library and pass in the parameters you configured:

```python
import doprompt

prompt = DoPrompt("./chatbot.prompt")
print(prompt.complete({'userQuestion': 'Which way is the library?'})
```

Alternatively if you need custom APIs, settings or vendors you can also manually pass down any parameters.
The following snippet results in equivalent behaviour

```python
import doprompt
from openai import OpenAI

prompt = DoPrompt("./chatbot.prompt")

openai = OpenAI()

messages = prompt.get_messages(values={
    'userQuestion': 'What is the capital of France?',
})


client = OpenAI()
completion = client.chat.completions.create(
    messages=prompt.get_messages(vals),
    model=prompt.model_name,
    temperature=prompt.get_config('temperature'),
)
print(completion.choices[0].message.content)
```

## Backgorund
Hardcoding prompt is a very constraining solution, since prompts often need very interactive development which is hard once they're embedded in code. 
The alterantive would be to use a prompt management platform, which create an additional dependency and point of failure, whilst siloing away your prompts from the parts they are actually very integrated into.

Separating them into their own file keeps them close to the code while allowing additional tooling to help you interactively develop them.

## Supported features
- [x] handlebars templating
- [x] config settings
- [x] roles
- [x] schema validation
- [ ] media support
- [ ] alternative templating languages

