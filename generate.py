import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def main():
    # Set the GPU device index
    device_index = 0  # Change this to the desired GPU device index

    # Set the device
    torch.cuda.set_device(device_index)

    # Check if CUDA is available
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"Using CUDA device: {torch.cuda.get_device_name(device_index)}")
    else:
        device = torch.device("cpu")
        print("CUDA is not available. Using CPU instead.")

    # Load the fine-tuned GPT-2 model and tokenizer
    model_path = "./model"  # Path to the directory where the fine-tuned model is saved
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained(model_path)
    model.to(device)
    model.eval()

    # Set the generation parameters
    max_length = 100  # Maximum number of tokens to generate
    num_return_sequences = 1  # Number of generated sequences to return

    # Prompt for text generation
    prompt = "Once"

    # Encode the prompt
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)

    # Generate text
    padding_token_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    attention_mask = input_ids.ne(padding_token_id).to(device)
    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        temperature=2.7,  # Adjust the temperature for controlling the randomness of the model
    )

    # Decode and print the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print(generated_text)
    with open('./output/output.txt', 'w', encoding='utf-8', errors='ignore') as f:
        f.write(generated_text)

# Run the main function
if __name__ == "__main__":
    main()
