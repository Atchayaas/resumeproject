# from test.autogen_ai import autogen_main
from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
from docx import Document
import PyPDF2
from langchain_openai import AzureChatOpenAI
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.environ['OPENAI_API_KEY'] = 'AZURE_OPENAI_API_KEY'
endpoint = os.getenv("ENDPOINT_URL", "https://selfservicepoc.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")
api_version = '2024-02-15-preview'


llm = AzureChatOpenAI(
            azure_endpoint=endpoint,  
            deployment_name='gpt-4o',
            openai_api_version=api_version
        
        )
# Function to process PDF files
def pdf_to_text(pdf_file_path):
    try:
        text = ''
        with open(pdf_file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text() + '\n'
        return text
    except Exception as e:
        return f"Error processing {pdf_file_path}: {e}"

# Function to process Word files
def word_to_text(word_file_path):
    try:
        text = ''
        document = Document(word_file_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + '\n'
        return text
    except Exception as e:
        return f"Error processing {word_file_path}: {e}"

@app.route('/')
def index():
    return render_template('index.html')


def gen_ai(text):
    try:

        
        prompt = """
                You are an expert resume analyzer tasked with categorizing and ranking candidates based on their technical expertise, professional experience, projects, certifications, and achievements. 

                ### Task:
                1. **Analyze the resume** to extract the candidate's:
                - **Experience** (years of work and domain expertise)
                - **Projects** (key contributions and technology stack)
                - **Technical Skills** (programming languages, frameworks, and tools)
                - **Certifications** (relevant to the technical domain)
                - **Achievements** (notable recognitions and milestones)

                2. **Classify** the candidate into one of the following categories based on their primary skill set:
                - Backend  
                - Frontend  
                - Full Stack  
                - Network  
                - Data Engineer  
                - Cloud Engineer  
                - Machine Learning/AI  
                - Security Engineer  
                - Other (if no predefined category fits)

                3. **Rank** the candidate by assessing:
                - Depth of technical knowledge  
                - Years of experience  
                - Complexity and impact of their projects
                - Relevant certifications and achievements  

                4. **Output the results** in the following JSON format:  
                            
                ##Few short Example
                1.{"FileName": "John_resume.pdf","Category": "Backend","Name": "John Doe","Position": "Senior Backend Engineer","Rank": "1"}
                2.{"FileName": "Jane_Smith_resume.pdf","Category": "Full Stack","Name": "Jane Smith","Position": "Full Stack Developer","Rank": "2"}
                3.{"FileName": "Alex_Kumar.pdf","Category": "Network", "Name": "Alex Kumar", "Position": "Network Engineer", "Rank": "3" }
                4.{"FileName": "Priya_Sharma_resume.pdf", "Category": "Frontend", "Name": "Priya Sharma", "Position": "Frontend Developer", "Rank": "4" }
                
                ##Response:
                [{"FileName":<FileName of that candidate>","Category": "<Technical stacks>", "Name": "<Candiate Name>", "Postition": "<Candidate Position>", "Rank":"<Rank based on the technical and experience part> }]
                
                Make sure it should return only List of JSON response. Don't include any other text.
                """

        
        messages = [
            (
                "system",
                "You have expertise in resume analysis and specialize in implementing a ranking system.",
            ),
            ("human", prompt  + '\n' + text ),
        ]
        ai_msg = llm.invoke(messages)
        print(json.loads(ai_msg.content.replace('```','').replace('json','')))
        return  json.loads(ai_msg.content.replace('```','').replace('json',''))
    
    except Exception as e:
        print(e)
        return [{"error":e}]

@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('files')
    file_type = request.form.get('file_type')
    text_output = ''
    
    for file in uploaded_files: 
        print(file.filename.endswith('pdf'))

        if file.filename.endswith('pdf'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            text_output += pdf_to_text(file_path) + '\n'
            print(text_output)
            with open('Resume_text.txt', 'w') as wr:
                wr.write(text_output)

        elif file.filename.endswith('.docx'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            text_output += file.filename + '\n' + word_to_text(file_path) + '\n'
            # with open('Resume_text.txt', 'w') as wr:
            #     wr.write(text_output)
        response = gen_ai(text_output)
    # return  jsonify(response)
    return render_template('result.html',results=response)

if __name__ == '__main__':
    app.run(debug=True)