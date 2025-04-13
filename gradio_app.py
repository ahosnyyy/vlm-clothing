import gradio as gr
import requests
import json
import io
from PIL import Image

def analyze_clothing(image, model):
    if image is None:
        return "No image provided"
    
    API_URL = "http://localhost:8000/analyze-clothing/"
    
    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    
    # Determine format - try JPG first, fallback to PNG
    try:
        if isinstance(image, str):
            # If image is a filepath (from examples)
            pil_image = Image.open(image)
        else:
            pil_image = Image.open(image)
            
        try:
            pil_image.save(img_byte_arr, format='JPEG')
            content_type = 'image/jpeg'
            filename = 'image.jpg'
        except Exception:
            img_byte_arr = io.BytesIO()  # Reset buffer
            pil_image.save(img_byte_arr, format='PNG')
            content_type = 'image/png'
            filename = 'image.png'
        
        img_byte_arr.seek(0)
        files = {"image": (filename, img_byte_arr, content_type)}
        data = {"model": model}
        response = requests.post(API_URL, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            output = f"""
            Description: {result['description']}
            
            Clothing Type: {', '.join(result['clothing_type'])}
            Sleeve Length: {result['sleeve_length']}
            Color: {result['color']}
            Wearing Glasses: {'Yes' if result['glasses'] else 'No'}
            Wearing Headwear: {'Yes' if result['headwear'] else 'No'}
            Accessories: {', '.join(result['accessories']) if result['accessories'] else 'None'}
            
            Model Used: {model}
            """
            return output
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Error processing image: {str(e)}"

# Create Gradio interface
demo = gr.Interface(
    fn=analyze_clothing,
    inputs=[
        gr.Image(type="filepath"),
        gr.Dropdown(
            choices=["gemma3:12b", "llama3.2-vision:11b", "gemma3:4b"],
            value="llama3.2-vision:11b",
            label="Model"
        )
    ],
    outputs=gr.Textbox(label="Analysis Results", lines=10),
    title="Clothing Analysis",
    description="Upload an image to analyze the clothing and accessories worn by the person in the image.",
    examples=[["samples/F1.JPG", "gemma3:12b"], ["samples/F2.JPG", "gemma3:12b"], ["samples/M1.JPG", "gemma3:12b"]]
)

if __name__ == "__main__":
    demo.launch()