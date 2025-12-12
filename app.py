#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
أبشر الذكي - تطبيق الخدمات الإلكترونية الحكومية
Absher Intelligence - Smart Government Services Portal
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

# الحصول على المسار الحالي
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# تهيئة التطبيق
app = Flask(__name__, template_folder=TEMPLATE_DIR)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

# ================== البيانات ==================

absher_services = {
    'جوازات_السفر': {
        'name': '🛂 جوازات السفر',
        'description': 'إصدار وتجديد جوازات السفر',
        'steps': [
            'زيارة مكتب الجوازات',
            'تقديم الوثائق المطلوبة',
            'دفع الرسوم',
            'استلام الجواز'
        ]
    },
    'الهوية_الوطنية': {
        'name': '🆔 الهوية الوطنية',
        'description': 'إصدار وتجديد الهوية الوطنية',
        'steps': [
            'التسجيل في النظام',
            'تحديد موعد',
            'الحضور للمكتب',
            'استلام الهوية'
        ]
    },
    'المرور': {
        'name': '🚗 المرور والرخص',
        'description': 'خدمات المرور والرخص والمخالفات',
        'steps': [
            'دخول بوابة المرور',
            'اختيار الخدمة المطلوبة',
            'إدخال بيانات المركبة',
            'إتمام العملية'
        ]
    },
    'العقارات': {
        'name': '🏠 العقارات والأراضي',
        'description': 'خدمات التسجيل والملكية العقارية',
        'steps': [
            'الدخول لمنصة العقارات',
            'تسجيل العقار',
            'تقديم الوثائق',
            'استخراج الشهادة'
        ]
    },
    'الصحة': {
        'name': '⚕️ الخدمات الصحية',
        'description': 'المواعيد والتقارير الطبية',
        'steps': [
            'اختيار المستشفى',
            'اختيار التخصص',
            'حجز الموعد',
            'الحضور للموعد'
        ]
    }
}

# ================== الردود الذكية ==================

def get_bot_response(user_message):
    """معالجة الرسالة وإرجاع الرد"""
    
    message = user_message.lower().strip()
    
    # أسئلة شائعة
    if any(word in message for word in ['مرحبا', 'السلام', 'صباح', 'مساء', 'هلا', 'أهلا']):
        return {
            'response': '👋 مرحباً بك في أبشر الذكي! أنا هنا لمساعدتك في جميع الخدمات. كيف يمكنني مساعدتك؟',
            'options': ['الخدمات المتاحة', 'تجديد الهوية', 'مشاكل وحلول']
        }
    
    if any(word in message for word in ['خدمات', 'ايش', 'كم', 'كيف']) and any(word in message for word in ['الخدمات', 'متاحة', 'تقدمها']):
        services_list = '\n'.join([f"✓ {service['name']}" for service in absher_services.values()])
        return {
            'response': f'🎯 الخدمات المتاحة لديك:\n\n{services_list}\n\nاختر أي خدمة لمعرفة المزيد عنها',
            'options': ['جوازات السفر', 'الهوية الوطنية', 'المرور', 'العقارات', 'الصحة']
        }
    
    if any(word in message for word in ['جواز', 'جوازات', 'passport']):
        service = absher_services['جوازات_السفر']
        steps = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(service['steps'])])
        return {
            'response': f"🛂 {service['name']}\n\n📝 خطوات الإصدار:\n{steps}\n\n💡 رسوم الإصدار: 150 ريال",
            'options': ['توقيت العمل', 'المواقع', 'الوثائق المطلوبة']
        }
    
    if any(word in message for word in ['هوية', 'وطنية', 'بطاقة']):
        service = absher_services['الهوية_الوطنية']
        steps = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(service['steps'])])
        return {
            'response': f"🆔 {service['name']}\n\n📝 خطوات التجديد:\n{steps}\n\n💡 التجديد مجاني عند الانتهاء الصلاحية",
            'options': ['المواقع القريبة', 'المستندات المطلوبة', 'حالة الطلب']
        }
    
    if any(word in message for word in ['مرور', 'رخصة', 'مخالفة', 'سيارة']):
        service = absher_services['المرور']
        steps = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(service['steps'])])
        return {
            'response': f"🚗 {service['name']}\n\n📝 الخطوات:\n{steps}\n\n⚠️ سداد المخالفات متاح 24/7",
            'options': ['دفع المخالفات', 'تجديد الرخصة', 'معلومات المركبة']
        }
    
    if any(word in message for word in ['عقار', 'أرض', 'ملكية', 'تسجيل']):
        service = absher_services['العقارات']
        steps = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(service['steps'])])
        return {
            'response': f"🏠 {service['name']}\n\n📝 الخطوات:\n{steps}\n\n✅ خدمة آمنة وموثوقة",
            'options': ['استفسار عن عقار', 'تسجيل عقار جديد', 'الرسوم والتكاليف']
        }
    
    if any(word in message for word in ['صحة', 'طبيب', 'موعد', 'مستشفى', 'مراجعة']):
        service = absher_services['الصحة']
        steps = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(service['steps'])])
        return {
            'response': f"⚕️ {service['name']}\n\n📝 طريقة حجز الموعد:\n{steps}\n\n📞 الدعم الفني: 920010011",
            'options': ['المستشفيات المتاحة', 'التخصصات', 'الأوقات المتاحة']
        }
    
    if any(word in message for word in ['ساعات', 'توقيت', 'وقت', 'أيام']):
        return {
            'response': '⏰ ساعات العمل:\n\n📅 السبت - الخميس\n⏰ 8:00 صباحاً - 8:00 مساءً\n\n🔴 مغلق يوم الجمعة\n\n💻 الخدمات الإلكترونية متاحة 24/7',
            'options': ['المواقع', 'الاتصال بنا', 'الخدمات الإلكترونية']
        }
    
    if any(word in message for word in ['موقع', 'مكتب', 'عنوان', 'أين', 'الرياض']):
        return {
            'response': '📍 المواقع:\n\n🏢 الرياض: حي العليا - البرج الرئيسي\n🏢 جدة: الحمراء - مركز الخدمات\n🏢 الدمام: الخليج - المقر الشرقي\n🏢 المدينة: الراية - فرع المدينة\n\n📱 خريطة المواقع متاحة في التطبيق',
            'options': ['الرياض', 'جدة', 'الدمام']
        }
    
    if any(word in message for word in ['دفع', 'رسوم', 'تكلفة', 'سعر', 'ثمن']):
        return {
            'response': '💰 طرق الدفع:\n\n💳 بطاقة ائتمان/خصم\n💸 التحويل البنكي\n📱 المحفظة الرقمية\n🏧 الصراف الآلي\n\n✅ جميع الدفعات آمنة وموثوقة',
            'options': ['الرسوم الكاملة', 'استفسار', 'دفع الآن']
        }
    
    if any(word in message for word in ['مشكلة', 'خطأ', 'مساعدة', 'دعم']):
        return {
            'response': '🆘 يمكننا مساعدتك!\n\n📞 رقم الدعم الموحد: 199099\n📧 البريد الإلكتروني: support@absher.sa\n💬 الدردشة المباشرة متاحة الآن\n\n⏱️ وقت الاستجابة: أقل من 5 دقائق',
            'options': ['استفسار شامل', 'شكوى', 'اقتراح']
        }
    
    if any(word in message for word in ['شكرا', 'شكراً', 'ممنون']):
        return {
            'response': '😊 على الرحب والسعة! إن احتجت أي مساعدة أخرى، أنا هنا دائماً. شكراً لاستخدام أبشر الذكي 💚',
            'options': ['الخدمات', 'الاتصال بنا', 'الرجوع للهوم']
        }
    
    # الرد الافتراضي
    return {
        'response': '🤔 عذراً، لم أفهم سؤالك بوضوح. يرجى إعادة الصياغة أو اختيار من الخيارات أدناه',
        'options': ['الخدمات المتاحة', 'المواقع', 'ساعات العمل', 'الاتصال بنا']
    }

# ================== المسارات ==================

@app.route('/')
def home():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@app.route('/chatbot')
def chatbot_page():
    """صفحة الشات بوت"""
    return render_template('chatbot.html')

@app.route('/chatbot.html')
def chatbot_html():
    """redirect من chatbot.html للـ /chatbot"""
    return render_template('chatbot.html')

# ================== API ==================

@app.route('/api/chat', methods=['POST'])
def chat():
    """معالجة رسائل الشات - API endpoint"""
    try:
        # الحصول على البيانات
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'لم يتم إرسال بيانات',
                'status': 'error'
            }), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'error': 'الرسالة فارغة',
                'status': 'error'
            }), 400
        
        # الحصول على الرد من البوت
        response_data = get_bot_response(user_message)
        
        # إرسال الرد
        return jsonify({
            'response': response_data['response'],
            'options': response_data.get('options', []),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }), 200
    
    except Exception as e:
        print(f'❌ خطأ في /api/chat: {str(e)}')
        return jsonify({
            'error': f'خطأ في معالجة الطلب: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/services', methods=['GET'])
def get_services():
    """الحصول على قائمة الخدمات"""
    try:
        services = []
        for key, service in absher_services.items():
            services.append({
                'id': key,
                'name': service['name'],
                'description': service['description']
            })
        return jsonify({
            'services': services,
            'count': len(services),
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/service/<service_id>', methods=['GET'])
def get_service(service_id):
    """الحصول على تفاصيل خدمة معينة"""
    try:
        if service_id in absher_services:
            service = absher_services[service_id]
            return jsonify({
                'id': service_id,
                'name': service['name'],
                'description': service['description'],
                'steps': service['steps'],
                'status': 'success'
            }), 200
        return jsonify({
            'error': 'الخدمة غير موجودة',
            'status': 'error'
        }), 404
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """الحصول على حالة النظام"""
    try:
        return jsonify({
            'status': 'online',
            'timestamp': datetime.now().isoformat(),
            'services_count': len(absher_services),
            'version': '1.0.0',
            'health': 'excellent'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """تقديم تقييم"""
    try:
        data = request.get_json()
        feedback = {
            'rating': data.get('rating'),
            'comment': data.get('comment'),
            'timestamp': datetime.now().isoformat()
        }
        
        # حفظ التقييم
        with open('feedback.json', 'a', encoding='utf-8') as f:
            json.dump(feedback, f, ensure_ascii=False)
            f.write('\n')
        
        return jsonify({
            'message': 'شكراً على تقييمك!',
            'status': 'success'
        }), 200
    
    except Exception as e:
        print(f'❌ خطأ في حفظ التقييم: {str(e)}')
        return jsonify({
            'error': f'خطأ في حفظ التقييم: {str(e)}',
            'status': 'error'
        }), 500

# ================== معالجة الأخطاء ==================

@app.errorhandler(404)
def not_found(error):
    """صفحة غير موجودة"""
    return jsonify({
        'error': 'الصفحة غير موجودة',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """خطأ في السيرفر"""
    return jsonify({
        'error': 'خطأ في السيرفر',
        'status': 'error'
    }), 500

# ================== التشغيل ==================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 أبشر الذكي - نظام الخدمات الذكي الذكي")
    print("=" * 70)
    print("📍 الرئيسية: http://localhost:5000/")
    print("💬 الشات: http://localhost:5000/chatbot")
    print("📊 الخدمات: http://localhost:5000/api/services")
    print("=" * 70)
    print("✅ النظام جاهز للعمل")
    print("=" * 70 + "\n")
    
    # تشغيل التطبيق
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=True
    )