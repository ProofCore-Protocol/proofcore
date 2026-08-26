import gradio as gr
from .client import seal


class NotarizedOutput:
    """
    Drop-in UI component for Hugging Face Spaces.
    Wraps standard text output with a ProofCore cryptographic badge.
    """

    def __init__(self, label: str = "AI Output (Anchored on TON)"):
        with gr.Group():
            self.textbox = gr.Textbox(label=label, interactive=False)  # , show_copy_button=True)
            self.badge_html = gr.HTML(visible=False)

        # Список аутпутов, которые нужно прокидывать в btn.click(outputs=...)
        self.outputs = [self.textbox, self.badge_html]

    def process(self, content: str, title: str = "HF Space Generation", agent_id: str = "Hugging Face Space"):
        """
        Takes raw string from AI, seals it via ProofCore, and returns updated UI components.
        """
        if not content:
            return "", gr.update(visible=False)

        try:
            # Синхронный вызов нашего API
            deal = seal(content=content, title=title, agent_id=agent_id)
            deal_id = deal["deal_id"]

            # 🔥 ИСПРАВЛЕНИЯ:
            # 1. Текст кнопки изменен на "Open Proof Explorer ↗"
            # 2. В тег <img> добавлен атрибут onload, который заставляет картинку саму себя обновлять каждые 5 секунд!
            html_content = f"""
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: -10px; padding: 12px; background: #050b14; border: 1px solid #1e293b; border-radius: 0 0 8px 8px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <span style="font-size: 24px;">🛡️</span>
                                <div style="display: flex; flex-direction: column; justify-content: center;">
                                    <span style="font-size: 10px; color: #00d2ff; text-transform: uppercase; font-weight: bold; letter-spacing: 1px;">Cryptographically Secured</span>
                                    <img src="https://api.proofcore.org/api/badge/{deal_id}" alt="ProofCore Status" style="height: 20px; margin-top: 4px;" onload="setTimeout(() => this.src = 'https://api.proofcore.org/api/badge/{deal_id}?t=' + Date.now(), 5000)" onerror="setTimeout(() => this.src = 'https://api.proofcore.org/api/badge/{deal_id}?t=' + Date.now(), 5000)"/>
                                </div>
                            </div>
                            <a href="https://proofcore.org/app/{deal_id}" target="_blank" style="background: linear-gradient(135deg, #00f298, #00d2ff); color: #050b14; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 11px; font-weight: bold; text-transform: uppercase;">Open Proof Explorer ↗</a>
                        </div>
                        """
            return content, gr.update(value=html_content, visible=True)
        except Exception as e:
            # Fallback, если API недоступно
            error_html = f"<div style='color: #ef4444; padding: 10px; font-size: 12px;'>⚠️ ProofCore Error: {str(e)}</div>"
            return content, gr.update(value=error_html, visible=True)