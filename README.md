---
language:
- ar
multilinguality:
- monolingual
task_categories:
- automatic-speech-recognition
task_ids:
- speech-recognition
tags:
- audio
- algerian-dialect
- darja
- speech
- sidi-bel-abbes
- el-bayadh
size_categories:
- n<1K
dataset_info:
  features:
  - name: audio
    dtype: audio
  - name: file_name
    dtype: string
  - name: transcription
    dtype: string
  - name: region
    dtype: string
  - name: dialect
    dtype: string
  - name: split
    dtype: string
  splits:
  - name: train
    num_examples: 340
  - name: test
    num_examples: 86
---

# Algerian Dialects Audio Foundry (Western & South-Western Algeria)

## نظرة عامة (Overview)
مجموعة بيانات صوتية مخصصة للتعرف الآلي على الكلام وتصنيف اللهجات الجزائرية المحلية، مع التركيز على لهجات الغرب والجنوب الغربي الجزائري (منطقتي **سيدي بلعباس** و **البيّض**).

- **إجمالي العينات:** 426 مقطع صوتي بصيغة WAV.
- **التفريغ النصي:** تفريغ حرفي للدارجة الجزائرية مع توحيد المعجم وإزالة التشكيل غير الضروري.
- **التقسيم:** 80% تدريب (`train`) و 20% اختبار (`test`) متوازن جغرافياً.

## الاستخدام عبر مكتبة Datasets (Usage)

```python
from datasets import load_dataset

dataset = load_dataset("termuxphone/dialects-algerian-audio")
print(dataset["train"][0])
```

## الترخيص والتوثيق
تم إعداد وفهرسة وتطبيع هذه المجموعة لدعم أبحاث ونماذج المعالجة الآلية للهجات المحلية.
