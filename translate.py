import jsonlines
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json

def translate_between_languages(text, model):
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForSeq2SeqLM.from_pretrained(model)

    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
    output = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return output[0]

def translate_english_to_swedish(english_text):
    swedish_text = translate_between_languages(english_text, "Helsinki-NLP/opus-mt-en-sv")

    # check for the characters å ä ö and make sure they are in the correct format
    #swedish_text = clean_åäö(swedish_text)

    return swedish_text
 
def clean_åäö(text):
    ö = "\u00f6"
    å = "\u00e5"
    ä = "\u00c4"

    if ö in text:
        text = text.replace(ö, 'ö')
    elif å in text:
        text = text.replace(å, 'å')
    elif ä in text:
        text = text.replace(ä, 'ä')

    return text


def translate_jsonl(input_file, output_file):
    # open the file as json
    with open(input_file) as f:
        data = json.load(f)
        with open(output_file, mode='w') as writer:
            # write beginning of json
            writer.write('[')
            for line in data:
                instruction = line['instruction']
                input_text = line['input']
                output_text = line['output']

                instruction_translated = translate_english_to_swedish(instruction)
                input_text_translated = translate_english_to_swedish(input_text) if input_text else ""
                output_text_translated = translate_english_to_swedish(output_text)

                # check for the characters å ä ö and make sure they are in the correct format


                line['instruction'] = instruction_translated
                line['input'] = input_text_translated
                line['output'] = output_text_translated

                json.dump(line, writer, ensure_ascii=False)
                # write new line character
                writer.write(',\n')

                # writer.write(str(line))
            # write end of json
            writer.write(']')

translate_jsonl('alpaca_data.json', 'tiny_alpaca_swedish.json')