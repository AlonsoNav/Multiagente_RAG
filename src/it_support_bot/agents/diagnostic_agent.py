from it_support_bot.rag.vector_store import ask_question
from it_support_bot.agents.resolution_agent import ResolutionAgent

class DiagnosticAgent:
    def handle_question(self, pregunta):
        # Aquí podrías agregar lógica para decidir si usar RAG o no
        respuesta_rag = ask_question(pregunta)
        resolution_agent = ResolutionAgent()
        return resolution_agent.resolve(respuesta_rag)