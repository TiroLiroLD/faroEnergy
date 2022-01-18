import re
import string

''' 
Inicialmente foi usado apenas o dicionário. No entanto, vamos usar a lista para ordenar as palavras em ordem alfabética. 
'''
word_list = []
word_count_dict = {}

with open("input/big.txt", 'r') as file:
    raw_text = file.read()

'''
Abaixo, usamos re.split com um regex contendo caracteres delimitadores de frases (ponto ".", exclamação "!" e 
interrogação "?") para criar uma lista de frases e preparar nosso dicionário já com a informaçao do número da frase onde
a palavra está inserida. Criar o dicionário sem a lista, ou seja, separando todas as palavras do texto principal, teria
maior tempo de execução, pois não teríamos a informaçao o número da frase sem iterar novamente pelo texto, ou um código 
maior, por ter a necessidade de verificar se a próxima palavra está em outra frase pelo número de espaços em branco. 
'''
phrases = re.split(r"[.!?]", raw_text)
phrase_number = 0

'''
Antes de usar um .split() para separar as palavras de uma frase, usamos um regex transformando tudo que não for uma
letra em espaços em branco. Estamos assumindo que não devem ser contabilizados números ou caracteres especiais. 

Estamos utilizando o método .lower() na primeira palavra para que não sejam contabilizadas como palavras diferentes 
aquelas que comecem com letra maiúscula no início de uma frase. Siglas, substantivos próprios e comuns no início de 
frases podem ser afetados com essa opção, porém com menor frequência quando comparado ao uso do .lower() em todas as 
palavras. 
'''
for phrase in phrases:
    phrase_number += 1
    phrase = re.sub(r"[^A-Za-z]", " ", phrase)
    words = phrase.split()
    if len(words) > 0:
        words[0] = words[0].lower()
    for word in words:
        if word in word_list:
            word_count_dict[word]["count"] += 1
            word_count_dict[word]["phrases"].append(phrase_number)
        else:
            word_count_dict[word] = {"count": 1, "phrases": [phrase_number]}
            word_list.append(word)
file.close()

word_list.sort()


def provide_index_letter(wordNumber):
    """
    Criamos o método provide_index_letter para que possamos ter um bullet ou enumeração de palavras utilizando letras
    como índices. O método é chamado de forma recursiva, de forma a garantir que não haverá erro em textos grandes
    após todas as letras do alfabeto serem utilizadas, nos dando como resultado algo na forma:

    ...
    y. AGREE: {4: 20000 20001 29329 29330}
    z. AGREEMENT: {2: 20001 29330}
    aa. AGRICULTURE: {3: 7517 7883 15029}
    ab. AK: {2: 20044 29373}
    ...

    """
    if wordNumber < len(string.ascii_lowercase):
        return string.ascii_lowercase[wordNumber]
    else:
        return provide_index_letter(wordNumber // len(string.ascii_lowercase) - 1) \
               + provide_index_letter(wordNumber % len(string.ascii_lowercase))


'''
Terminamos a execução armazenando o resultado em um arquivo log.txt
'''
with open("output/log.txt", 'w') as file:
    for index in range(len(word_list)):
        word = word_list[index]
        indexLetter = provide_index_letter(index)
        ocurrences = ""
        for ocurrence in range(word_count_dict[word]["count"]):
            ocurrences += " " + str(word_count_dict[word]['phrases'][ocurrence])
        file.write(f"{indexLetter}. {word}: " + "{" + f"{word_count_dict[word]['count']}:{ocurrences}" + "}\n")
file.close()
