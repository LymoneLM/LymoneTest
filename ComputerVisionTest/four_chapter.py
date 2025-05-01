import cv2
import numpy


def execute_processing():
    src_image = cv2.imread(r'.\img\2.jpg', cv2.IMREAD_GRAYSCALE)
    if src_image is None:
        print("Error: Failed to load image")
        return

    background_blur = cv2.GaussianBlur(src_image, (50 * 2 + 1, 50 * 2 + 1), 0)

    selection_rect = cv2.selectROI("Select Area (SPACE/ENTER confirm)", src_image, False)
    cv2.destroyAllWindows()

    selection_mask = numpy.zeros_like(src_image)
    px, py, w, h = selection_rect
    cv2.ellipse(selection_mask,
                (px + w // 2, py + h // 2),
                (w // 2, h // 2),
                0, 0, 360, 255, -1)

    blend_weights = cv2.blur(selection_mask, (25 * 2 + 1, 25 * 2 + 1)).astype(numpy.float32) / 255

    layer_foreground = src_image.astype(numpy.float32) * blend_weights
    layer_background = background_blur.astype(numpy.float32) * (1.0 - blend_weights)
    composite_image = cv2.add(layer_foreground, layer_background).astype(numpy.uint8)

    cv2.imshow('Source Image', src_image)
    cv2.imshow('Background Layer', background_blur)
    cv2.imshow('Output Preview', composite_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite('output_image.jpg', composite_image)
    print("Output saved: output_image.jpg")


if __name__ == "__main__":
    execute_processing()