import sys
import openai
from openai import OpenAI
import settings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

import logging

logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY
model_name = settings.SECONDARY_GPT_MODEL



class SpeechToText:
    def __init__(self):
        self.client = OpenAI(api_key = settings.OPENAI_API_KEY)
        
        self._llm = ChatOpenAI(temperature=0.0, model_name=model_name)
        
        
        self.refine_trancribed_chain = self._get_refined_trancribed_chain()
        

    def convert_audio_to_text(self, audio_file_path: str) -> str:
        """
        Convert an MP3 audio file (given by path) to text using OpenAI's Whisper model.

        :param audio_file_path: A string containing the path to the audio file.
        :return: The transcribed text from the audio.
        """
        # Call the OpenAI API to get the translation
        with open(audio_file_path, "rb") as audio_file:
            translation = self.client.audio.translations.create(
                model=settings.TRANSCRIPTION_MODEL_NAME,
                file=audio_file
            )
        
        return translation.text
    
    
    def _get_refine_transcribed_prompt(self):
        """
        Get the prompt for refining the transcribed text.
        """
        
        
        refine_query_prompt_template = """You are a helpful assistant who will help in preprocessing the user's transcribed text related to taxation and corporate compliance. Your task is to process the text by following these guidelines:

1. **Remove Filler Words**: Eliminate words and phrases like "umm", "uhh", "like", "you know", and other similar expressions that do not add value to the content.
2. **Correct Spelling and Grammar**: Ensure that all words are spelled correctly and that the text follows proper grammatical rules without changing the original meaning or adding new information.
3. **Maintain Context**: Keep the context of the conversation intact while preprocessing the text, especially in relation to taxation, corporate tax laws, and compliance matters.
4. **Output Format**: Present the preprocessed text clearly and concisely.
5. If the user's query is already preprocessed, you can skip this step and return the original query.
6. Return question do not add prepocessed text prefix to the question. just plain question , not wrapped in any text.
7. If audio text is empty then return empty string.
**Domain Context**: Simpla specializes in providing comprehensive solutions for corporate tax compliance, including guidance on Value Added Tax (VAT), Corporate Tax (CT), and related regulations. They assist businesses in navigating the complexities of tax laws, ensuring compliance, and optimizing tax strategies.

Example of Preprocessed query generation:
1:  Human: I was just wondering, umm, what is the VAT in UAE? 
    Preprocessed query: I was just wondering what is the VAT in UAE?
2:  Human: So, like, can you tell me if panadol is zero-rated in UAE? 
    Preprocessed query: Can you tell me if panadol is zero-rated in UAE?
3:  Human: Uhh, what is pluto? 
    Preprocessed query: What is pluto?

User prompt:
    {userPrompt}

Remember to output the preprocessed query in your final answer."""
        router_selection_prompt = PromptTemplate(
            input_variables=["userPrompt"], template=refine_query_prompt_template
        )
        return router_selection_prompt
    
    def _get_refined_trancribed_chain(self):
        
        """
        Get the chain for refining the transcribed text.
        
        :return: The chain for refining the transcribed text.
        """
    
        prompt = self._get_refine_transcribed_prompt()
        
        chain = prompt | self._llm | StrOutputParser()
        
        return chain
    
    
    
    def get_refined_trancribed_text(self, audio_file_path:str):
        """
        Get the refined transcribed text from the audio file.
        
        :param audio_file_path: A string containing the path to the audio file.
        
        :return: The refined transcribed text. {str}
        """
        
        transcibed_text = self.convert_audio_to_text(audio_file_path)
        
        refined_transcribed_text = self.refine_trancribed_chain.invoke(
            { 
             "userPrompt": transcibed_text
             }
            )
        
        logger.info(f"Refined transcribed text: {refined_transcribed_text}")
        
      
        return refined_transcribed_text
    
    
    
speech_to_text = SpeechToText()

    

