#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/29 17:09
# @Author  : cg
# @File    : run_to_onnx.py
# @Software: PyCharm
import torch
import torch.onnx
import platform
import sys
import onnxruntime as rt;
import  numpy as np

if platform.system() == 'Windows':
    module_dir = r"D:\python_workspace\TinyNet"
else:
    module_dir = '/home/cg/python_workspace/TinyNet'
if module_dir not in sys.path:
    sys.path.append(module_dir)


def run_onnx_model(onnx_path, inputs):
    session = rt.InferenceSession(onnx_path)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    result = session.run([output_name], {input_name: inputs})



def run_to_onnx():
    checkpoint_path = r"D:\python_workspace\TinyNet\model_saved_my2024\Random_static_searched_net_UnityNet_v4-8-SubnetV4_moeFalse_MiniNetV4_ResNet3stages_8layers_useResidualTrue_OutC128_GNinEVENLayer_16channel_cifar100\afterSearched_subnetgene_SubRegCoef0.5_300epoch_lr0.1_batchsize128_earlyExitReg0.5\checkpoint\flop=396295968,accuracy=0.73240.pth"
    checkpoint = torch.load(checkpoint_path)
    u_net = checkpoint['net']
    # 将模型设置为评估模式
    u_net.eval()

    # 2. 创建示例输入
    # 假设输入图像的大小是 (1, 3, 224, 224) 其中 1 是批次大小，3 是通道数，224 是宽和高
    dummy_input = torch.randn(1, 3, 32, 32).cuda()
    for i, subnet in enumerate(u_net.subnet_list):
        # 3. 导出为 ONNX
        onnx_path = r'D:\python_workspace\TinyNet\model_saved_my2024\Random_static_searched_net_UnityNet_v4-8-SubnetV4_moeFalse_MiniNetV4_ResNet3stages_8layers_useResidualTrue_OutC128_GNinEVENLayer_16channel_cifar100\afterSearched_subnetgene_SubRegCoef0.5_300epoch_lr0.1_batchsize128_earlyExitReg0.5\checkpoint\model_{}.onnx'.format(
            i)
        torch.onnx.export(
            subnet,  # 需要转换的模型
            dummy_input,  # 示例输入
            onnx_path,  # 导出ONNX文件的路径
            export_params=True,  # 是否导出参数
            opset_version=11,  # ONNX opset版本
            do_constant_folding=True,  # 是否执行常量折叠优化
            input_names=['input'],  # 输入名称
            output_names=['output'],  # 输出名称
            dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}  # 动态轴设置
        )

if __name__ == '__main__':
    onnx_path = r'D:\python_workspace\TinyNet\model_saved_my2024\Random_static_searched_net_UnityNet_v4-8-SubnetV4_moeFalse_MiniNetV4_ResNet3stages_8layers_useResidualTrue_OutC128_GNinEVENLayer_16channel_cifar100\afterSearched_subnetgene_SubRegCoef0.5_300epoch_lr0.1_batchsize128_earlyExitReg0.5\checkpoint\model_{}.onnx'.format(0)
    dummy_input = np.array(torch.randn(1, 3, 32, 32))
    a = run_onnx_model(onnx_path, dummy_input)
