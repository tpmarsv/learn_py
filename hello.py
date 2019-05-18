# Если ничего не введено, то input вернет none и при проверке будет false
for_who = input("Напиши свое имя и я поприветствую тебя по-английски:  ")
if for_who:
    print(f"Hello {for_who}")
else:
    print("Тогда я попривествую весь мир: Hello world!")
