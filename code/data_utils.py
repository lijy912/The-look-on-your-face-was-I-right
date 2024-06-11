import os
import json
import torch
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset

# 加载数据集
def load_data(json_path):
    print("Loading data...")
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("Data loaded.")
    return data

# 加载和预处理图片的函数
def load_and_preprocess_image(img_path, target_size=(640, 640), device='cpu'):
    img = Image.open(img_path).convert('RGB')
    img = img.resize(target_size)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img_tensor = transform(img)
    img_tensor = img_tensor.unsqueeze(0).to(device)  # 添加 batch 维度并移动到GPU
    return img_tensor

# 定义数据集类
class MyDataset(Dataset):
    def __init__(self, json_file, img_folder, transform=None):
        self.data = json.load(open(json_file, encoding='utf-8'))
        self.img_folder = img_folder
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        img = Image.open(self.img_folder + item['filename'])
        
        # 检查图像通道数
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        if self.transform:
            img = self.transform(img)
        return img