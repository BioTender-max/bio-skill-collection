# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import os
import json
import tempfile
import pytesseract
import pdfplumber
import requests
import io
import re
from PIL import Image
from pdf2image import convert_from_path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Import your custom JSON repair function
from .ToolAgent import Json_Format_Agent

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    First attempt to extract text using pdfplumber; if no text is found (scanned version),
    then use pdf2image + pytesseract for OCR.
    """
    extracted_text_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            extracted_text_pages.append(page_text)
    all_text = "\n".join(extracted_text_pages).strip()

    if all_text:
        return all_text

    # If pdfplumber didn't get text, use OCR
    ocr_text_pages = []
    with tempfile.TemporaryDirectory() as tempdir:
        pages = convert_from_path(pdf_path, dpi=300, output_folder=tempdir)
        for page_image in pages:
            text = pytesseract.image_to_string(page_image)
            ocr_text_pages.append(text)
    return "\n".join(ocr_text_pages)

def extract_text_from_url(url: str, process_images: bool = True, api_key: str = None) -> str:
    """
    Extract text content from a webpage URL, optionally process images
    
    Parameters:
        url: Web page URL
        process_images: Whether to process images in the webpage
        api_key: API key for vision model
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Ensure request was successful
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text
        text = soup.get_text(separator='\n')
        
        # Clean text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # If image processing is enabled and API key is provided
        if process_images and api_key:
            image_texts = extract_text_from_images(soup, url, api_key)
            if image_texts:
                text += "\n\n--- Image Content ---\n" + "\n\n".join(image_texts)
        
        return text
    except Exception as e:
        return f"Error extracting text from URL: {str(e)}"

def extract_text_from_images(soup, base_url, api_key):
    """Extract images from webpage and perform OCR or visual analysis"""
    image_texts = []
    
    # Find all image tags
    for img in soup.find_all('img'):
        try:
            # Get image URL
            img_url = img.get('src')
            if not img_url:
                continue
                
            # Convert relative URL to absolute URL
            img_url = urljoin(base_url, img_url)
            
            # Determine if it's a real image (exclude icons, etc.)
            if img.get('width') and int(img.get('width')) < 100:
                continue
                
            # Download image
            img_response = requests.get(img_url, stream=True)
            if img_response.status_code != 200:
                continue
                
            # Open image
            img_content = Image.open(io.BytesIO(img_response.content))
            
            # Perform OCR processing
            text = pytesseract.image_to_string(img_content)
            
            # Only keep OCR results with substantial content
            if len(text.strip()) > 10:  # Assume less than 10 characters is noise
                image_texts.append(text)
                
            # Optional: Can also replace/add vision model processing
            # vision_text = analyze_image_with_vision_model(img_content, api_key)
            # if vision_text:
            #     image_texts.append(vision_text)
            
        except Exception as e:
            continue  # Ignore errors processing a single image, continue with other images
            
    return image_texts

def analyze_image_with_vision_model(image, api_key):
    """
    Analyze image content using vision language model
    This is an example implementation, needs to be adjusted based on the actual API used
    """
    try:
        # This is sample code for integrating vision language model API
        # For example, using OpenAI's GPT-4 Vision or other vision language model API
        
        # Example: If using OpenAI
        # First need to convert image to base64 format
        import base64
        from io import BytesIO
        
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Then call API
        # response = openai.chat.completions.create(
        #     model="gpt-4-vision-preview",
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": [
        #                 {"type": "text", "text": "What's in this image? Extract any text visible and describe key elements."},
        #                 {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
        #             ]
        #         }
        #     ],
        #     max_tokens=300
        # )
        # return response.choices[0].message.content
        
        # Since this part needs actual API integration, return placeholder
        return "Vision language model functionality to be integrated"
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def summarize_content_as_workflow(content_path: str, api_key: str, base_url: str, process_images: bool = True) -> str:
    """
    1. Extract text from PDF or webpage
    2. Use GPT to summarize text, output specific JSON structure
    3. Call Json_Format_Agent to fix JSON ensuring validity
    
    Parameters:
        content_path: PDF file path or webpage URL
        api_key: OpenAI API key
        base_url: OpenAI API base URL
        process_images: Process webpage images (only valid for URLs)
    """
    # Determine if input is PDF file or URL
    is_url = bool(urlparse(content_path).scheme)
    
    if is_url:
        all_text = extract_text_from_url(content_path, process_images, api_key)
    else:
        all_text = extract_text_from_pdf(content_path)

    template_for_summary = """
    You are an expert bioinformatics workflow specialist. Your task is to read the provided scientific paper and extract the methodological workflows and techniques used in the research.
    
    Please analyze the paper and create a detailed step-by-step workflow with the following requirements:
    
    1. Number each step sequentially (Step 1, Step 2, Step 3, etc.)
    2. Break down the workflow into fine-grained steps, with each step using preferably only ONE tool
    3. For each step, clearly specify:
       - Description: Brief explanation of what this step accomplishes
       - Tool Used: The specific software/tool used in this step
       - Input Required: What data or files are needed as input
       - Expected Output: What results or files are produced
    4. Be as comprehensive as possible, capturing all methodological details
    
    Format your response as a valid JSON according to the following structure:
    
    {{
        "content": "This is a workflow for [Brief description of the workflow]\n\nStep 1: [Step Name]\nDescription: [Brief description of the step]\nInput Required: [Input data/files needed]\nExpected Output: [Output data/files produced]\nTool Used: [Specific tool name].\n\nStep 2: [Step Name]\nDescription: [Brief description of the step]\nInput Required: [Input data/files needed]\nExpected Output: [Output data/files produced]\nTool Used: [Specific tool name].\n\n[Continue with remaining steps...]",
        "metadata": {{
            "source": "workflow",
            "page": 1
        }}
    }}
    
    Paper text to analyze:
    {text}
    """

    os.environ['OPENAI_API_KEY'] = api_key

    summary_prompt = ChatPromptTemplate.from_template(template_for_summary)
    llm = ChatOpenAI(model="o3-mini-2025-01-31", base_url=base_url)
    parser = StrOutputParser()
    chain = summary_prompt | llm | parser

    # Call model to get preliminary JSON
    raw_json_output = chain.invoke({"text": all_text})
    # Fix JSON
    corrected_json = Json_Format_Agent(raw_json_output, api_key=api_key, base_url=base_url)
    return corrected_json

# Keep original function name as alias for backward compatibility
summarize_pdf_as_workflow = summarize_content_as_workflow

def append_summary_to_plan_knowledge(corrected_json: str, plan_knowledge_path: str = "./doc/Plan_Knowledge.json"):
    # If file doesn't exist, create an empty JSON array file first
    if not os.path.exists(plan_knowledge_path):
        with open(plan_knowledge_path, 'w', encoding='utf-8') as f:
            f.write("[]")

    # Read existing JSON
    with open(plan_knowledge_path, 'r', encoding='utf-8') as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

    if not isinstance(existing_data, list):
        existing_data = [existing_data]

    # Convert string form of corrected_json to Python object
    try:
        new_summary_obj = json.loads(corrected_json)
    except json.JSONDecodeError:
        print("The provided corrected_json is not a valid JSON string, please check.")
        return

    # Append to list
    existing_data.append(new_summary_obj)

    # Write back to file
    with open(plan_knowledge_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

def generate_workflow_markdown(content_path: str, api_key: str, base_url: str, output_path: str = "plan_knowledge.md", process_images: bool = True) -> str:
    """
    Generate Markdown format workflow description from document content and save to file
    
    Parameters:
        content_path: PDF file path or webpage URL
        api_key: OpenAI API key
        base_url: OpenAI API base URL
        output_path: Output Markdown file path
        process_images: Process webpage images (only valid for URLs)
    
    Returns:
        Generated Markdown content string
    """
    # Determine if input is PDF file or URL
    is_url = bool(urlparse(content_path).scheme)
    
    if is_url:
        all_text = extract_text_from_url(content_path, process_images, api_key)
    else:
        all_text = extract_text_from_pdf(content_path)

    template_for_summary = """
    You are an expert bioinformatics workflow specialist. Your task is to read the provided scientific paper and extract the methodological workflows and techniques used in the research.
    
    Please analyze the paper and create a detailed step-by-step workflow with the following requirements:
    
    1. Number each step sequentially (Step 1, Step 2, Step 3, etc.)
    2. Break down the workflow into fine-grained steps, with each step using preferably only ONE tool
    3. For each step, clearly specify:
       - Description: Brief explanation of what this step accomplishes
       - Tool Used: The specific software/tool used in this step
       - Input Required: What data or files are needed as input
       - Expected Output: What results or files are produced
    4. Be as comprehensive as possible, capturing all methodological details
    
    Format your response in Markdown format starting with:
    
    # Workflow for [Brief description of the workflow]
    
    ## Step 1: [Step Name]
    **Description:** [Brief description of the step]
    **Input Required:** [Input data/files needed]
    **Expected Output:** [Output data/files produced]
    **Tool Used:** [Specific tool name]
    
    ## Step 2: [Step Name]
    **Description:** [Brief description of the step]
    **Input Required:** [Input data/files needed]
    **Expected Output:** [Output data/files produced]
    **Tool Used:** [Specific tool name]
    
    [Continue with remaining steps...]
    
    Paper text to analyze:
    {text}
    """

    os.environ['OPENAI_API_KEY'] = api_key

    summary_prompt = ChatPromptTemplate.from_template(template_for_summary)
    llm = ChatOpenAI(model="o3-mini-2025-01-31", base_url=base_url)
    parser = StrOutputParser()
    chain = summary_prompt | llm | parser

    # Call model to generate Markdown
    markdown_output = chain.invoke({"text": all_text})
    
    # Save Markdown to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_output)
        
    print(f"Generated workflow Markdown file: {output_path}")
    return markdown_output

def convert_markdown_to_json(markdown_path: str, json_path: str = "./doc/Plan_Knowledge.json"):
    """
    Convert Markdown format workflow to JSON format and save
    
    Parameters:
        markdown_path: Markdown file path
        json_path: Output JSON file path
    """
    try:
        # Read Markdown file
        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Extract workflow title
        title_match = re.search(r'# Workflow for (.*?)(?:\n|$)', markdown_content)
        workflow_title = title_match.group(1) if title_match else "Unnamed Workflow"
        
        # Build text content, convert Markdown to plain text format
        text_content = f"This is a workflow for {workflow_title}\n\n"
        
        # Extract each step
        step_pattern = r'## Step (\d+): (.*?)(?:\n|$)(.*?)(?=## Step \d+:|$)'
        steps = re.findall(step_pattern, markdown_content, re.DOTALL)
        
        for step_num, step_name, step_content in steps:
            # Extract step details
            description = re.search(r'\*\*Description:\*\* (.*?)(?:\n|$)', step_content)
            input_req = re.search(r'\*\*Input Required:\*\* (.*?)(?:\n|$)', step_content)
            output = re.search(r'\*\*Expected Output:\*\* (.*?)(?:\n|$)', step_content)
            tool = re.search(r'\*\*Tool Used:\*\* (.*?)(?:\n|$)', step_content)
            
            # Build step text
            step_text = f"Step {step_num}: {step_name}\n"
            if description: step_text += f"Description: {description.group(1)}\n"
            if input_req: step_text += f"Input Required: {input_req.group(1)}\n"
            if output: step_text += f"Expected Output: {output.group(1)}\n"
            if tool: step_text += f"Tool Used: {tool.group(1)}\n"
            
            text_content += step_text + "\n"
        
        # Build JSON object
        json_obj = {
            "content": text_content,
            "metadata": {
                "source": "workflow",
                "page": 1
            }
        }
        
        # Prepare to save to Plan_Knowledge.json
        if not os.path.exists(os.path.dirname(json_path)) and os.path.dirname(json_path):
            os.makedirs(os.path.dirname(json_path))
            
        if os.path.exists(json_path):
            # Read existing JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []
            
        if not isinstance(existing_data, list):
            existing_data = [existing_data]
            
        # Add new JSON object
        existing_data.append(json_obj)
        
        # Save to file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
            
        print(f"Converted Markdown to JSON and saved to: {json_path}")
        return json.dumps(json_obj, ensure_ascii=False)
    
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return None


__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
