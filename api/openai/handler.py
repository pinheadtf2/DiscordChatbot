import requests

from rich.console import Console

console = Console()

headers = {
    "Content-Type": "application/json"
}
max_tokens = 180


def generate_response(url: str, chat_history: [], character: str, username: str, preferred_name: str) -> [str, []]:
    request = {
        "messages": chat_history,
        "mode": "chat-instruct",
        "max_tokens": max_tokens,
        "character": "Sabine",
        "name1": f"{preferred_name}",
        "user_bio": f"Username: f{username}\nPreferred Name: {preferred_name}",
        "stop": ["\n\n\n", "\n#", "\n##", "\n###", "##", "###", "</s>", "000000000000", "1111111111",
                 "0.0.0.0.", "1.1.1.1.", "2.2.2.2.", "3.3.3.3.", "4.4.4.4.", "5.5.5.5.", "6.6.6.6.", "7.7.7.7.",
                 "8.8.8.8.", "9.9.9.9.", "22222222222222", "33333333333333", "4444444444444444", "5555555555555",
                 "66666666666666", "77777777777777", "888888888888888", "999999999999999999", "01010101", "0123456789",
                 "<noinput>", "<nooutput>"],
    }
    console.print(request)

    response = requests.post(url, headers=headers, json=request, verify=False)
    if response.status_code == 200:
        response_json = response.json()
        assistant_message = response_json['choices'][0]['message']['content']
        console.print(response_json)
        chat_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message, chat_history
    else:
        console.print(response)
        console.print(response.json())
