from openai import OpenAI

client = OpenAI(
    api_key='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'
)

def chatting(user_query):
    response = client.chat.completions.create(
        n=10,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content":  "너는 오직 숫자로만 답할 수 있어. 고객의 요구사항이 2개 이상이라면 콤마로 구분한 숫자들을 출력해.\
             만약 고객이 경비를 불러달라고 하면 1. 고객이 사이다를 달라고 하면 2, 콜라를 달라고 하면 3을 출력해.\
             비슷한 방식으로 환타는 4, 밀키스는 5, 닥터페퍼를 달라고 했을 땐 6을 출력하면 돼."
             },
            {"role": "user", "content": user_query}
        ]
    )
    return response.choices
    
if __name__ == '__main__':
    for idx, choice in enumerate(chatting("경비불러! 환타도 내놔! 닥페도! 콜라도!")):
        print(f"Choice {idx}: {choice}")