# Quantum Noise Simulator：三量子比特重复码基线

这个实验用 Python 标准库模拟一个教学性的 bit-flip 噪声通道，并比较单个比特与三比特重复码（majority decoding）的成功率。它不是物理量子电路模拟器，而是帮助建立量子纠错直觉的最小可复现实验。

## 研究问题

在独立 bit-flip 概率为 `p` 时，三比特重复码什么时候能降低逻辑错误率？它的代价是将一个逻辑比特扩展为三个物理比特，并且只处理特定类型的噪声。

## 运行

```bash
python experiments/quantum-noise-simulator/simulator.py
python experiments/quantum-noise-simulator/simulator.py --trials 10000 --seed 7 --probabilities 0.02 0.15 0.25
```

对于低于 50% 的独立 bit-flip 噪声，理想 majority decoding 通常会提高成功率；当噪声接近或超过 50% 时，简单重复码不再提供这种收益。输出使用固定随机种子，便于复现。

## 局限与下一步

实验忽略了量子相位、测量误差、门错误、相关噪声、综合征提取和解码延迟，因此不能代表真实量子硬件表现。下一步可以用 Qiskit 或 Cirq 重写同一实验，加入 X/Z 噪声、测量电路和不同解码器，并将逻辑错误率与物理错误率绘制成曲线。
