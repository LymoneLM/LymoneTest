import onnxruntime as ort

POSENET_MODEL = '../../resource/model_zoo/scrfd_500m_bnkps_shape160x160.onnx'

# 加载ONNX模型
class OnnxRun:
    def __init__(self, model_name="face_detect", model_path=POSENET_MODEL):
        """
        model_name: 模型名称
        model_path: 模型路径
        """
        self.model_name = model_name

        self.ort_session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.ort_session.get_inputs()[0].name

        input = self.ort_session.get_inputs()
        output = self.ort_session.get_outputs()
        print(self.model_name + "_input_shape", input[0])

        for shape in output:
            # 获取输出数据的形状
            print(self.model_name + "_output_shape", shape)
        print("outpput", len(output))

    def inference(self, img):
        input_data = img
        return self.ort_session.run(None, {self.input_name: input_data})

if __name__ == "__main__":
    onnx_run = OnnxRun()