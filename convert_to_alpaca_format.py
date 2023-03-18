import json

def convert_jsonl_format(input_file, output_file):
    converted_data = []

    with open(input_file, 'r') as reader:
        for line in reader:
            original_data = json.loads(line)
            user_text = original_data['user_text']
            assistant_response = original_data['assistant_response']

            new_data = {
                'instruction': user_text,
                'input': "",
                'output': assistant_response
            }

            converted_data.append(new_data)

    with open(output_file, 'w') as writer:
        json.dump(converted_data, writer, ensure_ascii=False, indent=2)

# Replace 'input_file.jsonl' and 'output_file.json' with your input and output file names
convert_jsonl_format('oa_swedish_super_cleaned.jsonl', 'oa_swedish_alpaca.json')