# -*- coding: utf-8 -*-

from datetime import datetime
import re
from search_engine import SearchEngine
from absher_data import user_data, services, personal_info_keywords

class AbsherChatbot:
    """
    بوت أبشر الذكي - يتعامل مع الاستفسارات ويعرض المعلومات الشخصية والخدمات
    """
    
    def __init__(self, voice_enabled=False):
        self.search_engine = SearchEngine()
        self.conversation_history = []
        self.voice_enabled = voice_enabled
        self.user_data = user_data
        self.services_data = services
    
    def add_to_history(self, message, message_type):
        """إضافة رسالة إلى السجل"""
        self.conversation_history.append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'type': message_type,
            'message': message
        })
    
    def check_personal_info_request(self, user_input):
        """التحقق من طلب معلومات شخصية"""
        for keywords, info_type in personal_info_keywords.items():
            pattern = keywords.replace('|', '|')
            if re.search(pattern, user_input):
                return info_type
        return None
    
    def format_personal_info(self, info_type):
        """تنسيق معلومات شخصية مع زر الوصول المباشر"""
        if info_type not in self.user_data:
            return None
        
        data = self.user_data[info_type]
        link = data.get('رابط', '')
        
        # بناء الرسالة مع المعلومات
        if info_type == 'المخالفات':
            message = f"""
🚨 **المخالفات المرورية الخاصة بك:**

📊 **الملخص:**
- عدد المخالفات: {data['عدد المخالفات']}
- المجموع المستحق: {data['المجموع المستحق']}

📋 **تفاصيل المخالفات:**
"""
            for violation in data['المخالفات']:
                message += f"""
✗ المخالفة: {violation['الرقم']}
  • التاريخ: {violation['التاريخ']}
  • السبب: {violation['السبب']}
  • المبلغ: {violation['المبلغ']}
  • الحالة: {violation['الحالة']}
"""
        else:
            message = f"🔖 **معلومات {info_type}:**\n\n"
            for key, value in data.items():
                if key not in ['رابط', 'نوع']:
                    message += f"• {key}: {value}\n"
        
        # إضافة زر الوصول المباشر
        message += f"\n\n**👉 للوصول للمعلومات الكاملة والمزيد من الخدمات:**"
        message += f"\n[اضغط هنا]({link})"
        
        return message
    
    def format_service_response(self, service_name):
        """تنسيق رد الخدمة مع زر مباشر"""
        if service_name not in self.services_data:
            return None
        
        service = self.services_data[service_name]
        link = service.get('رابط', '')
        button_text = service.get('اسم الزر', 'اذهب للخدمة')
        
        message = f"""
🎯 **{service_name}**

📝 **الوصف:**
{service.get('الوصف', '')}

💰 **الرسوم:**
{service.get('الرسم', 'مجاني')}

⏱️ **المدة:**
{service.get('المدة', 'سريع')}

✓ **الشروط:**
{service.get('الشروط', service.get('المزايا', 'لا توجد شروط خاصة'))}

📌 **خطوات الخدمة:**
{service.get('الخطوات', '')}

---
**👇 للانتقال للخدمة مباشرة:**
[{button_text}]({link})
"""
        return message
    
    def handle_commands(self, user_input):
        """معالجة الأوامر الخاصة"""
        user_input = user_input.strip().lower()
        
        if user_input in ['خروج', 'exit', 'quit']:
            self.add_to_history('المستخدم: خروج', 'user')
            return 'خروج'
        
        if user_input in ['خدمات', 'services']:
            self.add_to_history('المستخدم: خدمات', 'user')
            services_list = '📋 **الخدمات المتاحة:**\n\n'
            for i, service_name in enumerate(self.services_data.keys(), 1):
                services_list += f'{i}. {service_name}\n'
            return services_list
        
        if user_input in ['إحصائيات', 'statistics']:
            self.add_to_history('المستخدم: إحصائيات', 'user')
            stats = f"""
📊 **الإحصائيات:**

- إجمالي الرسائل: {len(self.conversation_history)}
- رسائل المستخدم: {sum(1 for m in self.conversation_history if m['type'] == 'user')}
- ردود البوت: {sum(1 for m in self.conversation_history if m['type'] == 'bot')}
"""
            return stats
        
        if user_input in ['من أنت', 'about']:
            self.add_to_history('المستخدم: من أنت', 'user')
            return """
🤖 **من أنا؟**

أنا بوت أبشر الذكي، مساعدك الرقمي المتخصص في:

✅ الإجابة على أسئلتك عن الخدمات الحكومية
✅ عرض معلوماتك الشخصية (الهوية، الرخصة، المخالفات، إلخ)
✅ توجيهك مباشرة للخدمات على منصة أبشر
✅ تقديم الدعم والمساعدة 24/7

كيف يمكنني مساعدتك؟
- اسأل عن أي خدمة
- اطلب معلوماتك الشخصية
- استفسر عن المخالفات أو الراتب
"""
        
        return None
    
    def respond(self, user_input):
        """الرد على المستخدم"""
        self.add_to_history(f'المستخدم: {user_input}', 'user')
        
        # 1. التحقق من طلب معلومات شخصية
        personal_info = self.check_personal_info_request(user_input)
        if personal_info:
            response = self.format_personal_info(personal_info)
            if response:
                self.add_to_history(response, 'bot')
                return response
        
        # 2. البحث عن الخدمة المطلوبة
        search_result = self.search_engine.search(user_input)
        
        if search_result:
            service_name = search_result['result']
            # التحقق من أن الخدمة موجودة وتنسيقها مع الأزرار
            if service_name in self.services_data:
                response = self.format_service_response(service_name)
                if response:
                    self.add_to_history(response, 'bot')
                    return response
        
        # 3. رد عام إذا لم تطابق أي شيء
        default_response = """
😊 اعتذر، لم أفهم سؤالك تماماً.

هل تبحث عن:
✓ معلومات شخصية (هوية، رخصة، مخالفات، راتب)؟
✓ خدمة معينة (تجديد رخصة، دفع مخالفات)؟
✓ معلومات عن أبشر؟

اكتب سؤالك بشكل أوضح وسأساعدك! 💚
"""
        
        self.add_to_history(default_response, 'bot')
        return default_response