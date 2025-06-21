from it_support_bot.agents.diagnostic_agent import DiagnosticAgent

class UserAgent:
    def start(self):
        pregunta = input("Haz tu pregunta técnica: ")
        diagnostic_agent = DiagnosticAgent()
        respuesta = diagnostic_agent.handle_question(pregunta)
        print("\nRespuesta del sistema:")
        print(respuesta)