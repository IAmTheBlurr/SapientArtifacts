# youtube-to-openai
Utility pet project that allows me to expand and reason about a target YouTube videos' content subject by way of OpenAI API capabilities

## Background
I will often be watching some YouTube video with a complex and interesting subject which I would like to reason about a lot further beyond the content.

When this happens, I think to myself, "Man! It would be great to be able to just give ChatGPT the transcript of this video to be able to explore the content more deeply..."

And here we are!

## How it works
There is a `main.py` file where I tend to make top level changes when I want to use the modules

The `modules` directory is a Python package where classes in each module are imported in the package `__init__.py` file

It goes something like this

```python
""" Example use of the TargetVideo class """
from modules import TargetVideo

# Create a TargetVideo object with the video ID and the name of the video (arbitrary naming)
# Note: You can find the video ID in the URL of the video after `?v=`
target = TargetVideo('piJkuavhV50', 'four_d_geometry_sadness')

# Download the captions of the video
target.download_captions()

# Download the video itself
target.download_video()
```

### Notes:
- The current working directory is the download location for both the video and caption files
- The video is downloaded in the highest quality available
- The caption file is downloaded in the `.vtt` format ("WebVTT" is the human name for it)

## Future Work
### OpenAI Integration
Next thing I'm sure I'll do to make my life easier is adding OpenAI API wrapper helper functionality so the downloaded VTT content can be fed into the API for further exploration.

I expect that I'll simplify the choices to an explicitly defined set of common requests for different types of reasoning output from the LLM.

**Example:**
- "Summarize the subject content of the video by determining all topics and describing them in a few paragraphs each"
- "Generate a list of questions that could be asked about the content of the video"
- etc.

### Maximally Instructive Save State Prompt for LLMs
I know of a way to generate what is effectively a subject-matter based conversational "save state" which is structured to be maximally instructive to other LLM conversations/contexts.

The structure of one of these "save states" acts as a kind of meta-scaffolding of subject-matter for topics in the content.

I've found that providing one of these "save states" to a new LLM context/conversation is more effective at getting the LLM to "restore a comprehension space" based on the subject-matter of the content than providing the entire raw transcription, or providing a summary of the topic.

I'll probably add this as a feature to the OpenAI integration, a way of quickly generating the "save state" prompt you can give to ChatGPT manually.

### Iterative Development
For now, just being able to download the captions as a .vtt file is enough to make this little project useful to me.

No idea where this project will go, but it's nice to have it for myself at least.

If you find this repo and find it useful to you and want to request some features (or just say Hi), find me on X ([@WzrdOfGwendolyn](https://x.com/WzrdOfGwendolyn)).

### More to Come
I'm sure I'll think of more things to add as I go along. I'll update this README as I do.

## Find Me
- X: [@WzrdOfGwendolyn](https://x.com/WzrdOfGwendolyn)

