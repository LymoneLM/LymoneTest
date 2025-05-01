import cv2
import numpy

def create_header(source_img, caption, bar_height=50):
    dimensions = source_img.shape
    new_canvas = numpy.zeros((dimensions[0]+bar_height, dimensions[1], 3), dtype=numpy.uint8)
    new_canvas[bar_height:,:] = source_img
    cv2.putText(new_canvas, caption, (10,35), cv2.FONT_HERSHEY_PLAIN, 2.3, (100,255,100), 2)
    return new_canvas

source_data = cv2.imread(r'.\img\2.jpg')

blue_layer, green_layer, red_layer = cv2.split(source_data)
edge_blue = cv2.Canny(blue_layer, 50, 150)
edge_green = cv2.Canny(green_layer, 50, 150)
edge_red = cv2.Canny(red_layer, 50, 150)
edge_combined = cv2.bitwise_or(edge_red, edge_green)
edge_map = cv2.bitwise_or(edge_combined, edge_blue)
edge_visual = cv2.cvtColor(edge_map, cv2.COLOR_GRAY2RGB)

yuv_layers = cv2.cvtColor(source_data, cv2.COLOR_BGR2YUV)
y_layer, u_layer, v_layer = cv2.split(yuv_layers)
smoothed_y = cv2.GaussianBlur(y_layer, (9,9), 3)
enhanced_y = cv2.addWeighted(y_layer, 1.8, smoothed_y, -0.8, 10)
processed_yuv = cv2.merge([enhanced_y, u_layer, v_layer])
sharpened_output = cv2.cvtColor(processed_yuv, cv2.COLOR_YUV2BGR)

with_header_1 = create_header(source_data, "Source Image")
with_header_2 = create_header(edge_visual, "Edge Detection")
with_header_3 = create_header(sharpened_output, "Enhanced Image")

merged_output = numpy.hstack((with_header_1, with_header_2, with_header_3))
display_scale = 0.72
resized_output = cv2.resize(merged_output, None, fx=display_scale, fy=display_scale)

cv2.imshow('Visualization Panel', resized_output)
cv2.waitKey(0)
cv2.destroyAllWindows()