import time
from PIL import Image
from multiprocessing import Process


def resize_image(input_path, output_path, size):
    img = Image.open(f"images/{input_path}")
    img = img.resize(size)  # Resize the image
    img.save(f"images/{output_path}")
    print(f"Processed {input_path} -> {output_path}")


def main():
    images = [
        ("input1.jpg", "output1.jpg"),
        ("input2.jpg", "output2.jpg"),
        ("input3.jpg", "output3.jpg"),
    ]

    processes = []
    size = (600, 600)

    start = time.time()

    for input_path, output_path in images:
        p = Process(target=resize_image, args=(input_path, output_path, size))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print(f"All images processed in {time.time() - start:.2f} seconds.")


if __name__ == '__main__':
    main()
