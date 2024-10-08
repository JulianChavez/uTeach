import os
import openai
openai.api_key = ''

def get_user_prompt():
    return input("Say a fact: ")

def get_type():
    return input("Enter a type: ")

def scoreText(textSegment, scoreType):
    tokenCount = 1
    gradeCompletion = openai.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages = [
            {"role": "user", "content": "Give a number between 1 and 100 grading the " + scoreType + " of the following statement: " + textSegment}
        ],
        max_tokens=tokenCount,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    if not gradeCompletion.choices[0].message.content.isnumeric():
        gradeCompletion.choices[0].message.content = 5
    tokenCount = 110 - (3*(int(gradeCompletion.choices[0].message.content)+1))
    if tokenCount <= 0:
        tokenCount = 10
    adviceCompletion = openai.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages = [
            {"role": "user", "content": "Provide an explanation less than " + str(tokenCount) + " words on how " + scoreType + " the following statement is or how to improve it: " + textSegment}
        ],
        max_tokens=tokenCount,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    return([str(gradeCompletion.choices[0].message.content), adviceCompletion.choices[0].message.content])

def main():
    print("'exit' to quit.")

    while True:
        scoreType = get_type()
        textSegment = get_user_prompt()
        if textSegment.lower() == "exit":
            print("Program terminated.")
            break
        
        response = scoreText(textSegment, scoreType)
        print("ChatGPT Grade of " + scoreType + ": " + str(response[0]))
        print("ChatGPT Advice of " + scoreType + ": " + str(response[1]))

if __name__ == "__main__":
    main()
