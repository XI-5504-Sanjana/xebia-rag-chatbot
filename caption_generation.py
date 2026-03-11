
import base64
import mimetypes
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

#Base64 is a way to convert binary data (like images) into text format. open the image file, read the file as bianry data , convert binary data -> base 64 string -> return the string 
def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")#the image file -> converted -> text string , the text string is wht gets sents to ai model

#detect wht type of image file it is ?
def guess_mime_type(image_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        return "image/png"
    return mime_type

#it sends the image to the ai model and asks it to describe the diagram .
def generate_caption(image_path: str, model: str = "gpt-4o-mini") -> str:
    """
    Generate a technical caption for a car manual image.
    Returns a plain text string; on error returns a fallback message.
    """

    base64_image = encode_image_to_base64(image_path) #encode the image 
    mime_type = guess_mime_type(image_path) #detect image type 

    data_url = f"data:{mime_type};base64,{base64_image}"

    system_prompt = (
        "You are an assistant that writes concise, technical captions for images from a "
        "car owner's manual. Focus on clearly identifying dashboard controls, buttons, "
        "switches, indicators, labels, and what the diagram is illustrating. Use clear, "
        "neutral language and do not invent anything that is not visible."
    )

    user_prompt = (
        "Describe this car manual image in 1–3 sentences.\n"
        "1) Name all visible controls, buttons, switches, indicators, and labels.\n"
        "2) Explain what the diagram is mainly illustrating (for example, the location or "
        "function of a control).\n"
        "3) Do NOT guess about behavior or features that are not directly visible in the image."
        
    )

    try:

        response = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": data_url}
                        },
                    ],
                },
            ],
        )

        caption = response.choices[0].message.content.strip()

        return caption

    except Exception as e:
        print(f"Caption generation failed for {image_path}: {e}")
        return "Car manual diagram"