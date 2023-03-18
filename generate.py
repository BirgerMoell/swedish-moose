import torch
from peft import PeftModel
import transformers

assert (
    "LlamaTokenizer" in transformers._import_structure["models.llama"]
), "LLaMA is now in HuggingFace's main branch.\nPlease reinstall it: pip uninstall transformers && pip install git+https://github.com/huggingface/transformers.git"
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig

tokenizer = LlamaTokenizer.from_pretrained("decapoda-research/llama-7b-hf")

model = LlamaForCausalLM.from_pretrained(
    "decapoda-research/llama-7b-hf",
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
)
# model = PeftModel.from_pretrained(
#     model, "tloen/alpaca-lora-7b", torch_dtype=torch.float16
# )

swedish_model = "/home/bmoell/llama/alpaca-lora/lora-alpaca-swedish-large"
english_model = "/home/bmoell/llama/alpaca-lora/lora-alpaca"

model = PeftModel.from_pretrained(
    model, swedish_model, torch_dtype=torch.float16)


def generate_prompt(instruction, input=None):
    if input:
        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input}

### Response:"""
    else:
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Response:"""


model.eval()


def evaluate(instruction, input=None, **kwargs):
    prompt = generate_prompt(instruction, input)
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"].cuda()
    # generation_config = GenerationConfig(
    #     temperature=0.1,
    #     top_p=0.75,
    #     num_beams=4,
    #     **kwargs,
    # )

    generation_config = GenerationConfig(
        temperature=1.0,
        top_p=0.5,
        num_beams=4,
        **kwargs,
    )

    generation_output = model.generate(
        input_ids=input_ids,
        generation_config=generation_config,
        return_dict_in_generate=True,
        output_scores=True,
        max_new_tokens=2048,
    )
    s = generation_output.sequences[0]
    output = tokenizer.decode(s)
    return output.split("### Response:")[1].strip()


englis_prompts = [
        "Tell me about alpacas.",
        "Tell me about the president of Mexico in 2019.",
        "Tell me about the king of France in 2019.",
        "List all Canadian provinces in alphabetical order.",
        "Write a Python program that prints the first 10 Fibonacci numbers.",
        "Write a program that prints the numbers from 1 to 100. But for multiples of three print 'Fizz' instead of the number and for the multiples of five print 'Buzz'. For numbers which are multiples of both three and five print 'FizzBuzz'.",
        "Tell me five words that rhyme with 'shock'.",
        "Translate the sentence 'I have no mouth but I must scream' into Spanish.",
        "Count up from 1 to 500.",
    ]

swedish_prompts = [
        "Skriv en saga om en alpaka.",
        "Berätta om Mexikos president år 2019.",
        "Berätta om Frankrikes kung år 2019.",
        "Lista alla kanadensiska provinser i alfabetisk ordning.",
        "Skriv ett Python-program som skriver ut de första 10 Fibonacci-talen.",
]


if __name__ == "__main__":
    # testing code for readme
    for instruction in swedish_prompts:
        print("Instruction:", instruction)
        print("Response:", evaluate(instruction))
        print()