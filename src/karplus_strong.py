"""
MIDI to Guitar Audio Converter: 
这是一个基于 Karplus-Strong 算法实现的 MIDI 转吉他音频工具。
--------------------------------------------------------------------------------
版权所有 © 2024 何铭洋。保留所有权利

本程序是自由软件：你可以再分发之和/或依照由自由软件基金会发布的
GNU 宽通用公共许可证 (GNU Lesser General Public License, LGPL) 修改之，
无论是版本 3 许可证，还是（按你的决定）任何以后版都可以。

发布该程序是希望它能有用，但是并无保障；甚至连可销售和符合某个特定的目的都不保证。
请参看 GNU 宽通用公共许可证，了解详情。

你应该随程序获得一份 GNU 宽通用公共许可证的复本。
如果没有，请看 <https://www.gnu.org/licenses/>。
--------------------------------------------------------------------------------
免责声明：
MIDI to Guitar Audio Converter 按”原样”提供，不提供任何形式的保证。
作者和贡献者不承担任何默认保证，包括但不限于
对适销性、特定用途适用性和不侵权的任何默认保证。

在任何情况下，作者或贡献者均不对因使用、无法使用或使用 MIDI to Guitar Audio Converter、
任何网站或其内容而引起或与之相关的任何直接、间接、特殊、偶然或后果性损害负责，
包括但不限于依赖损失、利润损失、储蓄损失、业务中断和/或计算机故障或失灵，
即使作者已被告知此类损害的可能性。
--------------------------------------------------------------------------------
我的电子邮箱: He-mingyang@outlook.com
"""

"""
MIDI to Guitar Audio Converter: This is a tool for converting MIDI 
to guitar audio based on the Karplus-Strong algorithm.
--------------------------------------------------------------------------------
Copyright (c) 2024 何铭洋. All rights reserved.

This program is free software: you can redistribute it and/or modify 
it under the terms of the The GNU Lesser General Public License as published by 
the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
The GNU Lesser General Public License for more details.

You should have received a copy of the The GNU Lesser General Public License 
along with this program. If not, see <https://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------
Warranty Disclaimer: 
MIDI to Guitar Audio Converter is provided "AS IS" without warranty of any kind. 
The authors and contributors disclaim all implied warranties including: without 
limitation, any implied warranties of merchantability, fitness for a particular 
purpose, and non-infringement.

In no event shall the authors or contributors be liable for any direct, indirect, 
special, incidental, or consequential damages arising out of or related to the 
use, inability to use, or the results of use of MIDI to Guitar Audio Converter, 
any web sites, or the contents thereof, including but not limited to reliance 
loss, lost profits, lost savings, business interruption, and/or computer failure 
or malfunction, even if the authors have been advised of the possibility of such 
damages.
--------------------------------------------------------------------------------
My E-mail: He-mingyang@outlook.com
"""

import os
import subprocess
import sys
from functools import lru_cache
from tkinter import filedialog

import numpy as np
from mido import MetaMessage, MidiFile
from scipy.io.wavfile import write
from tqdm import tqdm


# 使用 LRU 缓存装饰器来缓存函数结果，以提高性能
@lru_cache(maxsize=128)
def karplus_strong(sampling_rate, frequency, decay_factor, harmonic_time):
    """
    使用 Karplus-Strong 算法生成音频信号

    参数:
    sampling_rate (int): 采样率
    frequency (float): 音高
    decay_factor (float): 衰减因子，范围为 0 到 1
    harmonic_time (float): 泛音持续时间，单位为秒

    返回:
    output_signal (numpy.array): 生成的音频信号
    """

    # 计算周期长度
    period_length = max(round(sampling_rate / frequency), 1)
    harmonic_time = max(harmonic_time, 0.1)
    # 计算总采样点数
    count = max(round(sampling_rate * harmonic_time), 1)

    # 初始化输出数组为 0
    output_signal = np.zeros(count)
    # 为第一个周期生成初始激励信号（白噪音）
    output_signal[:period_length] = 2 * np.random.rand(period_length) - 1

    # 从第二个周期开始，迭代计算每个采样点的值（卷积）
    decay = 0.5 * decay_factor
    for i in range(period_length, count):
        delay = i - period_length
        output_signal[i] = (output_signal[delay] + output_signal[delay - 1]) * decay
    return output_signal


# 生成 MIDI 音符编号到频率的查找表
FREQUENCY_TABLE = {
    note_number: 440.0 * (2.0 ** ((note_number - 69) / 12.0))
    for note_number in range(128)
}


@lru_cache(maxsize=128)
def note_number_to_frequency(note_number):
    """
    使用查找表将 MIDI 音符编号转换为频率

    参数:
    note_number (int): MIDI 音符编号

    返回:
    frequency (float): 频率
    """

    if not (0 <= note_number <= 127):
        raise ValueError(f"无效的音符编号: {note_number}。必须在 0 到 127 之间。")
    return FREQUENCY_TABLE[note_number]


@lru_cache(maxsize=128)
def process_note_on(note, velocity, sampling_rate, decay_factor, harmonic_time):
    """
    处理 MIDI 音符 ON 消息，生成 Karplus-Strong 算法生成的音频信号

    参数:
    note (int): MIDI 音符编号
    velocity (int): 音符力度
    sampling_rate (int): 采样率
    decay_factor (float): 衰减因子
    harmonic_time (float): 泛音持续时间，单位为秒

    返回:
    output_signal (numpy.array): 生成的音频信号
    """

    try:
        note_frequency = note_number_to_frequency(note)
        if note_frequency is None:
            raise ValueError("无效的音符编号")

        # 根据 velocity 调整幅度
        velocity_factor = velocity / 127.0
        output_signal = (
            karplus_strong(sampling_rate, note_frequency, decay_factor, harmonic_time)
            * velocity_factor
        )

        return output_signal
    except (ValueError, TypeError) as e:
        print(f"处理 MIDI 音符 ON 消息时发生错误: {e}")
        sys.exit(1)


def get_bpm(midi_file):
    """
    从 MIDI 文件中解析 BPM

    参数:
    midi_file (str): MIDI 文件路径

    返回:
    bpm (float): 实际的 BPM
    """

    midi = MidiFile(midi_file)
    bpm = 120  # 默认 BPM

    # 解析 set_tempo 消息以获取实际的 BPM
    for track in midi.tracks:
        for msg in track:
            if isinstance(msg, MetaMessage) and msg.type == "set_tempo":  # type: ignore
                microseconds_per_beat = msg.tempo  # type: ignore
                bpm = 60000000 / microseconds_per_beat
                break  # 找到第一个 set_tempo 消息后即可退出

    if bpm == 120:
        print(
            f"警告: MIDI 文件 {midi_file} 中没有找到 set_tempo 消息，使用默认 BPM 120。"
        )
    return bpm


def get_max_time(audio_signals, sampling_rate):
    """
    计算音频信号的最大时间

    参数:
    audio_signals (list): 包含 (start_time, signal) 的列表
    sampling_rate (int): 采样率

    返回:
    max_time (float): 最大时间
    """

    times = [
        start_time + len(signal) / sampling_rate for start_time, signal in audio_signals
    ]
    return max(times)


def combine_signals(audio_signals, sampling_rate):
    """
    将多个音频信号叠加到一个输出数组中

    参数:
    audio_signals (list): 包含 (start_time, signal) 的列表
    sampling_rate (int): 采样率

    返回:
    combined_signal (numpy.array): 叠加后的音频信号
    """

    if not audio_signals:
        return np.array([])

    # 计算总采样点数，初始化输出数组
    max_time = get_max_time(audio_signals, sampling_rate)
    total_samples = round(max_time * sampling_rate)
    combined_signal = np.zeros(total_samples)

    # 将所有音频信号叠加到一个数组中
    for start_time, signal in audio_signals:
        start_sample = int(start_time * sampling_rate)
        end_sample = start_sample + len(signal)
        combined_signal[start_sample:end_sample] += signal
    print(f"信号叠加完成")

    # 归一化音频信号
    max_abs_val = np.max(np.abs(combined_signal))
    if max_abs_val > 0:
        scale_factor = 0.99 / max_abs_val
        combined_signal *= scale_factor
    print(f"音频信号归一化完成")

    return combined_signal


def midi_to_audio(midi_file, sampling_rate, decay_factor, harmonic_time, output_file):
    """
    读取 MIDI 文件并生成音频信号

    参数:
    midi_file (str): MIDI 文件路径
    sampling_rate (int): 采样率
    decay_factor (float): 衰减因子
    harmonic_time (float): 泛音持续时间，单位为秒
    output_file (str): 输出 WAV 文件路径
    """

    try:
        midi = MidiFile(midi_file)
    except IOError as e:
        print(f"无法读取 MIDI 文件: {e}")
        sys.exit(1)
    audio_signals = []

    # 获取 BPM
    bpm = get_bpm(midi_file)
    if bpm <= 0:
        raise ValueError("无效的 BPM 值")

    # 检查 ticks_per_beat 是否为 0
    if midi.ticks_per_beat == 0:
        raise ValueError("MIDI 文件的 ticks_per_beat 为 0, 无法计算时间")

    time_per_tick = 60 / (midi.ticks_per_beat * bpm)

    # 外层进度条用于显示所有轨道的处理进度
    with tqdm(
        total=len(midi.tracks), desc="处理轨道", position=0, mininterval=2
    ) as pbar_outer:
        # 遍历 MIDI 文件中的轨道
        for i, track in enumerate(midi.tracks):
            # 内层进度条用于显示当前轨道的处理进度
            with tqdm(
                total=len(track),
                desc=f"轨道 {i+1}",
                position=1,
                leave=False,
                mininterval=1,
            ) as pbar_inner:
                current_time = 0.0
                # 遍历轨道中的消息
                for msg in track:
                    if msg.type == "note_on" and msg.velocity > 0:
                        output_signal = process_note_on(
                            msg.note,
                            msg.velocity,
                            sampling_rate,
                            decay_factor,
                            harmonic_time,
                        )
                        # 仅在输出信号非空时添加到列表中
                        if output_signal.size > 0:
                            audio_signals.append((current_time, output_signal))
                    current_time += msg.time * time_per_tick  # 更新当前时间
                    pbar_inner.update(1)  # 更新内层进度条
            pbar_outer.update(1)  # 更新外层进度条
    print(f"轨道处理完成")

    # 将所有轨道的音频信号合并成一个
    combined_signal = combine_signals(audio_signals, sampling_rate)

    # 保存为 WAV 文件
    try:
        with open(output_file, "wb") as f:
            write(f, sampling_rate, combined_signal.astype(np.float32))
    except (OSError, IOError, ValueError) as e:
        print(f"保存音频文件时发生错误: {e}")
        sys.exit(1)


def validate_and_prepare_paths(input_midi_file, output_file):
    """
    验证输入文件路径和生成输出文件路径

    参数:
    input_midi_file (str): 输入 MIDI 文件路径
    output_file (str): 输出 WAV 文件路径

    返回:
    output_file (str): 生成的输出文件路径
    """

    if not os.path.isfile(input_midi_file) or not os.access(input_midi_file, os.R_OK):
        print(f"无效的文件路径或无法读取文件: {input_midi_file}")
        sys.exit(1)
    if not os.access(os.path.dirname(output_file), os.W_OK):
        print(f"无法写入输出文件路径: {output_file}")
        sys.exit(1)
    return output_file


def open_folder(file_path):
    """
    打开文件所在文件夹

    参数:
    file_path (str): 文件路径
    """

    if not os.path.isfile(file_path):
        print(f"无效的文件路径: {file_path}")
        return

    folder_path = os.path.dirname(file_path)
    if os.name == "nt":  # Windows
        os.startfile(folder_path)
    elif os.name == "posix":  # macOS 和 Linux
        subprocess.run(["open", folder_path])
    else:
        print(f"不支持的操作系统: {os.name}")


def main():
    print(
        """
---------------------------------------------------------------------------------------
MIDI to Guitar Audio Converter Copyright (c) 2023 何铭洋
This program comes with ABSOLUTELY NO WARRANTY;
view the details in the DISCLAMBER file.
This is free software, and you are welcome to redistribute it under certain conditions;
view the details in the LICENSE file.
---------------------------------------------------------------------------------------
"""
    )

    # 弹出文件选择对话框
    input_midi_file = filedialog.askopenfilename(
        title="选择 MIDI 文件",
        filetypes=[("MIDI 文件", "*.mid"), ("所有文件", "*.*")],
    )
    if not input_midi_file:
        print("未选择文件，程序退出。")
        sys.exit(1)
    # 生成输出文件名
    output_file = os.path.splitext(input_midi_file)[0] + ".wav"
    output_file = validate_and_prepare_paths(input_midi_file, output_file)
    print("选择的 MIDI 文件：" + os.path.basename(input_midi_file))

    # 设置参数
    sampling_rate = 44100  # 采样率
    decay_factor = 0.996  # 衰减因子
    harmonic_time = 4  # 泛音持续时长
    try:
        # 生成音频
        midi_to_audio(
            input_midi_file, sampling_rate, decay_factor, harmonic_time, output_file
        )
        print(f"音频已保存到： {output_file}")

        # 打开音频文件所在文件夹
        open_folder(output_file)
    except (FileNotFoundError, PermissionError, ValueError) as e:
        print(f"生成音频时发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
