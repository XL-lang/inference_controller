import onnx
import torch
from pathlib import Path
from onnxruntime_extensions import pnp, OrtPyFunction
from transformers import AutoTokenizer, GPT2LMHeadModel
from transformers.onnx import export, FeaturesManager
import onnxruntime as _ort
from onnxruntime_extensions import get_library_path as _lib_path
import numpy as np
import json
so = _ort.SessionOptions()
so.register_custom_ops_library(_lib_path())

def getBertInput():
    model_name = "textattack/bert-base-uncased-MRPC"
    model_path = r"D:\project\inference_controller\tets\bert_two_layer_0.onnx"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    mrpc_text1 = "The quick brown fox jumps over the lazy dog"
    mrpc_text2 = "A fast brown fox leaps over a lazy dog"
    dummy_input = tokenizer(mrpc_text1,
                            mrpc_text2,  # MRPC 是句子对任务
                            max_length=128,  # 设置合适的最大长度
                            truncation=True,  # 启用截断
                            padding='max_length',  # 启用填充到最大长度
                            );
    dummy_input = dict(dummy_input)

    return dummy_input

def getBertMiddle():
    return {
        "attention_mask": np.ones((1,128),dtype=np.int64).tolist(),
        "hidden_states": np.zeros((1,128,768),dtype=np.float32).tolist(),
    }

