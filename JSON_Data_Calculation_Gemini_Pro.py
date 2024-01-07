import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def generate():
  model = GenerativeModel("gemini-pro")
  responses = model.generate_content(
    """You are a expert in extracting information from JSON content.
Based on the JSON document below, what is the  revenue in 2022. Don\'t make up data, if the information cannot be found in the provided context with 100% certainty then just say not available in context. 
Analysed if calculation is required, and if it is then detail step by step the approach and value used for the calculation.

JSON content:

```json
{
\"table\": {
\"headers\": [
\"Ended December 31,\",
\"2020\",
\"2021\",
\"2022\"
],
\"body\": [
[
\"Google Search & other\",
\"104,062\",
\"148,951\",
\"162,450\"
],
[
\"YouTube ads\",
\"19,772\",
\"28,845\",
\"29,243\"
],
[
\"Google Network\",
\"23,090\",
\"31,701\",
\"22,473\"
],
[
\"Google advertising\",
\"146,924\",
\"209,497\",
\"224,473\"
],
[
\"Google Services total\",
\"168,635\",
\"237,528\",
\"253,528\"
],
[
\"Google Cloud\",
\"657\",
\"753\",
\"1,068\"
],
[
\"Other Bets\",
\"13,059\",
\"19,206\",
\"26,280\"
],
[
\"Hedging gains (losses)\",
\"(176)\",
\"176\",
\"195\"
],
[
\"Total revenues\",
\"182,527\",
\"257,637\",
\"282,836\"
]
]
}
}
```""",
    generation_config={
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 1
    },
  stream=True,
  )
  
  for response in responses:
      print(response.candidates[0].content.parts[0].text)


if __name__ == "__main__":
    generate()



