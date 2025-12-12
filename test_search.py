# -*- coding: utf-8 -*-

import sys
import io

# 🔧 إعدادات لدعم اللغة العربية
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from search_engine import SearchEngine

# إنشاء محرك البحث
engine = SearchEngine()

# 🧪 اختبار 1: البحث عن تجديد الرخصة
print("اختبار 1: البحث عن الرخصة")
result = engine.search("كيفية تجديد الرخصة")
print(result)

# 🧪 اختبار 2: البحث عن الراتب
print("\nاختبار 2: البحث عن الراتب")
result = engine.search("أين أشوف راتبي")
print(result)

# 🧪 اختبار 3: سؤال شائع
print("\nاختبار 3: سؤال عن الرسوم")
result = engine.search("الرسوم كم")
print(result)

# 🧪 اختبار 4: سؤال غير واضح
print("\nاختبار 4: سؤال غير واضح")
result = engine.search("مرحبا")
print(result)

# 🧪 اختبار 5: عرض جميع الخدمات
print("\nاختبار 5: جميع الخدمات")
result = engine.show_all_services()
print(result)