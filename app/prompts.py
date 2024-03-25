summarize_templates = {
    'en': """
        Your task is to summarise the main ideas of the arguments expressed by the participants in this debate on {question}. 
        Their arguments are presented below, separated by lines:

        {text}

        You must generate three standard arguments which summarise the trends and consensus of the individual arguments.
        Each standard argument should be a maximum of 250 characters long and should be arranged in order of recurrence, from most to least frequent. 
        Also indicate the level of recurrence of each standard argument on a scale of 0 to 5.
        The result must be in JSON format, with the keys "argument" and "occurrences".
        Each of the three arguments must respect this format: {response_format}
        """,
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
        """,
    'es':
        """Tu tarea consiste en resumir las ideas principales de los argumentos expresados por los participantes en este debate sobre {question}. 
        Sus argumentos se presentan a continuación, separados por líneas:

        {text}

        Debe generar tres argumentos estándar que resuman las tendencias y el consenso de los argumentos individuales.
        Cada argumento estándar debe tener una longitud máxima de 250 caracteres y debe ordenarse por orden de recurrencia, de más a menos frecuente. 
        Indique también el nivel de recurrencia de cada argumento estándar en una escala de 0 a 5.
        El resultado debe estar en formato JSON, con las claves "argument" y "ocurrences".
        Cada uno de los tres argumentos debe respetar este formato: {response_format}
        """
}

keyphrases_templates = {
    'en': """
        Your task is to extract keywords from the set of arguments provided: {text}. 
        You must extract 5 distinct keywords that are the most recurrent in this set of arguments, 
        excluding any keywords that are similar or directly related to the debate question: {question}.
        Make sure that the keywords chosen are varied, relevant and do not relate directly to the central elements of the debate question.
        Each keyword must be different from the others. You should provide the number of times the keywords occur in the set of arguments provided. 
        Make sure you choose keywords that are relevant but distinct from the key elements of the question asked. 
        The format of the response must be in JSON and follow this model: {response_format}.
        """,
    'fr': """
        Votre tâche consiste à extraire des mots-clés de cet ensemble d'arguments fournis : {text}. 
        Vous devez extraire 5 mots-clés distincts qui sont les plus récurrents dans cet ensemble d'arguments, 
        en excluant tout mot-clé qui est similaire ou directement lié à la question de débat: {question}.
        Assurez-vous que les mots-clés choisis sont variés, pertinents et ne se rapportent pas directement aux éléments centraux de la question de débat.
        Chaque mot-clé doit être différent des autres. Vous devez fournir le nombre de fois que les mots-clés sont présents dans l'ensemble des arguments fournis. 
        Assurez-vous de choisir des mots-clés pertinents mais distincts des éléments clés de la question posée. 
        Le format de la réponse doit être en JSON et respecter ce modèle: {response_format}.
        """,
    'es': 
        """
        Su tarea consiste en extraer palabras clave del conjunto de argumentos proporcionado: {text}. 
        Debe extraer 5 palabras clave distintas que sean las más recurrentes en este conjunto de argumentos, 
        excluyendo cualquier palabra clave que sea similar o esté directamente relacionada con la pregunta del debate: {question}.
        Asegúrese de que las palabras clave elegidas sean variadas, pertinentes y no estén directamente relacionadas con los elementos centrales de la pregunta del debate.
        Cada palabra clave debe ser diferente de las demás. Debe indicar el número de veces que aparecen las palabras clave en el conjunto de argumentos proporcionados. 
        Asegúrese de elegir palabras clave que sean pertinentes pero distintas de los elementos centrales de la pregunta formulada. 
        El formato de la respuesta debe estar en JSON y seguir este modelo: {response_format}.
        """
}