# RIO Programming Language

> لغة برمجة بسيطة وقابلة للقراءة تُترجم إلى Python.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Experimental](https://img.shields.io/badge/status-experimental-orange.svg)](https://github.com/abidinfan8-wq/Rio-n-programming-language)
[![Version](https://img.shields.io/badge/version-5.1-blue.svg)](https://github.com/abidinfan8-wq/Rio-n-programming-language/releases)

## ما هي RIO؟

RIO لغة برمجة ذات نحو مختصر وواضح. يقوم المترجم بتحويل برامج RIO إلى Python صالح للتنفيذ، مما يتيح الاستفادة من مكتبات Python مع الحفاظ على نحو RIO.

المشروع حاليًا تجريبي، ويجري تطوير RIO 6 باستخدام Lexer وParser وAST ومكتبة قياسية ومدير حزم.

## مثال سريع

```rio
fanc greet(name):
    return "مرحبًا {name}!"

prn greet("RIO")

rep i in 1..3:
    prn i
```

## الميزات

- متغيرات وعمليات حسابية.
- شروط `if` و`elif` و`else`.
- حلقات `rep` و`while`.
- دوال باستخدام `fanc`.
- كلاسات ومنشئات باستخدام `cls` و`new`.
- معالجة الأخطاء باستخدام `try` و`catch` و`finally`.
- دمج النصوص تلقائيًا باستخدام `{expression}`.
- إمكانية استخدام مكتبات Python.
- رسائل خطأ مناسبة للمبتدئين.

## المتطلبات

- Python 3.6 أو أحدث في RIO 5.
- لا توجد تبعيات خارجية مطلوبة للنسخة الأساسية.

## التشغيل

```bash
python3 rio-5.py examples/hello.rio --run
```

## حالة المشروع

| الإصدار | الحالة |
|---|---|
| RIO 5.1 | نسخة تجريبية قابلة للاستخدام |
| RIO 6 | قيد التطوير |

## خارطة RIO 6

- Lexer كامل.
- Parser وAST.
- محلل دلالي.
- رسائل أخطاء مرتبطة بملف RIO الأصلي.
- مكتبة قياسية خاصة بـ RIO.
- مدير حزم.
- اختبارات آلية وتوثيق موسع.

## المساهمة

الاقتراحات، الأمثلة، التوثيق، وطلبات السحب مرحب بها. اقرأ [دليل المساهمة](CONTRIBUTING.md) قبل إرسال التغييرات.

## الأمان

لا تشغل ملفات RIO غير موثوقة؛ فهي تستطيع استخدام وظائف Python والمكتبات المستوردة. راجع [سياسة الأمان](SECURITY.md).

## الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE).

## روابط

- [دليل الصياغة](docs/SYNTAX.md)
- [خارطة الطريق](ROADMAP.md)
- [سجل التغييرات](CHANGELOG.md)
- [المساهمة](CONTRIBUTING.md)
- [المستودع على GitHub](https://github.com/abidinfan8-wq/Rio-n-programming-language)
