from Calculate import postfix_converter
from Postfix_converter import Solver
from Exp_simplifier import simplifier
from url_to_exp import *

url = 'https://firebasestorage.googleapis.com/v0/b/photocalculator-438b1.appspot.com' \
      '/o/'+ 'images%2Fpic.jpg?alt=media&token=5fce423f-4f26-45de-810b-9364e744edeb'

image = url_to_image(url)

exp = create_exp(image)

simplified_exp = simplifier(exp)

postfix_exp = postfix_converter(simplified_exp)

answer = Solver(postfix_exp)

print(answer)
