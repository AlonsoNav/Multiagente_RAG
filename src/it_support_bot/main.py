from it_support_bot.rag.vector_store import ask_question

if __name__ == "__main__":
    pregunta = input("Haz tu pregunta técnica: ")
    respuesta = ask_question(pregunta)
    print("\nRespuesta del sistema:")
    print(respuesta)
