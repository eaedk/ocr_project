import gradio as gr
import os

# from transformers import (
#     PerceiverFeatureExtractor,
#     PerceiverForImageClassificationConvProcessing,
# )

# import requests
# from PIL import Image


# feature_extractor = PerceiverFeatureExtractor.from_pretrained(
#     "deepmind/vision-perceiver-conv"
# )
# model = PerceiverForImageClassificationConvProcessing.from_pretrained(
#     "deepmind/vision-perceiver-conv"
# )


# def inference(image):
#     # prepare input
#     inputs = feature_extractor(image, return_tensors="pt").pixel_values
#     # forward pass
#     outputs = model(inputs)
#     logits = outputs.logits
#     return "Predicted class:" + model.config.id2label[logits.argmax(-1).item()]

def inference(file):


demo = gr.Blocks()

with demo:
    gr.Markdown(
        """
    # OCR App made using Gradio"""
    )
    #  : A General Architecture for Structured Inputs & Outputs
    # Start by adding a image, this demo uses deepmind/vision-perceiver-conv model from Hugging Face model Hub for a image classification demo, for more details read the [model card on Hugging Face](https://huggingface.co/deepmind/vision-perceiver-conv)

    # inp = gr.Image(type="pil")
    inp = gr.File()
    out = gr.Label()

    button = gr.Button(value="Run")
    # gr.Examples(
    #     examples=[os.path.join(os.path.dirname(__file__),"data" ,"lion.jpeg")],
    #     inputs=inp,
    #     outputs=out,
    #     fn=inference,
    #     cache_examples=False)

    button.click(fn=inference, inputs=inp, outputs=out)


demo.launch()
