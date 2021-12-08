import math


def bubble_sort(str, prob):
    for i in range(len(str) - 1):
        for j in range(len(str) - 1):
            if prob[j] < prob[j + 1]:
                prob[j], prob[j + 1] = prob[j + 1], prob[j]
                str[j], str[j + 1] = str[j + 1], str[j]


with open("text.txt", "r", encoding='utf-8') as func:
    text = func.read()
text = text.lower()

# поиск уникальных символов
alphabet = []
for j in range(len(text)):
    if text[j] not in alphabet:
        alphabet.append(text[j])

# расчет вероятности появления символа в тексте
probability = []
for i in range(len(alphabet)):
    probability.append(text.count(alphabet[i]))
    probability[i] /= len(text)

# сортировка по убыванию вероятности
bubble_sort(alphabet, probability)

sum_dictionary = {}  # словарь хранящий узлы бинарного дерева
keys = []  # список хранящий ключи к sum_dictionary

# расчет таблицы Хаффмана и значений бинарного дерева
Huffman_table = []
Huffman_table.append(probability)
temp = probability[:]
for i in range(len(alphabet) - 1):
    sum = temp[-1] + temp[-2]
    sum_dictionary[sum] = [temp[-2], temp[-1]]
    keys.append(sum)
    del temp[-1]
    temp[-1] = sum
    temp.sort(reverse=True)
    Huffman_table.append(temp[:])

code = []  # список хранящий словари, где ключ - вероятность появления, значение - код, найденный по методике Хаффмана
for i in range(len(alphabet)):
    code.append({probability[i]: ""})


# проход бинарного дерева в глубину для вычисления кода символа по методике Хаффмана
def generate_code(code, str, current_str, current_prob, prob_level_up=1.0):
    current_str += str

    for i in range(len(alphabet)):
        if current_prob == probability[i] and code[i][probability[i]] == "":
            code[i][probability[i]] = current_str
            return
    prob_level_up = current_prob
    current_prob = sum_dictionary[current_prob][0]
    generate_code(code, "1", current_str, current_prob, prob_level_up)

    current_prob = prob_level_up
    current_prob = sum_dictionary[current_prob][1]
    generate_code(code, "0", current_str, current_prob, prob_level_up)


generate_code(code, "", "", keys[len(alphabet) - 2], 1.0)

# форматированный вывод таблицы, содержащей символ, вероятность появления и код, созданный по методике Хаффмана
def print_code(code, alphabet,probability):
    max_length_probability = len(str(probability[0]))
    for i in range(len(alphabet)):
        if len(str(probability[i])) > max_length_probability:
            max_length_probability = len(str(probability[i]))

    max_length_code = len(code[0][probability[0]])
    for i in range(len(alphabet)):
        if len(code[i][probability[i]]) > max_length_code:
            max_length_code = len(code[i][probability[i]])

    print("+---+-" + "".ljust(max_length_probability, "-") + "-+-" + "".ljust(max_length_code, "-") + "-+")
    for i in range(len(alphabet)):
        temporary = "| " + alphabet[i] + " | " + str(probability[i]).center(max_length_probability) + " | " + code[i][
            probability[i]].ljust(max_length_code) + " |"
        print(temporary)
    print("+---+-" + "".ljust(max_length_probability, "-") + "-+-" + "".ljust(max_length_code, "-") + "-+")


print_code(code, alphabet,probability)


def coding_message(message, code, alphabet):
    coded_messge = ""
    message = message.lower()
    message = list(message)
    for i in range(len(message)):
        for j in range(len(alphabet)):
            if message[i] == alphabet[j]:
                coded_messge += code[j][probability[j]]

    return coded_messge


def decoding_message(coded_message, code, alphabet):
    decoded_message = ""
    coded_message = list(coded_message)
    current_symbol = ""
    for i in range(len(coded_message)):
        current_symbol += coded_message[i]
        for j in range(len(alphabet)):
            if code[j][probability[j]] == current_symbol:
                decoded_message += alphabet[j]
                current_symbol = ""

    return decoded_message


coded_message = coding_message("Шизофрения", code, alphabet)
print(coded_message)
decoded_message = decoding_message(coded_message, code, alphabet)
print(decoded_message)

entropy = 0
for i in range(len(probability)):
    entropy += probability[i] * math.log2(1 / probability[i])
print("Iср(энтропия) = " + str(entropy))

average_length = 0
for i in range(len(probability)):
    average_length += probability[i] * len(code[i][probability[i]])
print("Nср(среднее количество двоичных разрядов разрядов) = " + str(average_length))
