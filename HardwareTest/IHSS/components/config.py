
class AI_Config:
    # 基本设置
    window_name = "face_detect"

    CAM_HEIGHT = 480
    CAM_WIDTH = 640
    INPUT_SIZE = (320, 320) # (h,w)

    # 模型配置
    FEAT_STRIDE_FPN = [8, 16, 32]
    THRESHOLD = 0.2

    # 模型路径
    # FACE_DET_PATH = "./resource/model_zoo/scrfd_500m_bnkps_shape160x160.onnx"
    # DEEPSORT_PATH = "./resource/model_zoo/original_ckpt.onnx"
    FONT_PATH = "./resource/font/simsun.ttc"
    FONT_SIZE = 20

ai_cfg = AI_Config()