import torch
import numpy as np

x_np = np.array([[1., 2.], [3., 4.]])
z_np = np.array([[3., 3.], [3., 3.]])
x = torch.from_numpy(x_np)
z = torch.from_numpy(z_np)

x.requires_grad_(True)
z.requires_grad_(True)

y = x**2 + 2*z

# print(y)
y.backward(z)
# print(z.grad)

lambda_weights = torch.from_numpy(np.array([1., 1., 1.])).view(-1, 1)
comp = torch.from_numpy(np.array([[1., 1., 1.]]))
print(lambda_weights)
print(comp)
print(torch.mm(comp, lambda_weights))
