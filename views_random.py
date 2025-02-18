import random
import string
from django.http import JsonResponse

def generate_random_string(request):
    length = int(request.GET.get('length', 8))
    specials = int(request.GET.get('specials', 0))
    digits = int(request.GET.get('digits', 0))

    if length < 1 or length > 100:
        return JsonResponse({'error': 'Length must be between 1 and 100'}, status=400)
    if specials not in [0, 1] or digits not in [0, 1]:
        return JsonResponse({'error': 'Specials and digits must be 0 or 1'}, status=400)

    characters = string.ascii_letters
    if specials:
        characters += '!"№;%:?*()_+'
    if digits:
        characters += string.digits

    random_string = ''.join(random.choices(characters, k=length))
    return JsonResponse({'random_string': random_string})