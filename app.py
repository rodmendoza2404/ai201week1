import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources_text = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources_text

with gr.Blocks(title="FIU CS Unofficial Guide") as demo:
    gr.Markdown("# 🎓 FIU CS Unofficial Guide")
    gr.Markdown("Ask questions about FIU CS professors, courses, and workload — answered from real student reviews.")
    
    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder="e.g. What do students say about Mark Weiss's exams?",
            lines=2
        )
    
    btn = gr.Button("Ask", variant="primary")
    
    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=8)
        sources = gr.Textbox(label="Sources used", lines=8)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()