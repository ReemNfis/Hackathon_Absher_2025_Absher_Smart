# -*- coding: utf-8 -*-

from absher_data import services as absher_services, faq, keywords

class SearchEngine:
    """محرك بحث ذكي بسيط لأبشر"""
    
    def __init__(self):
        self.services = absher_services
        self.faq = faq
        self.keywords = keywords
    
    # 🔍 الدالة الأساسية: البحث عن الإجابة
    def search(self, user_query):
        """
        تبحث عن الإجابة المناسبة للسؤال
        Input: سؤال المستخدم (نص)
        Output: الإجابة (نص)
        """
        
        # تحويل السؤال لأحرف صغيرة
        query = user_query.lower()
        
        # ✅ الطريقة 1: البحث باستخدام الكلمات المفتاحية
        for keyword, service_name in self.keywords.items():
            if keyword in query:
                return self.get_service_details(service_name)
        
        # ✅ الطريقة 2: البحث في الأسئلة الشائعة
        for question, answer in self.faq.items():
            if self.similarity(query, question.lower()) > 0.6:
                return answer
        
        # إذا ما فاتت نتيجة
        return self.default_response()
    
    # 📊 دالة للبحث عن التشابه (Similarity)
    def similarity(self, text1, text2):
        """
        تحسب نسبة التشابه بين نصين
        (نسخة بسيطة جداً)
        """
        # تقسيم النصين لكلمات
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        # كم كلمة مشتركة؟
        common_words = words1.intersection(words2)
        
        # حساب النسبة
        if len(words2) == 0:
            return 0
        
        similarity_score = len(common_words) / len(words2)
        return similarity_score
    
    # 📋 دالة الحصول على تفاصيل الخدمة
    def get_service_details(self, service_name):
        """تعيد تفاصيل الخدمة المطلوبة"""
        
        if service_name in self.services:
            service = self.services[service_name]
            
            # صيغة جميلة للإجابة
            response = f"\n{'='*50}\n"
            response += f"🔖 {service_name}\n"
            response += f"{'='*50}\n"
            response += f"📝 الوصف: {service['الوصف']}\n"
            
            if 'الشروط' in service:
                response += f"✅ الشروط: {', '.join(service['الشروط'])}\n"
            
            if 'الخطوات' in service:
                response += f"👣 الخطوات: {', '.join(service['الخطوات'])}\n"
            
            response += f"⏱️  المدة: {service['المدة']}\n"
            response += f"💰 الرسوم: {service['الرسوم']}\n"
            response += f"{'='*50}\n"
            
            return response
        
        return self.default_response()
    
    # 🤖 الرد الافتراضي
    def default_response(self):
        """إجابة عندما ما نلاقي نتيجة"""
        return """
❌ عذراً، ما قدرت أفهم سؤالك بشكل واضح.

يمكنك السؤال عن:
✅ تجديد الرخصة
✅ تجديد الإقامة
✅ الاستعلام عن الراتب
✅ دفع المخالفات
✅ الاستعلام عن الطلبات

أو اسأل عن الرسوم والمواعيد والدفع الإلكتروني 💬
        """
    
    # 📋 دالة تعرض جميع الخدمات
    def show_all_services(self):
        """تعرض قائمة بجميع الخدمات المتاحة"""
        response = "\n📋 الخدمات المتاحة:\n"
        response += "="*50 + "\n"
        
        for i, service_name in enumerate(self.services.keys(), 1):
            response += f"{i}. {service_name}\n"
        
        response += "="*50 + "\n"
        return response