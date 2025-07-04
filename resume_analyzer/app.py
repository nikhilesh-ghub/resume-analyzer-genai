import gradio as gr
from resume_utils import analyze_resume

iface = gr.Interface(
    fn=analyze_resume,
    inputs=[
        gr.File(label="Upload Resume (PDF or TXT)", type="filepath"),
        gr.File(label="Upload Job Description (PDF or TXT)", type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Status"),
        gr.Textbox(label="Skill Gaps"),
        gr.Textbox(label="Job-Fit Score"),
        gr.Textbox(label="Resume Improvement Suggestions"),
        gr.Textbox(label="Tailored Cover Letter")
    ],
    title="AI-Powered Resume Analyzer",
    description="Upload your resume and a job description to get a skill gap analysis, job-fit score, resume suggestions, and a tailored cover letter."
)

iface.launch(share=True)

