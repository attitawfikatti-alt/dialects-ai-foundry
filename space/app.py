import gradio as gr
import torch
from transformers import pipeline

FINE_TUNED_ID = "Termuxphone/whisper-small-algerian-merged"
BASE_ID = "openai/whisper-small"
device = 0 if torch.cuda.is_available() else -1

algerian_pipe = pipeline(
    "automatic-speech-recognition",
    model=FINE_TUNED_ID,
    device=device,
)

base_pipe = pipeline(
    "automatic-speech-recognition",
    model=BASE_ID,
    device=device,
)

def compare_models(audio_path):
    if audio_path is None:
        return "يرجى تسجيل صوت أو رفع ملف صوتي أولاً.", ""
    
    gen_kwargs = {"language": "arabic", "task": "transcribe"}
    
    algerian_out = algerian_pipe(audio_path, generate_kwargs=gen_kwargs)["text"]
    base_out = base_pipe(audio_path, generate_kwargs=gen_kwargs)["text"]
    
    return algerian_out, base_out

with gr.Blocks(theme=gr.themes.Soft(), title="Algerian Multi-Dialect Whisper ASR") as demo:
    gr.Markdown(
        """
        # 🇩🇿 Algerian Multi-Dialect Whisper ASR (`dialects-ai-foundry`)
        **تطوير:** Tawfik Atti (`Termuxphone`) | **الرخصة:** `CC-BY-NC-4.0` (للاستخدام البحثي غير التجاري — للتراخيص التجارية والـ API يرجى التواصل)
        
        سجّل صوتك باللهجة الجزائرية (سيدي بلعباس، البيّض، سكيكدة، الجلفة، تيزي وزو، بشار، عنابة، باتنة، تبسة) أو ارفع ملفاً صوتياً لمقارنة دقة النموذج المكيّف مع Whisper الأصلي.
        """
    )
    
    with gr.Row():
        audio_input = gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="🎙️ التسجيل الصوتي أو رفع ملف (WAV / MP3)"
        )
    
    submit_btn = gr.Button("تفريغ الصوت ومقارنة النماذج 🚀", variant="primary")
    
    with gr.Row():
        algerian_text = gr.Textbox(
            label="✅ نتيجة نموذج dialects-ai-foundry (المكيّف للهجات الجزائرية)",
            lines=4
        )
        base_text = gr.Textbox(
            label="⚪ نتيجة Whisper Small الأصلي (بدون تكييف)",
            lines=4
        )
    
    submit_btn.click(
        fn=compare_models,
        inputs=audio_input,
        outputs=[algerian_text, base_text]
    )

if __name__ == "__main__":
    demo.launch()
