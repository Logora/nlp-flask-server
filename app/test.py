from app import argument_summary_analysis
from seeds import arguments, arguments_1, arguments_es
import requests
import json
from argument_summary import get_summary
from keyphrase_extraction import get_keyphrases

# print(get_summary('argument-summary-1-1', arguments['first_position'], arguments["question"]))
# print(get_summary('argument-summary-1-2', arguments['second_position'], arguments["question"]))
# print(get_summary('argument-summary-2-1', arguments_1['first_position'], arguments_1["question"]))
# print(get_summary('argument-summary-2-2', arguments_1['second_position'], arguments_1["question"]))

# print(get_keyphrases('keyphrases-extraction-1-1', arguments['first_position'], arguments["question"]))
# print(get_keyphrases('keyphrases-extraction-1-2', arguments['second_position'], arguments["question"]))
# print(get_keyphrases('keyphrases-extraction-2-1', arguments_1['first_position'], arguments_1["question"]))
# print(get_keyphrases('keyphrases-extraction-2-2', arguments_1['second_position'], arguments_1["question"]))

print(get_summary('argument-summary-es-1', arguments_es['first_position'], arguments_es["question"], "es"))
print(get_summary('argument-summary-es-2', arguments_es['second_position'], arguments_es["question"], "es"))

print(get_keyphrases('keyphrases-extraction-es-1', arguments_es['first_position'], arguments_es["question"], "es"))
print(get_keyphrases('keyphrases-extraction-es-2', arguments_es['second_position'], arguments_es["question"], "es"))