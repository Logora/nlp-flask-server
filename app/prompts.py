map_templates = {
    'en': """
        Your task is to summarize contributions from people who responded to the following debate: {question}.
        Here are the contributions separated by a line:

        {text}

        Summarize these contributions by displaying the three most recurring arguments. For each argument, also provide the recurrence of these arguments (from 0 to 5, with 5 being the most recurring).
        These arguments should be a maximum of 250 characters each and should be ranked from most recurring to least recurring.

        ARGUMENTS:""",
    'fr': """
        Ta tâche est de résumer des contributions de personnes ayant répondu au débat suivant : {question}.
        Voici les contributions séparées par une ligne :

        {text}

        Résume ces contributions en affichant les trois arguments les plus récurrents. Pour chaque argument, donne aussi la récurrence de ces arguments (de 0 à 5, 5 étant le plus récurrent).
        Ces arguments doivent être de 250 caractères maximum chacun et être classés du plus récurrent au moins récurrent.

        ARGUMENTS:"""
}

reduce_templates = {
    'en': """
        Your task is to summarize arguments in response to the following debate: {question}.
        Here are the arguments separated by a line:

        {text}

        Summarize these arguments by displaying the three most recurring arguments. For each argument, also provide the recurrence of these arguments (from 0 to 5, with 5 being the most recurring).
        These arguments should be a maximum of 250 characters each and should be ranked from most recurring to least recurring, in JSON format, with keys "argument" and "occurrences".

        ARGUMENTS:""",
    'fr': """
        Ta tâche est de résumer des arguments en réponse au débat suivant : {question}.
        Voici les arguments séparées par une ligne :

        {text}

        Résume ces arguments en affichant les trois arguments les plus récurrents. Pour chaque argument, donne aussi la récurrence de ces arguments (de 0 à 5, 5 étant le plus récurrent).
        Ces arguments doivent être de 250 caractères maximum chacun et être classés du plus récurrent au moins récurrent, et sous format JSON, avec les clés "argument" et "occurrences".

        ARGUMENTS:"""
}