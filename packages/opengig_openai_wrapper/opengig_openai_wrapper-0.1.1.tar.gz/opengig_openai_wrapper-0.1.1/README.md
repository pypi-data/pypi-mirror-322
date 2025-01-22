# NextJS Project
    - Add openai-wrapper.ts in lib folder in NextJS Project
    - 

# Examples
# Example usage
if __name__ == "__main__":
    # Initialize the wrapper
    wrapper = SimpleOpenAIWrapper(
        service_provider="openai", 
        max_retries=3
    )

    # Generate a response
    system_prompt = "You are a helpful assistant."
    user_prompt = "Explain the significance of the Pythagorean theorem."
    response = wrapper.generate_response(
        system_prompt=system_prompt, 
        user_prompt=user_prompt, 
        model="gpt-4", 
        max_tokens=150, 
        output_format="str"
    )
    print("Response:", response)