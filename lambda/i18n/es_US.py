from i18n import i18nTexts


class es_USTexts(i18nTexts):
    SKILL_NAME = "Verdadero o Falso"
    HELP_TEXT = "Dime que te haga una pregunta y empezaré a preguntarte cosas"
    EXIT_TEXT = "Me lo he pasado muy bien, ¡Hasta la próxima!"
    EXCEPTION_TEXT = (
        'No se cómo responder a eso. Prueba a repetirlo o dime "vuelve a empezar".'
    )
    EXCEPTION_REPROMPT_TEXT = (
        'Puedes repetir lo que has dicho o decirme "vuelve a empezar"'
    )
    HELLO_TEXT = "¡Bienvenido a verdadero o falso! Dime que te haga una pregunta y empezaré. Te diré si tu respuesta es correcta o no, y podrás pedirme otra"
    HELLO_REPROMPT_TEXT = 'Prueba a decirme, "hazme una pregunta"'
    TRUE_FALSE_TEXT = "¿Verdadero o Falso?"
    CORRECT_ANSWER_SPEECHCONS = [
        "ajá",
        "así mero",
        "awesome",
        "bien",
        "bravo",
        "chido",
        "chidísimo",
        "exactamente",
        "fabuloso",
        "fantástico",
        "fenomenal",
        "great",
        "touchdown",
        "well done",
        "yay",
    ]
    INCORRECT_ANSWER_SPEECHCONS = [
        "bummer",
        "diablos",
        "lástima",
        "lo lamento",
        "lo siento",
        "maldición",
        "maldita sea",
        "no",
        "oops",
        "ouch",
    ]
    NEW_ANSWER_TEXT = "¿Quieres otra pregunta?"
    START_OVER_TEXT = "De acuerdo, empezamos de nuevo."
