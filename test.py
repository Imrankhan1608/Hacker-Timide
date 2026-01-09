# ce ficher m'as permis de tester quelque logique utilise dans le script principale
nb_sr = 4
nb_h = 4
nb_f = []
nb_int = ''
for i in range(nb_sr):
    nb_f.append("1")


for i in range(nb_h):
    nb_f.append("0")
print(nb_f)


for partie in nb_f:
    nb_int = nb_int + partie
print(nb_int)

decimal = int(nb_int,2)
print(decimal)

nb = "11111111"
nb = int(nb,2)
print(nb)