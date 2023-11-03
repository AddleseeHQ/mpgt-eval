# mpgt-eval

This repository contains the code and data published in the SIGdial 2023 paper titled: "Multi-party Goal Tracking with LLMs: Comparing Pre-training, Fine-tuning, and Prompt Engineering" by Angus Addlesee, Weronika Sieińska, Nancie Gunson, Daniel Hernández Garcia, Christian Dondrup, and Oliver Lemon. The paper can be found here: [Our SIGdial 2023 paper](https://sigdialinlg2023.github.io/paper_sigdial109.html).

If you use this repository in your work - please cite us:

Harvard:
```
Addlesee, A. and Sieinska, W. and Gunson, N. and Garcia, DH. and Dondrup, C. and Lemon, O., 2023. Multi-party Goal Tracking with LLMs: Comparing Pre-training, Fine-tuning, and Prompt Engineering. Proceedings of the 24th Annual Meeting of the Special Interest Group on Discourse and Dialogue (SIGdial).
```

BibTeX:
```
@inproceedings{addlesee2023multiparty,
  title={Multi-party Goal Tracking with LLMs: Comparing Pre-training, Fine-tuning, and Prompt Engineering},
  author={Addlesee, Angus and Siei{\'n}ska, Weronika and Gunson, Nancie and Garcia, Daniel Hern{\'a}ndez and Dondrup, Christian and Lemon, Oliver},
  booktitle={Proceedings of the 24th Annual Meeting of the Special Interest Group on Discourse and Dialogue},
  year={2023}
}
```

## Structure of repo

### Mapping

You will likely not need these. This directory contains the scripts we used to convert our annotated ELAN files into the format DialogLM expected for preprocessing. ELAN is a common annotation tool, so they may be useful with some tweaks if needed.

### Preprocessing

This directory contains the data and files used to preprocess the dialogues for our experiments. The task in the paper is window-based de-noising, so this injects the noisy windows.

The `train-test-split.py` script splits the data, the size and specific task/nshot values must be set before running.

The `data` directory contains the original dialogues, the dialogues after running the preprocessing, and the splits we used. These are organised by task.

The `dst_and_goal_masking.py` script adds windows of noise to the dialogues. This is the DialogLM `inject_noise_to_dialogue.py` script with our added goal and dst masking tasks. See [original repo](https://github.com/microsoft/DialogLM)

### gpt

Finally, this directory contains the scripts we used to run our various GPT experiments. You must add your OpenAI credentials to use their API. The DialogLM experiments used their original code [here](https://github.com/microsoft/DialogLM)
