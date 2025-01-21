# coding = utf-8
# @Time    : 2024-12-17  19:13:45
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: ASV model.

import os

import librosa
import torch
import torchaudio
from scipy import signal

from dguard.asv.dfaudio_model import ECAPA_TDNN_oneclass as dfaudio_model
from dguard.asv.dfaudio_model.audio_utils import delta


class DguardASV:
    def __init__(self, device="cuda:0", threshold=0):
        DGUARD_MODEL_PATH = os.getenv("DGUARD_MODEL_PATH", None)
        if DGUARD_MODEL_PATH is not None:
            model_path = os.path.join(DGUARD_MODEL_PATH, "dfaudio_model.pt")
            ocsoftmax = os.path.join(DGUARD_MODEL_PATH, "dfaudio_ocsoftmax.pt")
        else:
            # use ~/.dguard as default
            print(f"DGUARD_MODEL_PATH is not set, using default path: {DGUARD_MODEL_PATH}")
            DGUARD_MODEL_PATH = os.path.expanduser("~/.dguard")
            model_path = os.path.join(DGUARD_MODEL_PATH, "dfaudio_model.pt")
            ocsoftmax = os.path.join(DGUARD_MODEL_PATH, "dfaudio_ocsoftmax.pt")
            if not os.path.exists(DGUARD_MODEL_PATH):
                raise FileNotFoundError(
                    f"DGUARD_MODEL_PATH is not set, and default path {DGUARD_MODEL_PATH} does not exist."
                )
            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"Model file {model_path} does not exist in default path {DGUARD_MODEL_PATH}."
                )
            if not os.path.exists(ocsoftmax):
                raise FileNotFoundError(
                    f"Model file {ocsoftmax} does not exist in default path {DGUARD_MODEL_PATH}."
                )
            
        self.device = device
        self.model, self.oc_class = dfaudio_model.dfaudio_model(
            feat_model_path=model_path, oc_model_path=ocsoftmax, device=device
        ).get_models()
        self.th = threshold
        self.trans_lfcc = torchaudio.transforms.LFCC(
            sample_rate=16000,
            n_filter=20,
            n_lfcc=20,
            speckwargs={
                "n_fft": 512,
                "win_length": 320,
                "hop_length": 160,
                "window_fn": torch.hamming_window,
            },
        )

    def infer(self, audio_path, channel=0, length=-1):
        audio, fs = librosa.load(audio_path, sr=16000)
        if len(audio.shape) == 1:
            audio = audio.reshape(1, -1)
        # print(f"Loaded audio: {audio.shape}, Sample Rate: {fs}")
        audio = audio[channel]
        if length > 0:
            audio = audio[: length * fs]
        # print(f"Loaded audio: {audio.shape}, Sample Rate: {fs}")
        audio = signal.lfilter([1, -0.97], [1], audio)
        x = torch.FloatTensor(audio)
        # print(f"After lfilter: {x.shape}")
        x = self.trans_lfcc(x).transpose(0, 1).unsqueeze(0)
        # print(f"After LFCC transform: {x.shape}")
        lfcc_delta = delta(x)
        lfcc_delta_delta = delta(lfcc_delta)
        x = (
            torch.cat((x, lfcc_delta, lfcc_delta_delta), 2)
            .squeeze(0)
            .transpose(0, 1)
            .to(self.device, non_blocking=True)
        )
        # print(f"Feature tensor shape: {x.shape}")
        feats = self.model(x)
        labels = torch.tensor(0).to(self.device)
        _, score = self.oc_class(feats, labels, is_train=False)
        # score to float
        score = score.item()
        if score < self.th:
            # fake
            return {
                "score": score,
                "label": "fake",
            }
        else:
            # real
            return {
                "score": score,
                "label": "real",
            }


if __name__ == "__main__":
    asv = DguardASV(device="cpu")
    audio_path = (
        "/home/zhaosheng/Documents/dguard_project/dguard_home/aliasr/example/zh.mp3"
    )
    DF_result = asv.infer(audio_path)
    print(DF_result)
