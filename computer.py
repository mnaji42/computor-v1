#!/Applications/Python3.8
# -*-coding:Utf-8 -*

# Bonus:
# Gérer les erreurs sur l’entrée (lexique et syntaxe) done
# Gérer les entrées sorties sous forme naturelle. done
# Afficher la (les) solution sous forme de fraction irréductible quand c’est intéressant.
# Afficher des étapes intermédiaires done

import sys

def checkEquation(eq):

	validChar = "0123456789.X^=*-/+ "
	equal = 0

	for c in eq:
		if not c in validChar:
			print("You can use only \"", validChar, "characters")
			return False
		if c == '=':
			equal += 1

	if equal != 1:
		print("Error with the equality")
		return False

	eq = eq.replace(" ","")

	i = 0
	while i < len(eq):
		try:
			if eq[i] == '^' and (i == 0 or eq[i - 1] != 'X'):
				print("You must put a 'X' behind '^'")
				return False
			if eq[i] == '^' and (eq[i + 1] < '0' or eq[i + 1] > '9'):
				raise IndexError()
			if eq[i] == '^' and (eq[i + 1] < '0' or eq[i + 1] > '2'):
				print("You can write only second degree equation")
				return False
		except IndexError:
			print("You must write a number after ^")
			return False
		if (eq[i] == 'X' and i != (len(eq) - 1) and ((eq[i + 1] >= '0' and eq[i + 1] <= '9') or eq[i + 1] == 'X')):
			print("Wrong syntax after 'X")
			return False
		if eq[i] == 'X' and i != 0 and not (eq[i] != '+' or eq[i] != '*' or eq[i] != '/' or eq[i] != '-' or eq[i] != '='):
			print("i =", i)
			print("Wrong syntax before 'X")
			return False
		if (eq[i] == '+' or eq[i] == '*' or eq[i] == '/' or eq[i] == '-' or eq[i] == '=') and\
			(eq[i + 1] == '+' or eq[i + 1] == '*' or eq[i + 1] == '/' or eq[i + 1] == '-' or eq[i + 1] == '='):
			if not (eq[i] == '=' and (eq[i + 1] == '-' or eq[i + 1] == '+')):
				print("You use two mathematical signs in a row")
				return False
		i += 1

	return True

def strToInt(s):
	if len(s) == 0:
		return 0

	i = 0
	signe  = 1
	if s[i] == '+':
		i += 1
	elif s[i] == '-':
		signe = -1
		i += 1
	if s[i] == 'X':
		return 1 * signe

	ret = 0
	while i < len(s) and (s[i] >= '0' and s[i] <= '9'):
		ret *= 10
		ret += int(s[i])
		i += 1
	
	if (s[i] == '.'):
		i += 1
		count = 0
		while i < len(s) and (s[i] >= '0' and s[i] <= '9'):
			count += 1
			ret += int(s[i]) * 10**(-count)
			i += 1

	return ret * signe
	

def parse(eq):

	start = 0
	end = 1
	while end < len(eq) and (eq[end] != '+' and eq[end] != '-'):
		end += 1
	x0 = eq[start:end]
	start = end
	end += 1
	if x0.find("X^2") != -1:
		x2 = x0
		x0 = ""
		x1 = ""
	else:
		if x0.find("X^1") != -1 or (x0.find("X^0") == -1 and x0.find("X") != -1):
			x1 = x0
			x0 = ""
		else:
			while end < len(eq) and (eq[end] != '+' and eq[end] != '-'):
				end += 1
			x1 = eq[start:end]
			start = end
			end += 1
			if x1.find("X^2") != -1:
				x2 = x1
				x1 = ""
		try:
			test = x2
		except NameError:
			while end < len(eq) and (eq[end] != '+' and eq[end] != '-'):
				end += 1
			x2 = eq[start:end]
		start = end
		end += 1

	x = [0, 0, 0]
	x[0] = strToInt(x0)
	x[1] = strToInt(x1)
	x[2] = strToInt(x2)

	return x
	
def reduceForm(eq):
	reduceForm = ""
	if eq[0]:
		reduceForm += str(eq[0]) + " * X^0"
	if eq[1]:
		if eq[1] > 0:
			reduceForm += " + "
			reduceForm += str(eq[1])
		else:
			reduceForm += " - "
			reduceForm += str(-eq[1])
		reduceForm += " X^1"
	if eq[2]:
		if eq[2] > 0:
			reduceForm += " + "
			reduceForm += str(eq[2])
		else:
			reduceForm += " - "
			reduceForm += str(-eq[2])
		reduceForm += " X^2"
	reduceForm += " = 0"
	return reduceForm

def solveFirstDegree(eq):
	if eq[1] == 0:
		if eq[0] == 0:
			print("Puisque que a, b, et c sont égale à 0 on a l'equation '0 = 0' qui est vrai, donc tous les nombre réel sont solutions")
			print("Reduced form: 0 = 0")
			print("Polynomial degree: 0")
			print("Solution : R (all real)")
		else:
			print("Puisque a et b sont egales à 0 et que c est égale à", eq[0], "on a l'équation'", eq[0], "= 0' qui est fausse, donc il n'y a pas de solution")
			print("Reduced form:", eq[0] ,"= 0")
			print("Polynomial degree: 0")
			print("Solution : no solution")
	else:
		print("Ce polynome etant du premier degrée, et sachant que a et b ne sont pas nul on peut resoudre l'equation ax + b = 0 <==> x = b/a")
		print("Reduced form:", reduceForm(eq))
		print("Polynomial degree: 1")
		print("The solution is:\n", -eq[0] / eq[1], sep="")
	
def solveSecondDegree(eq):
	delta = eq[1] * eq[1] - 4 * eq[2] * eq[0]
	print("On calcule le descriminant : delta = b^2 - 4ac =", "{}^2 - 4{}{}".format(eq[1], eq[2], eq[0]), "=", delta)
	if delta < 0:
		print("Puisque delta est inferieur à 0, il n'y a pas de solution")
		print("Reduced form:", reduceForm(eq))
		print("Polynomial degree: 2")
		print("Discriminant is strictly negativ, there is no solution")
	elif delta == 0:
		print("Delta etant egale à 0, on sait qu'il y a qu'une seul solution : -b/2a =", "{}/2{}".format(eq[1], eq[2]), "=", eq[1] / (2 * eq[2]))
		print("Reduced form:", reduceForm(eq))
		print("Polynomial degree: 2")
		print("Discriminant is equal to 0, the solution is:\n", -eq[1] / (2 * eq[2]), sep="")
	else:
		print("delta =", delta, "a =", eq[2], "b =", eq[1], "c =", eq[0])
		print("Delta etant positif, on sait qu'il y a deux solutions : (-b-racine(delta)) / 2a et (-b+racine(delta)) / 2a = ", "(-{0}-racine({1})) / 2{2} et (-{0}-racine({1})) / 2{2}".format(eq[1], delta, eq[2]), "=", ((-eq[1] - delta**(1/2)) / (2 * eq[2])), "et", ((-eq[1] + delta**(1/2)) / (2 * eq[2])))
		print("Reduced form:", reduceForm(eq))
		print("Polynomial degree: 2")
		print("Discriminant is strictly positive, the two solutions are:\n",(-eq[1] - delta**(1/2)) / (2 * eq[2]), "\n", (-eq[1] + delta**(1/2)) / (2 * eq[2]), sep="")

def solve(eq):

	eq = eq.replace(" ","")
	eq = eq.split('=')

	eqS = parse(eq[0]), parse(eq[1])
	eq = [eqS[0][0] - eqS[1][0], eqS[0][1] - eqS[1][1], eqS[0][2] - eqS[1][2]]
	if eq[2] == 0:
		solveFirstDegree(eq)
	else:
		solveSecondDegree(eq)
	


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("usage : ./computor \"equation\"")
	elif len(sys.argv) > 2:
		print("usage : ./computor \"equation\"\nYou must enter the equation in single string")
	elif not checkEquation(sys.argv[1]):
		print("Please write a correct equation")
	else:
		solve(sys.argv[1])
		
		