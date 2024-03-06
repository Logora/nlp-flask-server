summarize_templates = {
    'en': """
        Your task is to summarize arguments in response to the following debate: {question}.
        Here are the arguments separated by a line:

        {text}

        Summarize these arguments by displaying the three most recurring arguments. For each argument, also provide the recurrence of these arguments (from 0 to 5, with 5 being the most recurring).
        These arguments should be a maximum of 250 characters each and should be ranked from most recurring to least recurring, in JSON format, with keys "argument" and "occurrences".

        ARGUMENTS:""",
    'fr': 
        """

        Vous devez synthétiser les idées principales des arguments exprimés par les participants à ce débat sur {question}. 
        Leurs arguments sont présentés ci-dessous, séparés par des lignes :

        {text}

        Vous devez générer trois arguments types qui récapitulent les tendances et consensus des arguments individuels.
        Chaque argument type doit être formulé en maximum 250 caractères et être classé par ordre de récurrence, du plus au moins fréquent. 
        Indiquez également le niveau de récurrence de chaque argument type sur une échelle de 0 à 5.
        Le résultat doit être sous format JSON, avec les clés "argument" et "occurrences".
        Chacun des trois arguments doit impérativement respecter ce format: {response_format}
        """
}

keyphrases_templates = {
    'en': """
        Your task is to extract keywords from this set of  provided arguments: {text}. You must extract 5 distinct keywords that are the most recurrent in this set of argument.
        Each keyword must be different from each other. You must provide the number of times the keywords is present in the set of arguments provided. 
        The response format must be in JSON following this format: {response_format}.
        """,
    'fr': """
        Votre tâche consiste à extraire des mots-clés de cet ensemble d'arguments fournis : {text}. 
        Vous devez extraire 5 mots-clés distincts qui sont les plus récurrents dans cet ensemble d'arguments, 
        en excluant tout mot-clé qui est similaire ou directement lié à la question de débat: {question}.
        Assurez-vous que les mots-clés choisis sont variés, pertinents et ne se rapportent pas directement aux éléments centraux de la question de débat.
        Chaque mot-clé doit être différent des autres. Vous devez fournir le nombre de fois que les mots-clés sont présents dans l'ensemble des arguments fournis. 
        Assurez-vous de choisir des mots-clés pertinents mais distincts des éléments clés de la question posée. 
        Le format de la réponse doit être en JSON et respecter ce modèle: {response_format}.
        """
}