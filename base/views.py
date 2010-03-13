# Create your views here.
from utils import *

def home(request):
    return render_to_response('index.html')
