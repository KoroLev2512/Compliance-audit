from tkinter import filedialog


# открываем файл с БД
def input_data():
    filepath_bd_1 = filedialog.askopenfilename()
    if filepath_bd_1 != "":
        with open(filepath_bd_1, "r") as file:
            print("Открыт файл БД 1")
    filepath_bd_2 = filedialog.askopenfilename()
    if filepath_bd_2 != "":
        with open(filepath_bd_2, "r") as file:
            print("Открыт файл БД 2")


# сохраняем текст из текстового поля в файл
def optimisation():
    filepath = filedialog.asksaveasfilename()
    if filepath != "":
        with open(filepath, "w") as file:
            file.write('huy')
            print("Файл сохранен")
