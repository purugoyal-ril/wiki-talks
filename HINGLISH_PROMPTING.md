# Hinglish Prompting Strategy for wiki-talks

## How We Achieve Natural Hinglish Conversations

Our LLM prompting strategy for wiki-talks focuses on creating authentic Hinglish (Hindi-English code-switching) through carefully crafted system prompts and V3 audio tag integration. The system prompt explicitly instructs the model to use natural filler words like "achcha", "hain na", "yaar", and "waah" while maintaining conversational flow. We leverage ElevenLabs V3's audio tags (`[laughs]`, `[sighs]`, `[whispers]`) to add emotional depth, and use punctuation (`...` for hesitation) and CAPS (for emphasis like "Arre BAS!") to guide natural pacing. Interruptions are handled by ending one speaker's line with `-` and starting the next with `[fast]`, creating realistic conversational overlaps. By avoiding SSML and relying on V3's native audio processing, we ensure the output sounds natural and non-robotic, with the API automatically handling conversation flow and timing.

