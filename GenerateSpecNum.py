import torch
import torch.nn as nn
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
 
num_img=9
class discriminator(nn.Module):
 def __init__(self):
  super(discriminator, self).__init__()
  self.dis = nn.Sequential(
   nn.Conv2d(1, 32, 5, stride=1, padding=2),
   nn.LeakyReLU(0.2, True),
   nn.MaxPool2d((2, 2)),
 
   nn.Conv2d(32, 64, 5, stride=1, padding=2),
   nn.LeakyReLU(0.2, True),
   nn.MaxPool2d((2, 2))
  )
  self.fc = nn.Sequential(
   nn.Linear(7 * 7 * 64, 1024),
   nn.LeakyReLU(0.2, True),
   nn.Linear(1024, 10),
   nn.Sigmoid()
  )
 
 def forward(self, x):
  x = self.dis(x)
  x = x.view(x.size(0), -1)
  x = self.fc(x)
  return x
 
 
class generator(nn.Module):
 def __init__(self, input_size, num_feature):
  super(generator, self).__init__()
  self.fc = nn.Linear(input_size, num_feature) # 1*56*56
  self.br = nn.Sequential(
   nn.BatchNorm2d(1),
   nn.ReLU(True)
  )
  self.gen = nn.Sequential(
   nn.Conv2d(1, 50, 3, stride=1, padding=1),
   nn.BatchNorm2d(50),
   nn.ReLU(True),
 
   nn.Conv2d(50, 25, 3, stride=1, padding=1),
   nn.BatchNorm2d(25),
   nn.ReLU(True),
 
   nn.Conv2d(25, 1, 2, stride=2),
   nn.Tanh()
  )
 
 def forward(self, x):
  x = self.fc(x)
  x = x.view(x.size(0), 1, 56, 56)
  x = self.br(x)
  x = self.gen(x)
  return x
 
 
def show(images):
 images = images.detach().numpy()
 images = 255 * (0.5 * images + 0.5)
 images = images.astype(np.uint8)
 plt.figure(figsize=(4, 4))
 width = images.shape[2]
 gs = gridspec.GridSpec(1, num_img, wspace=0, hspace=0)
 for i, img in enumerate(images):
  ax = plt.subplot(gs[i])
  ax.set_xticklabels([])
  ax.set_yticklabels([])
  ax.set_aspect('equal')
  plt.imshow(img.reshape(width, width), cmap=plt.cm.gray)
  plt.axis('off')
  plt.tight_layout()
 plt.tight_layout()
 # plt.savefig(r'drive/深度学习/DCGAN/images/%d.png' % count, bbox_inches='tight')
 return width
 
def show_all(images_all):
 x=images_all[0]
 for i in range(1,len(images_all),1):
  x=np.concatenate((x,images_all[i]),0)
 print(x.shape)
 x = 255 * (0.5 * x + 0.5)
 x = x.astype(np.uint8)
 plt.figure(figsize=(9, 10))
 width = x.shape[2]
 gs = gridspec.GridSpec(10, num_img, wspace=0, hspace=0)
 for i, img in enumerate(x):
  ax = plt.subplot(gs[i])
  ax.set_xticklabels([])
  ax.set_yticklabels([])
  ax.set_aspect('equal')
  plt.imshow(img.reshape(width, width), cmap=plt.cm.gray)
  plt.axis('off')
  plt.tight_layout()
 
 
 # 导入相应的模型
z_dimension = 110
D = discriminator()
G = generator(z_dimension, 3136) # 1*56*56
# D.load_state_dict(torch.load(r'./CGAN/Discriminator.pkl'))
# G.load_state_dict(torch.load(r'./CGAN/Generator.pkl'))
D.load_state_dict(torch.load('./Discriminator_cuda_50.pkl'))
G.load_state_dict(torch.load('./Generator_cuda_50.pkl'))
# 依次生成0到9
lis=[]
for i in range(10):
 z = torch.randn((num_img, 100)) # 随机生成向量
 x=np.zeros((num_img,10))
 x[:,i]=1
 z = np.concatenate((z.numpy(), x),1)
 z = torch.from_numpy(z).float()
 fake_img = G(z) # 将向量放入生成网络G生成一张图片
 lis.append(fake_img.detach().numpy())
 output = D(fake_img) # 经过判别器得到结果
 show(fake_img)
 plt.savefig('./generatorImg/%d.png' % i, bbox_inches='tight')
 
show_all(lis)
plt.savefig('./generatorImg/all.png', bbox_inches='tight')
plt.show()
