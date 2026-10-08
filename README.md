# Super Chat AI

تطبيق Flet بسيط وذكي لواجهة دردشة عربية، ويستخدم خدمة Pollinations AI لتوليد الردود.

## المزايا
- واجهة عربية ومريحة
- ألوان مناسبة ومظهر حديث
- دعم إدخال الرسالة بالـ Enter
- زر مسح المحادثة
- مؤشر تحميل أثناء انتظار الرد
- تصميم مناسب للـ Android وDesktop

## المتطلبات
- Python 3.10+
- Flet

## التثبيت
```bash
pip install -r requirements.txt
```

## التشغيل
```bash
python main.py
```

## بناء APK
```bash
flet build apk
```

## ملاحظات
- التطبيق يعتمد على شبكة الإنترنت بسبب استدعاء API الخارجي.
- لو واجهت مشكلة في البناء، تأكد إنك داخل نظام Linux/Ubuntu والـ Java وAndroid SDK جاهزين.
