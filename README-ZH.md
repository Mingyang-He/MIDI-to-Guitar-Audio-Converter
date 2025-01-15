* [English](README.md)   [中文](README-ZH.md)

![GitHub License](https://img.shields.io/github/license/Mingyang-He/MIDI-to-Guitar-Audio-Converter)     ![Static Badge](https://img.shields.io/badge/Python-3.13.1-blue?link=https%3A%2F%2Fwww.python.org%2Fdownloads%2Frelease%2Fpython-3131%2F)     ![Static Badge](https://img.shields.io/badge/numpy-blue)   ![Static Badge](https://img.shields.io/badge/mido-blue)   ![Static Badge](https://img.shields.io/badge/scipy-blue)   ![Static Badge](https://img.shields.io/badge/tqdm-blue)

# 关于

MIDI to Guitar Audio Converter 是一个基于 Karplus-Strong 算法实现的 MIDI 转吉他音频工具。它能够通过调整采样率、衰减因子和谐波时间等参数，将 MIDI 文件转换为逼真的吉他音频文件，适用于音乐创作、教育及娱乐等领域。

# 背景

这是我的数字信号处理课程作业，它很简单又十分有趣，所以我想分享给大家玩玩。

# 特点

* 采用 Python 语言开发，并在程序运行中提供了相应的调试信息以方便用户使用
* 在运算速度等方面上做了很大优化
* 目前能处理多轨道 MIDI 文件，将其转换为单轨道 WAV 文件。

# 使用

请转到：[使用说明书 · Mingyang-He/MIDI-to-Guitar-Audio-Converter Wiki](https://github.com/Mingyang-He/MIDI-to-Guitar-Audio-Converter/wiki/%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E%E4%B9%A6)

# 环境与依赖

请转到：[开发环境与运行环境 · Mingyang-He/MIDI-to-Guitar-Audio-Converter Wiki](https://github.com/Mingyang-He/MIDI-to-Guitar-Audio-Converter/wiki/%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E4%B8%8E%E8%BF%90%E8%A1%8C%E7%8E%AF%E5%A2%83)

# 技术原理

请转到：[技术文档 · Mingyang-He/MIDI-to-Guitar-Audio-Converter Wiki](https://github.com/Mingyang-He/MIDI-to-Guitar-Audio-Converter/wiki/%E6%8A%80%E6%9C%AF%E6%96%87%E6%A1%A3)

# 项目结构

> /doc

这里存放了关于使用说明、环境、技术原理等相关的文档。

> /src

这里存放了项目的源代码。

# 讨论与反馈

想要发布相关讨论和问题的话，请到 Github 的这儿：

[Mingyang-He/MIDI-to-Guitar-Audio-Converter · Discussions · GitHub](https://github.com/Mingyang-He/MIDI-to-Guitar-Audio-Converter/discussions)

想要报告 Bug 和请求新功能的话，请到 Github 的这儿并选择对应的模板：

[Issues · Mingyang-He/MIDI-to-Guitar-Audio-Converter](https://github.com/Mingyang-He/MIDI-to-Guitar-Audio-Converter/issues)

*（我想我没有时间去关注这些，大概率不会做出任何回复，请见谅）*

# 参与贡献方式

直接提交 PR 或者自己 fork 下来在自己的仓库中改进它。

*（我想我没有时间去关注这些，大概率不会做出任何回复，请见谅）*

# 版权和许可证

版权所有 © 2024 何铭洋。保留所有权利

本程序是自由软件：你可以再分发之和/或依照由自由软件基金会发布的 GNU 宽通用公共许可证 (GNU Lesser General Public License, LGPL) 修改之，无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。

发布该程序是希望它能有用，但是并无保障；甚至连可销售和符合某个特定的目的都不保证。请参看 GNU 宽通用公共许可证，了解详情。

你应该随程序获得一份 GNU 宽通用公共许可证的复本。如果没有，请看 [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/)。

# 免责声明

MIDI to Guitar Audio Converter 按 “原样” 提供，不提供任何形式的保证。作者和贡献者不承担任何默认保证，包括但不限于对适销性、特定用途适用性和不侵权的任何默认保证。

在任何情况下，作者或贡献者均不对因使用、无法使用或使用 MIDI to Guitar Audio Converter、任何网站或其内容而引起或与之相关的任何直接、间接、特殊、偶然或后果性损害负责，包括但不限于依赖损失、利润损失、储蓄损失、业务中断和/或计算机故障或失灵，即使作者已被告知此类损害的可能性。
