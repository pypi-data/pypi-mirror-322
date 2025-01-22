import torch
import torch.nn as nn
import torch.nn.functional as F


# Question: self.weight is the learned time-series-reduce matrix
class GraphConvolution(nn.Module):

    def __init__(self, num_in, num_out, device, bias=False):

        super(GraphConvolution, self).__init__()

        self.num_in = num_in
        self.num_out = num_out
        self.weight = nn.Parameter(torch.FloatTensor(num_in, num_out).to(device))
        nn.init.xavier_normal_(self.weight)
        self.bias = None
        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(num_out).to(device))
            nn.init.zeros_(self.bias)

    def forward(self, x, adj):
        out = torch.matmul(adj, x)
        out = torch.matmul(out, self.weight)
        if self.bias is not None:
            return out + self.bias
        else:
            return out


class Linear(nn.Module):
    def __init__(self, in_features, out_features, bias=True):
        super(Linear, self).__init__()
        self.linear = nn.Linear(in_features, out_features, bias=bias)
        nn.init.xavier_normal_(self.linear.weight)
        if bias:
            nn.init.zeros_(self.linear.bias)

    def forward(self, inputs):
        return self.linear(inputs)


def normalize_A(A, symmetry=False):
    A = F.relu(A)
    if symmetry:
        A = A + torch.transpose(A, 0, 1)
        d = torch.sum(A, 1)
        d = 1 / torch.sqrt(d + 1e-10)
        D = torch.diag_embed(d)
        L = torch.matmul(torch.matmul(D, A), D)
    else:
        d = torch.sum(A, 1)
        d = 1 / torch.sqrt(d + 1e-10)
        D = torch.diag_embed(d)
        L = torch.matmul(torch.matmul(D, A), D)
    return L


def generate_cheby_adj(A, K, device):
    support = []
    for i in range(K):
        if i == 0:
            support.append(torch.eye(A.shape[1]).to(device))
        elif i == 1:
            support.append(A)
        else:
            temp = torch.matmul(support[-1], A)
            support.append(temp)
    return support


class Chebynet(nn.Module):
    def __init__(self, xdim, K, num_out, device):
        super(Chebynet, self).__init__()
        self.K = K
        self.device = device
        self.gc1 = nn.ModuleList()
        for i in range(K):
            self.gc1.append(GraphConvolution(xdim[2], num_out, device=device))

    def forward(self, x, L):
        adj = generate_cheby_adj(L, self.K, device=self.device)
        for i in range(len(self.gc1)):
            if i == 0:
                result = self.gc1[i](x, adj[i])
            else:
                result += self.gc1[i](x, adj[i])
        result = F.relu(result)
        return result


class DGCNN(nn.Module):
    def __init__(self, xdim, k_adj, num_out, device, nclass=2):
        # xdim: (batch_size*num_nodes*num_features_in)
        # k_adj: num_layers
        # num_out: num_features_out
        super(DGCNN, self).__init__()
        self.K = k_adj
        self.layer1 = Chebynet(xdim, k_adj, num_out, device=device)
        self.BN1 = nn.BatchNorm1d(xdim[2])
        ### FIXME: batch normalize
        # self.fc1 = Linear(xdim[1] * num_out, 25)
        self.fc1 = nn.Sequential(Linear(xdim[1] * num_out, 25), nn.BatchNorm1d(25))
        ###
        self.fc2 = Linear(25, nclass)
        self.A = nn.Parameter(torch.FloatTensor(xdim[1], xdim[1]).to(device))
        nn.init.xavier_normal_(self.A)

    def forward(self, x):
        x = self.BN1(x.transpose(1, 2)).transpose(1, 2)
        L = normalize_A(self.A)
        result = self.layer1(x, L)
        result = result.reshape(x.shape[0], -1)
        result = F.relu(self.fc1(result))
        result = self.fc2(result)
        return F.softmax(result, dim=1)
