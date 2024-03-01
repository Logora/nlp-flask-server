map_templates = {
    'en': """
        Your task is to summarize contributions from people who responded to the following debate: {question}.
        Here are the contributions separated by a line:

        {text}

        Summarize these contributions by displaying the three most recurring arguments. For each argument, also provide the recurrence of these arguments (from 0 to 5, with 5 being the most recurring).
        These arguments should be a maximum of 250 characters each and should be ranked from most recurring to least recurring.

        ARGUMENTS:""",
    'fr': """
        Vous êtes chargé(e) de synthétiser les idées principales des arguments exprimés par les participants à ce débat sur {question}. 
        Leurs interventions sont présentées ci-dessous, séparées par des lignes :

        {text}

        Votre mission consiste à générer trois arguments types qui récapitulent les tendances et consensus des arguments individuels. 
        Chaque argument type doit être formulé en maximum 250 caractères et être classé par ordre de récurrence, du plus au moins fréquent. 
        Indiquez également le niveau de récurrence de chaque argument type sur une échelle de 0 à 5.

        FORMAT DE RÉSULTAT: 
        "1. [Argument type]. (X/5)"
        Où X est le niveau de récurrence de l'argument type sur une échelle de 0 à 5.

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
        Vous êtes chargé(e) de synthétiser les idées principales des arguments exprimés par les participants à ce débat sur {question}. 
        Leurs interventions sont présentées ci-dessous, séparées par des lignes :

        {text}

        Votre mission consiste à générer trois arguments types qui récapitulent les tendances et consensus des arguments individuels. 
        Chaque argument type doit être formulé en maximum 250 caractères et être classé par ordre de récurrence, du plus au moins fréquent. 
        Indiquez également le niveau de récurrence de chaque argument type sur une échelle de 0 à 5.

        FORMAT DE RÉSULTAT: 
        "1. [Argument type]. (X/5)"
        Où X est le niveau de récurrence de l'argument type sur une échelle de 0 à 5.
        Il doit n'y avoir que 3 arguments impérativement. Chaque argument possède un numéro unique.

        EXEMPLE DE RÉSULTAT:
        "1. [Argument type]. (X/5)"
        "2. [Autre argument type]. (X/5)"
        "3. [Autre argument type]. (X/5)"

        Le résultat doit toujours suivre le format de l'exemple. L'échelle de 0 à 5 doit toujours être entre paranthèses.

        ARGUMENTS:"""
}