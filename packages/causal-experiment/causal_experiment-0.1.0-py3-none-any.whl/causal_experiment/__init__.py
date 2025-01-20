import random
import argparse
from causal_experiment.dataset import generate_dataset
from causal_experiment.train_small_causal_model import training
from devtools import debug

def main() -> None:
    parser = argparse.ArgumentParser(description="Causal Experiment Application")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Subparser for 'generate' command
    generate_parser = subparsers.add_parser("generate", help="Generate datasets")
    generate_parser.add_argument(
        "-o",
        type=str,
        required=False,
        help="Comma-separated list to remove from the dataset"
    )
    generate_parser.set_defaults(func=handle_generate)


    parser.add_argument(
        "--train",
        action="store_true",
        help="Run training"
    )
    parser.add_argument(
        "--test",
        type=str,
        help="Run manual test with a given prompt"
    )

    args = parser.parse_args()


    if args.command == "generate":
        args.func(args)
    elif args.train:
        call_training()
    elif args.test:
        prompt = args.test
        result = call_test(prompt)
        print(f"Test result: {result}")
    else:
        print("No valid command provided. Use --help for usage information.")
        
def handle_generate(args):
    if args.o:
        to_omit_list = args.o.split(";")
        call_generate_dataset(to_omit_list)
    else:
        print("No omission list provided. Generating full dataset...")

    

def call_generate_dataset(to_omit_list) -> None:
    random.seed(42)
    generate_dataset(20000, "dataset/train.jsonl",to_omit_list)
    generate_dataset(2000, "dataset/valid.jsonl",to_omit_list)
    generate_dataset(2000, "dataset/test.jsonl",to_omit_list)
    
def call_training() -> None:
    training()
    
    
def call_test(prompt_text: str) -> dict:
    import torch
    from transformers import GPT2LMHeadModel, GPT2TokenizerFast

    from causal_experiment.dataset import manual_test
    manual_res = manual_test(prompt_text)
    debug(manual_res)
    
    model_path = "./out/tiny-gpt2-causal/final"
    tokenizer = GPT2TokenizerFast.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    model.eval()



    input_ids = tokenizer.encode(prompt_text, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=64,
            num_return_sequences=1,
            do_sample=False
        )
        
    output = tokenizer.decode(output[0])
    debug(output)
    return str(output)

