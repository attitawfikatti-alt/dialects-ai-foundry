---
language:
- ar
multilinguality:
- monolingual
size_categories:
- 100<n<1K
task_categories:
- automatic-speech-recognition
tags:
- speech
- algerian-arabic
- darja
- audio
- whisper
dataset_info:
  features:
  - name: audio
    dtype: audio
  - name: sentence
    dtype: string
  - name: duration
    dtype: float64
  - name: province
    dtype: string
  - name: region
    dtype: string
  splits:
  - name: train
  - name: validation
  - name: test
license: apache-2.0
---

# dialects-ai-foundry 🇩🇿

قاعدة بيانات صوتية مفتوحة المصدر مخصصة للدارجة الجزائرية وتنوعاتها الصوتية الإقليمية، مجهزة ومعالجة بنظام أندرويد عبر بيئة Termux لتدريب واختبار نماذج التعرف الآلي على الكلام (ASR).

## التغطية الجغرافية الحالية
- **الشرق:** سكيكدة، عنابة، باتنة
- **الغرب:** سيدي بلعباس
- **الهضاب العليا والوسط:** الجلفة
- **الجنوب الغربي:** بشار
- **منطقة القبائل:** تيزي وزو

## المواصفات التقنية للصوت
- **الصيغة:** 16-bit PCM WAV
- **معدل العينات (Sampling Rate):** 16,000 Hz
- **القنوات (Channels):** أحادي (Mono)
- **التفريغ:** مؤتمت عبر whisper.cpp بنموذج `base` مع التنقيح والمطابقة.
