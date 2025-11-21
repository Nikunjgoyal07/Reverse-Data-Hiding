import os
from PIL import Image

def preprocess_images(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff")):
            input_path = os.path.join(input_dir, filename)

            # Replace extension with .png
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, base_name + ".png")

            try:
                img = Image.open(input_path)

                # Convert to 8-bit grayscale
                img = img.convert("L")

                # Resize to 512×512 (this part is inherently lossy, unavoidable)
                img = img.resize((512, 512), Image.BICUBIC)

                # Save as PNG → LOSSLESS
                img.save(output_path, format="PNG")

                print(f"Processed: {filename} → {base_name}.png")

            except Exception as e:
                print(f"Failed: {filename} -> {e}")


# Example usage:
input_folder = "img_align_celeba_main"
output_folder = "dataset_final"

preprocess_images(input_folder, output_folder)
