
from autogen_ai import autogen_main
from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
from docx import Document
import PyPDF2
from langchain_openai import AzureChatOpenAI


os.environ['OPENAI_API_KEY'] = 'AZURE_OPENAI_API_KEY'
endpoint = os.getenv("ENDPOINT_URL", "https://selfservicepoc.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")
api_version = '2024-02-15-preview'

llm = AzureChatOpenAI(
            azure_endpoint=endpoint,  
            deployment_name='gpt-4o',
            openai_api_version=api_version,
            response_format="json_object"
        )

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
ai_msg