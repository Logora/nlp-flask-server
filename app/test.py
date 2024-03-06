from app import argument_summary_analysis
from seeds import arguments, arguments_1
import requests
import json
from argument_summary import get_summary
from keyphrase_extraction import get_keyphrases

url = 'http://localhost:8000/analysis'
params = {
    'uid': 'argument-summary-1',
    'name': 'argument_summary',
    'question': arguments["question"],
    'language': 'en'
}

body = {
    'documents': [
        '''L'union européenne c'est la tour de Babel. Ils veulent tous tirer la couverture à eux que ce ne sont des pis à lait sans succès. Nous signons des traités avec l'Ukraine qui ne servent à rien. Nous ne voulons pas la guerre. Pour qui, pour les Américains ? De Gaulle ne voulait pas de l'OTAN à juste titre,il a fallu Sarkozy pour nous y remettre. Nous sommes incapables d'avoir notre propre défense européenne. Aider l'Ukraine un pays corrompu, verser des subventions à se partager, notre Président sans vision politique cohérente, où allons nous tout simplement ?
        De plus ce serait un cassus belli vis à vis de la Russie. pour faire plaisir aux américains qui nous disent maintenant qu'ils ne nous défendaient pas en cas de conflit avec la Russie ??Mais on nous prend pour des imbéciles,  que nous apporter l'OTAN finalement ?
        Pourquoi pas être 'neutre" comme Autriche, Suisse ??? 
        L'OTAN devient un fourre tout à discrétion de politiciens plus ou moins intéressés.Quand à la force de dissuasion nucléaire,elle doit rester à notre seule et unique disposition,on ne peut laisser le choix d'un bombardement nucléaire et donc des mesures de rétorsion pour notre pays à discrétion de politiques étrangers.
        Un pays gangrené par la corruption de grande ampleur n'a pas sa place dans l'OTAN ils n'ont déjà pas le finances pour  pouvoir se défendre qui va payer pour eux au sein  de l'OTAN.
        Ou alors dans très longtemps.''',
        '''Nous n'allons pas sacrifier notre agriculture et notre industrie sans contrepartie. 
        Restons éveillés, cherchons à comprendre l'imbroglio pour trouver la voie de la paix. Écoutons autre chose que les médias main stream, entre autres, Emmanuel Todd, Jacques Baud, Natacha Polony.... Qui veut une troisième guerre mondiale ? On dirait que nos dirigeants l'appellent tous de leurs voeux, les inconséquents !''',
        '''Mais soutien et protection toujours aux victimes des guerres, les ukrainiens en particulier. La grande majorité des personnes n'aspirent qu'à une vie paisible.
        On va être envahi de produits agricoles non conforme à notre réglementation 
        Toutes coalitions  engendrent la guerre par l'irresponsabilité de certain !
        Si l'on ne veut pas une guerre mondiale...''',
        '''OUf, ça fit du bien de voir que tous les français ne sont pas zombifiés à la propagande des neocons américains. Otan vecteur de paixx .... Mort de rire ?
        Pourquoi faire entrer l'Ukraine dans l'OTAN ? Faudrait déjà que les dirigeants de ce pays soient claires et exemplaires dans leur comportement nationale , ce qui est loin d'être le cas.
        Je suis contre. Qu''elle soit neutre, mais armee jusqu' aux dents par l'Otan, pour ne ps se faire bouffer par la Russie. Elle servira de tampon entre l'Otan et la Russie. Cette dernière sera, rassurree. Espérons qu'elle ne cherxhera pas à récupérer les Pays  baltes membres ddl'Otan
        Les pays en bordure de la frontière avec la Russie devraient rester neutres !
        Jamais le résultat serait mettre la France  l'Europe en état de guerre larvée avec la Russie, la Chine, l'Inde, la corée du nord ainsi que tous les pays du sud global se  serait le début de la 3ème guerre mondiale.'''
    ]
}
# print(get_summary('argument-summary-1-1', arguments['first_position'], arguments["question"]))
# print(get_summary('argument-summary-1-2', arguments['second_position'], arguments["question"]))
# print(get_summary('argument-summary-2-1', arguments_1['first_position'], arguments_1["question"]))
# print(get_summary('argument-summary-2-2', arguments_1['second_position'], arguments_1["question"]))

print(arguments["question"])
print(get_keyphrases('keyphrases-extraction-1-1', arguments['first_position'], arguments["question"]))
print(arguments["question"])
print(get_keyphrases('keyphrases-extraction-1-2', arguments['second_position'], arguments["question"]))
print(arguments_1["question"])
print(get_keyphrases('keyphrases-extraction-2-1', arguments_1['first_position'], arguments_1["question"]))
print(arguments_1["question"])
print(get_keyphrases('keyphrases-extraction-2-2', arguments_1['second_position'], arguments_1["question"]))