import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0) if GOOGLE_API_KEY else None

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that extracts key information from text."),
    ("user", "Extract the following information from the text below:\n\nSkills:\nExperience:\nEducation:\nKeywords:\n\nText:\n{text}")
])

def extract_info_with_langchain(text):
    if llm is None:
        return {"Error": "LLM not initialized"}
    chain = extraction_prompt | llm
    response = chain.invoke({"text": text})
    response_text = response.content if isinstance(response, BaseMessage) else str(response)
    extracted_data = {}
    for section in response_text.split('\n\n'):
        if ':' in section:
            key, value = section.split(':', 1)
            extracted_data[key.strip()] = value.strip()
    for key in ['Skills', 'Experience', 'Education', 'Keywords']:
        if key not in extracted_data:
            extracted_data[key] = ""
    return extracted_data

def generate_improvement_suggestions(resume_info, job_info, skill_gaps):
    if llm is None:
        return "LLM not initialized"
    suggestions_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful career coach."),
        ("user", "Resume Info:\n{resume_info}\n\nJob Info:\n{job_info}\n\nSkill Gaps:\n{skill_gaps}\n\nSuggestions:")
    ])
    chain = suggestions_prompt | llm
    response = chain.invoke({
        "resume_info": resume_info,
        "job_info": job_info,
        "skill_gaps": ", ".join(skill_gaps)
    })
    return response.content if isinstance(response, BaseMessage) else str(response)

def generate_cover_letter(resume_info, job_info):
    if llm is None:
        return "LLM not initialized"
    cover_letter_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional cover letter writer."),
        ("user", "Resume Info:\n{resume_info}\n\nJob Info:\n{job_info}\n\nWrite a tailored cover letter:")
    ])
    chain = cover_letter_prompt | llm
    response = chain.invoke({
        "resume_info": resume_info,
        "job_info": job_info
    })
    return response.content if isinstance(response, BaseMessage) else str(response)
