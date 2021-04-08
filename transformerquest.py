import string
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForQuestionAnswering
import torch
from random import randint
import os

#Adapt to your case 
path ="data/"
#story="amelie/" #story contains the name of the dir to use this run. The story of the dark knight is in "default/"
story="default/"

device = 'cuda' if torch.cuda.is_available() else 'cpu'



tokenizerqa = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
modelqa = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")
tokenizer = AutoTokenizer.from_pretrained("gpt2-large") #Don't forget to change according to your needs
model = AutoModelForCausalLM.from_pretrained("gpt2-large")


model = model.to(device)

model.config.pad_token_id = model.config.eos_token_id

#Some utility functions from storybro: https://github.com/storybro/storybro

def cut_trailing_quotes(text):
    num_quotes = text.count('"')
    if num_quotes % 2 == 0:
        return text
    else:
        final_ind = text.rfind('"')
        return text[:final_ind]

def cut_trailing_sentence(text):
    text = standardize_punctuation(text)
    last_punc = max(text.rfind("."), text.rfind("!"), text.rfind("?"))
    if last_punc <= 0:
        last_punc = len(text) - 1
    et_token = text.find("<")
    if et_token > 0:
        last_punc = min(last_punc, et_token - 1)
    act_token = text.find(">")
    if act_token > 0:
        last_punc = min(last_punc, act_token - 1)
    text = text[:last_punc]
    text = cut_trailing_quotes(text)
    return text+"."

def capitalize_helper(string):
    string_list = list(string)
    string_list[0] = string_list[0].upper()
    return "".join(string_list)

def standardize_punctuation(text):
    text = text.replace("’", "'")
    text = text.replace("`", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    return text

def capitalize_first_letters(text):
    first_letters_regex = re.compile(r"((?<=[\.\?!]\s)(\w+)|(^\w+))")
    def cap(match):
        return capitalize_helper(match.group())
    result = first_letters_regex.sub(cap, text)
    return result


#Read narrative file with the format described in the README

def read_narrative(namefile="narrative1.txt"): 
    filenar = open(path+story+namefile)
    READEN_TEXT = filenar.readlines()
    filenar.close()
    first_sentence = READEN_TEXT[0]
    PADDING_TEXT = READEN_TEXT[2]
    second_sentence = READEN_TEXT[4]
    keyword = READEN_TEXT[6]
    last_sentence = READEN_TEXT[8]
    return first_sentence, PADDING_TEXT, second_sentence, keyword, last_sentence

#Dialog function to extract pieces of information from the story of the narrative

def ask_enigma(first_sentence="Hello, the Dark Knight is listening!\n", PADDING_TEXT=""):
    print(first_sentence)
    while True:
        print("\nAny question? ")
        quest = input()
        print("\n")
        if quest[-1]=="?":
            inputsqa = tokenizerqa(quest, PADDING_TEXT, add_special_tokens=True, return_tensors="pt")
            inputqa_ids = inputsqa["input_ids"].tolist()[0]
            outputsqa = modelqa(**inputsqa, return_dict=True)
            answer_start_scores = outputsqa.start_logits
            answer_end_scores = outputsqa.end_logits
            answer_start = torch.argmax(answer_start_scores)
            answer_end = torch.argmax(answer_end_scores) + 1
            prompt = tokenizerqa.convert_tokens_to_string(tokenizerqa.convert_ids_to_tokens(inputqa_ids[answer_start:answer_end]))
            prompt = capitalize_first_letters(prompt)
            if answer_start.item()>=answer_end.item()-1:
                prompt="It's a good question!"
        elif re.search(r"\bno\b",quest.lower()):
                break           
        else:
            prompt=quest
            PADDING_TEXT=PADDING_TEXT+prompt
            prompt = ""
        PADDING_TEXT=PADDING_TEXT+" "
        pad_length=len(PADDING_TEXT)
        inputs = tokenizer.encode(PADDING_TEXT + prompt, add_special_tokens=False, return_tensors="pt", verbose=False)
        inputs = inputs.to(device)
        outputs = model.generate(inputs, max_length=len(inputs[0])+randint(50,150), do_sample=True, top_p=0.95, top_k=60)
        generated = tokenizer.decode(outputs[0][0:-1])[pad_length:]
        generated = cut_trailing_sentence(generated)
        print(generated)
    return True

#Function to check if the player can pass to the next sequence

def ask_end(first_sentence="\nWhat will you do now? ", PADDING_TEXT="Hello", trueresponse=r"\btintagel\b", endprompt="Ok, you can to the castle of Tintagel! Good luck!"):
    inputs_pad = tokenizer.encode(PADDING_TEXT, add_special_tokens=False, return_tensors="pt")
    pad_length = len(tokenizer.decode(inputs_pad[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))
    print(first_sentence+" ")
    response = input()
    print("\n")
    if re.search(trueresponse,response.lower()):
        prompt = endprompt
        inputs = tokenizer.encode(PADDING_TEXT + " " + prompt, add_special_tokens=False, return_tensors="pt", verbose=False)
        inputs=inputs.to(device)        
        outputs = model.generate(inputs, max_length=len(inputs[0])+randint(50,150), do_sample=True, top_p=0.95, top_k=60)
        generated = tokenizer.decode(outputs[0][0:-1])[pad_length:]
        generated = cut_trailing_sentence(generated)
        generated = capitalize_first_letters(generated)
        print(generated)
        return True
    else:
        return False

#The final function, if the response is the good one the player wins

def ask_final(first_sentence="Hello", PADDING_TEXT="Hello", second_sentence="\nWhat is the code of the safe?",keyword="123456", endprompt="Good by!"):
    inputs_pad = tokenizer.encode(PADDING_TEXT, add_special_tokens=False, return_tensors="pt")
    pad_length = len(tokenizer.decode(inputs_pad[0], skip_special_tokens=True, clean_up_tokenization_spaces=True))
    print(first_sentence)
    print(second_sentence+" ")
    response=input()
    print("\n")
    trueresponse = r'\b{}\b'.format(keyword)  
    prompt = endprompt
    inputs = tokenizer.encode(PADDING_TEXT + " " + prompt, add_special_tokens=False, return_tensors="pt", verbose=False)
    inputs=inputs.to(device)
    outputs = model.generate(inputs, max_length=len(inputs[0])+randint(50,150), do_sample=True, top_p=0.95, top_k=60)
    generated = tokenizer.decode(outputs[0][0:-1])[pad_length:]
    generated = cut_trailing_sentence(generated)
    generated = capitalize_first_letters(generated)
    print(generated)
    if re.search(trueresponse,response.lower()):
        print("\nYou win!!!\n")
    else:
        print("\nSorry, you loose!!!")
    return


#Run a sequence of the game (question+action)

def run_round(first_sentence="Hello", PADDING_TEXT="Hello", second_sentence="\nWhat will you do now? ", keyword="tintagel", endprompt="Ok, you can to the castle of Tintagel! Good luck!"):
    trueresponse = r'\b{}\b'.format(keyword)
    while True:
       print("\n")
       ask_enigma(PADDING_TEXT=PADDING_TEXT,first_sentence=first_sentence)
       if ask_end(PADDING_TEXT=PADDING_TEXT, first_sentence=second_sentence, trueresponse=trueresponse,  endprompt=endprompt):
        return
       else:
           first_sentence="\nI think that you need more informations\n"

#Read all the files in the directory data and sort them by alphabetical order

all_files = sorted(os.listdir(path+story))
for namefile in all_files[0:-1]:
    first_sentence, PADDING_TEXT, second_sentence, keyword, last_sentence=read_narrative(namefile)
    run_round(first_sentence=first_sentence, PADDING_TEXT=PADDING_TEXT, second_sentence=second_sentence[0:-1], keyword=keyword[0:-1], endprompt=last_sentence)

#The final sequence do decide if the player wins
print("\n")    
first_sentence, PADDING_TEXT, second_sentence, keyword, last_sentence=read_narrative(all_files[-1])
ask_final(first_sentence=first_sentence, PADDING_TEXT=PADDING_TEXT, second_sentence=second_sentence[0:-1], keyword=keyword[0:-1], endprompt=last_sentence)





        

