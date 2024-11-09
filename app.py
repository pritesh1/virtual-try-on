import os
import cv2
import gradio as gr
from gradio_client import Client as GradioClient, handle_file

# Gradio Client for Nymbo Virtual Try-On API
gradio_client = GradioClient("Nymbo/Virtual-Try-On")

# Function to interact with the Gradio API
def gradio_app(person_image_path, garment_image_path):
    try:
        # Interact with the Gradio API using the client
        result = gradio_client.predict(
            dict={"background": handle_file(person_image_path), "layers": [], "composite": None},
            garm_img=handle_file(garment_image_path),
            garment_des="A cool description of the garment",
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
        )

        print(f"API result: {result}")

        # Check if the result is returned correctly
        if result and len(result) > 0:
            try_on_image_path = result[0]  # First item in result is the output image path
            print(f"Generated try-on image path: {try_on_image_path}")

            # Ensure the static directory exists
            static_dir = 'static'
            if not os.path.exists(static_dir):
                os.makedirs(static_dir)
                print(f"Created directory: {static_dir}")

            # Make sure the path exists
            if os.path.exists(try_on_image_path):
                # Convert the image to PNG format and save it
                img = cv2.imread(try_on_image_path)
                target_path_png = os.path.join(static_dir, 'result.png')
                cv2.imwrite(target_path_png, img)
                print(f"Image saved to: {target_path_png}")
                return target_path_png  # Return the saved image path as output
            else:
                print(f"Image not found at: {try_on_image_path}")
                return None
        else:
            print("No result returned from the API.")
            return None

    except Exception as e:
        print(f"Error interacting with Gradio API: {e}")
        return None

# Create and launch the Gradio Interface
interface = gr.Interface(
    fn=gradio_app,
    inputs=[gr.Image(type="filepath", label="Upload Person Image"), gr.Image(type="filepath", label="Upload Garment Image")],
    outputs=gr.Image(type="filepath", label="Try-On Result"),
    title="Virtual Try-On App",
    description="Upload a person image and a garment image to see how they look together!"
)

if __name__ == "__main__":
    interface.launch()
